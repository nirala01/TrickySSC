// TSSC-SECTNOTE-V2 (2026-11-28): the blinking "Please note" box about subject / section mocks.
// One widget so the Subject Mocks list, the Plans screen and the purchase sheets all say the
// same thing the same way: a red box whose border pulses and whose PLEASE NOTE tag blinks.
import 'package:flutter/material.dart';

class SectNote extends StatefulWidget {
  const SectNote({super.key, this.margin = EdgeInsets.zero, this.text = _same});
  final EdgeInsetsGeometry margin;
  final String text;

  static const _same = 'Subject (section) mocks are the SAME full mocks, only split into sections. They are not separate or extra tests.';
  static const list = 'These are NOT new questions. Each test is one section of the same-numbered full mock, given as a separate timed test. One pass unlocks both.';

  @override
  State<SectNote> createState() => _SectNoteState();
}

class _SectNoteState extends State<SectNote> with SingleTickerProviderStateMixin {
  late final AnimationController _c;

  @override
  void initState() {
    super.initState();
    _c = AnimationController(vsync: this, duration: const Duration(milliseconds: 650))..repeat(reverse: true);
  }

  @override
  void dispose() {
    _c.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    const red = Color(0xFFDC2626);
    return AnimatedBuilder(
      animation: _c,
      builder: (context, child) {
        final t = Curves.easeInOut.transform(_c.value);
        return Container(
          margin: widget.margin,
          padding: const EdgeInsets.fromLTRB(12, 10, 12, 10),
          decoration: BoxDecoration(
            color: const Color(0xFFFEF2F2),
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: Color.lerp(red, const Color(0xFFF59E0B), t)!, width: 2),
            boxShadow: [BoxShadow(color: red.withValues(alpha: .35 * (1 - t)), blurRadius: 4 + 8 * t, spreadRadius: 3 * t)],
          ),
          child: Column(crossAxisAlignment: CrossAxisAlignment.start, mainAxisSize: MainAxisSize.min, children: [
            Opacity(
              opacity: 1 - .8 * t,
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                decoration: BoxDecoration(color: red, borderRadius: BorderRadius.circular(6)),
                child: const Text('⚠ PLEASE NOTE', style: TextStyle(fontSize: 11.5, fontWeight: FontWeight.w900, color: Colors.white, letterSpacing: .5)),
              ),
            ),
            const SizedBox(height: 6),
            child!,
          ]),
        );
      },
      child: Text(widget.text, style: const TextStyle(fontSize: 13.5, height: 1.35, fontWeight: FontWeight.w700, color: Color(0xFF7F1D1D))),
    );
  }
}
