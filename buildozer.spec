[app]
title = NetClient
package.name = netclient
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# HTTPS POST icin gerekli ag kutuphaneleri
requirements = python3,kivy,openssl,certifi

orientation = portrait
fullscreen = 0

# --- Android ---
# Internet izni
android.permissions = android.permission.INTERNET
android.api = 34
android.minapi = 24
android.ndk_api = 24
android.archs = arm64-v8a
android.accept_sdk_license = True
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 0
