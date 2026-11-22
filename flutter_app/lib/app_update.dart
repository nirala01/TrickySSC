// TSSC-INAPPUPDATE-V1: Google Play in-app updates.
// When Play has a newer version for this phone (testers and, after launch, everyone), the app shows
// "Update available" on Home and a red dot on Me; one tap installs it without leaving the app.
import 'dart:io';

import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:in_app_update/in_app_update.dart';
import 'package:url_launcher/url_launcher.dart';

import 'profile.dart' show appVersion;

const _storeUrl = 'https://play.google.com/store/apps/details?id=com.trickyssc.app';

class AppUpdater {
  AppUpdater._();

  /// The newer version code on Play, or null when the app is up to date (or this is not a Play install).
  static final ValueNotifier<int?> available = ValueNotifier<int?>(null);
  static AppUpdateInfo? _info;
  static bool _busy = false;

  /// Asks Play whether a newer version exists. Quiet: any error means "nothing to show".
  static Future<bool> check() async {
    if (kIsWeb || !Platform.isAndroid || kDebugMode) return false;
    try {
      final i = await InAppUpdate.checkForUpdate();
      _info = i;
      final has = i.updateAvailability == UpdateAvailability.updateAvailable ||
          i.updateAvailability == UpdateAvailability.developerTriggeredUpdateInProgress;
      available.value = has ? (i.availableVersionCode ?? 0) : null;
      return has;
    } catch (_) {
      return false;
    }
  }

  /// Installs the update: full-screen Play update when allowed, else a background download and restart.
  /// Falls back to the Play Store page.
  static Future<void> update(BuildContext context) async {
    if (_busy) return;
    _busy = true;
    final msg = ScaffoldMessenger.maybeOf(context);
    try {
      if (_info == null) await check();
      final i = _info;
      if (i != null && available.value != null) {
        if (i.immediateUpdateAllowed) {
          final r = await InAppUpdate.performImmediateUpdate();
          if (r == AppUpdateResult.success) return;
          if (r == AppUpdateResult.userDeniedUpdate) return;
        } else if (i.flexibleUpdateAllowed) {
          msg?.showSnackBar(const SnackBar(content: Text('Downloading the update… the app will restart when it is ready.')));
          final r = await InAppUpdate.startFlexibleUpdate();
          if (r == AppUpdateResult.success) {
            await InAppUpdate.completeFlexibleUpdate();
            return;
          }
          if (r == AppUpdateResult.userDeniedUpdate) return;
        }
      }
      await launchUrl(Uri.parse(_storeUrl), mode: LaunchMode.externalApplication);
    } catch (_) {
      try {
        await launchUrl(Uri.parse(_storeUrl), mode: LaunchMode.externalApplication);
      } catch (_) {}
    } finally {
      _busy = false;
    }
  }

  /// Me > App updates: checks now and tells the student what it found.
  static Future<void> checkNow(BuildContext context) async {
    final msg = ScaffoldMessenger.maybeOf(context);
    msg?.showSnackBar(const SnackBar(content: Text('Checking for updates…'), duration: Duration(seconds: 1)));
    final has = await check();
    if (!context.mounted) return;
    if (has) {
      await update(context);
    } else {
      msg?.showSnackBar(SnackBar(content: Text('You have the latest version ($appVersion).')));
    }
  }
}

/// On opening the app: a popup, like the plans popup, while a newer version is waiting. Once per app open.
Future<void> showUpdatePopup(BuildContext context) async {
  if (_shownThisOpen) return;
  final v = AppUpdater.available.value;
  if (v == null) return;
  _shownThisOpen = true;
  await showDialog<void>(
    context: context,
    builder: (c) => Dialog(
      backgroundColor: Colors.white,
      insetPadding: const EdgeInsets.symmetric(horizontal: 22, vertical: 24),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(24)),
      child: SingleChildScrollView(
        padding: const EdgeInsets.fromLTRB(18, 8, 18, 14),
        child: Column(mainAxisSize: MainAxisSize.min, crossAxisAlignment: CrossAxisAlignment.stretch, children: [
          Align(alignment: Alignment.centerRight, child: IconButton(onPressed: () => Navigator.pop(c), icon: const Icon(Icons.close, color: Color(0xFF64748B)))),
          Center(
            child: Container(
              width: 72,
              height: 72,
              alignment: Alignment.center,
              decoration: BoxDecoration(color: const Color(0xFFDCFCE7), borderRadius: BorderRadius.circular(22)),
              child: const Icon(Icons.system_update_rounded, size: 40, color: Color(0xFF16A34A)),
            ),
          ),
          const SizedBox(height: 12),
          const Text('New version available', textAlign: TextAlign.center, style: TextStyle(fontSize: 23, fontWeight: FontWeight.w900, color: Color(0xFF1E1B4B))),
          const SizedBox(height: 4),
          Text(v > 0 ? 'Version 2.0.$v · you have $appVersion' : 'You have $appVersion',
              textAlign: TextAlign.center, style: const TextStyle(fontSize: 13.5, color: Color(0xFF64748B), fontWeight: FontWeight.w700)),
          const SizedBox(height: 12),
          const Text('Update now to get the latest features and fixes. It takes less than a minute and your tests, scores and pass stay as they are.',
              textAlign: TextAlign.center, style: TextStyle(fontSize: 14.5, height: 1.4, color: Color(0xFF334155), fontWeight: FontWeight.w600)),
          const SizedBox(height: 16),
          FilledButton(
            onPressed: () {
              Navigator.pop(c);
              AppUpdater.update(context);
            },
            style: FilledButton.styleFrom(backgroundColor: const Color(0xFF16A34A), minimumSize: const Size.fromHeight(52), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14))),
            child: const Text('Update now', style: TextStyle(fontSize: 16.5, fontWeight: FontWeight.w900)),
          ),
          const SizedBox(height: 4),
          TextButton(onPressed: () => Navigator.pop(c), child: const Text('Later', style: TextStyle(fontSize: 15, fontWeight: FontWeight.w800, color: Color(0xFF64748B)))),
        ]),
      ),
    ),
  );
}

bool _shownThisOpen = false;

/// Home: a slim strip shown only while an update is waiting.
class UpdateStrip extends StatelessWidget {
  const UpdateStrip({super.key});

  @override
  Widget build(BuildContext context) => ValueListenableBuilder<int?>(
        valueListenable: AppUpdater.available,
        builder: (_, v, __) => v == null
            ? const SizedBox.shrink()
            : Padding(
                padding: const EdgeInsets.only(bottom: 8),
                child: Material(
                  color: const Color(0xFFDCFCE7),
                  borderRadius: BorderRadius.circular(14),
                  child: InkWell(
                    borderRadius: BorderRadius.circular(14),
                    onTap: () => AppUpdater.update(context),
                    child: Padding(
                      padding: const EdgeInsets.fromLTRB(12, 8, 8, 8),
                      child: Row(children: [
                        const Icon(Icons.system_update_rounded, color: Color(0xFF15803D), size: 22),
                        const SizedBox(width: 10),
                        const Expanded(
                          child: Text('New version available', style: TextStyle(fontWeight: FontWeight.w800, color: Color(0xFF14532D), fontSize: 14.5)),
                        ),
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 7),
                          decoration: BoxDecoration(color: const Color(0xFF16A34A), borderRadius: BorderRadius.circular(10)),
                          child: const Text('Update', style: TextStyle(color: Colors.white, fontWeight: FontWeight.w800)),
                        ),
                      ]),
                    ),
                  ),
                ),
              ),
      );
}
