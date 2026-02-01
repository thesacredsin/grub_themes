# GRUB Theme Installer - Themes Directory

This directory should contain your GRUB theme folders.

## Structure:
```
themes/
├── Nobara/
│   ├── theme.txt
│   └── ... (theme files)
├── Cyberpunk/
│   ├── theme.txt
│   └── ... (theme files)
├── ... (other themes)
└── watermark.png
```

## To add themes:
1. Extract the AppImage: `./GrubThemeInstaller.AppImage --appimage-extract`
2. Add your theme folders to `squashfs-root/themes/`
3. Repackage: Use appimagetool to create a new AppImage

## Note:
You need to provide your own theme files. Place each theme in its own folder
with a `theme.txt` file and associated resources.
