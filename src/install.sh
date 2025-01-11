#!/bin/bash

# შექმენით დირექტორიები
mkdir -p ~/.config/timely
sudo mkdir -p /usr/share/timely

# გადატანეთ ფაილები
cp config.ini ~/.config/timely/
cp translations.ini ~/.config/timely/
sudo cp dist/timely_exec /usr/local/bin/

echo "Installation complete. You can now run 'timely_exec'."
