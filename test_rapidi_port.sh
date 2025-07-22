#!/bin/bash
# 🔍 Test Rapidi Port Forwarding

echo "🔥 TEST RAPIDI PORT FORWARDING"
echo "================================"

# Ottieni IP
LOCAL_IP=$(hostname -I | awk '{print $1}')
PUBLIC_IP=$(curl -s ifconfig.me 2>/dev/null || echo "N/A")

echo "🏠 IP Locale: $LOCAL_IP"
echo "🌍 IP Pubblico: $PUBLIC_IP"
echo ""

# Test 1: Porta locale
echo "1️⃣ TEST PORTA LOCALE"
if nc -z localhost 12000 2>/dev/null; then
    echo "✅ Porta 12000 APERTA localmente"
else
    echo "❌ Porta 12000 CHIUSA localmente"
fi

# Test 2: HTTP locale
echo ""
echo "2️⃣ TEST HTTP LOCALE"
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://$LOCAL_IP:12000 2>/dev/null)
if [ "$HTTP_STATUS" = "200" ] || [ "$HTTP_STATUS" = "302" ]; then
    echo "✅ Server HTTP funziona (Status: $HTTP_STATUS)"
else
    echo "❌ Server HTTP non risponde (Status: $HTTP_STATUS)"
fi

# Test 3: Endpoint RAT
echo ""
echo "3️⃣ TEST ENDPOINT RAT"
RAT_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://$LOCAL_IP:12000/api/rat_connect 2>/dev/null)
if [ "$RAT_STATUS" = "200" ]; then
    echo "✅ Endpoint RAT funziona (Status: $RAT_STATUS)"
else
    echo "❌ Endpoint RAT non funziona (Status: $RAT_STATUS)"
fi

# Test 4: Porta esterna (se IP pubblico disponibile)
echo ""
echo "4️⃣ TEST PORTA ESTERNA"
if [ "$PUBLIC_IP" != "N/A" ] && [ "$PUBLIC_IP" != "$LOCAL_IP" ]; then
    if nc -z -w5 $PUBLIC_IP 12000 2>/dev/null; then
        echo "✅ Porta 12000 RAGGIUNGIBILE dall'esterno"
    else
        echo "❌ Porta 12000 NON raggiungibile dall'esterno"
        echo "   → Configura port forwarding sul router"
    fi
else
    echo "⚠️ Impossibile testare accesso esterno"
fi

# Test 5: Processi in ascolto
echo ""
echo "5️⃣ PROCESSI IN ASCOLTO"
echo "Porte aperte:"
netstat -tulpn 2>/dev/null | grep :12000 || echo "Nessun processo in ascolto sulla porta 12000"

echo ""
echo "📋 RIASSUNTO"
echo "============"
echo "Per accesso LOCALE: http://$LOCAL_IP:12000"
if [ "$PUBLIC_IP" != "N/A" ]; then
    echo "Per accesso ESTERNO: http://$PUBLIC_IP:12000 (richiede port forwarding)"
fi

echo ""
echo "🔧 COMANDI UTILI:"
echo "Avvia server: python3 app.py"
echo "Test porta: nc -zv $LOCAL_IP 12000"
echo "Test HTTP: curl http://$LOCAL_IP:12000"
echo "Verifica processi: netstat -tulpn | grep 12000"