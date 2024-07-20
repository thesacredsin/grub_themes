Grub Themer
======================================
Install Bootloader Themes with ease.

Installation
---------------

Simply enter following commands in your terminal :
1. Edit /etc/default/grub and comment out the below line:
   #GRUB_TERMINAL_OUTPUT="console"

2. git clone https://github.com/thesacredsin/grub_themes

3. cd grub_themes

4. sudo ./install.sh

Usage
---------------
- Select the number of the theme you want to install and follow the prompt.
- You can add custom themes to the Custom folder in grub_themes/themes/Custom/, then select option 2 to install
- Remove the files in grub_themes/themes/Custom/ if you wish to add another custom theme
- To remove previously themes if you don't need them anymore, navigate to /boot/grub/themes/ and delete the folders required eg. sudo rm -R CRT/

Dependencies
---------------
Requires the following dependencies:
- git

License
----------
Distributed under the MIT license.

Acknowledgements
-------------------
This was inspired and forked from Chris Titus Tech: https://www.youtube.com/@christitustech, go drop a subscribe there.
