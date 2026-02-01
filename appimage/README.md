# GRUB Theme Installer AppImage

A portable AppImage package for installing GRUB and Plymouth themes on Linux systems.

## Features

- ✅ Interactive dialog-based theme selection
- ✅ Automatic GRUB configuration
- ✅ Plymouth watermark installation
- ✅ Initramfs regeneration with dracut
- ✅ Automatic GRUB config backup
- ✅ Portable - no installation required

## Requirements

### System Requirements
- Linux operating system
- Root access (sudo)
- `dialog` package installed on your system
- GRUB bootloader
- (Optional) dracut for initramfs regeneration

### Installing dialog
```bash
# Debian/Ubuntu
sudo apt install dialog

# Fedora/RHEL/Nobara
sudo dnf install dialog

# Arch Linux
sudo pacman -S dialog
```

## Building the AppImage

### Prerequisites
- The build script will automatically download `appimagetool`
- Internet connection for first build

### Steps

1. **Add your theme files**:
   ```bash
   # Create theme directories
   mkdir -p grub-theme-installer.AppDir/themes/Nobara
   mkdir -p grub-theme-installer.AppDir/themes/Cyberpunk
   # ... add more themes as needed
   
   # Copy your theme files
   cp -r /path/to/your/theme/* grub-theme-installer.AppDir/themes/YourTheme/
   
   # Add watermark for Plymouth
   cp watermark.png grub-theme-installer.AppDir/themes/
   ```

2. **Build the AppImage**:
   ```bash
   ./build-appimage.sh
   ```

3. **Output**: `GrubThemeInstaller-x86_64.AppImage`

## Usage

### Running the AppImage

```bash
# Make it executable (first time only)
chmod +x GrubThemeInstaller-x86_64.AppImage

# Run with sudo
sudo ./GrubThemeInstaller-x86_64.AppImage
```

### What it does

1. Checks for root privileges
2. Displays theme selection menu
3. Backs up `/etc/default/grub` to `/etc/default/grub.bak`
4. Installs selected theme to `/boot/grub/themes/`
5. Installs Plymouth watermark
6. Configures GRUB settings:
   - Sets timeout to 10 seconds
   - Enables menu mode
   - Sets graphics mode to auto
   - Applies selected theme
7. Updates GRUB configuration
8. Regenerates initramfs with dracut (if available)

## Directory Structure

```
grub-theme-installer.AppDir/
├── AppRun                          # Main launcher
├── grub-theme-installer.desktop    # Desktop entry
├── grub-theme-installer.svg        # Icon
├── .DirIcon -> grub-theme-installer.svg
├── usr/
│   └── bin/
│       └── grub-theme-installer    # Main script
└── themes/                         # Theme files directory
    ├── README.md
    ├── Nobara/
    ├── Cyberpunk/
    ├── ... (other themes)
    └── watermark.png
```

## Customization

### Adding New Themes

1. Extract the AppImage:
   ```bash
   ./GrubThemeInstaller-x86_64.AppImage --appimage-extract
   ```

2. Add your theme to `squashfs-root/themes/YourTheme/`

3. Edit `squashfs-root/usr/bin/grub-theme-installer`:
   - Add your theme to the `themes` array
   - Add a corresponding case in `select_theme()`

4. Rebuild:
   ```bash
   ARCH=x86_64 appimagetool-x86_64.AppImage squashfs-root GrubThemeInstaller-x86_64.AppImage
   ```

### Modifying GRUB Settings

Edit `config_grub()` function in the installer script to customize:
- Timeout duration
- Graphics mode
- Other GRUB parameters

## Troubleshooting

### "dialog not found" error
Install the dialog package for your distribution (see Requirements section).

### "Run me as root" error
Use `sudo` to run the AppImage:
```bash
sudo ./GrubThemeInstaller-x86_64.AppImage
```

### Theme files not found
Make sure your theme folders are properly placed in the `themes/` directory before building.

### GRUB update fails
Check that you have one of these installed:
- `update-grub` (Debian/Ubuntu)
- `grub-mkconfig` (Generic)
- `grub2-mkconfig` (Fedora/RHEL)

## License

This packaging is provided as-is. Individual themes may have their own licenses.

## Credits

- AppImage technology by AppImage Project
- Dialog UI system
- GRUB theme creators

## Support

For issues related to:
- **AppImage packaging**: Check this README
- **Specific themes**: Contact theme authors
- **GRUB configuration**: Consult your distribution's documentation
