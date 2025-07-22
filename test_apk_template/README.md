# Test APK Template for RAT Binding

## How to use:

1. Open Android Studio
2. Create new project
3. Replace AndroidManifest.xml with the provided template
4. Replace MainActivity.java with the provided template
5. Build APK in debug mode
6. Use the generated APK for RAT binding

## Features:
- All required permissions for RAT
- Minimal code (no obfuscation)
- Small size (~1MB)
- Compatible with apktool
- Target SDK 28 (stable)

## Build command:
./gradlew assembleDebug

The APK will be in: app/build/outputs/apk/debug/app-debug.apk
