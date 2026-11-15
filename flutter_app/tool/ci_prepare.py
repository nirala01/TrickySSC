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

# 2c. launcher icons (same ones as the first app wrapper)
for d in ("mdpi", "hdpi", "xhdpi", "xxhdpi", "xxxhdpi"):
    src = repo / f"android/app/src/main/res/mipmap-{d}/ic_launcher.png"
    out = dst / f"app/src/main/res/mipmap-{d}/ic_launcher.png"
    if src.exists() and out.parent.exists():
        shutil.copyfile(src, out)

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
