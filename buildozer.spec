[app]
title = AdMobApp
package.name = app_by_bhavi
package.domain = org.test_bhavi
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,gif,mp4
version = 0.1

# Requirements: Cython version locked for Kivy 2.2.1
requirements = python3, kivy==2.2.1, kivymd, pyjnius, android, pyparsing, cython==0.29.33

orientation = portrait
fullscreen = 0

android.permissions = INTERNET, ACCESS_NETWORK_STATE, AD_ID

# GOLDEN STABLE COMBO: API 33 + NDK 23b
android.api = 33
android.sdk = 33
android.ndk = 23b
android.accept_sdk_license = True

# AdMob Meta-data
android.meta_data = com.google.android.gms.ads.APPLICATION_ID=ca-app-pub-3940256099942544~3347511713

# Dependencies
android.gradle_dependencies = "com.google.android.gms:play-services-ads:22.4.0", "androidx.appcompat:appcompat:1.6.1", "androidx.core:core:1.9.0"

android.enable_androidx = True

# Java compatibility for Java 17 Runners
android.add_compile_options = "sourceCompatibility = 11", "targetCompatibility = 11"

# Support both 32-bit and 64-bit for maximum compatibility
android.archs = armeabi-v7a, arm64-v8a

p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
