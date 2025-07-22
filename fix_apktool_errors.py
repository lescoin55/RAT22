#!/usr/bin/env python3
"""
🔧 Fix APKTool Binding Errors
Risolve errori comuni durante il binding di APK
"""

import os
import shutil
import subprocess
import tempfile
from pathlib import Path

def check_apktool_version():
    """Verifica versione apktool"""
    try:
        result = subprocess.run(['apktool', '--version'], capture_output=True, text=True)
        print(f"📦 APKTool version: {result.stdout.strip()}")
        return True
    except:
        print("❌ APKTool not found or not working")
        return False

def fix_apk_compatibility(apk_path, output_dir):
    """Prova a fixare problemi di compatibilità APK"""
    print(f"🔧 Fixing APK compatibility for: {apk_path}")
    
    # Crea directory temporanea
    temp_dir = tempfile.mkdtemp()
    decoded_dir = os.path.join(temp_dir, "decoded")
    
    try:
        # 1. Decompila con opzioni conservative
        print("📂 Decompiling APK with conservative options...")
        cmd = [
            'apktool', 'd', apk_path,
            '-o', decoded_dir,
            '--no-src',  # Non decompila sorgenti Java
            '--force-manifest',  # Forza decompilazione manifest
            '--no-debug-info'  # Rimuove info debug
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Decompilation failed: {result.stderr}")
            return False
        
        print("✅ Decompilation successful")
        
        # 2. Modifica apktool.yml per compatibilità
        yml_path = os.path.join(decoded_dir, "apktool.yml")
        if os.path.exists(yml_path):
            print("🔧 Fixing apktool.yml...")
            with open(yml_path, 'r') as f:
                content = f.read()
            
            # Fix common issues
            content = content.replace('unknownFiles: {}', 'unknownFiles:\n  assets/webkit/: true')
            content = content.replace('doNotCompress:', 'doNotCompress:\n- assets/webkit/\n- "*.so"')
            
            with open(yml_path, 'w') as f:
                f.write(content)
        
        # 3. Ricompila con opzioni conservative
        print("📦 Recompiling APK...")
        output_apk = os.path.join(output_dir, "fixed_" + os.path.basename(apk_path))
        
        cmd = [
            'apktool', 'b', decoded_dir,
            '-o', output_apk,
            '--use-aapt2',  # Usa AAPT2 più moderno
            '--no-crunch'   # Non ottimizza PNG
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Recompilation failed: {result.stderr}")
            return False
        
        print(f"✅ APK fixed successfully: {output_apk}")
        return output_apk
        
    finally:
        # Cleanup
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

def suggest_alternative_apks():
    """Suggerisce APK alternativi che funzionano meglio"""
    print("\n💡 ALTERNATIVE APK SUGGESTIONS")
    print("=" * 50)
    
    alternatives = [
        {
            "name": "Simple Flashlight",
            "reason": "Meno complesso, meno errori apktool",
            "size": "~1MB",
            "compatibility": "Excellent"
        },
        {
            "name": "File Manager (Simple)",
            "reason": "Struttura APK più semplice",
            "size": "~3MB", 
            "compatibility": "Very Good"
        },
        {
            "name": "QR Scanner (Basic)",
            "reason": "Pochi componenti nativi",
            "size": "~2MB",
            "compatibility": "Good"
        },
        {
            "name": "Note App (Simple)",
            "reason": "Architettura molto semplice",
            "size": "~1-2MB",
            "compatibility": "Excellent"
        }
    ]
    
    for i, app in enumerate(alternatives, 1):
        print(f"{i}. {app['name']}")
        print(f"   Size: {app['size']}")
        print(f"   Compatibility: {app['compatibility']}")
        print(f"   Why: {app['reason']}")
        print()

def create_simple_test_apk():
    """Crea un APK di test semplice"""
    print("\n🛠️ CREATING SIMPLE TEST APK")
    print("=" * 50)
    
    # Template per APK semplice
    manifest_template = '''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.test.simple"
    android:versionCode="1"
    android:versionName="1.0">
    
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
    <uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
    <uses-permission android:name="android.permission.CAMERA" />
    <uses-permission android:name="android.permission.RECORD_AUDIO" />
    <uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED" />
    
    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="Simple Test"
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
    
    print("📝 Template APK manifest created")
    print("💡 Use Android Studio to create a simple app with this manifest")
    print("🎯 This will have all required permissions and minimal complexity")

def troubleshoot_apktool_error(error_message):
    """Analizza errore apktool e suggerisce soluzioni"""
    print("\n🔍 APKTOOL ERROR ANALYSIS")
    print("=" * 50)
    
    if "Unsigned short value out of range" in error_message:
        print("❌ Error Type: DEX compilation overflow")
        print("\n🔧 SOLUTIONS:")
        print("1. APK troppo complesso per apktool")
        print("2. Usa APK più semplice (meno di 5MB)")
        print("3. Prova versione diversa di apktool")
        print("4. Usa APK con meno librerie native")
        
    elif "SmaliBuilder" in error_message:
        print("❌ Error Type: Smali compilation error")
        print("\n🔧 SOLUTIONS:")
        print("1. APK ha codice obfuscato")
        print("2. Usa APK non obfuscato")
        print("3. Prova con --no-src flag")
        
    elif "Exception occurred while writing code_item" in error_message:
        print("❌ Error Type: Code generation error")
        print("\n🔧 SOLUTIONS:")
        print("1. APK ha metodi troppo complessi")
        print("2. Scegli APK più semplice")
        print("3. Evita APK con ProGuard/R8")

def main():
    print("🔥 APKTOOL ERROR FIXER")
    print("=" * 50)
    
    # Check apktool
    if not check_apktool_version():
        print("❌ Please install apktool first")
        return
    
    # Analizza errore specifico
    error_msg = """
    Exception in thread "main" com.android.tools.smali.util.ExceptionWithContext: 
    Exception occurred while writing code_item for method LA3/b;->values()[LA3/b;
    Caused by: com.android.tools.smali.util.ExceptionWithContext: 
    Unsigned short value out of range: 65681
    """
    
    troubleshoot_apktool_error(error_msg)
    suggest_alternative_apks()
    create_simple_test_apk()
    
    print("\n✅ IMMEDIATE SOLUTIONS:")
    print("1. 🔄 Try a SIMPLER flashlight app (under 2MB)")
    print("2. 📱 Use 'Simple Flashlight' instead of 'LED Flashlight'")
    print("3. 🛠️ Create custom test APK with Android Studio")
    print("4. 📂 Try File Manager app instead")

if __name__ == "__main__":
    main()