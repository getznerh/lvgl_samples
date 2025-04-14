#!/bin/bash

# LVGL Unix mit SDL compilieren
../lvgl_micropython/build/lvgl_micropy_unix -i main.py

# das ist für den ESP32
# python3 make.py esp32 clean BOARD=ESP32_GENERIC_S3 BOARD_VARIANT=SPIRAM_OCT DISPLAY=rgb_display INDEV=gt911 --enable-cdc-repl=n --enable-jtag-repl=n

# das ist für Unix und SDL2 wird in build abgelegt
#python3 make.py unix clean FROZEN_MANIFEST=~/frozenmodules-gz/manifest.py DISPLAY=sdl_display INDEV=sdl_pointer
