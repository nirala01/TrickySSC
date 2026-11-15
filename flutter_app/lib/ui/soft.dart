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
