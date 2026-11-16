// "Plans" tab: what is free, what each pass gives, prices (Google Play price when Play lists it,
// otherwise the website price from config/pricing) and a Buy button for each pass.
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:flutter/material.dart';
import 'package:in_app_purchase/in_app_purchase.dart';

import '../billing.dart';
import '../data.dart';
import '../test/engine.dart' show freeLimit, paidLimit;
import '../ui/soft.dart';

class _Cat {
  final int? price, mrp, days;
  final String blurb, label;
  final List<String> grants;
  const _Cat({this.price, this.mrp, this.days, this.blurb = '', this.label = '', this.grants = const []});
}

class PlansTab extends StatefulWidget {
  final Exam exam;
  final Set<String> owned;
  const PlansTab({super.key, required this.exam, required this.owned});

  @override
  State<PlansTab> createState() => _PlansTabState();
}

class _PlansTabState extends State<PlansTab> {
  Map<String, _Cat> _cat = {}; // entitlement key ('all-mocks' or an exam pass) -> website product
  Map<String, ProductDetails> _play = {};
  bool _loaded = false;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    final cat = <String, _Cat>{};
    try {
      final snap = await FirebaseFirestore.instance.collection('config').doc('pricing').get();
      final products = (snap.data() ?? const {})['products'];
      if (products is List) {
        int? n(dynamic v) => v is num ? v.toInt() : int.tryParse('${v ?? ''}');
        for (final p in products) {
          if (p is! Map || p['live'] == false) continue;
          if ('${p['id'] ?? ''}'.startsWith('p-upgrade-')) continue;
          final grants = p['grants'] is List ? (p['grants'] as List).map((e) => '$e').toList() : <String>[];
          final passes = exams.where((e) => grants.contains(e.pass)).length;
          final combo = passes >= 2 && passes == grants.length && passes < exams.length ? comboProduct(grants) : null;
          final key = grants.contains('all-mocks') || passes >= exams.length ? 'all-mocks' : (combo ?? (grants.length == 1 ? grants.first : null));
          final price = n(p['price']);
          if (key == null || price == null || price <= 0) continue;
          final old = cat[key];
          if (old != null && (old.price ?? 1 << 30) <= price) continue;
          cat[key] = _Cat(price: price, mrp: n(p['mrp']), days: n(p['durationDays']) ?? 365, blurb: '${p['blurb'] ?? ''}', label: '${p['label'] ?? ''}', grants: grants);
        }
      }
    } catch (_) {}
    final play = await Billing.I.playProducts({for (final k in cat.keys) if (k.startsWith('combo_')) k});
    if (mounted) {
      setState(() {
        _cat = cat;
        _play = play;
        _loaded = true;
      });
    }
  }

  bool get _all => exams.every((e) => widget.owned.contains(e.pass));

  String? _priceText(String productId, String key) {
    final d = _play[productId];
    if (d != null) return d.price;
    final p = _cat[key]?.price;
    return p == null ? null : '₹$p';
  }

  @override
  Widget build(BuildContext context) {
    final exam = widget.exam;
    final owned = widget.owned;
    final mine = exams.where((e) => owned.contains(e.pass)).toList()
      ..sort((a, b) => a == exam ? -1 : (b == exam ? 1 : 0));
    final others = exams.where((e) => !owned.contains(e.pass)).toList()
      ..sort((a, b) => a == exam ? -1 : (b == exam ? 1 : 0));
    return RefreshIndicator(
      onRefresh: _load,
      child: ListView(
        padding: const EdgeInsets.fromLTRB(16, 8, 16, 28),
        children: [
          Text('Explore plans', style: baloo(26, color: exam.ink)),
          const SizedBox(height: 4),
          const Text('One payment · valid 1 year · Hindi & English · same login on the app and trickyssc.com',
              style: TextStyle(fontSize: 13.5, color: softMuted, fontWeight: FontWeight.w600, height: 1.35)),
          const SizedBox(height: 14),
          if (mine.isNotEmpty) _yours(mine),
          if (!_all) _allPass(),
          for (final k in _combos) _comboPass(k),
          for (final e in others) _examPass(e),
          _free(),
          _compare(),
          const SizedBox(height: 12),
          const Text(
            'Payments are handled by Google Play. A pass bought here also works on trickyssc.com with the same login, and a pass bought on the website works here.',
            textAlign: TextAlign.center,
            style: TextStyle(fontSize: 12, color: softMuted, height: 1.4),
          ),
          if (!_loaded) const Padding(padding: EdgeInsets.only(top: 14), child: Center(child: CircularProgressIndicator(strokeWidth: 2.5))),
        ],
      ),
    );
  }

  Widget _yours(List<Exam> mine) => Container(
        margin: const EdgeInsets.only(bottom: 14),
        padding: const EdgeInsets.fromLTRB(14, 12, 14, 12),
        decoration: BoxDecoration(color: const Color(0xFFECFDF5), borderRadius: BorderRadius.circular(18), border: Border.all(color: const Color(0xFFA7F3D0))),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Row(children: [
            const Icon(Icons.verified_rounded, color: Color(0xFF059669), size: 20),
            const SizedBox(width: 6),
            Text(_all ? 'You have full access' : 'Your passes', style: baloo(17, color: const Color(0xFF065F46))),
          ]),
          const SizedBox(height: 8),
          Wrap(spacing: 6, runSpacing: 6, children: [
            for (final e in mine)
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(999), border: Border.all(color: const Color(0xFFA7F3D0))),
                child: Text('${e.icon} ${e.name} · Active', style: const TextStyle(fontSize: 12.5, fontWeight: FontWeight.w800, color: Color(0xFF065F46))),
              ),
          ]),
          const SizedBox(height: 6),
          Text('Up to $paidLimit tests a day on your account.', style: const TextStyle(fontSize: 12.5, color: Color(0xFF047857), fontWeight: FontWeight.w600)),
        ]),
      );

  Widget _card({
    required Color c1,
    required String title,
    required String sub,
    required List<String> points,
    String? price,
    int? mrp,
    int? catPrice,
    String? badge,
    String? leading,
    VoidCallback? onBuy,
  }) {
    final off = mrp != null && catPrice != null && mrp > catPrice ? ((mrp - catPrice) * 100 / mrp).round() : 0;
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.fromLTRB(14, 12, 14, 12),
      decoration: softCard(radius: 20, glow: c1),
      child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
        if (badge != null)
          Align(
            alignment: Alignment.centerLeft,
            child: Container(
              margin: const EdgeInsets.only(bottom: 6),
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
              decoration: BoxDecoration(color: const Color(0xFFFEF3C7), borderRadius: BorderRadius.circular(999)),
              child: Text(badge, style: const TextStyle(fontSize: 10.5, fontWeight: FontWeight.w900, color: Color(0xFF92400E))),
            ),
          ),
        Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
          if (leading != null) Padding(padding: const EdgeInsets.only(right: 8, top: 1), child: Text(leading, style: const TextStyle(fontSize: 24))),
          Expanded(
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text(title, style: baloo(19)),
              Text(sub, style: const TextStyle(fontSize: 13, color: softMuted, fontWeight: FontWeight.w600)),
            ]),
          ),
          if (price != null)
            Column(crossAxisAlignment: CrossAxisAlignment.end, children: [
              Text(price, style: baloo(22, color: c1)),
              if (off > 0)
                Text('₹$mrp', style: const TextStyle(fontSize: 12.5, color: softMuted, decoration: TextDecoration.lineThrough, fontWeight: FontWeight.w600)),
              if (off > 0) Text('$off% off', style: const TextStyle(fontSize: 11.5, color: Color(0xFF16A34A), fontWeight: FontWeight.w900)),
            ]),
        ]),
        const SizedBox(height: 8),
        for (final t in points)
          Padding(
            padding: const EdgeInsets.only(bottom: 4),
            child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Icon(Icons.check_circle_rounded, size: 17, color: c1),
              const SizedBox(width: 6),
              Expanded(child: Text(t, style: const TextStyle(fontSize: 13.5, color: softInk, fontWeight: FontWeight.w600, height: 1.3))),
            ]),
          ),
        if (onBuy != null) ...[
          const SizedBox(height: 6),
          FilledButton(
            onPressed: onBuy,
            style: FilledButton.styleFrom(backgroundColor: c1, minimumSize: const Size.fromHeight(46), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(13))),
            child: Text(price == null ? 'Buy' : 'Buy for $price', style: const TextStyle(fontSize: 15.5, fontWeight: FontWeight.w800)),
          ),
        ],
      ]),
    );
  }

  String _mockLine(Exam e) => e.tier2 ? 'All ${e.mocks} (Tier I + Tier II), incl. new ones added during the year' : 'All ${e.mocks}, incl. new ones added during the year';

  Widget _allPass() {
    final c = _cat['all-mocks'];
    return _card(
      c1: const Color(0xFFD97706),
      badge: 'BEST VALUE · FULL ACCESS',
      leading: '👑',
      title: 'All Mocks Pass',
      sub: 'Every exam in one pass',
      price: _priceText(allMocksProduct, 'all-mocks'),
      mrp: c?.mrp,
      catPrice: c?.price,
      points: [
        'Full mock series of ${exams.map((e) => e.name.replaceFirst('SSC ', '')).join(', ')}',
        'Subject-wise mocks for every exam',
        'Up to $paidLimit tests a day (free: $freeLimit)',
        'Valid ${(c?.days ?? 365) >= 365 ? '1 year' : '${c!.days} days'} from purchase',
        if (c != null && c.blurb.isNotEmpty) c.blurb,
      ],
      onBuy: () => Billing.I.buy(allMocksProduct, 'all-mocks'),
    );
  }

  /// Combos the student does not fully own yet, cheapest first.
  List<String> get _combos {
    final out = [
      for (final k in _cat.keys)
        if (k.startsWith('combo_') && !_cat[k]!.grants.every(widget.owned.contains)) k
    ];
    out.sort((a, b) => (_cat[a]!.price ?? 0).compareTo(_cat[b]!.price ?? 0));
    return out;
  }

  Widget _comboPass(String k) {
    final c = _cat[k]!;
    final inc = exams.where((e) => c.grants.contains(e.pass)).toList();
    return _card(
      c1: const Color(0xFF7C3AED),
      badge: 'COMBO',
      leading: inc.map((e) => e.icon).join(),
      title: c.label.isNotEmpty ? c.label : '${inc.map((e) => e.name).join(' + ')} Combo',
      sub: '${inc.length} mock series in one pass',
      price: _priceText(k, k),
      mrp: c.mrp,
      catPrice: c.price,
      points: [
        for (final e in inc) '${e.name}: ${_mockLine(e).replaceFirst('All ', 'all ')}',
        'Subject-wise mocks of each',
        'Up to $paidLimit tests a day · valid ${(c.days ?? 365) >= 365 ? '1 year' : '${c.days} days'}',
        if (c.blurb.isNotEmpty) c.blurb,
      ],
      onBuy: () => Billing.I.buy(k, k),
    );
  }

  Widget _examPass(Exam e) {
    final c = _cat[e.pass];
    return _card(
      c1: e.c1,
      leading: e.icon,
      title: '${e.name} Mock Pass',
      sub: '${e.sub} · ${e.meta}',
      price: _priceText(productFor(e), e.pass),
      mrp: c?.mrp,
      catPrice: c?.price,
      points: [
        _mockLine(e),
        'Subject-wise mocks',
        'Detailed solutions, all-India rank and section analysis',
        'Up to $paidLimit tests a day · valid ${(c?.days ?? 365) >= 365 ? '1 year' : '${c!.days} days'}',
        if (c != null && c.blurb.isNotEmpty) c.blurb,
      ],
      onBuy: () => Billing.I.buy(productFor(e), e.pass),
    );
  }

  Widget _free() => _card(
        c1: const Color(0xFF64748B),
        leading: '🎁',
        title: 'Free',
        sub: 'No payment needed',
        price: '₹0',
        points: [
          'Free mocks of every exam, full and subject-wise (${exams.map((e) => '${e.name.replaceFirst('SSC ', '').replaceFirst('RRB ', '')} ${e.free}').join(', ')})',
          'All previous year papers (PYQs) and chapter-wise PYQs',
          'Chapter tests and current affairs',
          'Up to $freeLimit tests a day',
        ],
      );

  Widget _compare() {
    Widget row(String a, String b, String c, {bool head = false}) {
      final st = TextStyle(fontSize: 12.5, fontWeight: head ? FontWeight.w900 : FontWeight.w600, color: head ? softInk : softMuted);
      return Padding(
        padding: const EdgeInsets.symmetric(vertical: 5),
        child: Row(children: [
          Expanded(flex: 5, child: Text(a, style: st.copyWith(color: softInk))),
          Expanded(flex: 2, child: Text(b, textAlign: TextAlign.center, style: st)),
          Expanded(flex: 2, child: Text(c, textAlign: TextAlign.center, style: st.copyWith(color: head ? softInk : const Color(0xFF16A34A)))),
        ]),
      );
    }

    return Container(
      margin: const EdgeInsets.only(bottom: 4),
      padding: const EdgeInsets.fromLTRB(14, 10, 14, 10),
      decoration: softCard(radius: 20),
      child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
        Text('Free vs Pass', style: baloo(17)),
        const SizedBox(height: 4),
        row('', 'Free', 'Pass', head: true),
        const Divider(height: 8),
        row('Full-length mocks', 'First few', 'All'),
        row('Subject-wise mocks', 'First few', 'All'),
        row('PYQs & chapter tests', '✓', '✓'),
        row('Current affairs', '✓', '✓'),
        row('Tests per day', '$freeLimit', '$paidLimit'),
        row('Solutions & all-India rank', '✓', '✓'),
      ]),
    );
  }
}
