[app]
title = AdMobApprewared
package.name = app_by_bhavijati
package.domain = org.test_bhavijati
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,gif,mp4
version = 0.1

requirements = python3, kivy==2.3.0, kivymd, pyjnius, android, pyparsing,requests

orientation = portrait
fullscreen = 0

android.permissions = INTERNET, ACCESS_NETWORK_STATE, AD_ID

android.api = 33
android.minapi = 21
# Note: android.sdk ab zaroorat nahi hoti, sirf api kaafi hai
android.ndk = 25b
android.accept_sdk_license = True

android.meta_data = com.google.android.gms.ads.APPLICATION_ID=ca-app-pub-7264801834502563~9937823206

# FIX: Yahan se double quotes hata diye gaye hain
android.gradle_dependencies = com.google.android.gms:play-services-ads:22.6.0, androidx.appcompat:appcompat:1.6.1, androidx.core:core:1.9.0

android.enable_androidx = True

android.add_compile_options = "sourceCompatibility = 1.8", "targetCompatibility = 1.8"

android.archs = armeabi-v7a, arm64-v8a

p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
