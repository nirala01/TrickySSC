// Theme A · Soft 3D — shared look for the home screens.
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

const softBgTop = Color(0xFFEEF2FF);
const softBgMid = Color(0xFFF0F9FF);
const softBgBottom = Color(0xFFF5F3FF);
const softInk = Color(0xFF1E1B4B);
const softMuted = Color(0xFF5B5F86);
const softIndigo = Color(0xFF4F46E5);

const softBg = BoxDecoration(
  gradient: LinearGradient(colors: [softBgTop, softBgMid, softBgBottom], stops: [0, .55, 1], begin: Alignment.topCenter, end: Alignment.bottomCenter),
);

BoxDecoration softCard({double radius = 22, Color glow = const Color(0xFF6366F1)}) => BoxDecoration(
      color: Colors.white,
      borderRadius: BorderRadius.circular(radius),
      boxShadow: [BoxShadow(color: glow.withValues(alpha: .12), blurRadius: 22, offset: const Offset(0, 9))],
    );

/// The pale well an Icon3D sits in.
BoxDecoration softWell({double radius = 16}) => BoxDecoration(
      borderRadius: BorderRadius.circular(radius),
      gradient: const LinearGradient(colors: [Color(0xFFF8FAFF), Color(0xFFEEF2FF)], begin: Alignment.topCenter, end: Alignment.bottomCenter),
    );

TextStyle baloo(double size, {Color color = softInk, FontWeight weight = FontWeight.w800, double height = 1.1}) =>
    GoogleFonts.baloo2(fontSize: size, fontWeight: weight, color: color, height: height);

/// TSSC-T2TIMING-V1: SSC CGL Tier 2 mocks and the CGL All India Challenge run on the SSC CGL 2026 timing.
const cglT2Timing = 'New 2026 timing: Maths 30 · Reasoning 30 · English 40 · GA 20 · Computer 15 min. Each part locks when its time ends.';

/// The amber timing notice: a slim strip under a Start button, or ([box]) a highlighted box on the start screen.
class TimingNote extends StatelessWidget {
  final bool box;
  const TimingNote({super.key, this.box = false});

  @override
  Widget build(BuildContext context) => Container(
        width: double.infinity,
        padding: EdgeInsets.symmetric(horizontal: box ? 14 : 10, vertical: box ? 12 : 7),
        decoration: BoxDecoration(
          color: const Color(0xFFFEF3C7),
          borderRadius: BorderRadius.circular(box ? 14 : 10),
          border: Border.all(color: const Color(0xFFF59E0B), width: box ? 1.5 : 1),
        ),
        child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Icon(Icons.timer_outlined, size: box ? 20 : 15, color: const Color(0xFF92400E)),
          SizedBox(width: box ? 10 : 6),
          Expanded(child: Text(cglT2Timing, style: TextStyle(fontSize: box ? 14.5 : 12, height: 1.35, color: const Color(0xFF78350F), fontWeight: FontWeight.w700))),
        ]),
      );
}
