// Back + Home on every screen.
import 'package:flutter/material.dart';

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
