// Theme A · Soft 3D — list pieces shared by Mocks, PYQs, Subject mocks and Chapter tests.
import 'package:flutter/material.dart';

import 'icons3d.dart';
import 'soft.dart';

class SoftTag extends StatelessWidget {
  final String text;
  final Color fg, bg;
  const SoftTag(this.text, this.fg, this.bg, {super.key});
  const SoftTag.free({super.key}) : text = 'FREE', fg = const Color(0xFF047857), bg = const Color(0xFFD1FAE5);
  const SoftTag.premium({super.key}) : text = 'PREMIUM', fg = const Color(0xFF92400E), bg = const Color(0xFFFEF3C7);
  const SoftTag.paused({super.key}) : text = 'PAUSED', fg = const Color(0xFFB45309), bg = const Color(0xFFFEF3C7);
  const SoftTag.done({super.key, this.text = '✓ DONE'}) : fg = const Color(0xFF1D4ED8), bg = const Color(0xFFDBEAFE);

  @override
  Widget build(BuildContext context) => Container(
        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
        decoration: BoxDecoration(color: bg, borderRadius: BorderRadius.circular(999)),
        child: Text(text, style: TextStyle(color: fg, fontSize: 11.5, fontWeight: FontWeight.w800)),
      );
}

class SoftChip extends StatelessWidget {
  final String text;
  final bool on;
  final Color accent;
  final VoidCallback onTap;
  final IconData? icon;
  const SoftChip(this.text, this.on, this.accent, this.onTap, {super.key, this.icon});

  @override
  Widget build(BuildContext context) => Padding(
        padding: const EdgeInsets.only(right: 8),
        child: Material(
          color: Colors.transparent,
          child: Ink(
            decoration: BoxDecoration(
              color: on ? accent : Colors.white,
              borderRadius: BorderRadius.circular(999),
              boxShadow: [BoxShadow(color: (on ? accent : const Color(0xFF6366F1)).withValues(alpha: on ? .30 : .08), blurRadius: 12, offset: const Offset(0, 5))],
            ),
            child: InkWell(
              borderRadius: BorderRadius.circular(999),
              onTap: onTap,
              child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 17, vertical: 9),
                child: Row(mainAxisSize: MainAxisSize.min, children: [
                  if (icon != null) ...[Icon(icon, size: 16, color: on ? Colors.white : softInk), const SizedBox(width: 5)],
                  Text(text, style: TextStyle(fontSize: 14.5, fontWeight: FontWeight.w800, color: on ? Colors.white : (icon != null ? softInk : accent))),
                ]),
              ),
            ),
          ),
        ),
      );
}

/// "14 of 100 done" card with a progress bar.
class SoftSummary extends StatelessWidget {
  final String icon;
  final String title;
  final double progress;
  final String sub;
  final Color accent;
  final bool pct; // the "7%" pill beside the title (test lists)
  const SoftSummary({super.key, required this.icon, required this.title, required this.progress, required this.sub, required this.accent, this.pct = false});

  @override
  Widget build(BuildContext context) => Container(
        padding: const EdgeInsets.all(14),
        decoration: softCard(),
        child: Row(children: [
          Container(width: 58, height: 58, alignment: Alignment.center, decoration: softWell(), child: Icon3D(icon, size: 44)),
          const SizedBox(width: 14),
          Expanded(
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Row(children: [
                Expanded(child: Text(title, style: baloo(18))),
                if (pct)
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 3),
                    decoration: BoxDecoration(color: const Color(0xFFEDE9FE), borderRadius: BorderRadius.circular(999)),
                    child: Text('${(progress.clamp(0.0, 1.0) * 100).round()}%', style: baloo(14.5, color: const Color(0xFF4C1D95))),
                  ),
              ]),
              const SizedBox(height: 6),
              ClipRRect(
                borderRadius: BorderRadius.circular(8),
                child: SizedBox(
                  height: 8,
                  child: Stack(children: [
                    Container(color: Color.lerp(Colors.white, accent, .15)),
                    FractionallySizedBox(
                      widthFactor: progress.clamp(0.0, 1.0),
                      child: Container(decoration: BoxDecoration(gradient: LinearGradient(colors: [Color.lerp(accent, Colors.white, .3)!, accent]))),
                    ),
                  ]),
                ),
              ),
              const SizedBox(height: 5),
              Text(sub, style: const TextStyle(fontSize: 13, color: softMuted, fontWeight: FontWeight.w700)),
            ]),
          ),
        ]),
      );
}

/// One row of a test list: raised number badge, title with tags, and an action button (or a lock).
class SoftRow extends StatelessWidget {
  final String badge;
  final String title;
  final List<Widget> tags;
  final String meta;
  final String? action; // null = locked
  final bool resume;
  final Color accent;
  final VoidCallback onTap;
  const SoftRow({super.key, required this.badge, required this.title, this.tags = const [], this.meta = '', required this.action, this.resume = false, required this.accent, required this.onTap});

  @override
  Widget build(BuildContext context) {
    final locked = action == null;
    final badgeColors = locked ? const [Color(0xFFE2E8F0), Color(0xFFCBD5E1)] : [Color.lerp(accent, Colors.white, .38)!, accent];
    return Padding(
      padding: const EdgeInsets.only(bottom: 10),
      child: Opacity(
        opacity: locked ? .78 : 1,
        child: Material(
          color: Colors.transparent,
          child: Ink(
            decoration: softCard(radius: 20),
            child: InkWell(
              borderRadius: BorderRadius.circular(20),
              onTap: onTap,
              child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 11),
                child: Row(children: [
                  Container(
                    width: 48,
                    height: 48,
                    alignment: Alignment.center,
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(15),
                      gradient: LinearGradient(colors: badgeColors, begin: Alignment.topCenter, end: Alignment.bottomCenter),
                      boxShadow: [BoxShadow(color: badgeColors.last.withValues(alpha: .35), blurRadius: 8, offset: const Offset(0, 3))],
                    ),
                    child: Text(badge, style: baloo(badge.length > 2 ? 15 : 21, color: Colors.white)),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                      Text(title, maxLines: 1, overflow: TextOverflow.ellipsis, style: baloo(17.5)),
                      const SizedBox(height: 2),
                      if (tags.isNotEmpty) Wrap(spacing: 5, runSpacing: 4, children: tags),
                      if (meta.isNotEmpty) ...[
                        if (tags.isNotEmpty) const SizedBox(height: 3),
                        Text(meta, maxLines: 1, overflow: TextOverflow.ellipsis, style: const TextStyle(fontSize: 13, color: softMuted, fontWeight: FontWeight.w700)),
                      ],
                    ]),
                  ),
                  const SizedBox(width: 8),
                  if (locked)
                    const SizedBox(width: 86, height: 40, child: Icon(Icons.lock_outline_rounded, color: Color(0xFF94A3B8), size: 23))
                  else
                    Container(
                      width: 86,
                      height: 40,
                      alignment: Alignment.center,
                      decoration: BoxDecoration(
                        borderRadius: BorderRadius.circular(13),
                        gradient: LinearGradient(
                          colors: resume ? const [Color(0xFFFBBF24), Color(0xFFD97706)] : [Color.lerp(accent, Colors.white, .25)!, accent],
                          begin: Alignment.topCenter,
                          end: Alignment.bottomCenter,
                        ),
                        boxShadow: [BoxShadow(color: (resume ? const Color(0xFFD97706) : accent).withValues(alpha: .28), blurRadius: 10, offset: const Offset(0, 5))],
                      ),
                      child: Text(action!, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w900, fontSize: 15)),
                    ),
                ]),
              ),
            ),
          ),
        ),
      ),
    );
  }
}

enum RowState { done, progress, todo, locked }

/// Test list row (Mock tests, PYQs): icon · tags, title, sub line, meta line · status pill over an action button.
class TestRow extends StatelessWidget {
  final List<Widget> tags;
  final String title;
  final String sub;
  final List<(IconData, String)> meta;
  final RowState state;
  final String? score;
  final Color accent;
  final VoidCallback onTap;
  final VoidCallback? onAction; // the button; defaults to the row tap
  final Widget? note; // full-width notice under the row (the CGL Tier 2 timing)
  final Color? bar; // colour strip on the left edge (rowBar(i))
  const TestRow({super.key, this.tags = const [], required this.title, this.sub = '', this.meta = const [], required this.state, this.score, required this.accent, required this.onTap, this.onAction, this.note, this.bar});

  @override
  Widget build(BuildContext context) {
    final (fg, bg, icon, label) = switch (state) {
      RowState.done => (const Color(0xFF047857), const Color(0xFFD1FAE5), Icons.check_circle_rounded, 'Completed'),
      RowState.progress => (const Color(0xFF1D4ED8), const Color(0xFFDBEAFE), Icons.play_circle_fill_rounded, 'In Progress'),
      RowState.todo => (const Color(0xFFB91C1C), const Color(0xFFFEE2E2), Icons.cancel_rounded, 'Not Attempted'),
      RowState.locked => (const Color(0xFF64748B), const Color(0xFFF1F5F9), Icons.lock_outline_rounded, 'Locked'),
    };
    Widget button() {
      const ts = TextStyle(fontWeight: FontWeight.w800, fontSize: 13.5);
      final chev = Icon(Icons.chevron_right_rounded, size: 17, color: state == RowState.done ? accent : Colors.white);
      switch (state) {
        case RowState.done:
          return Container(
            height: 38,
            alignment: Alignment.center,
            decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(12), border: Border.all(color: accent, width: 2)),
            child: FittedBox(fit: BoxFit.scaleDown, child: Row(mainAxisSize: MainAxisSize.min, children: [Icon(Icons.replay_rounded, size: 16, color: accent), const SizedBox(width: 3), Text('Re-attempt', style: ts.copyWith(color: accent))])),
          );
        case RowState.locked:
          return Container(
            height: 38,
            alignment: Alignment.center,
            decoration: BoxDecoration(color: const Color(0xFFF1F5F9), borderRadius: BorderRadius.circular(12)),
            child: const Row(mainAxisAlignment: MainAxisAlignment.center, children: [
              Icon(Icons.lock_outline_rounded, size: 15, color: Color(0xFF64748B)),
              SizedBox(width: 4),
              Text('Unlock', style: TextStyle(fontWeight: FontWeight.w800, fontSize: 13.5, color: Color(0xFF64748B))),
            ]),
          );
        default:
          final prog = state == RowState.progress;
          final g = prog ? const [Color(0xFFFBBF24), Color(0xFFD97706)] : [Color.lerp(accent, Colors.white, .3)!, accent];
          return Container(
            height: 38,
            alignment: Alignment.center,
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(12),
              gradient: LinearGradient(colors: g, begin: Alignment.topCenter, end: Alignment.bottomCenter),
              boxShadow: [BoxShadow(color: g.last.withValues(alpha: .28), blurRadius: 10, offset: const Offset(0, 4))],
            ),
            child: FittedBox(fit: BoxFit.scaleDown, child: Row(mainAxisSize: MainAxisSize.min, children: [Text(prog ? 'Resume Test' : 'Start Test', style: ts.copyWith(color: Colors.white)), chev])),
          );
      }
    }

    return Padding(
      padding: const EdgeInsets.only(bottom: 10),
      child: Material(
        color: Colors.transparent,
        child: Ink(
          decoration: softCard(radius: 20),
          child: InkWell(
            borderRadius: BorderRadius.circular(20),
            onTap: onTap,
            child: Padding(
              padding: EdgeInsets.fromLTRB(bar != null ? 8 : 12, 11, 12, 11),
              child: Column(mainAxisSize: MainAxisSize.min, children: [
              IntrinsicHeight(
                child: Row(children: [
                  if (bar != null) Container(width: 4, height: double.infinity, margin: const EdgeInsets.only(right: 9), decoration: BoxDecoration(color: bar, borderRadius: BorderRadius.circular(4))),
                  Container(
                    width: 46,
                    height: 46,
                    alignment: Alignment.center,
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(15),
                      gradient: const LinearGradient(colors: [Color(0xFFF5F3FF), Color(0xFFEDE9FE)], begin: Alignment.topCenter, end: Alignment.bottomCenter),
                    ),
                    child: const Icon(Icons.assignment_outlined, color: Color(0xFF7C3AED), size: 26),
                  ),
                  const SizedBox(width: 10),
                  Expanded(
                    child: Column(crossAxisAlignment: CrossAxisAlignment.start, mainAxisAlignment: MainAxisAlignment.center, children: [
                      if (tags.isNotEmpty) Padding(padding: const EdgeInsets.only(bottom: 3), child: Wrap(spacing: 4, runSpacing: 3, children: tags)),
                      Text(title, maxLines: 1, overflow: TextOverflow.ellipsis, style: baloo(16.5)),
                      if (sub.isNotEmpty) Text(sub, maxLines: 1, overflow: TextOverflow.ellipsis, style: const TextStyle(fontSize: 12.5, color: softMuted, fontWeight: FontWeight.w700)),
                      if (meta.isNotEmpty)
                        Padding(
                          padding: const EdgeInsets.only(top: 4),
                          child: Row(children: [
                            for (var i = 0; i < meta.length; i++) ...[
                              if (i > 0) const Padding(padding: EdgeInsets.symmetric(horizontal: 6), child: Text('|', style: TextStyle(color: Color(0xFFCBD5E1)))),
                              Icon(meta[i].$1, size: 15, color: softMuted),
                              const SizedBox(width: 3),
                              Flexible(child: Text(meta[i].$2, maxLines: 1, overflow: TextOverflow.ellipsis, style: const TextStyle(fontSize: 12.5, color: Color(0xFF475569), fontWeight: FontWeight.w700))),
                            ],
                          ]),
                        ),
                    ]),
                  ),
                  const SizedBox(width: 8),
                  SizedBox(
                    width: 108,
                    child: Column(mainAxisAlignment: MainAxisAlignment.center, crossAxisAlignment: CrossAxisAlignment.stretch, children: [
                      Center(
                        child: FittedBox(
                          fit: BoxFit.scaleDown,
                          child: Container(
                            padding: const EdgeInsets.fromLTRB(5, 3, 8, 3),
                            decoration: BoxDecoration(color: bg, borderRadius: BorderRadius.circular(999)),
                            child: Row(mainAxisSize: MainAxisSize.min, children: [
                              Icon(icon, size: 15, color: fg),
                              const SizedBox(width: 3),
                              Text(label, style: TextStyle(fontSize: 11.5, fontWeight: FontWeight.w800, color: fg)),
                            ]),
                          ),
                        ),
                      ),
                      const SizedBox(height: 7),
                      onAction == null ? button() : GestureDetector(onTap: onAction, child: button()),
                      if (score != null) Padding(padding: const EdgeInsets.only(top: 4), child: Text('Score $score', textAlign: TextAlign.center, style: const TextStyle(fontSize: 11.5, color: softMuted, fontWeight: FontWeight.w800))),
                    ]),
                  ),
                ]),
              ),
              if (note != null) Padding(padding: const EdgeInsets.only(top: 8), child: note),
              ]),
            ),
          ),
        ),
      ),
    );
  }
}

// TSSC-LISTUI-V2: the test-list look shared by Mock tests and PYQs - big tab buttons, subject tiles,
// year chips with counts, a colour strip on every card.

const _rowBars = [Color(0xFFEA580C), Color(0xFF2563EB), Color(0xFF16A34A), Color(0xFF7C3AED)];
Color rowBar(int i) => _rowBars[i % _rowBars.length];

/// Big tab buttons (Tier 1 / Tier 2 …): two share the width, more scroll sideways.
class SoftTabs extends StatelessWidget {
  final List<(String, IconData)> items;
  final int index;
  final Color accent;
  final void Function(int) onTap;
  const SoftTabs({super.key, required this.items, required this.index, required this.accent, required this.onTap});

  Widget _tab(int i) {
    final on = i == index;
    return Material(
      color: Colors.transparent,
      child: Ink(
        height: 48,
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(16),
          color: on ? null : Colors.white,
          gradient: on ? LinearGradient(colors: [Color.lerp(accent, Colors.white, .22)!, accent], begin: Alignment.topCenter, end: Alignment.bottomCenter) : null,
          boxShadow: [BoxShadow(color: (on ? accent : const Color(0xFF6366F1)).withValues(alpha: on ? .30 : .10), blurRadius: 12, offset: const Offset(0, 5))],
        ),
        child: InkWell(
          borderRadius: BorderRadius.circular(16),
          onTap: () => onTap(i),
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 14),
            child: FittedBox(
              fit: BoxFit.scaleDown,
              child: Row(mainAxisSize: MainAxisSize.min, children: [
                Icon(items[i].$2, size: 21, color: on ? Colors.white : const Color(0xFF6D28D9)),
                const SizedBox(width: 8),
                Text(items[i].$1, style: baloo(17, color: on ? Colors.white : softInk)),
              ]),
            ),
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    if (items.length <= 2) {
      return Row(children: [
        for (var i = 0; i < items.length; i++) ...[if (i > 0) const SizedBox(width: 10), Expanded(child: _tab(i))],
      ]);
    }
    return SizedBox(
      height: 62,
      child: ListView(scrollDirection: Axis.horizontal, clipBehavior: Clip.none, padding: const EdgeInsets.only(bottom: 14), children: [
        for (var i = 0; i < items.length; i++) Padding(padding: const EdgeInsets.only(right: 10), child: _tab(i)),
      ]),
    );
  }
}

/// Subject tiles (Full Paper, Quant, Reasoning …): icon over a label on a pale colour.
class SubjectTiles extends StatelessWidget {
  final List<(String, String)> items; // key ('' = the full paper), label
  final String selected;
  final Color accent;
  final void Function(String) onTap;
  const SubjectTiles({super.key, required this.items, required this.selected, required this.accent, required this.onTap});

  static const _look = <String, (IconData, Color, Color)>{
    '': (Icons.article_rounded, Color(0xFF7C3AED), Color(0xFFFCE7F3)),
    'quant': (Icons.calculate_rounded, Color(0xFF2563EB), Color(0xFFDBEAFE)),
    'reasoning': (Icons.psychology_rounded, Color(0xFF7C3AED), Color(0xFFEDE9FE)),
    'gk': (Icons.layers_rounded, Color(0xFF16A34A), Color(0xFFDCFCE7)),
    'english': (Icons.menu_book_rounded, Color(0xFFD97706), Color(0xFFFEF3C7)),
  };
  static const _more = [(Icons.calculate_rounded, Color(0xFF2563EB), Color(0xFFDBEAFE)), (Icons.bar_chart_rounded, Color(0xFF0E7490), Color(0xFFCFFAFE)), (Icons.psychology_rounded, Color(0xFF7C3AED), Color(0xFFEDE9FE)), (Icons.extension_rounded, Color(0xFF16A34A), Color(0xFFDCFCE7))];
  static String _short(String l) => l == 'Gen. Awareness' ? 'Gen. Aw.' : l == 'English / Hindi' ? 'Eng / Hindi' : l;

  @override
  Widget build(BuildContext context) => LayoutBuilder(builder: (_, bc) {
        final n = items.length;
        final w = n <= 4 ? (bc.maxWidth - (n - 1) * 8) / (n < 1 ? 1 : n) : (bc.maxWidth - 3 * 8) / 4.35;
        return SizedBox(
          height: 90,
          child: ListView(scrollDirection: Axis.horizontal, clipBehavior: Clip.none, padding: const EdgeInsets.only(bottom: 12), children: [
            for (var i = 0; i < n; i++)
              Builder(builder: (_) {
                final it = items[i];
                final on = it.$1 == selected;
                final lk = _look[it.$1] ?? _more[i % _more.length];
                return Padding(
                  padding: EdgeInsets.only(right: i == n - 1 ? 0 : 8),
                  child: Material(
                    color: Colors.transparent,
                    child: Ink(
                      width: w,
                      decoration: BoxDecoration(
                        borderRadius: BorderRadius.circular(18),
                        gradient: LinearGradient(colors: [Colors.white, lk.$3], begin: Alignment.topLeft, end: Alignment.bottomRight),
                        border: Border.all(color: on ? accent : Colors.white, width: on ? 2.2 : 1.5),
                        boxShadow: [BoxShadow(color: lk.$2.withValues(alpha: on ? .26 : .12), blurRadius: 12, offset: const Offset(0, 5))],
                      ),
                      child: InkWell(
                        borderRadius: BorderRadius.circular(18),
                        onTap: () => onTap(it.$1),
                        child: Padding(
                          padding: const EdgeInsets.symmetric(horizontal: 4),
                          child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
                            Icon(lk.$1, size: 28, color: lk.$2),
                            const SizedBox(height: 4),
                            FittedBox(fit: BoxFit.scaleDown, child: Text(_short(it.$2), maxLines: 1, style: baloo(14.5))),
                          ]),
                        ),
                      ),
                    ),
                  ),
                );
              }),
          ]),
        );
      });
}
