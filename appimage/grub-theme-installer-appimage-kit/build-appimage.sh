#!/bin/bash
# Build script for GRUB Theme Installer AppImage

set -e

echo "=== Building GRUB Theme Installer AppImage ==="

# Download appimagetool if not present
if [ ! -f appimagetool-x86_64.AppImage ]; then
    echo "Downloading appimagetool..."
    wget -q "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
    chmod +x appimagetool-x86_64.AppImage
fi

# Verify AppDir structure
echo "Verifying AppDir structure..."
if [ ! -f grub-theme-installer.AppDir/AppRun ]; then
    echo "Error: AppRun not found!"
    exit 1
fi

if [ ! -f grub-theme-installer.AppDir/grub-theme-installer.desktop ]; then
    echo "Error: .desktop file not found!"
    exit 1
fi

# Build the AppImage
echo "Building AppImage..."
ARCH=x86_64 ./appimagetool-x86_64.AppImage grub-theme-installer.AppDir GrubThemeInstaller-x86_64.AppImage

if [ -f GrubThemeInstaller-x86_64.AppImage ]; then
    chmod +x GrubThemeInstaller-x86_64.AppImage
    echo ""
    echo "=== Build Complete! ==="
    echo "AppImage created: GrubThemeInstaller-x86_64.AppImage"
    echo ""
    echo "To use:"
    echo "  1. Add your theme folders to grub-theme-installer.AppDir/themes/"
    echo "  2. Run this script again to rebuild"
    echo "  3. Execute with: sudo ./GrubThemeInstaller-x86_64.AppImage"
    echo ""
    ls -lh GrubThemeInstaller-x86_64.AppImage
else
    echo "Error: AppImage build failed!"
    exit 1
fi
