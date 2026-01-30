#!/bin/bash

THEME_DIR='/boot/grub/themes'
THEME_NAME=""

DIALOG=dialog
HEIGHT=15
WIDTH=60

themes=(
  1 "Nobara"
  2 "Custom"
  3 "Cyberpunk"
  4 "Cyberpunk_2077"
  5 "Shodan"
  6 "fallout"
  7 "CyberRe"
  8 "CyberSynchro"
  9 "CyberEXS"
 10 "CRT"
 11 "BIOS"
 12 "retro"
 13 "Quit"
)

cleanup() {
  clear
}
trap cleanup EXIT

check_root() {
  if [[ $EUID -ne 0 ]]; then
    $DIALOG --title "Error" \
      --msgbox "Please run this script as root.\n\nTry:\n  sudo ./install.sh" 10 50
    exit 1
  fi
}

splash() {
  $DIALOG --title "GRUB Theme Changer" \
    --msgbox "Welcome to the GRUB Theme Changer\n\nChoose a theme to install." 10 50
}

select_theme() {
  choice=$(
    $DIALOG --clear \
      --title "Select Theme" \
      --menu "Choose a GRUB theme:" \
      $HEIGHT $WIDTH 13 \
      "${themes[@]}" \
      3>&1 1>&2 2>&3
  )

  case "$choice" in
    13|"") cleanup; exit 0 ;;
    *)
      THEME_NAME="${themes[$((choice*2-1))]}"
      ;;
  esac
}

backup() {
  cp -an /etc/default/grub /etc/default/grub.bak
}

install_theme() {
  $DIALOG --infobox "Installing $THEME_NAME theme..." 5 50
  sleep 1

  mkdir -p "${THEME_DIR}/${THEME_NAME}"
  cp -a "./themes/${THEME_NAME}/"* "${THEME_DIR}/${THEME_NAME}"
  cp -a ./themes/watermark.png /usr/share/plymouth/themes/spinner/
}

config_grub() {
  $DIALOG --infobox "Configuring GRUB..." 5 50
  sleep 1

  sed -i '/GRUB_TIMEOUT_STYLE=/d' /etc/default/grub
  sed -i '/GRUB_TIMEOUT=/d' /etc/default/grub
  sed -i '/GRUB_THEME=/d' /etc/default/grub
  sed -i '/GRUB_GFXMODE=/d' /etc/default/grub

  cat >> /etc/default/grub <<EOF
GRUB_TIMEOUT_STYLE="menu"
GRUB_TIMEOUT="10"
GRUB_THEME="${THEME_DIR}/${THEME_NAME}/theme.txt"
GRUB_GFXMODE="auto"
EOF
}

update_grub() {
  $DIALOG --infobox "Updating GRUB configuration..." 5 50
  sleep 1

  if command -v update-grub &>/dev/null; then
    update-grub
  elif command -v grub-mkconfig &>/dev/null; then
    grub-mkconfig -o /boot/grub/grub.cfg
  elif command -v grub2-mkconfig &>/dev/null; then
    grub2-mkconfig -o /boot/grub2/grub.cfg
  fi
}

main() {
  check_root
  splash
  select_theme
  backup
  install_theme
  config_grub
  update_grub

  $DIALOG --title "Success" \
    --msgbox "GRUB and Plymouth theme \"$THEME_NAME\" installed successfully!" 8 50
}

main
