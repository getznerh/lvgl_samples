import lvgl as lv  # NOQA
#import lvgl_panel_config as cfg
import time
import sys

# die Display und Touch Initialisierung nach dem Netzwerk
import lvgl_panel_utils as utils

# Welche Programmvarianten haben wir in Betrieb
USE_COUNTERBUTTON = 0
USE_SLIDER = 0
USE_BUTTON_PALETTE = 0
USE_METER = 0   # lv.meter gibt es zumindest derzeit nicht in MP
USE_IMAGE = 0 # https://github.com/lvgl/lv_binding_micropython/blob/master/examples/example1.py
USE_EXAMPLE3 = 0 # https://github.com/lvgl/lv_binding_micropython/blob/master/examples/example3.py
USE_PNGLOAD = 0 # laden eines PNG mit Verschieben
USE_ADVANCED_DEMO = 0 # funktioniert nicht, sehr kompliziert
USE_SQUARELINE = 1 # Test mit dem Squareline Beuspiel von Elecrow

#---------------------------------------------------------------------------
# da gibts Speicherfehler, WFIFI for dem Displaytreiber laden !

#utils.network_init()

#---------------------------------------------------------------------------
# Wifi muss vor dem Dsplay initialisiert werden, sonst Speicherfehler
# hier ist nur die Display und Touch Initialisierung

import lvgl_panel_init as cfg

#---------------------------------------------------------------------------
# hier wird eine Menge von Buttons mit unterschiedlichen Farben generiert

if cfg.USE_LVGL_MICROPYTHON:
    cfg.display.set_power(True)
    cfg.display.init()
    cfg.display.set_backlight(100)

    scrn = lv.screen_active()
    scr = scrn # die Beispiele haben überall scr

#---------------------------------------------------------------------------
# Test mit dem Squareline Beuspiel von Elecrow

if USE_SQUARELINE:
    print("Import UI")
    #import tempui.ui.ui as ui
    import ui
    '''
    class TEM_HUM():
        def __init__(self, ui_Screen1):
            # 读取DHT20传感器的温湿度值
            global tem, hum
        
            tem = 24 #sensor.temperature()
            hum = 65 #sensor.humidity()
            
            # 更新UI界面上的温湿度显示
            ui.ui_Label1.set_text(f"{round(tem)}")  # 更新温度显示
            ui.ui_Label2.set_text(f"{round(hum)}")       # 更新湿度显示


    TEM_HUM(ui.ui_Screen1)
    lv.screen_load(ui.ui_Screen1)
        
    import time

    while True:
    try:
        time.sleep(0.02)
        #sensor.measure()
        temp = 26 #sensor.temperature()
        hum = 64 #sensor.humidity()
        #temp_f = temp * (9/5) + 32.0
        print('Temperature: %3.1f C' %temp)
        #print('Temperature: %3.1f F' %temp_f)
        print('Humidity: %3.1f %%' %hum)
        ui.ui_Label1.set_text(f"{round(temp)}")
        ui.ui_Label2.set_text(f"{round(hum)}")
        
    except OSError as e:
        print('Failed to read sensor.')

    '''

    print("Ende UI")

#---------------------------------------------------------------------------
# aus dem advanced_demo.py vn lv_micropython

if USE_ADVANCED_DEMO:
  # Styles
  class ColorStyle(lv.style_t):
      def __init__(self, color):
          super().__init__()
          self.set_bg_opa(lv.OPA.COVER)
          self.set_bg_color(lv.color_hex3(color))
          self.set_bg_grad_color(lv.color_hex3(0xFFF))
          self.set_bg_grad_dir(lv.GRAD_DIR.VER)
          self.set_bg_main_stop(0)
          self.set_bg_grad_stop(128)

  class ShadowStyle(lv.style_t):
      def __init__(self):
          super().__init__()
          self.set_shadow_opa(lv.OPA.COVER)
          self.set_shadow_width(3)
          self.set_shadow_color(lv.color_hex3(0xAAA))
          self.set_shadow_offset_x(5)
          self.set_shadow_offset_y(3)
          self.set_shadow_spread(0)

  # A square button with a shadow when not pressed
  class ButtonStyle(lv.style_t):
      def __init__(self):
          super().__init__()
          self.set_radius(lv.dpx(8))
          self.set_shadow_opa(lv.OPA.COVER)
          self.set_shadow_width(lv.dpx(10))
          self.set_shadow_color(lv.color_hex3(0xAAA))
          self.set_shadow_offset_x(lv.dpx(10))
          self.set_shadow_offset_y(lv.dpx(10))
          self.set_shadow_spread(0)

  class ButtonPressedStyle(lv.style_t):
      def __init__(self):
          super().__init__()
          self.set_shadow_offset_x(lv.dpx(0))
          self.set_shadow_offset_y(lv.dpx(0))


  ##############################################################################
  # Themes
  ##############################################################################

  class AdvancedDemoTheme(lv.theme_t):

      def __init__(self):
          print("1")
          super().__init__()
          print("2")
          self.button_style = ButtonStyle()
          print("3")
          self.button_pressed_style = ButtonPressedStyle()
          print("4")

          # This theme is based on active theme (material)
          base_theme = lv.theme_get_from_obj(lv.screen_active())
          print("5")

          # This theme will be applied only after base theme is applied
          self.set_parent(base_theme)
          print("6")

          # Set the "apply" callback of this theme to our custom callback
          #self.set_apply_cb(self.apply)
          print("7")

          # Activate this theme on default display
          lv.display_get_default().set_theme(self)
          print("8")
      
      def apply(self, theme, obj):
          if obj.get_class() == lv.button_class:
              obj.add_style(self.button_style, lv.PART.MAIN)
              obj.add_style(self.button_pressed_style, lv.PART.MAIN | lv.STATE.PRESSED)

  ##############################################################################

  member_name_cache = {}

  def get_member_name(obj, value):
      try:
          return member_name_cache[id(obj)][id(value)]
      except KeyError:
          pass

      for member in dir(obj):
          if getattr(obj, member) == value:
              try:
                  member_name_cache[id(obj)][id(value)] = member
              except KeyError:
                  member_name_cache[id(obj)] = {id(value): member}
              return member


  class SymbolButton(lv.button):
      def __init__(self, parent, symbol, text):
          super().__init__(parent)
          self.symbol = lv.label(self)
          self.symbol.set_text(symbol)
          self.label = lv.label(self)
          self.label.set_text(text)
          self.set_flex_flow(lv.FLEX_FLOW.COLUMN)
          self.set_flex_align(lv.FLEX_ALIGN.SPACE_EVENLY, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER)


  class Page_Buttons:
      def __init__(self, app, page):
          self.app = app
          self.page = page
          self.button_event_count = {'Play': 0, 'Pause': 0}

          self.page.set_flex_flow(lv.FLEX_FLOW.ROW)
          self.page.set_flex_align(lv.FLEX_ALIGN.SPACE_EVENLY, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.START)

          self.button1 = SymbolButton(page, lv.SYMBOL.PLAY, "Play")
          self.button1.set_size(80, 80)

          self.button2 = SymbolButton(page, lv.SYMBOL.PAUSE, "Pause")
          self.button2.set_size(80, 80)

          self.label = lv.label(page)
          self.label.add_flag(lv.obj.FLAG.IGNORE_LAYOUT)
          self.label.align(lv.ALIGN.BOTTOM_LEFT, 0, 0)

          def button_cb(event, name):
              self.button_event_count[name] += 1
              event_name = get_member_name(lv.EVENT, event.code)
              if all((not event_name.startswith(s)) for s in ['DRAW', 'GET', 'STYLE', 'REFR']):
                  self.label.set_text('[%d] %s %s' % (self.button_event_count[name], name, event_name))

          for button, name in [(self.button1, 'Play'), (self.button2, 'Pause')]:
              button.add_event_cb(lambda event, button_name=name: button_cb(event, button_name), lv.EVENT.ALL, None)


  class Page_Simple:
      def __init__(self, app, page):
          self.app = app
          self.page = page
          self.test_events = []

          self.page.set_flex_flow(lv.FLEX_FLOW.COLUMN)
          self.page.set_flex_align(lv.FLEX_ALIGN.SPACE_EVENLY, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER)

          # slider
          self.slider = lv.slider(page)
          self.slider.set_width(lv.pct(80))
          self.slider_label = lv.label(page)
          self.slider.add_event_cb(self.on_slider_changed, lv.EVENT.VALUE_CHANGED, None)
          self.on_slider_changed(None)

          # style selector
          self.styles = [('Gray', ColorStyle(0xCCC)),
                        ('Red', ColorStyle(0xF00)), 
                        ('Green',ColorStyle(0x0F0)),
                        ('Blue', ColorStyle(0x00F))] 
      
          self.style_selector = lv.dropdown(page)
          self.style_selector.add_style(ShadowStyle(), lv.PART.MAIN)
          self.style_selector.align(lv.ALIGN.OUT_BOTTOM_LEFT, 0, 40)
          self.style_selector.set_options('\n'.join(x[0] for x in self.styles))
          self.style_selector.add_event_cb(self.on_style_selector_changed, lv.EVENT.VALUE_CHANGED, None)

          # counter button
          self.counter_button = lv.button(page)
          self.counter_button.set_size(80,80)
          self.counter_label = lv.label(self.counter_button)
          self.counter_label.set_text("Count")
          self.counter_label.align(lv.ALIGN.CENTER, 0, 0)
          self.counter_button.add_event_cb(self.on_counter_button, lv.EVENT.CLICKED, None)
          self.counter = 0

      def on_slider_changed(self, event):
          self.slider_label.set_text(str(self.slider.get_value()))

      def on_style_selector_changed(self, event):
          selected = self.style_selector.get_selected()
          tabview = self.app.screen_main.tabview
          if hasattr(self, 'selected_style'): tabview.remove_style(self.selected_style, lv.PART.MAIN)
          self.selected_style = self.styles[selected][1]
          tabview.add_style(self.selected_style, lv.PART.MAIN)

      def on_counter_button(self, event):
          self.counter += 1
          self.counter_label.set_text(str(self.counter))

  class Anim(lv.anim_t):
      def __init__(self, obj, val, size, exec_cb, path_cb, time=500, playback=False, completed_cb=None):
          super().__init__()
          self.init()
          self.set_time(time)
          self.set_values(val, val + size)
          if callable(exec_cb):
              self.set_custom_exec_cb(exec_cb)
          else:
              self.set_exec_cb(obj, exec_cb)
          self.set_path_cb(path_cb)
          if playback:
              self.set_playback(0)
          if completed_cb:
              self.set_completed_cb(completed_cb)
          self.start()
          

  class AnimatedChart(lv.chart):
      def __init__(self, parent, val, size):
          super().__init__(parent)
          self.val = val
          self.size = size
          self.max = 2000
          self.min = 500
          self.factor = 100
          self.anim_phase1()

      def anim_phase1(self):
          self.phase1 = Anim(
              self,
              self.val,
              self.size,
              lambda a, val: self.set_range(self.AXIS.PRIMARY_Y, 0, val),
              lv.anim_t.path_ease_in,
              completed_cb=lambda a:self.anim_phase2(),
              time=(self.max * self.factor) // 100,
          )

      def anim_phase2(self):
          self.phase2 = Anim(
              self,
              self.val + self.size,
              -self.size,
              lambda a, val: self.set_range(self.AXIS.PRIMARY_Y, 0, val),
              lv.anim_t.path_ease_out,
              completed_cb=lambda a:self.anim_phase1(),
              time=(self.min * self.factor) // 100,
          )
  class Page_Text:
      def __init__(self, app, page):
          self.app = app
          self.page = page
          self.page.set_flex_flow(lv.FLEX_FLOW.ROW)
          self.page.set_flex_align(lv.FLEX_ALIGN.SPACE_EVENLY, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER)
          self.ta = lv.textarea(self.page)
          self.ta.set_height(lv.pct(100))
          self.ta.set_width(lv.pct(100))

  class Page_Chart:
      def __init__(self, app, page):
          self.app = app
          self.page = page
          self.page.set_flex_flow(lv.FLEX_FLOW.ROW)
          self.page.set_flex_align(lv.FLEX_ALIGN.SPACE_EVENLY, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER)
          self.page.set_style_pad_all(10, lv.PART.MAIN)
          self.page.set_style_pad_gap(10, lv.PART.MAIN)
          self.chart = AnimatedChart(page, 100, 1000)
          self.chart.set_flex_grow(1)
          self.chart.set_height(lv.pct(100))
          self.series1 = self.chart.add_series(lv.color_hex(0xFF0000), self.chart.AXIS.PRIMARY_Y)
          self.chart.set_type(self.chart.TYPE.LINE)
          self.chart.set_style_line_width(3, lv.PART.ITEMS)
          self.chart.add_style(ColorStyle(0x055), lv.PART.ITEMS)
          self.chart.set_range(self.chart.AXIS.PRIMARY_Y, 0, 100)
          self.chart.set_point_count(10)
          self.chart.set_ext_y_array(self.series1, [10, 20, 30, 20, 10, 40, 50, 90, 95, 90])
          # self.chart.set_x_tick_texts("a\nb\nc\nd\ne", 2, lv.chart.AXIS.DRAW_LAST_TICK)
          # self.chart.set_x_tick_length(10, 5)
          # self.chart.set_y_tick_texts("1\n2\n3\n4\n5", 2, lv.chart.AXIS.DRAW_LAST_TICK)
          # self.chart.set_y_tick_length(10, 5)
          self.chart.set_div_line_count(5, 5)

          # Create a slider that controls the chart animation speed

          def on_slider_changed(event):
              self.chart.factor = self.slider.get_value()

          self.slider = lv.slider(page)
          self.slider.set_size(10, lv.pct(100))
          self.slider.set_range(10, 200)
          self.slider.set_value(self.chart.factor, 0)
          self.slider.add_event_cb(on_slider_changed, lv.EVENT.VALUE_CHANGED, None)

  class Screen_Main(lv.obj):
      def __init__(self, app, *args, **kwds):
          # self.app = app
          # super().__init__(*args, **kwds)
          self.theme = AdvancedDemoTheme()
          self.tabview = lv.tabview(self)
          # self.page_simple = Page_Simple(self.app, self.tabview.add_tab("Simple"))
          # self.page_buttons = Page_Buttons(self.app, self.tabview.add_tab("Buttons"))
          # self.page_text = Page_Text(self.app, self.tabview.add_tab("Text"))
          # self.page_chart = Page_Chart(self.app, self.tabview.add_tab("Chart"))

  class AdvancedDemoApplication:
      # def init_gui_SDL(self):
      #     self.keyboard = lv.sdl_keyboard_create()
      #     self.keyboard.set_group(self.group)
          
      def init_gui_esp32(self):

          self.disp = cfg.display
          self.touch = cfg.indev

      def init_gui(self):
          import sys
          self.group = lv.group_create()
          self.group.set_default()

          # Identify platform and initialize it
          #if sys.platform in ('esp32'):
          self.init_gui_esp32()
          # if sys.platform in ('linux', 'darwin'):
          #   self.init_gui_SDL()

          # Create the main screen and load it.
          self.screen_main = Screen_Main(self)
          #lv.screen_load(self.screen_main)

  app = AdvancedDemoApplication()
  app.init_gui()
   

#---------------------------------------------------------------------------
# laden PNG von SD Karte und verschieben mit dem Finger

if USE_PNGLOAD:
  # Load the image
  png_image_dsc = utils.lvgl_get_image_desc("png_decoder_test.png")
  # Create an image using the decoder
  image1 = lv.image(scr)
  image1.set_src(png_image_dsc)
  image1.set_pos(100,50)

  # Create an image from a symbol
  image2 = lv.image(scr)
  image2.set_src(lv.SYMBOL.OK + " Accept")
  image2.set_pos(100,200)

  # Drag handler
  def drag_event_handler(e):
      self = e.get_target_obj()
      #indev = lv.indev_get_act()
      vect = lv.point_t()
      cfg.indev.get_vect(vect)
      x = self.get_x() + vect.x
      y = self.get_y() + vect.y
      self.set_pos(x, y)

  # Register drag handler for images
  for image in [image1, image2]:
      image.add_flag(image.FLAG.CLICKABLE)
      image.add_event_cb(drag_event_handler, lv.EVENT.PRESSING, None)

#---------------------------------------------------------------------------
# aus https://github.com/lvgl/lv_binding_micropython/blob/master/examples/example3.py

if USE_EXAMPLE3:
  scr1 = lv.obj()
  scr2 = lv.obj()
  lv.screen_load(scr1)

  slider = lv.slider(scr2)
  slider.set_width(150)
  slider.align(lv.ALIGN.TOP_MID, 0, 15)

  button1 = lv.button(scr1)
  button1.align(lv.ALIGN.TOP_RIGHT, -5, 5)
  label = lv.label(button1)
  label.set_text(">")

  button2 = lv.button(scr2)
  button2.align(lv.ALIGN.TOP_LEFT, 5, 5)
  label2 = lv.label(button2)
  label2.set_text("<")

  led1 = lv.led(scr2)
  led1.align(lv.ALIGN.CENTER, 0, 0)
  led1.set_brightness(slider.get_value() * 2)
  # led1.set_drag(True)
  led1.set_size(20,20)

  def slider_event_cb(event):
      led1.set_brightness(slider.get_value() * 2)

  def button1_event_cb(event):
      lv.screen_load(scr2)

  def button2_event_cb(event):
      lv.screen_load(scr1)

  slider.add_event_cb(slider_event_cb, lv.EVENT.VALUE_CHANGED, None)
  button1.add_event_cb(button1_event_cb, lv.EVENT.CLICKED, None)
  button2.add_event_cb(button2_event_cb, lv.EVENT.CLICKED, None)

  # Create a keyboard
  kb = lv.keyboard(scr1)
  # kb.set_cursor_manage(True)

  # Create a text area. The keyboard will write here
  ta = lv.textarea(scr1)
  ta.set_width(450)
  ta.set_height(70)
  ta.align(lv.ALIGN.CENTER, 0, 0)
  ta.set_text("")

  # Assign the text area to the keyboard
  kb.set_textarea(ta)

  # Create a Spinner object
  spin = lv.spinner(scr2)
  spin.set_anim_params(1000, 100)
  spin.set_size(100, 100)
  spin.align(lv.ALIGN.CENTER, 0, 0)
  # spin.set_type(lv.spinner.TYPE.FILLSPIN_ARC)

#---------------------------------------------------------------------------
# aus https://github.com/lvgl/lv_binding_micropython/blob/master/examples/example1.py

if USE_IMAGE:
  # Image data
  # with open('lib/lv_bindings/examples/blue_flower_32.bin','rb') as f:
  #   image_data = f.read()
  # Pixel format: Fix 0xFF: 8 bit, Red: 8 bit, Green: 8 bit, Blue: 8 bit
  # import sampleimage
  # image_data = sampleimage.image_data

  # # Create a screen with a draggable image
  # image = lv.image(scr)
  # image.align(lv.ALIGN.CENTER, 0, 0)
  # image_dsc = lv.image_dsc_t(
  #     {
  #         "header": {"w": 100, "h": 75, "cf": lv.COLOR_FORMAT.ARGB8888},
  #         "data_size": len(image_data),
  #         "data": image_data,
  #     }
  # )
  # image.set_src(image_dsc)

  # Bilddaten von der SD-Karte lesen
  # with open('/sd/HoPOS_small_320.bin', 'rb') as file:
  #   image_data = file.read()
  image_data = utils.read_file("HoPOS_small_320.bin")
  # Canvas-Objekt erstellen und Bilddaten darauf anzeigen
  canvas = lv.canvas(scrn)  # Canvas wird auf dem erstellten Bildschirm hinzugefügt
  canvas.set_buffer(image_data, 320, 240, lv.COLOR_FORMAT.RGB565)  # Setzt Bildgröße und RGB565-Format
  canvas.align(lv.ALIGN.CENTER, 0, 0)  # Zentriert das Bild auf dem Bildschirm
  # image.set_drag(True)

  # Load the screen and display image
  #lv.screen_load(scr)

#---------------------------------------------------------------------------

if USE_BUTTON_PALETTE:
  scrn.set_style_bg_color(lv.color_hex3(0x000), 0)
  bstyle=lv.style_t()
  bstyle.init()
  bstyle.set_text_color(lv.color_hex3(0x000))

  button_container = lv.obj(scrn)
  button_container.set_size(800,480) #x,y
  button_container.set_flex_flow(lv.FLEX_FLOW.COLUMN_WRAP)
  button_container.set_style_bg_color(lv.color_hex3(0x000),0)

  btn=[]
  btn_lbl=[]
  i=0
  c_red = lv.palette_main(lv.PALETTE.RED)
  c_pink = lv.palette_main(lv.PALETTE.PINK)
  c_purple = lv.palette_main(lv.PALETTE.PURPLE)
  c_deeppurple = lv.palette_main(lv.PALETTE.DEEP_PURPLE)
  c_indigo = lv.palette_main(lv.PALETTE.INDIGO)
  c_blue = lv.palette_main(lv.PALETTE.BLUE)
  c_lightblue = lv.palette_main(lv.PALETTE.LIGHT_BLUE)
  c_cyan = lv.palette_main(lv.PALETTE.CYAN)
  c_teal = lv.palette_main(lv.PALETTE.TEAL)
  c_green = lv.palette_main(lv.PALETTE.GREEN)
  c_lightgreen = lv.palette_main(lv.PALETTE.LIGHT_GREEN)
  c_lime = lv.palette_main(lv.PALETTE.LIME)
  c_yellow = lv.palette_main(lv.PALETTE.YELLOW)
  c_amber = lv.palette_main(lv.PALETTE.AMBER)
  c_orange = lv.palette_main(lv.PALETTE.ORANGE)
  c_deeporange = lv.palette_main(lv.PALETTE.DEEP_ORANGE)
  c_brown = lv.palette_main(lv.PALETTE.BROWN)
  c_bluegrey = lv.palette_main(lv.PALETTE.BLUE_GREY)
  c_grey = lv.palette_main(lv.PALETTE.GREY)

  colors={"RED":c_red,"PINK":c_pink,"PURPLE":c_purple,"DEEP PURPLE":c_deeppurple,"INDIGO":c_indigo,"BLUE":c_blue,
          "LIGHT BLUE":c_lightblue,"CYAN":c_cyan,"TEAL":c_teal,"GREEN":c_green,"LIGHT GREEN":c_lightgreen,"LIME":c_lime,
          "YELLOW":c_yellow,"AMBER":c_amber,"ORANGE":c_orange,"DEEP ORANGE":c_deeporange,"BROWN":c_brown,"BLUE GREY":c_bluegrey,"GREY":c_grey}
  for color_name in colors:
      color=colors[color_name]
      hex_color = '{:02X}{:02X}{:02X}'.format(int(color.red),int(color.green),int(color.blue))
      print('color:',color.red,color.green,color.blue,hex_color)
      btn.append(lv.button(button_container))
      btn[-1].set_style_bg_color(color,0)
      btn_lbl.append(lv.label(btn[-1]))
      btn_lbl[-1].set_text(color_name + ' '+hex_color)
      #btn_lbl[-1].add_style(fontstyle24, 0)
      btn_lbl[-1].add_style(bstyle, 0)

#---------------------------------------------------------------------------
# zudem noch ein Slider zu Test des Toucinterfaces

if USE_SLIDER:
  scrn.set_style_bg_color(lv.color_hex(0xff7733), 0)
  slider = lv.slider(scrn)
  slider.set_size(200, 45)
  slider.center()

  # Callback bei Slider Touch
  def on_value_changed(e):
      print('VALUE_CHANGED:', e.get_target_obj().get_value())

  slider.add_event_cb(on_value_changed, lv.EVENT.VALUE_CHANGED, None)

#---------------------------------------------------------------------------
# Counterbutton aus Elecrow Examples

if USE_COUNTERBUTTON:
  scrn.set_style_bg_color(lv.color_hex(0xff0000), 0)
  class CounterBtn():
  
      def __init__(self, scr):
          self.cnt = 0
          btn = lv.button(scr)
          btn.align(lv.ALIGN.CENTER,0,0)
          btn.add_event_cb(self.btn_event_cb, lv.EVENT.ALL, None)
          label = lv.label(btn)
          label.set_text("Button")
          label.center()

      def btn_event_cb(self, evt):
          code = evt.get_code()
          btn = evt.get_target_obj()
          if code == lv.EVENT.CLICKED:
              self.cnt += 1
              print(f"Zähler {self.cnt}")
              # das darf nur bei EVENT.CLICKED ausgeführt werden!
              label = btn.get_child(0)
              label.set_text("ButtonS: " + str(self.cnt))

  counterBtn = CounterBtn(scrn)

#---------------------------------------------------------------------------
# Meteranzeige aus dem Beispiel von elecrow biaopan-5.0.py

if USE_METER:
  # lv.meter gibt es zumindest derzeit nicht in MP

  # 1. Create a display screen. Will need to display the component added to the screen to display
  #scrn = lv.obj()  # scr====> screen
  #fs_drv = lv.fs_drv_t()
  #fs_driver.fs_register(fs_drv, 'S')
  # scrn = lv.scr_act()
  # scrn.clean()

  # 2. Encapsulate the component to display
  class MyWidget():
      def __init__(self, scr):
          # 1. Create the dashboard object
          self.meter = lv.meter(scr)
          self.meter.center()
          self.meter.set_size(200, 200)  # width: 200 height: 200

          # 2. To create calibration object
          scale = self.meter.add_scale()

          self.meter.set_scale_ticks(scale, 51, 2, 10, lv.palette_main(lv.PALETTE.GREY))

          self.meter.set_scale_major_ticks(scale, 10, 4, 15, lv.color_black(), 20)

          # 3. Add warning scale line
          blue_arc = self.meter.add_arc(scale, 2, lv.palette_main(lv.PALETTE.BLUE), 0)
          self.meter.set_indicator_start_value(blue_arc, 0)
          self.meter.set_indicator_end_value(blue_arc, 20)

          blue_arc_scale = self.meter.add_scale_lines(scale, lv.palette_main(lv.PALETTE.BLUE), lv.palette_main(lv.PALETTE.BLUE), False, 0)
          self.meter.set_indicator_start_value(blue_arc_scale, 0)
          self.meter.set_indicator_end_value(blue_arc_scale, 20)

          red_arc = self.meter.add_arc(scale, 2, lv.palette_main(lv.PALETTE.RED), 0)
          self.meter.set_indicator_start_value(red_arc, 80)
          self.meter.set_indicator_end_value(red_arc, 100)

          red_arc_scale = self.meter.add_scale_lines(scale, lv.palette_main(lv.PALETTE.RED), lv.palette_main(lv.PALETTE.RED), False, 0)
          self.meter.set_indicator_start_value(red_arc_scale, 80)
          self.meter.set_indicator_end_value(red_arc_scale, 100)

          # 4. meter needle
          self.indic = self.meter.add_needle_line(scale, 4, lv.palette_main(lv.PALETTE.GREY), -10)

          # 5. Creating animated objects
          a = lv.anim_t()
          a.init()
          a.set_var(self.indic)
          a.set_values(0, 100)
          a.set_time(2000)
          a.set_repeat_delay(100)
          a.set_playback_time(500)
          a.set_playback_delay(100)
          a.set_repeat_count(lv.ANIM_REPEAT.INFINITE)
          a.set_custom_exec_cb(self.set_value)
          lv.anim_t.start(a)

      def set_value(self, anmi_obj, value):
          """Animation callbacks"""
          self.meter.set_indicator_value(self.indic, value)

  # 3. Create the component to display
  MyWidget(scrn)

#---------------------------------------------------------------------------
# ab hier die Standardbehandlung für alle Beispiele

#lv.scr_load(scrn)

# Beispiel Event btn
# btn.add_event(lambda event: print('Button clicked!'),lv.EVENT.CLICKED,None)
# Bild laden:
# https://github.com/lvgl/lv_binding_micropython/blob/master/examples/png_example.py
# Advanced Sample https://github.com/lvgl/lv_binding_micropython/blob/master/examples/advanced_demo.py

#---------------------------------------------------------------------------
# das ist praktisch der Eventloop
# import task_handler
# th = task_handler.TaskHandler()

#------------------------------------------------------------------------------
# this is a better way to handle updating on a set schedule. This doesn't block
# the main thread making it easier to interrupt the running program when 
# needing to do something like uploading files.
# the other thing is it doesn't block the repl so you can connect over the USB 
# and you will get a repl prompt and be able to pass code to it.
# this all works because of the task handler above and it scheduling a task 
# that interrupts the main thread to update the display

'''
import utime

def timer_callback(_):
    #Get the current time
    current_time = utime.localtime()
    #Format the current time as "dd/mm/yyyy HH:MM"
    formatted_time = "{:02d}.{:02d}.{} {:02d}:{:02d}:{:02d}".format(current_time[2], current_time[1], current_time[0], current_time[3], current_time[4], current_time[5])
    # wenn das GUI entfernt wird. läuft evtl. die Task weiter, dann gibts einen Fehler
    try:
        ui.ui_Time.set_text(formatted_time)
    except:
        pass
    pass
    # global a
    # ui.ui_Label2.set_text(str(a))
    # a += 1
    
timer = lv.timer_create(timer_callback, 1000, None)
timer.set_repeat_count(-1) # indefinitely
lv.timer_enable(True) # gilt für ALLE Timer

# da kommt aber REPL wieder
print("Timer gestartet, Zurück zum REPL, Task läuft weiter")

'''

# ------------------------------ Guard dog to restart ESP32 equipment --start------------------------
# Programm muss in einer Schleife bleiben, sonst sieht man die print nicht

while True:
    time.sleep(1)

# try:
#     import machine
#     wdt = machine.WDT(timeout=10000)  # enable it with a timeout of 10s
#     print("Hint: Press Ctrl+C to end the program")
#     while True:
#         wdt.feed()
#         time.sleep(0.9)
# except KeyboardInterrupt as ret:
#     print("The program stopped running, ESP32 has restarted...")
#     #tft.deinit()
#     time.sleep(10)
# #    machine.reset()
# ------------------------------ Guard dog to restart ESP32 equipment --stop-------------------------

#------------------------------------------------------------------------------
