#!/usr/bin/env python3
"""
🔍 Port Forwarding Test Tool
Test se il port forwarding funziona correttamente per il RAT server
"""

import socket
import requests
import time
import threading
from datetime import datetime

def test_local_port(port=12000):
    """Test se la porta è aperta localmente"""
    print(f"🔍 Testing local port {port}...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        
        if result == 0:
            print(f"✅ Port {port} is OPEN locally")
            return True
        else:
            print(f"❌ Port {port} is CLOSED locally")
            return False
    except Exception as e:
        print(f"❌ Error testing local port: {e}")
        return False

def test_external_port(external_ip, port=12000):
    """Test se la porta è raggiungibile dall'esterno"""
    print(f"🌐 Testing external access {external_ip}:{port}...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        result = sock.connect_ex((external_ip, port))
        sock.close()
        
        if result == 0:
            print(f"✅ Port {port} is ACCESSIBLE from external IP {external_ip}")
            return True
        else:
            print(f"❌ Port {port} is NOT accessible from external IP {external_ip}")
            return False
    except Exception as e:
        print(f"❌ Error testing external port: {e}")
        return False

def test_http_response(ip, port=12000):
    """Test se il server HTTP risponde correttamente"""
    print(f"🌐 Testing HTTP response from {ip}:{port}...")
    try:
        url = f"http://{ip}:{port}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200 or response.status_code == 302:
            print(f"✅ HTTP server responding on {ip}:{port} (Status: {response.status_code})")
            return True
        else:
            print(f"⚠️ HTTP server responding but with status {response.status_code}")
            return False
    except requests.exceptions.ConnectTimeout:
        print(f"❌ Connection timeout to {ip}:{port}")
        return False
    except requests.exceptions.ConnectionError:
        print(f"❌ Connection refused to {ip}:{port}")
        return False
    except Exception as e:
        print(f"❌ HTTP test error: {e}")
        return False

def get_public_ip():
    """Ottieni il tuo IP pubblico"""
    try:
        response = requests.get('https://api.ipify.org', timeout=5)
        return response.text.strip()
    except:
        try:
            response = requests.get('https://ifconfig.me', timeout=5)
            return response.text.strip()
        except:
            return None

def get_local_ip():
    """Ottieni il tuo IP locale"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        local_ip = sock.getsockname()[0]
        sock.close()
        return local_ip
    except:
        return "127.0.0.1"

def test_rat_endpoints(ip, port=12000):
    """Test specifici endpoint del RAT"""
    print(f"🤖 Testing RAT endpoints on {ip}:{port}...")
    
    endpoints = [
        "/api/rat_connect",
        "/api/heartbeat", 
        "/dashboard",
        "/"
    ]
    
    results = {}
    for endpoint in endpoints:
        try:
            url = f"http://{ip}:{port}{endpoint}"
            response = requests.get(url, timeout=5)
            results[endpoint] = response.status_code
            print(f"  {endpoint}: Status {response.status_code}")
        except Exception as e:
            results[endpoint] = f"Error: {e}"
            print(f"  {endpoint}: ❌ {e}")
    
    return results

def continuous_test(ip, port=12000, duration=60):
    """Test continuo per verificare la stabilità"""
    print(f"🔄 Starting continuous test for {duration} seconds...")
    start_time = time.time()
    success_count = 0
    total_count = 0
    
    while time.time() - start_time < duration:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            result = sock.connect_ex((ip, port))
            sock.close()
            
            total_count += 1
            if result == 0:
                success_count += 1
                print(f"✅ Test {total_count}: Connection successful")
            else:
                print(f"❌ Test {total_count}: Connection failed")
                
            time.sleep(2)
        except KeyboardInterrupt:
            break
        except Exception as e:
            total_count += 1
            print(f"❌ Test {total_count}: Error - {e}")
            time.sleep(2)
    
    success_rate = (success_count / total_count * 100) if total_count > 0 else 0
    print(f"\n📊 Continuous test results:")
    print(f"   Total tests: {total_count}")
    print(f"   Successful: {success_count}")
    print(f"   Success rate: {success_rate:.1f}%")
    
    return success_rate

def main():
    print("🔥 PORT FORWARDING TEST TOOL")
    print("=" * 50)
    
    # Get IPs
    local_ip = get_local_ip()
    public_ip = get_public_ip()
    
    print(f"🏠 Local IP: {local_ip}")
    print(f"🌍 Public IP: {public_ip}")
    print()
    
    # Test port
    port = 12000
    
    # 1. Test local port
    print("1️⃣ TESTING LOCAL PORT")
    local_ok = test_local_port(port)
    print()
    
    # 2. Test local HTTP
    print("2️⃣ TESTING LOCAL HTTP")
    local_http_ok = test_http_response(local_ip, port)
    print()
    
    # 3. Test external port (if public IP available)
    if public_ip and public_ip != local_ip:
        print("3️⃣ TESTING EXTERNAL PORT")
        external_ok = test_external_port(public_ip, port)
        print()
        
        print("4️⃣ TESTING EXTERNAL HTTP")
        external_http_ok = test_http_response(public_ip, port)
        print()
    else:
        print("3️⃣ ⚠️ Cannot test external access (no public IP or same as local)")
        external_ok = False
        external_http_ok = False
        print()
    
    # 4. Test RAT endpoints
    print("5️⃣ TESTING RAT ENDPOINTS")
    rat_results = test_rat_endpoints(local_ip, port)
    print()
    
    # 5. Quick continuous test
    print("6️⃣ TESTING CONNECTION STABILITY")
    stability = continuous_test(local_ip, port, 30)
    print()
    
    # Summary
    print("📋 SUMMARY")
    print("=" * 50)
    print(f"Local Port Open: {'✅' if local_ok else '❌'}")
    print(f"Local HTTP Working: {'✅' if local_http_ok else '❌'}")
    print(f"External Port Open: {'✅' if external_ok else '❌'}")
    print(f"External HTTP Working: {'✅' if external_http_ok else '❌'}")
    print(f"Connection Stability: {stability:.1f}%")
    
    if local_ok and local_http_ok:
        print("\n✅ LOCAL ACCESS: Working perfectly!")
        print(f"   Use this for local network: {local_ip}:{port}")
    
    if external_ok and external_http_ok:
        print("\n✅ EXTERNAL ACCESS: Port forwarding working!")
        print(f"   Use this for external access: {public_ip}:{port}")
    elif public_ip:
        print("\n❌ EXTERNAL ACCESS: Port forwarding NOT working")
        print("   Check your router configuration")
    
    print("\n🔧 TROUBLESHOOTING TIPS:")
    if not local_ok:
        print("   - Start the RAT server first: python3 app.py")
        print("   - Check if port 12000 is already in use")
    
    if not external_ok and public_ip:
        print("   - Configure port forwarding on your router")
        print(f"   - Forward external port {port} to {local_ip}:{port}")
        print("   - Check firewall settings")
        print("   - Ensure router supports port forwarding")

if __name__ == "__main__":
    main()