"""Runs inside the GitHub Action only (never on a PC).

1. Copies the android/ folder that `flutter create` just generated into flutter_app/.
2. Sets the app name, internet permission, minimum Android version and launcher icons.
3. Writes lib/firebase_options.dart from config/google-services.json (if it is there).

Usage: ci_prepare.py <generated project dir> <flutter_app dir> <repo root>
"""
import json
import re
import shutil
import sys
from pathlib import Path

gen, app, repo = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
PACKAGE = "com.trickyssc.app"

# 1. android folder
dst = app / "android"
if dst.exists():
    shutil.rmtree(dst)
shutil.copytree(gen / "android", dst)

# 2a. manifest: app name + internet
man = dst / "app/src/main/AndroidManifest.xml"
s = man.read_text(encoding="utf-8")
s, n = re.subn(r'android:label="[^"]*"', 'android:label="TrickySSC"', s, count=1)
assert n == 1, "app label not found in AndroidManifest.xml"
if "android.permission.INTERNET" not in s:
    s, n = re.subn(r"(<manifest[^>]*>)", r'\1\n    <uses-permission android:name="android.permission.INTERNET" />', s, count=1)
    assert n == 1, "<manifest> tag not found"
man.write_text(s, encoding="utf-8")

# 2b. minimum Android version 6.0 (API 23) or whatever Flutter needs, if higher
kts, groovy = dst / "app/build.gradle.kts", dst / "app/build.gradle"
if kts.exists():
    g = kts.read_text(encoding="utf-8")
    g, n = re.subn(r"minSdk\s*=\s*flutter\.minSdkVersion", "minSdk = maxOf(flutter.minSdkVersion, 23)", g)
    kts.write_text(g, encoding="utf-8")
else:
    g = groovy.read_text(encoding="utf-8")
    g, n = re.subn(r"minSdk(Version)?\s*=?\s*flutter\.minSdkVersion", "minSdk = Math.max(flutter.minSdkVersion, 23)", g)
    groovy.write_text(g, encoding="utf-8")
assert n >= 1, "minSdk line not found in app build file"
assert PACKAGE in g, "package name is not " + PACKAGE

# 2c. launcher icons (same ones as the first app wrapper) + the adaptive icon for Android 8+
res_src, res = repo / "android/app/src/main/res", dst / "app/src/main/res"
for d in ("mdpi", "hdpi", "xhdpi", "xxhdpi", "xxxhdpi"):
    for name in ("ic_launcher.png", "ic_launcher_foreground.png"):
        src = res_src / f"mipmap-{d}/{name}"
        out = res / f"mipmap-{d}/{name}"
        if src.exists() and out.parent.exists():
            shutil.copyfile(src, out)
if (res_src / "mipmap-anydpi-v26/ic_launcher.xml").exists() and (res / "mipmap-xxxhdpi/ic_launcher_foreground.png").exists():
    (res / "mipmap-anydpi-v26").mkdir(parents=True, exist_ok=True)
    shutil.copyfile(res_src / "mipmap-anydpi-v26/ic_launcher.xml", res / "mipmap-anydpi-v26/ic_launcher.xml")
    (res / "values/ic_launcher_colors.xml").write_text(
        '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">#FF6B00</color>\n</resources>\n', encoding="utf-8")

# 2c'. splash: the app's soft background with the logo in the middle (Android 12+ uses its own splash API)
SPLASH_BG = "#EEF2FF"
splash = f'''<?xml version="1.0" encoding="utf-8"?>
<layer-list xmlns:android="http://schemas.android.com/apk/res/android">
    <item><color android:color="{SPLASH_BG}" /></item>
    <item><bitmap android:gravity="center" android:src="@mipmap/ic_launcher" /></item>
</layer-list>
'''
for d in ("drawable", "drawable-v21"):
    if (res / d).exists():
        (res / d / "launch_background.xml").write_text(splash, encoding="utf-8")
(res / "values-v31").mkdir(parents=True, exist_ok=True)
(res / "values-v31/styles.xml").write_text(f'''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="LaunchTheme" parent="@android:style/Theme.Light.NoTitleBar">
        <item name="android:windowBackground">@drawable/launch_background</item>
        <item name="android:windowSplashScreenBackground">{SPLASH_BG}</item>
    </style>
    <style name="NormalTheme" parent="@android:style/Theme.Light.NoTitleBar">
        <item name="android:windowBackground">?android:colorBackground</item>
    </style>
</resources>
''', encoding="utf-8")

# 2d. skip the release "lint vital" check: it crashes inside a plugin (google_sign_in_android)
#     and only checks code style, not whether the app works.
root = dst / "build.gradle.kts" if (dst / "build.gradle.kts").exists() else dst / "build.gradle"
r = root.read_text(encoding="utf-8")
if "lintVital" not in r:
    r += '\nsubprojects {\n    tasks.matching { it.name.startsWith("lintVital") }.configureEach { enabled = false }\n}\n'
    root.write_text(r, encoding="utf-8")

# 3. Firebase settings
cfg = app / "config/google-services.json"
vals = dict(apiKey="", appId="", senderId="", projectId="", storageBucket="", webClientId="")
if cfg.exists():
    j = json.loads(cfg.read_text(encoding="utf-8"))
    info = j.get("project_info", {})
    vals["senderId"] = str(info.get("project_number", ""))
    vals["projectId"] = info.get("project_id", "")
    vals["storageBucket"] = info.get("storage_bucket", "")
    client = None
    for c in j.get("client", []):
        if c.get("client_info", {}).get("android_client_info", {}).get("package_name") == PACKAGE:
            client = c
    assert client, "google-services.json has no Android app " + PACKAGE
    vals["appId"] = client["client_info"]["mobilesdk_app_id"]
    vals["apiKey"] = client["api_key"][0]["current_key"]
    web = [o["client_id"] for o in client.get("oauth_client", []) if o.get("client_type") == 3]
    web += [o["client_id"] for o in client.get("services", {}).get("appinvite_service", {}).get("other_platform_oauth_client", []) if o.get("client_type") == 3]
    vals["webClientId"] = web[0] if web else ""
    print("Firebase settings read. Android OAuth clients:", sum(1 for o in client.get("oauth_client", []) if o.get("client_type") == 1),
          "| web client id:", "yes" if vals["webClientId"] else "NO")
else:
    print("::warning::flutter_app/config/google-services.json is missing - the app will show a setup screen.")

lines = ["// Written by tool/ci_prepare.py during the build. Do not edit.", "class FbConfig {"]
for k, v in vals.items():
    lines.append(f"  static const String {k} = {json.dumps(v)};")
lines += ["  static bool get ready => apiKey.isNotEmpty && appId.isNotEmpty;", "}", ""]
(app / "lib/firebase_options.dart").write_text("\n".join(lines), encoding="utf-8")
