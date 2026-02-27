[app]
title = AdMobApp
package.name = app_by_bhavi
package.domain = org.test_bhavi
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,gif,mp4
version = 0.1

# REQUIREMENTS: Cython yahan se hata diya hai (Internal handle hoga)
requirements = python3, kivy==2.3.0, kivymd, pyjnius, android, pyparsing

orientation = portrait
fullscreen = 0

# Permissions for AdMob
android.permissions = INTERNET, ACCESS_NETWORK_STATE, AD_ID

# STABLE BUILD COMBO: API 33 + NDK 25b
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.accept_sdk_license = True

# AdMob Meta-data (Important for AdMob initialization)
android.meta_data = com.google.android.gms.ads.APPLICATION_ID=ca-app-pub-3940256099942544~3347511713

# Dependencies for AdMob & AndroidX
android.gradle_dependencies = "com.google.android.gms:play-services-ads:22.6.0", "androidx.appcompat:appcompat:1.6.1", "androidx.core:core:1.9.0"

android.enable_androidx = True

# Java compatibility for Java 17 Runners
android.add_compile_options = "sourceCompatibility = 1.8", "targetCompatibility = 1.8"

# Archs for Play Store & Modern Phones
android.archs = armeabi-v7a, arm64-v8a

p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
