# aus dem Readme von lv_micropython
# zum Test der Windows Version

import lvgl as lv
lv.init()

# Create an event loop and Register SDL display/mouse/keyboard drivers.
from lv_utils import event_loop

WIDTH = 480
HEIGHT = 320

event_loop = event_loop()
disp_drv = lv.sdl_window_create(WIDTH, HEIGHT)
mouse = lv.sdl_mouse_create()
keyboard = lv.sdl_keyboard_create()
#keyboard.set_group(self.group)
