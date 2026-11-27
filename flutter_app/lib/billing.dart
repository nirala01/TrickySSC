// Google Play billing: buy a mock pass in the app.
// The purchase is checked by the trickyssc-play Worker (play_worker/worker.js), which opens the pass in Firestore.
import 'dart:async';
import 'dart:convert';

import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:in_app_purchase/in_app_purchase.dart';

import 'data.dart';
import 'profile.dart';
import 'ui/soft.dart';

const String playApi = 'https://trickyssc-play.nirala01.workers.dev';
const String allMocksProduct = 'pass_all_mocks';
const List<String> upgradeProducts = ['upgrade_full_49', 'upgrade_full_20'];

/// The student's upgrade offer, worked out by the trickyssc-play Worker from their paid orders.
class UpgradeQuote {
  final bool paid, full;
  final int? price; // 49, 20 or null (free user / already full access)
  final String? product;
  final Map<String, int> owned; // exam pass key -> expiry (ms)
  const UpgradeQuote({required this.paid, required this.full, this.price, this.product, this.owned = const {}});
  bool get offer => paid && !full && price != null;

  /// "Your SSC CGL pass stays valid till 21 Oct 2027. All other courses: 1 year from today."
  String get validity {
    const mon = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    final parts = <String>[];
    for (final e in exams) {
      final ms = owned[e.pass];
      if (ms == null) continue;
      final d = DateTime.fromMillisecondsSinceEpoch(ms);
      parts.add('${e.name} pass stays valid till ${d.day} ${mon[d.month - 1]} ${d.year}');
    }
    if (parts.isEmpty) return 'All courses: 1 year from today.';
    return 'Your ${parts.join(', ')}. All other courses: 1 year from today.';
  }
}

/// Play product id of a combo: combo_cgl_chsl (exams in app order). Null if [passes] is not 2 or more exams (but not all of them).
String? comboProduct(Iterable<String> passes) {
  final ks = [for (final e in exams) if (passes.contains(e.pass)) e.k];
  return ks.length >= 2 && ks.length < exams.length && ks.length == passes.length ? 'combo_${ks.join('_')}' : null;
}

/// Play product id of an exam's pass: ssc-cgl-mocks -> pass_ssc_cgl.
String productFor(Exam e) => e.play.isNotEmpty ? e.play : 'pass_${e.pass.replaceAll('-mocks', '').replaceAll('-', '_')}';

class Billing with WidgetsBindingObserver {
  Billing._();
  static final Billing I = Billing._();

  final _iap = InAppPurchase.instance;
  StreamSubscription<List<PurchaseDetails>>? _sub;
  final _prices = <String, double>{};

  /// Called when a pass has been opened (reload what the account owns).
  VoidCallback? onGranted;

  /// Shows a short message to the student.
  void Function(String)? onMessage;

  /// True while a payment just made is being confirmed and the pass opened (a few seconds after the
  /// Google Play sheet closes). The app shows "please wait" over the screen. (2026-11-18)
  final ValueNotifier<bool> busy = ValueNotifier<bool>(false);

  /// A payment Google Play has taken but not confirmed yet (UPI, net banking: the bank confirms a few
  /// minutes later). The app shows a "waiting for Google Play" card until it is confirmed. (2026-11-19)
  final ValueNotifier<String?> waiting = ValueNotifier<String?>(null);
  final _waitIds = <String>{};

  /// The name of a pass just opened, for the "Payment successful" message.
  final ValueNotifier<String?> unlocked = ValueNotifier<String?>(null);

  /// Ask Google Play again for purchases it has confirmed (the "Check now" button, and on returning to the app).
  void recheck() => _iap.restorePurchases().catchError((_) {});

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    if (state == AppLifecycleState.resumed && waiting.value != null) recheck();
  }

  String passName(String productId) {
    if (productId == allMocksProduct || productId.startsWith('upgrade_')) return 'Full Access';
    for (final e in exams) {
      if (productFor(e) == productId) return '${e.name} pass';
    }
    return productId.startsWith('combo_') ? 'combo pass' : 'pass';
  }

  void _stopWaiting(String id) {
    _waitIds.remove(id);
    if (waiting.value == id) waiting.value = _waitIds.isEmpty ? null : _waitIds.first;
  }

  /// Same breadcrumb as the website checkout (checkoutIntents/{uid}), so a student who opened the
  /// app's buy sheet but did not pay shows on admin-premium.html under "Started, not paid".
  void recordIntent(String stage, String courseId, [Map<String, dynamic> extra = const {}]) {
    final u = FirebaseAuth.instance.currentUser;
    if (u == null) return;
    FirebaseFirestore.instance.collection('checkoutIntents').doc(u.uid).set({
      'uid': u.uid,
      'email': u.email ?? '',
      'stage': stage,
      'courseId': courseId,
      'page': 'android-app',
      'build': 'app-$appVersion',
      'clicks': FieldValue.increment(1),
      'lastAt': FieldValue.serverTimestamp(),
      ...extra,
    }, SetOptions(merge: true)).catchError((_) {});
  }

  String _keyOf(String productId) {
    for (final e in exams) {
      if (productFor(e) == productId) return e.pass;
    }
    return _keyOfId(productId);
  }

  String _keyOfId(String productId) => productId.startsWith('combo_') || productId.startsWith('upgrade_') ? productId : productId == allMocksProduct ? 'all-mocks' : '${productId.replaceFirst('pass_', '').replaceAll('_', '-')}-mocks';

  void start() {
    if (_sub == null) WidgetsBinding.instance.addObserver(this);
    _sub ??= _iap.purchaseStream.listen(_onPurchases, onError: (_) {});
    // purchases paid for but not yet opened (app closed mid-way, slow payment)
    _iap.isAvailable().then((ok) {
      if (ok) _iap.restorePurchases().catchError((_) {});
    }).catchError((_) {});
  }

  Future<void> _onPurchases(List<PurchaseDetails> list) async {
    for (final p in list) {
      if (p.status == PurchaseStatus.pending) {
        _waitIds.add(p.productID);
        waiting.value = p.productID;
        recordIntent('google-play', _keyOf(p.productID), {'failedAt': '', 'lastError': 'payment pending in Google Play'});
        continue;
      }
      if (p.status == PurchaseStatus.error || p.status == PurchaseStatus.canceled) _stopWaiting(p.productID);
      if (p.status == PurchaseStatus.error) {
        onMessage?.call('Payment did not go through. You have not been charged.');
        recordIntent('failed', _keyOf(p.productID), {'failedAt': 'google-play', 'lastError': p.error?.message ?? 'error'});
      }
      if (p.status == PurchaseStatus.canceled) {
        recordIntent('failed', _keyOf(p.productID), {'failedAt': 'dismissed', 'lastError': 'closed Google Play'});
      }
      if (p.status == PurchaseStatus.purchased || p.status == PurchaseStatus.restored) {
        // fresh: paid just now, or a payment we were waiting on (it may come back as "restored")
        final fresh = p.status == PurchaseStatus.purchased || _waitIds.contains(p.productID);
        if (fresh) busy.value = true;
        bool ok;
        try {
          ok = await _verify(p);
        } finally {
          if (fresh) busy.value = false;
          _stopWaiting(p.productID);
        }
        if (ok) {
          if (fresh) recordIntent('paid', _keyOf(p.productID), {'failedAt': '', 'lastError': ''});
          onGranted?.call();
          // a pass bought earlier and re-checked at start opens silently
          if (fresh) unlocked.value = passName(p.productID);
        } else {
          recordIntent('failed', _keyOf(p.productID), {'failedAt': 'verify', 'lastError': _lastError.isEmpty ? 'paid on Google Play, pass not opened yet' : _lastError});
          onMessage?.call(_lastError == 'already-full' || _lastError == 'not-eligible'
              ? 'This upgrade does not match your account, so it was not used. Google Play refunds it automatically within 3 days.'
              : 'Payment received, but the pass could not be opened yet. It will open automatically; if not, write to contact@trickyssc.com.');
        }
      }
      if (p.pendingCompletePurchase && p.status != PurchaseStatus.purchased && p.status != PurchaseStatus.restored) {
        try {
          await _iap.completePurchase(p);
        } catch (_) {}
      }
    }
  }

  String _lastError = '';

  Future<bool> _verify(PurchaseDetails p) async {
    _lastError = '';
    try {
      final u = FirebaseAuth.instance.currentUser;
      if (u == null) return false;
      final r = await http
          .post(Uri.parse('$playApi/verify'),
              headers: {'content-type': 'application/json'},
              body: jsonEncode({
                'idToken': await u.getIdToken(),
                'productId': p.productID,
                'purchaseToken': p.verificationData.serverVerificationData,
                'amount': _prices[p.productID],
              }))
          .timeout(const Duration(seconds: 25));
      final j = jsonDecode(r.body);
      if (r.statusCode == 200 && j is Map && j['ok'] == true) {
        try {
          if (p.pendingCompletePurchase) await _iap.completePurchase(p);
        } catch (_) {}
        return true;
      }
      if (j is Map) _lastError = '${j['error'] ?? ''}';
    } catch (_) {}
    return false;
  }

  /// All six passes as Google Play lists them (price in the buyer's currency). Empty when Play is unavailable.
  Future<Map<String, ProductDetails>> playProducts([Set<String> extra = const {}]) async {
    final out = <String, ProductDetails>{};
    try {
      if (!await _iap.isAvailable()) return out;
      final res = await _iap.queryProductDetails({for (final e in exams) productFor(e), allMocksProduct, ...upgradeProducts, ...extra});
      for (final d in res.productDetails) {
        out[d.id] = d;
        _prices[d.id] = d.rawPrice;
      }
    } catch (_) {}
    return out;
  }

  /// Same rule as the Worker, worked out in the app from the student's own records. Used to show the
  /// offer when the Worker cannot be reached; the Worker still checks everything before granting.
  Future<UpgradeQuote?> _localQuote(String uid) async {
    try {
      final db = FirebaseFirestore.instance;
      final ent = (await db.collection('entitlements').doc(uid).get()).data() ?? const <String, dynamic>{};
      final now = DateTime.now().millisecondsSinceEpoch;
      // a pass opened by hand (active, no expiry date) counts as owned, as in data.dart _active: -1
      int exp(dynamic m) {
        if (m is! Map || m['active'] != true) return 0;
        final ms = expiryMs(m['expiresAt']);
        if (ms == null) return -1;
        return ms > now ? ms : 0;
      }

      final mods = ent['modules'] is Map ? ent['modules'] as Map : const {};
      final owned = <String, int>{};
      var have = 0;
      for (final e in exams) {
        final x = exp(mods[e.pass]);
        if (x != 0) have++;
        if (x > 0) owned[e.pass] = x;
      }
      final full = exp(ent['allAccess']) != 0 || exp(mods['all-mocks']) != 0 || have == exams.length;
      final paid = have > 0;
      num total = 0;
      if (paid && !full) {
        final sn = await db.collection('payments').where('uid', isEqualTo: uid).get();
        for (final d in sn.docs) {
          final p = d.data();
          if (p['status'] != 'paid' || p['mode'] == 'test') continue;
          final a = p['amount'];
          final n = a is num ? a : num.tryParse('$a') ?? 0;
          if (n > 0 && n < 100000) total += n;
        }
      }
      final int? price = full || !paid ? null : (total >= 70 ? 20 : 49) /* 2026-11-18: no free upgrade any more */;
      return UpgradeQuote(paid: paid, full: full, price: price, product: price == 49 ? 'upgrade_full_49' : (price == 20 ? 'upgrade_full_20' : null), owned: owned);
    } catch (_) {
      return null;
    }
  }

  /// From the Worker; if it cannot be reached, worked out in the app.
  Future<UpgradeQuote?> quote() async {
    final u = FirebaseAuth.instance.currentUser;
    if (u == null) return null;
    return (await _workerQuote(u)) ?? await _localQuote(u.uid);
  }

  Future<UpgradeQuote?> _workerQuote(User u) async {
    try {
      final r = await http
          .post(Uri.parse('$playApi/quote'), headers: {'content-type': 'application/json'}, body: jsonEncode({'idToken': await u.getIdToken()}))
          .timeout(const Duration(seconds: 8));
      final j = jsonDecode(r.body);
      if (r.statusCode != 200 || j is! Map || j['ok'] != true) return null;
      final o = j['owned'];
      return UpgradeQuote(
        paid: j['paid'] == true,
        full: j['full'] == true,
        price: j['price'] is num ? (j['price'] as num).toInt() : null,
        product: j['product'] is String ? j['product'] as String : null,
        owned: {if (o is Map) for (final e in o.entries) if (e.value is num) '${e.key}': (e.value as num).toInt()},
      );
    } catch (_) {
      return null;
    }
  }

  /// Paid students: their one offer.
  Future<void> upgrade(UpgradeQuote q) async {
    if (q.product != null) await buy(q.product!, q.product!);
  }

  /// Opens Google Play for one pass (from the Plans tab).
  Future<void> buy(String productId, String courseId) async {
    recordIntent('opened', courseId, {'via': 'plans'});
    final d = (await playProducts({productId}))[productId];
    if (d == null) {
      onMessage?.call('This pass is not on sale in the app yet. Please try again after the next update.');
      return;
    }
    await _launch(d);
  }

  Future<void> _launch(ProductDetails d) async {
    final u = FirebaseAuth.instance.currentUser;
    if (u == null) return;
    recordIntent('google-play', _keyOf(d.id));
    try {
      await _iap.buyConsumable(purchaseParam: PurchaseParam(productDetails: d, applicationUserName: u.uid), autoConsume: false);
    } catch (_) {
      onMessage?.call('Could not open Google Play. Please try again.');
    }
  }

  /// Welcome popup for a student with no pass: Full Access first, then a link to every other pass.
  /// [top]: shown first in the popup (the All India Challenge strip, as on the website's offers pop-up).
  Future<void> showFullAccessPopup(BuildContext context, {required VoidCallback onExplore, Widget Function(BuildContext)? top}) async {
    int? cat, mrp;
    for (final p in await pricingProducts()) {
      if (p is Map && p['id'] == 'p-all-mocks' && p['live'] != false) {
        cat = p['price'] is num ? (p['price'] as num).toInt() : null;
        mrp = p['mrp'] is num ? (p['mrp'] as num).toInt() : null;
      }
    }
    final play = await playProducts();
    if (!context.mounted) return;
    final price = play[allMocksProduct]?.price ?? (cat == null ? null : '₹$cat');
    Widget point(String t) => Padding(
          padding: const EdgeInsets.only(bottom: 5),
          child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
            const Icon(Icons.check_circle_rounded, size: 18, color: Color(0xFFD97706)),
            const SizedBox(width: 7),
            Expanded(child: Text(t, style: const TextStyle(fontSize: 14, color: softInk, fontWeight: FontWeight.w600, height: 1.3))),
          ]),
        );
    await showDialog<void>(
      context: context,
      builder: (c) => Dialog(
        backgroundColor: Colors.white,
        insetPadding: const EdgeInsets.symmetric(horizontal: 22, vertical: 24),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(24)),
        child: SingleChildScrollView(
          padding: const EdgeInsets.fromLTRB(18, 8, 18, 14),
          child: Column(mainAxisSize: MainAxisSize.min, crossAxisAlignment: CrossAxisAlignment.stretch, children: [
            Align(alignment: Alignment.centerRight, child: IconButton(onPressed: () => Navigator.pop(c), icon: const Icon(Icons.close, color: softMuted))),
            if (top != null) top(c),
            const Text('👑', textAlign: TextAlign.center, style: TextStyle(fontSize: 38)),
            Text('Full Access', textAlign: TextAlign.center, style: baloo(26)),
            if (price != null)
              Row(mainAxisAlignment: MainAxisAlignment.center, crossAxisAlignment: CrossAxisAlignment.end, children: [
                Text(price, style: baloo(34, color: const Color(0xFFD97706))),
                if (mrp != null && cat != null && mrp > cat)
                  Padding(
                    padding: const EdgeInsets.only(left: 8, bottom: 9),
                    child: Text('₹$mrp', style: const TextStyle(fontSize: 15, color: softMuted, decoration: TextDecoration.lineThrough, fontWeight: FontWeight.w700)),
                  ),
                const Padding(padding: EdgeInsets.only(left: 6, bottom: 9), child: Text('for 1 year', style: TextStyle(fontSize: 13.5, color: softMuted, fontWeight: FontWeight.w700))),
              ]),
            const SizedBox(height: 10),
            point('Every mock of ${exams.map((e) => e.name.replaceFirst('SSC ', '').replaceFirst('RRB ', '')).join(', ')}'),
            point('Tier I and Tier II, plus subject-wise mocks'),
            point('New mock series added during the year are included'),
            point('Hindi & English, solutions and all-India rank'),
            point('Works on the app and trickyssc.com with the same login'),
            const SizedBox(height: 10),
            FilledButton(
              onPressed: () {
                Navigator.pop(c);
                buy(allMocksProduct, 'all-mocks');
              },
              style: FilledButton.styleFrom(backgroundColor: const Color(0xFFD97706), minimumSize: const Size.fromHeight(52), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14))),
              child: Text(price == null ? 'Get Full Access' : 'Get Full Access for $price', style: const TextStyle(fontSize: 16.5, fontWeight: FontWeight.w900)),
            ),
            const SizedBox(height: 4),
            TextButton(
              onPressed: () {
                Navigator.pop(c);
                onExplore();
              },
              child: const Text('Explore other passes →', style: TextStyle(fontSize: 15, fontWeight: FontWeight.w800)),
            ),
          ]),
        ),
      ),
    );
  }

  /// Upgrade sheet for students who already paid: one offer only (plan doc).
  Future<void> showUpgradeSheet(BuildContext context, Exam exam, UpgradeQuote q, {Widget Function(BuildContext)? top}) async {
    final play = q.product == null ? <String, ProductDetails>{} : await playProducts({q.product!});
    if (!context.mounted) return;
    final price = play[q.product]?.price ?? '₹${q.price}';
    await showModalBottomSheet<void>(
      context: context,
      backgroundColor: Colors.white,
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(22))),
      builder: (c) => SafeArea(
        child: Padding(
          padding: const EdgeInsets.fromLTRB(18, 18, 18, 14),
          child: Column(mainAxisSize: MainAxisSize.min, crossAxisAlignment: CrossAxisAlignment.stretch, children: [
            if (top != null) top(c),
            const Text('👑', textAlign: TextAlign.center, style: TextStyle(fontSize: 34)),
            Text('Get Full Access', textAlign: TextAlign.center, style: baloo(23)),
            const SizedBox(height: 4),
            Text('Every exam: ${exams.map((e) => e.short).join(', ')} · all mocks${exams.any((e) => e.subjects.isNotEmpty) ? ' and subject mocks' : ''}',
                textAlign: TextAlign.center, style: const TextStyle(fontSize: 13.5, color: softMuted, fontWeight: FontWeight.w600)),
            const SizedBox(height: 10),
            Container(
              padding: const EdgeInsets.all(10),
              decoration: BoxDecoration(color: const Color(0xFFFFFBEB), borderRadius: BorderRadius.circular(12), border: Border.all(color: const Color(0xFFFDE68A))),
              child: Text(q.validity, style: const TextStyle(fontSize: 13, color: Color(0xFF92400E), fontWeight: FontWeight.w700, height: 1.35)),
            ),
            const SizedBox(height: 12),
            FilledButton(
              onPressed: () {
                Navigator.pop(c);
                upgrade(q);
              },
              style: FilledButton.styleFrom(backgroundColor: const Color(0xFFD97706), minimumSize: const Size.fromHeight(52), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14))),
              child: Text('Get Full Access, pay $price more', style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w900)),
            ),
            const SizedBox(height: 6),
            Text('Payment is handled by Google Play.',
                textAlign: TextAlign.center, style: const TextStyle(fontSize: 12, color: softMuted)),
          ]),
        ),
      ),
    );
  }

  /// Opens the "choose a pass" sheet for this exam.
  // TSSC-PLANS-LOADING-V1: a "Loading plans…" box from the tap until the plans sheet opens, so the
  // lock button gives an instant response and a second tap does nothing.
  bool _opening = false;
  Future<void> showBuySheet(BuildContext context, Exam exam) async {
    if (_opening) return;
    _opening = true;
    final nav = Navigator.of(context, rootNavigator: true);
    var loading = true;
    showDialog<void>(
      context: context,
      useRootNavigator: true,
      barrierDismissible: false,
      barrierColor: Colors.black38,
      builder: (_) => PopScope(
        canPop: false,
        child: Center(
          child: Material(
            color: Colors.white,
            borderRadius: BorderRadius.circular(16),
            child: const Padding(
              padding: EdgeInsets.symmetric(horizontal: 24, vertical: 18),
              child: Row(mainAxisSize: MainAxisSize.min, children: [
                SizedBox(width: 22, height: 22, child: CircularProgressIndicator(strokeWidth: 2.6, color: Color(0xFF6D28D9))),
                SizedBox(width: 14),
                Text('Loading plans…', style: TextStyle(fontSize: 15, fontWeight: FontWeight.w700, color: Color(0xFF1E293B))),
              ]),
            ),
          ),
        ),
      ),
    );
    void closeLoad() {
      if (!loading) return;
      loading = false;
      _opening = false;
      try {
        nav.pop();
      } catch (_) {}
    }

    try {
      await _buySheet(context, exam, closeLoad);
    } finally {
      closeLoad();
    }
  }

  Future<void> _buySheet(BuildContext context, Exam exam, VoidCallback closeLoad) async {
    final u = FirebaseAuth.instance.currentUser;
    if (u == null) return;
    final q = await quote();
    if (!context.mounted) return;
    if (q != null && q.offer) {
      closeLoad();
      return showUpgradeSheet(context, exam, q);
    }
    // combos that include this exam, from admin-pricing
    final combos = <String, String>{}; // play id -> label
    // TSSC-SM-PRICING-V1: as on the website, this exam's own pass is sold only while a live admin-pricing
    // product grants it (a new course stays locked until its pass is switched Live in admin pricing).
    var passLive = false;
    final prods = await pricingProducts();
    for (final p in prods) {
      if (p is! Map || p['live'] == false || '${p['id'] ?? ''}'.startsWith('p-upgrade-')) continue;
      final g = p['grants'] is List ? (p['grants'] as List).map((e) => '$e').where((k) => exams.any((e) => e.pass == k)).toList() : <String>[];
      if (g.length == 1 && g.first == exam.pass) passLive = true;
      final id = g.contains(exam.pass) && g.length < exams.length ? comboProduct(g) : null;
      if (id != null) combos[id] = '${p['label'] ?? ''}'.replaceAll(' Mock Tests (Combo)', ' Combo');
    }
    List<ProductDetails> products = [];
    var available = false;
    try {
      available = await _iap.isAvailable();
      if (available) {
        final res = await _iap.queryProductDetails({productFor(exam), allMocksProduct, ...combos.keys});
        products = res.productDetails;
        for (final d in products) {
          _prices[d.id] = d.rawPrice;
        }
      }
    } catch (_) {}
    if (!context.mounted) return;
    closeLoad();
    ProductDetails? find(String id) {
      for (final d in products) {
        if (d.id == id) return d;
      }
      return null;
    }

    final one = passLive || prods.isEmpty ? find(productFor(exam)) : null, all = find(allMocksProduct);
    recordIntent('opened', exam.pass);
    await showModalBottomSheet<void>(
      context: context,
      backgroundColor: Colors.white,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(22))),
      builder: (c) {
        Widget option(ProductDetails d, String title, String sub, {bool best = false}) => Padding(
              padding: const EdgeInsets.only(bottom: 10),
              child: Material(
                color: Colors.transparent,
                child: Ink(
                  decoration: softCard(radius: 18, glow: best ? const Color(0xFFF59E0B) : exam.c1),
                  child: InkWell(
                    borderRadius: BorderRadius.circular(18),
                    onTap: () {
                      Navigator.pop(c);
                      _launch(d);
                    },
                    child: Padding(
                      padding: const EdgeInsets.fromLTRB(14, 12, 14, 12),
                      child: Row(children: [
                        Expanded(
                          child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                            if (best)
                              Container(
                                margin: const EdgeInsets.only(bottom: 4),
                                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                                decoration: BoxDecoration(color: const Color(0xFFFEF3C7), borderRadius: BorderRadius.circular(999)),
                                child: const Text('BEST VALUE', style: TextStyle(fontSize: 10.5, fontWeight: FontWeight.w900, color: Color(0xFF92400E))),
                              ),
                            Text(title, style: baloo(17.5)),
                            Text(sub, style: const TextStyle(fontSize: 13, color: softMuted, fontWeight: FontWeight.w600)),
                          ]),
                        ),
                        const SizedBox(width: 10),
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 9),
                          decoration: BoxDecoration(
                            borderRadius: BorderRadius.circular(12),
                            gradient: LinearGradient(colors: [Color.lerp(exam.c1, Colors.white, .3)!, exam.c1], begin: Alignment.topCenter, end: Alignment.bottomCenter),
                          ),
                          child: Text(d.price, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w900, fontSize: 15.5)),
                        ),
                      ]),
                    ),
                  ),
                ),
              ),
            );
        return SafeArea(
          child: Padding(
            padding: const EdgeInsets.fromLTRB(16, 18, 16, 12),
            child: Column(mainAxisSize: MainAxisSize.min, crossAxisAlignment: CrossAxisAlignment.stretch, children: [
              Text('Unlock ${exam.name} mocks', style: baloo(21)),
              const Text('One payment · valid 1 year · Hindi & English · works on the website too', style: TextStyle(fontSize: 13.5, color: softMuted, fontWeight: FontWeight.w600)),
              if (exam.held)
                Container(
                  margin: const EdgeInsets.only(top: 10),
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 9),
                  decoration: BoxDecoration(color: const Color(0xFFFEF3C7), borderRadius: BorderRadius.circular(12)),
                  child: Text('📅 ${exam.name} mocks open on 1 December. Full Access opens the mocks already uploaded today.',
                      style: const TextStyle(fontSize: 13.5, fontWeight: FontWeight.w700, color: Color(0xFF92400E))),
                ),
              const SizedBox(height: 14),
              if (all != null) option(all, 'Full Access · All Mocks Pass', 'Every exam: ${exams.map((e) => e.short).join(', ')}', best: true),
              for (final e in combos.entries)
                if (find(e.key) != null) option(find(e.key)!, e.value.isEmpty ? 'Combo' : e.value, 'Two mock series in one pass'),
              if (one != null) option(one, '${exam.name} Mock Pass', exam.subjects.isEmpty ? 'All ${exam.mocks}' : 'All ${exam.mocks} + subject mocks'),
              if (one == null && all == null && combos.keys.every((k) => find(k) == null))
                Padding(
                  padding: const EdgeInsets.symmetric(vertical: 14),
                  child: Text(
                    available ? 'Passes are not on sale in this version of the app yet. Please update the app from the Play Store.' : 'Google Play is not available on this phone right now. Please try again later.',
                    style: const TextStyle(fontSize: 15, color: softInk, fontWeight: FontWeight.w600),
                  ),
                ),
              const Text('Payment is handled by Google Play.', textAlign: TextAlign.center, style: TextStyle(fontSize: 12, color: softMuted)),
            ]),
          ),
        );
      },
    );
  }
}
