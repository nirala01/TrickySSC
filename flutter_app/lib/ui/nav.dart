// Back + Home on every screen.
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import 'soft.dart';

/// Bumped to ask the shell to show its Home tab.
final homeRequest = ValueNotifier<int>(0);

void goHome(BuildContext context) {
  Navigator.of(context).popUntil((r) => r.isFirst);
  homeRequest.value++;
}

class HomeButton extends StatelessWidget {
  final Future<bool> Function()? confirm;
  const HomeButton({super.key, this.confirm});

  @override
  Widget build(BuildContext context) => IconButton(
        tooltip: 'Home',
        icon: const Icon(Icons.home_rounded),
        onPressed: () async {
          if (confirm != null && !await confirm!()) return;
          if (context.mounted) goHome(context);
        },
      );
}

/// TSSC-LISTUI-V3: the violet-to-blue header of every inner screen - white title with a yellow
/// stroke under it, Back and Home, and an optional line in a pill below.
PreferredSizeWidget softAppBar(String title, {String? sub, List<Widget>? actions}) => AppBar(
      backgroundColor: Colors.transparent,
      surfaceTintColor: Colors.transparent,
      scrolledUnderElevation: 0,
      elevation: 0,
      centerTitle: true,
      foregroundColor: Colors.white,
      iconTheme: const IconThemeData(color: Colors.white),
      systemOverlayStyle: SystemUiOverlayStyle.light,
      toolbarHeight: 60,
      actions: actions ?? const [HomeButton()],
      flexibleSpace: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(colors: [Color(0xFF6D28D9), Color(0xFF4338CA), Color(0xFF2563EB)], begin: Alignment.topLeft, end: Alignment.bottomRight),
          borderRadius: BorderRadius.vertical(bottom: Radius.circular(26)),
        ),
      ),
      title: Column(mainAxisSize: MainAxisSize.min, children: [
        Text(title, maxLines: 1, overflow: TextOverflow.ellipsis, style: baloo(21, color: Colors.white)),
        Container(margin: const EdgeInsets.only(top: 2), width: 56, height: 3, decoration: BoxDecoration(color: const Color(0xFFFBBF24), borderRadius: BorderRadius.circular(3))),
      ]),
      bottom: sub == null
          ? null
          : PreferredSize(
              preferredSize: const Size.fromHeight(46),
              child: Padding(
                padding: const EdgeInsets.fromLTRB(16, 0, 16, 12),
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 6),
                  decoration: BoxDecoration(color: const Color(0x26FFFFFF), borderRadius: BorderRadius.circular(999), border: Border.all(color: const Color(0x66FFFFFF))),
                  child: Text(sub, maxLines: 1, overflow: TextOverflow.ellipsis, style: const TextStyle(color: Colors.white, fontSize: 13.5, fontWeight: FontWeight.w700)),
                ),
              ),
            ),
    );
