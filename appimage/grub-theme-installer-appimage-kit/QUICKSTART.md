# Quick Start Guide - Building GRUB Theme Installer AppImage

## Prerequisites

You need to download `appimagetool` manually since network access is restricted in this environment.

### Download appimagetool

On your Linux system, run:

```bash
wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
chmod +x appimagetool-x86_64.AppImage
```

## Build Steps

1. **Extract the provided package** to your Linux system

2. **Add your theme files**:
   ```bash
   # Example: Adding a Cyberpunk theme
   mkdir -p grub-theme-installer.AppDir/themes/Cyberpunk
   cp -r /path/to/Cyberpunk-theme/* grub-theme-installer.AppDir/themes/Cyberpunk/
   
   # Add watermark
   cp watermark.png grub-theme-installer.AppDir/themes/
   ```

3. **Run the build script**:
   ```bash
   chmod +x build-appimage.sh
   ./build-appimage.sh
   ```

4. **Or build manually**:
   ```bash
   ARCH=x86_64 ./appimagetool-x86_64.AppImage grub-theme-installer.AppDir GrubThemeInstaller-x86_64.AppImage
   chmod +x GrubThemeInstaller-x86_64.AppImage
   ```

## Testing

```bash
# Install dialog if needed
sudo apt install dialog  # or dnf/pacman

# Run the AppImage
sudo ./GrubThemeInstaller-x86_64.AppImage
```

## What's Included

- ✅ Complete AppDir structure
- ✅ AppRun launcher with dialog check
- ✅ Desktop file and icon
- ✅ Modified installer script (works with AppImage paths)
- ✅ Build script
- ✅ Documentation

## Next Steps

1. Add your actual GRUB theme files to `grub-theme-installer.AppDir/themes/`
2. Ensure each theme has a `theme.txt` file
3. Build the AppImage
4. Distribute the single `.AppImage` file

## Notes

- The AppImage requires `dialog` to be installed on the target system
- Must be run with `sudo` to modify system GRUB configuration
- Themes directory can be customized before building
- The script automatically detects the AppImage's resource path

Enjoy your portable GRUB theme installer! 🚀
