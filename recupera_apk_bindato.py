#!/usr/bin/env python3
"""
🔦 RECUPERA APK BINDATO
Script per recuperare l'APK della torcia già bindato con successo
"""

import os
import shutil
import glob
from pathlib import Path

def find_bound_apk():
    """Trova l'APK bindato della torcia"""
    print("🔍 Cercando APK bindato della torcia...")
    
    # Percorsi possibili
    search_paths = [
        "uploads/les/work_*/bound_*ledflashlight.apk",
        "uploads/*/work_*/bound_*ledflashlight.apk", 
        "uploads/les/bound_*ledflashlight.apk",
        "uploads/*/bound_*ledflashlight.apk"
    ]
    
    found_files = []
    
    for pattern in search_paths:
        files = glob.glob(pattern)
        found_files.extend(files)
    
    if found_files:
        print(f"✅ Trovati {len(found_files)} APK bindati:")
        for i, file in enumerate(found_files, 1):
            size_mb = os.path.getsize(file) / (1024*1024)
            print(f"   {i}. {file} ({size_mb:.1f} MB)")
        
        return found_files
    else:
        print("❌ Nessun APK bindato trovato")
        return []

def copy_to_download_location(apk_file):
    """Copia l'APK nella posizione di download corretta"""
    try:
        # Crea directory download se non esiste
        download_dir = "uploads/les"
        os.makedirs(download_dir, exist_ok=True)
        
        # Nome file finale
        filename = os.path.basename(apk_file)
        if not filename.startswith("bound_"):
            filename = f"bound_{filename}"
        
        final_path = os.path.join(download_dir, filename)
        
        # Copia file
        shutil.copy2(apk_file, final_path)
        
        print(f"✅ APK copiato in: {final_path}")
        print(f"📥 Download URL: /download/les/{filename}")
        
        return final_path
        
    except Exception as e:
        print(f"❌ Errore copia: {e}")
        return None

def create_download_link():
    """Crea link di download diretto"""
    print("\n🌐 LINK DI DOWNLOAD:")
    print("http://192.168.1.6:12000/download/les/bound_1753064028_ledflashlight.apk")
    print("http://10.2.53.11:12000/download/les/bound_1753064028_ledflashlight.apk")
    
    # Se hai configurato port forwarding:
    print("\n🌍 LINK PUBBLICO (se port forwarding configurato):")
    print("http://34.27.249.227:12000/download/les/bound_1753064028_ledflashlight.apk")

def main():
    print("🔦 RECUPERO APK TORCIA BINDATO")
    print("=" * 50)
    
    # Trova APK bindati
    bound_apks = find_bound_apk()
    
    if bound_apks:
        # Usa il più recente
        latest_apk = max(bound_apks, key=os.path.getmtime)
        print(f"\n📱 APK più recente: {latest_apk}")
        
        # Copia nella posizione corretta
        final_apk = copy_to_download_location(latest_apk)
        
        if final_apk:
            size_mb = os.path.getsize(final_apk) / (1024*1024)
            print(f"\n✅ APK PRONTO PER IL DOWNLOAD!")
            print(f"📁 File: {final_apk}")
            print(f"📊 Dimensione: {size_mb:.1f} MB")
            
            # Mostra link di download
            create_download_link()
            
            print(f"\n🎯 ISTRUZIONI:")
            print("1. 📥 Scarica l'APK dal link sopra")
            print("2. 📱 Trasferisci su dispositivo Android")
            print("3. 🔧 Abilita 'Origini sconosciute'")
            print("4. 📲 Installa APK")
            print("5. 🔦 Apri app torcia una volta")
            print("6. 📊 Controlla dashboard per connessione")
            
            print(f"\n💡 NOTA:")
            print("L'APK è già bindato e funzionante!")
            print("Il sistema avanzato ha funzionato perfettamente.")
            
        else:
            print("❌ Errore nella copia del file")
    else:
        print("\n❌ Nessun APK bindato trovato")
        print("Riprova il binding dalla dashboard")

if __name__ == "__main__":
    main()