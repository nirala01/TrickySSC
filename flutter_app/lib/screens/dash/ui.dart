// Small shared widgets for the dashboard pages (Soft 3D look).
import 'package:flutter/material.dart';

import '../../data.dart';
import '../../ui/nav.dart';
import '../../ui/soft.dart';

const cGood = Color(0xFF16A34A);
const cWarn = Color(0xFFD97706);
const cBad = Color(0xFFDC2626);
const cBlue = Color(0xFF2563EB);

Color accColor(double p) => p >= 0.7 ? cGood : (p >= 0.5 ? cWarn : cBad);

class DashPage extends StatelessWidget {
  final Exam exam;
  final String title;
  final List<Widget> children;
  final Future<void> Function()? onRefresh;
  final String? sub; // a line in a pill under the title
  const DashPage({super.key, required this.exam, required this.title, required this.children, this.onRefresh, this.sub});

  @override
  Widget build(BuildContext context) {
    final list = ListView(
      physics: const AlwaysScrollableScrollPhysics(),
      padding: EdgeInsets.fromLTRB(14, 12, 14, 20 + MediaQuery.of(context).padding.bottom),
      children: children,
    );
    return examTheme(
      context,
      exam,
      Container(
        decoration: softBg,
        child: Scaffold(
          backgroundColor: Colors.transparent,
          appBar: softAppBar(title, sub: sub),
          body: onRefresh == null ? list : RefreshIndicator(onRefresh: onRefresh!, child: list),
        ),
      ),
    );
  }
}

class PCard extends StatelessWidget {
  final String? title;
  final String? sub;
  final List<Widget> children;
  final Widget? trailing;
  const PCard({super.key, this.title, this.sub, required this.children, this.trailing});

  @override
  Widget build(BuildContext context) => Container(
        margin: const EdgeInsets.only(bottom: 12),
        padding: const EdgeInsets.fromLTRB(16, 14, 16, 14),
        decoration: softCard(radius: 20),
        child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
          if (title != null)
            Row(children: [
              Expanded(child: Text(title!, style: baloo(18))),
              if (trailing != null) trailing!,
            ]),
          if (sub != null) Padding(padding: const EdgeInsets.only(top: 2), child: Text(sub!, style: const TextStyle(fontSize: 13, color: softMuted, fontWeight: FontWeight.w600))),
          if (title != null) const SizedBox(height: 10),
          ...children,
        ]),
      );
}

class KV extends StatelessWidget {
  final String label;
  final String value;
  final Color? color;
  const KV(this.label, this.value, {super.key, this.color});

  @override
  Widget build(BuildContext context) => Padding(
        padding: const EdgeInsets.symmetric(vertical: 5),
        child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Expanded(child: Text(label, style: const TextStyle(fontSize: 14.5, color: Color(0xFF475569), fontWeight: FontWeight.w600))),
          const SizedBox(width: 10),
          Flexible(child: Text(value, textAlign: TextAlign.right, style: TextStyle(fontSize: 15, fontWeight: FontWeight.w800, color: color ?? softInk))),
        ]),
      );
}

class Bar extends StatelessWidget {
  final String label;
  final double frac;
  final String value;
  final Color color;
  const Bar(this.label, this.frac, this.value, this.color, {super.key});

  @override
  Widget build(BuildContext context) => Padding(
        padding: const EdgeInsets.symmetric(vertical: 6),
        child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
          Row(children: [
            Expanded(child: Text(label, maxLines: 2, overflow: TextOverflow.ellipsis, style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w700, color: Color(0xFF334155)))),
            const SizedBox(width: 8),
            Text(value, style: TextStyle(fontSize: 14, fontWeight: FontWeight.w800, color: color)),
          ]),
          const SizedBox(height: 4),
          ClipRRect(
            borderRadius: BorderRadius.circular(6),
            child: LinearProgressIndicator(value: frac.clamp(0.0, 1.0), minHeight: 8, color: color, backgroundColor: const Color(0xFFEEF2FF)),
          ),
        ]),
      );
}

class Note extends StatelessWidget {
  final String text;
  final Color? color;
  const Note(this.text, {super.key, this.color});

  @override
  Widget build(BuildContext context) => Container(
        margin: const EdgeInsets.only(top: 10),
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(color: (color ?? cBlue).withValues(alpha: .07), borderRadius: BorderRadius.circular(12)),
        child: Text(text, style: TextStyle(fontSize: 13.5, height: 1.35, color: Color.lerp(color ?? cBlue, Colors.black, .35), fontWeight: FontWeight.w600)),
      );
}

class Big extends StatelessWidget {
  final String value;
  final String label;
  final Color color;
  const Big(this.value, this.label, this.color, {super.key});

  @override
  Widget build(BuildContext context) => Padding(
        padding: const EdgeInsets.only(bottom: 6),
        child: Row(crossAxisAlignment: CrossAxisAlignment.end, children: [
          Text(value, style: baloo(40, color: color, height: 1)),
          const SizedBox(width: 10),
          Expanded(child: Padding(padding: const EdgeInsets.only(bottom: 6), child: Text(label, style: const TextStyle(fontSize: 14.5, color: softMuted, fontWeight: FontWeight.w700)))),
        ]),
      );
}

Widget emptyNote(String t) => Padding(padding: const EdgeInsets.all(8), child: Note(t, color: softMuted));
