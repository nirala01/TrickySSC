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
  const SoftChip(this.text, this.on, this.accent, this.onTap, {super.key});

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
                child: Text(text, style: TextStyle(fontSize: 14.5, fontWeight: FontWeight.w800, color: on ? Colors.white : accent)),
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
  const SoftSummary({super.key, required this.icon, required this.title, required this.progress, required this.sub, required this.accent});

  @override
  Widget build(BuildContext context) => Container(
        padding: const EdgeInsets.all(14),
        decoration: softCard(),
        child: Row(children: [
          Container(width: 58, height: 58, alignment: Alignment.center, decoration: softWell(), child: Icon3D(icon, size: 44)),
          const SizedBox(width: 14),
          Expanded(
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text(title, style: baloo(18)),
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
