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

/// Play product id of an exam's pass: ssc-cgl-mocks -> pass_ssc_cgl.
String productFor(Exam e) => 'pass_${e.pass.replaceAll('-mocks', '').replaceAll('-', '_')}';

class Billing {
  Billing._();
  static final Billing I = Billing._();

  final _iap = InAppPurchase.instance;
  StreamSubscription<List<PurchaseDetails>>? _sub;
  final _prices = <String, double>{};

  /// Called when a pass has been opened (reload what the account owns).
  VoidCallback? onGranted;

  /// Shows a short message to the student.
  void Function(String)? onMessage;

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

  String _keyOf(String productId) => productId == allMocksProduct ? 'all-mocks' : '${productId.replaceFirst('pass_', '').replaceAll('_', '-')}-mocks';

  void start() {
    _sub ??= _iap.purchaseStream.listen(_onPurchases, onError: (_) {});
    // purchases paid for but not yet opened (app closed mid-way, slow payment)
    _iap.isAvailable().then((ok) {
      if (ok) _iap.restorePurchases().catchError((_) {});
    }).catchError((_) {});
  }

  Future<void> _onPurchases(List<PurchaseDetails> list) async {
    for (final p in list) {
      if (p.status == PurchaseStatus.pending) {
        onMessage?.call('Payment is pending. Your pass opens as soon as it is confirmed.');
        continue;
      }
      if (p.status == PurchaseStatus.error) {
        onMessage?.call('Payment did not go through. You have not been charged.');
        recordIntent('failed', _keyOf(p.productID), {'failedAt': 'google-play', 'lastError': p.error?.message ?? 'error'});
      }
      if (p.status == PurchaseStatus.canceled) {
        recordIntent('failed', _keyOf(p.productID), {'failedAt': 'dismissed', 'lastError': 'closed Google Play'});
      }
      if (p.status == PurchaseStatus.purchased || p.status == PurchaseStatus.restored) {
        final ok = await _verify(p);
        if (ok) {
          if (p.status == PurchaseStatus.purchased) recordIntent('paid', _keyOf(p.productID), {'failedAt': '', 'lastError': ''});
          onGranted?.call();
          onMessage?.call('Pass unlocked. All the best!');
        } else {
          recordIntent('failed', _keyOf(p.productID), {'failedAt': 'verify', 'lastError': 'paid on Google Play, pass not opened yet'});
          onMessage?.call('Payment received, but the pass could not be opened yet. It will open automatically; if not, write to contact@trickyssc.com.');
        }
      }
      if (p.pendingCompletePurchase && p.status != PurchaseStatus.purchased && p.status != PurchaseStatus.restored) {
        try {
          await _iap.completePurchase(p);
        } catch (_) {}
      }
    }
  }

  Future<bool> _verify(PurchaseDetails p) async {
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
    } catch (_) {}
    return false;
  }

  /// Opens the "choose a pass" sheet for this exam.
  Future<void> showBuySheet(BuildContext context, Exam exam) async {
    final u = FirebaseAuth.instance.currentUser;
    if (u == null) return;
    List<ProductDetails> products = [];
    var available = false;
    try {
      available = await _iap.isAvailable();
      if (available) {
        final res = await _iap.queryProductDetails({productFor(exam), allMocksProduct});
        products = res.productDetails;
        for (final d in products) {
          _prices[d.id] = d.rawPrice;
        }
      }
    } catch (_) {}
    if (!context.mounted) return;
    ProductDetails? find(String id) {
      for (final d in products) {
        if (d.id == id) return d;
      }
      return null;
    }

    final one = find(productFor(exam)), all = find(allMocksProduct);
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
                    onTap: () async {
                      Navigator.pop(c);
                      recordIntent('google-play', _keyOf(d.id));
                      try {
                        await _iap.buyConsumable(purchaseParam: PurchaseParam(productDetails: d, applicationUserName: u.uid), autoConsume: false);
                      } catch (_) {
                        onMessage?.call('Could not open Google Play. Please try again.');
                      }
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
              const SizedBox(height: 14),
              if (one != null) option(one, '${exam.name} Mock Pass', 'All ${exam.mocks} + subject mocks'),
              if (all != null) option(all, 'All Mocks Pass', 'Every exam: CGL, CHSL, MTS, GD, NTPC', best: true),
              if (one == null && all == null)
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
