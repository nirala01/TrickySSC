// Theme A · Soft 3D — list pieces shared by Mocks, PYQs, Subject mocks and Chapter tests.
import 'package:flutter/material.dart';

import 'icons3d.dart';
import 'soft.dart';

class SoftTag extends StatelessWidget {
  final String text;
  final Color fg, bg;
  const SoftTag(this.text, this.fg, this.bg, {super.key});
  const SoftTag.free({super.key}) : text = 'FREE', fg = const Color(0xFF047857), bg = const Color(0xFFD1FAE5);
  const SoftTag.premium({super.key}) : text = '👑 PREMIUM', fg = const Color(0xFF92400E), bg = const Color(0xFFFEF3C7);
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

/// TSSC-LISTUI-V3 colours: one per card, in turn.
const softTones = [Color(0xFF7C3AED), Color(0xFF0891B2), Color(0xFFF97316), Color(0xFF16A34A), Color(0xFFDB2777), Color(0xFF2563EB)];
Color softTone(int i) => softTones[i % softTones.length];
const _blue1 = Color(0xFF2F7BEA), _blue2 = Color(0xFF1552C4);

/// A white (or tinted) card with a colour edge on its left.
BoxDecoration softEdgeCard(Color edge, {double radius = 20, Color? tint}) => BoxDecoration(
      borderRadius: BorderRadius.circular(radius),
      gradient: LinearGradient(colors: [edge, edge, Colors.white, tint ?? Colors.white], stops: const [0, .016, .016, 1]),
      boxShadow: [BoxShadow(color: edge.withValues(alpha: .14), blurRadius: 18, offset: const Offset(0, 8))],
    );

/// The blue pill button ("Open ›", "Start ›").
class SoftPill extends StatelessWidget {
  final String text;
  final List<Color> colors;
  final double height;
  final IconData? lead;
  const SoftPill(this.text, {super.key, this.colors = const [_blue1, _blue2], this.height = 38, this.lead});

  @override
  Widget build(BuildContext context) => Container(
        height: height,
        alignment: Alignment.center,
        padding: const EdgeInsets.symmetric(horizontal: 10),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(999),
          gradient: LinearGradient(colors: colors, begin: Alignment.topCenter, end: Alignment.bottomCenter),
          boxShadow: [BoxShadow(color: colors.last.withValues(alpha: .30), blurRadius: 10, offset: const Offset(0, 4))],
        ),
        child: FittedBox(
          fit: BoxFit.scaleDown,
          child: Row(mainAxisSize: MainAxisSize.min, children: [
            if (lead != null) ...[Icon(lead, size: 16, color: const Color(0xFFFDE68A)), const SizedBox(width: 4)],
            Text(text, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w800, fontSize: 14)),
            const Icon(Icons.chevron_right_rounded, size: 18, color: Colors.white),
          ]),
        ),
      );
}

/// One row of a chapter / test list: colour badge ("36 Tests"), title with tags, a line of detail, and a pill button (or a lock).
class SoftRow extends StatelessWidget {
  final String badge;
  final String? badgeSub; // small word under the badge number ("Tests")
  final String? emoji; // chapter picture, in a pale circle after the badge
  final int? tone; // which colour of softTones; null = the exam colour
  final String title;
  final List<Widget> tags;
  final String meta;
  final String? action; // null = locked
  final bool resume;
  final Color accent;
  final VoidCallback onTap;
  const SoftRow({super.key, required this.badge, this.badgeSub, this.emoji, this.tone, required this.title, this.tags = const [], this.meta = '', required this.action, this.resume = false, required this.accent, required this.onTap});

  @override
  Widget build(BuildContext context) {
    final locked = action == null;
    final c = locked ? const Color(0xFF94A3B8) : (tone == null ? accent : softTone(tone!));
    return Padding(
      padding: const EdgeInsets.only(bottom: 10),
      child: Opacity(
        opacity: locked ? .8 : 1,
        child: Material(
          color: Colors.transparent,
          child: Ink(
            decoration: softEdgeCard(c),
            child: InkWell(
              borderRadius: BorderRadius.circular(20),
              onTap: onTap,
              child: Padding(
                padding: const EdgeInsets.fromLTRB(16, 11, 12, 11),
                child: Row(children: [
                  Container(
                    width: 52,
                    height: 56,
                    alignment: Alignment.center,
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(15),
                      gradient: LinearGradient(colors: [Color.lerp(c, Colors.white, .22)!, Color.lerp(c, Colors.black, .12)!], begin: Alignment.topCenter, end: Alignment.bottomCenter),
                      boxShadow: [BoxShadow(color: c.withValues(alpha: .35), blurRadius: 8, offset: const Offset(0, 3))],
                    ),
                    child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
                      FittedBox(fit: BoxFit.scaleDown, child: Text(badge, style: baloo(badgeSub == null ? 21 : 20, color: Colors.white, height: 1))),
                      if (badgeSub != null) Text(badgeSub!, style: const TextStyle(color: Colors.white, fontSize: 11, fontWeight: FontWeight.w800, height: 1.1)),
                    ]),
                  ),
                  if (emoji != null && emoji!.isNotEmpty) ...[
                    const SizedBox(width: 8),
                    Container(
                      width: 40,
                      height: 40,
                      alignment: Alignment.center,
                      decoration: BoxDecoration(shape: BoxShape.circle, color: Color.lerp(Colors.white, c, .12)),
                      child: Text(emoji!, style: const TextStyle(fontSize: 21)),
                    ),
                  ],
                  const SizedBox(width: 10),
                  Expanded(
                    child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                      Text(title, maxLines: 2, overflow: TextOverflow.ellipsis, style: baloo(16.5)),
                      const SizedBox(height: 2),
                      if (tags.isNotEmpty) Wrap(spacing: 5, runSpacing: 4, children: tags),
                      if (meta.isNotEmpty) ...[
                        if (tags.isNotEmpty) const SizedBox(height: 4),
                        Row(children: [
                          const Icon(Icons.help_outline_rounded, size: 15, color: softMuted),
                          const SizedBox(width: 4),
                          Flexible(child: Text(meta, maxLines: 1, overflow: TextOverflow.ellipsis, style: const TextStyle(fontSize: 12.5, color: Color(0xFF475569), fontWeight: FontWeight.w700))),
                        ]),
                      ],
                    ]),
                  ),
                  const SizedBox(width: 8),
                  if (locked)
                    const SizedBox(width: 78, height: 38, child: Icon(Icons.lock_outline_rounded, color: Color(0xFF94A3B8), size: 23))
                  else
                    SizedBox(width: 82, child: SoftPill(action!, colors: resume ? const [Color(0xFFFBBF24), Color(0xFFD97706)] : const [_blue1, _blue2])),
                ]),
              ),
            ),
          ),
        ),
      ),
    );
  }
}

/// "35 Chapters | 319 Tests" with small icons (subject cards).
class SubjectCounts extends StatelessWidget {
  final int chapters, tests;
  const SubjectCounts(this.chapters, this.tests, {super.key});

  @override
  Widget build(BuildContext context) {
    Widget part(IconData ic, int n, String word) => Row(mainAxisSize: MainAxisSize.min, children: [
          Icon(ic, size: 16, color: softInk),
          const SizedBox(width: 4),
          Text('$n', style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w900, color: Color(0xFF4C1D95))),
          Text(' $word${n == 1 ? '' : 's'}', style: const TextStyle(fontSize: 13.5, fontWeight: FontWeight.w700, color: Color(0xFF334155))),
        ]);
    return FittedBox(
      fit: BoxFit.scaleDown,
      alignment: Alignment.centerLeft,
      child: Row(mainAxisSize: MainAxisSize.min, children: [
        part(Icons.layers_outlined, chapters, 'Chapter'),
        const Padding(padding: EdgeInsets.symmetric(horizontal: 8), child: Text('|', style: TextStyle(color: Color(0xFF94A3B8)))),
        part(Icons.article_outlined, tests, 'Test'),
      ]),
    );
  }
}

/// A subject card: tinted, colour edge, icon, name, a line under it, and a round arrow.
class SubjectCard extends StatelessWidget {
  final String icon3d;
  final String title;
  final Widget line;
  final int tone;
  final VoidCallback onTap;
  const SubjectCard({super.key, required this.icon3d, required this.title, required this.line, required this.tone, required this.onTap});

  static const _tones = [
    (Color(0xFFE11D48), Color(0xFFFCE7F3)),
    (Color(0xFF2563EB), Color(0xFFDBEAFE)),
    (Color(0xFFF59E0B), Color(0xFFFEF3C7)),
    (Color(0xFF16A34A), Color(0xFFDCFCE7)),
    (Color(0xFF7C3AED), Color(0xFFEDE9FE)),
    (Color(0xFF0284C7), Color(0xFFE0F2FE)),
    (Color(0xFF0D9488), Color(0xFFCCFBF1)),
  ];

  @override
  Widget build(BuildContext context) {
    final t = _tones[tone % _tones.length];
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: Material(
        color: Colors.transparent,
        child: Ink(
          decoration: softEdgeCard(t.$1, radius: 22, tint: t.$2),
          child: InkWell(
            borderRadius: BorderRadius.circular(22),
            onTap: onTap,
            child: Padding(
              padding: const EdgeInsets.fromLTRB(18, 14, 14, 14),
              child: Row(children: [
                Container(
                  width: 60,
                  height: 60,
                  alignment: Alignment.center,
                  decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(18), boxShadow: [BoxShadow(color: t.$1.withValues(alpha: .16), blurRadius: 10, offset: const Offset(0, 4))]),
                  child: Icon3D(icon3d, size: 44),
                ),
                const SizedBox(width: 14),
                Expanded(
                  child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                    Text(title, maxLines: 2, overflow: TextOverflow.ellipsis, style: baloo(19)),
                    const SizedBox(height: 4),
                    line,
                  ]),
                ),
                const SizedBox(width: 8),
                Container(
                  width: 34,
                  height: 34,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    gradient: const LinearGradient(colors: [Color(0xFF8B5CF6), Color(0xFF5B21B6)], begin: Alignment.topCenter, end: Alignment.bottomCenter),
                    border: Border.all(color: Colors.white, width: 2),
                    boxShadow: const [BoxShadow(color: Color(0x405B21B6), blurRadius: 8, offset: Offset(0, 3))],
                  ),
                  child: const Icon(Icons.chevron_right_rounded, color: Colors.white, size: 22),
                ),
              ]),
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
      const chev = Icon(Icons.chevron_right_rounded, size: 17, color: Colors.white);
      switch (state) {
        case RowState.done:
          return Container(
            height: 38,
            alignment: Alignment.center,
            decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(999), border: Border.all(color: _blue2, width: 2)),
            child: FittedBox(fit: BoxFit.scaleDown, child: Row(mainAxisSize: MainAxisSize.min, children: [const Icon(Icons.replay_rounded, size: 16, color: _blue2), const SizedBox(width: 3), Text('Re-attempt', style: ts.copyWith(color: _blue2))])),
          );
        case RowState.locked:
          return Container(
            height: 38,
            alignment: Alignment.center,
            decoration: const BoxDecoration(),
            child: const SoftPill('Unlock', colors: [Color(0xFF9F67F5), Color(0xFF6D28D9)], lead: Icons.workspace_premium_rounded),
          );
        default:
          final prog = state == RowState.progress;
          final g = prog ? const [Color(0xFFFBBF24), Color(0xFFD97706)] : const [_blue1, _blue2];
          return Container(
            height: 38,
            alignment: Alignment.center,
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(999),
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
          decoration: bar == null ? softCard(radius: 20) : softEdgeCard(bar!),
          child: InkWell(
            borderRadius: BorderRadius.circular(20),
            onTap: onTap,
            child: Padding(
              padding: EdgeInsets.fromLTRB(bar != null ? 16 : 12, 11, 12, 11),
              child: Column(mainAxisSize: MainAxisSize.min, children: [
              IntrinsicHeight(
                child: Row(children: [
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
                  const VerticalDivider(width: 16, thickness: 1, color: Color(0xFFE2E8F0)),
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

const _rowBars = [Color(0xFF2563EB), Color(0xFF16A34A), Color(0xFF7C3AED), Color(0xFFDB2777), Color(0xFFF97316)];
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
    'computer': (Icons.computer_rounded, Color(0xFF0E7490), Color(0xFFCFFAFE)),
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
                        gradient: LinearGradient(colors: on ? const [_blue1, _blue2] : [Colors.white, lk.$3], begin: Alignment.topLeft, end: Alignment.bottomRight),
                        border: Border.all(color: on ? const Color(0xFF93C5FD) : Colors.white, width: 1.5),
                        boxShadow: [BoxShadow(color: (on ? _blue2 : lk.$2).withValues(alpha: on ? .30 : .12), blurRadius: 12, offset: const Offset(0, 5))],
                      ),
                      child: InkWell(
                        borderRadius: BorderRadius.circular(18),
                        onTap: () => onTap(it.$1),
                        child: Padding(
                          padding: const EdgeInsets.symmetric(horizontal: 4),
                          child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
                            Icon(lk.$1, size: 28, color: on ? Colors.white : lk.$2),
                            const SizedBox(height: 4),
                            FittedBox(fit: BoxFit.scaleDown, child: Text(_short(it.$2), maxLines: 1, style: baloo(14.5, color: on ? Colors.white : softInk))),
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
