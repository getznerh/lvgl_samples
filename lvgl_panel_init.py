# Konfiguration für das verwendete Displaypanel
# hier aktuell 5" Elecrow ESP32S3 N4R8, also 4 MB Flash und 8 MB RAM
# alternativ  7" WaveShare ESP32S3 N8R8, also 8 MB Flash und 8 MB RAM

# hier ist nur der tatsächlich für das Display und Touch notwendige Initialisierungsteil
'''
Firmware build

Für ESP32S3 mit SPIRAM
es geht auch, mehrere INDEV gleichzeitig zu definieren, dann sind beide Varianten möglich
python3 make.py esp32 clean BOARD=ESP32_GENERIC_S3 BOARD_VARIANT=SPIRAM_OCT 
    --flash-size=4 DISPLAY=rgb_display INDEV=gt911 INDEV=xpt2046 
    --enable-cdc-repl=n --enable-jtag-repl=n --enable-cdc-repl=y

alternativ mit --flash-size=4 

Für die UNIX Variante unter WSL und SDL2:
python3 make.py unix clean DISPLAY=sdl_display INDEV=sdl_pointer

Evtl. mit FROZEN_MANIFEST
FROZEN_MANIFEST=~/frozenmodules-gz/manifest.py 

'''

USE_LVGL_MICROPYTHON = True
USE_SQUARELINE_LV = False

#from micropython import const  # NOQA
import time
import sys

# Mit den if xxx Varianten funktionieren die  const() anweisungen nicht, da der Compiler
# beim ersten Auftreten die Variable als const definiert und die zweite Zuweisung fehlschlägt
USE_4ZOLL_DISPLAY = False # https://www.waveshare.com/wiki/ESP32-S3-Touch-LCD-4.3
USE_5ZOLL_DISPLAY = False # https://www.elecrow.com/wiki/5.0-inch_ESP32_Display_MicroPython_Tutorial.html#resources
USE_7ZOLL_DISPLAY = False # https://www.waveshare.com/wiki/ESP32-S3-Touch-LCD-7
USE_SDL_DISPLAY = True

# die Display-Größe
if USE_4ZOLL_DISPLAY:
    _WIDTH = 480
    _HEIGHT = 272
    _USE_SD_CARD = True
if USE_5ZOLL_DISPLAY:
    _WIDTH = 800
    _HEIGHT = 480
    _USE_SD_CARD = True
if USE_7ZOLL_DISPLAY:
    _WIDTH = 800
    _HEIGHT = 480
    _USE_SD_CARD = True
if USE_SDL_DISPLAY:
    _WIDTH = 800
    _HEIGHT = 480
    _USE_SD_CARD = False

I2C_BUS = None

if USE_LVGL_MICROPYTHON:
    import lvgl as lv  # NOQA
    import lcd_bus  # NOQA
    lv.init()
if USE_SQUARELINE_LV:
    import gc
    from display_driver_utils import driver
    drv = driver( width=_WIDTH, height=_HEIGHT)


# Display und Touch initialisieren
# wenn das Programm auch unter WSL laufen soll
if sys.platform in ('linux', 'darwin', 'win32'):
    if USE_LVGL_MICROPYTHON:
        import sdl_pointer
        import sdl_display
        
        bus = lcd_bus.SDLBus(flags=0)
        #buf = bus.allocate_framebuffer(_WIDTH * _HEIGHT * 3, 0)    
        
        display = sdl_display.SDLDisplay(
            data_bus=bus,
            display_width=_WIDTH,
            display_height=_HEIGHT,
            #frame_buffer1=buf,
            color_space=lv.COLOR_FORMAT.RGB565        
        )
        
        indev = sdl_pointer.SDLPointer()

        '''
        # Unter WSL compilieren und ausführen
        sudo apt update
        sudo apt install -y libx11-6 libxext6 libxcursor1 libxrandr2 libxinerama1 libxi6
        sudo apt install -y libsdl2-2.0-0
        python3 make.py unix DISPLAY=sdl_display INDEV=sdl_pointer
        chmod +x lvgl_micropy_unix
        ./lvgl_micropy_unix
        '''

else: # ESP32S3 Elecrow5" Board SPIRAM OCT 4 MB Flash, 8 MB RAM oder 7" Waveshare 8MB/8MB
    #from machine import Pin
    if USE_4ZOLL_DISPLAY:
        _CTP_SCL = 20
        _CTP_SDA = 19

        _LCD_FREQ = 13000000
        _PCLK_ACTIVE_NEG = 1

        _HSYNC_PULSE_WIDTH = 4
        _HSYNC_BACK_PORCH = 8
        _HSYNC_FRONT_PORCH = 8

        _VSYNC_PULSE_WIDTH = 4
        _VSYNC_BACK_PORCH = 8
        _VSYNC_FRONT_PORCH = 8

        # Die PIN Nummern stimmen mit dem Beispiel in https://pastebin.com/raw/aNBxmQhg überein
        _PCLK = 42
        _HSYNC = 39
        _VSYNC = 41
        _DE = 40
        _DISP = -1
        _BCKL = 2
        _DRST = None
        _DPWR = None

        _DATA15 = 14  # B7
        _DATA14 = 21  # B6
        _DATA13 = 47  # B5
        _DATA12 = 48  # B4
        _DATA11 = 45  # B3
        _DATA10 = 4  # G7
        _DATA9 = 16  # G6
        _DATA8 = 15  # G5
        _DATA7 = 7  # G4
        _DATA6 = 6  # G3
        _DATA5 = 5  # G2
        _DATA4 = 1  # R7
        _DATA3 = 9  # R6
        _DATA2 = 46  # R5
        _DATA1 = 3  # R4
        _DATA0 = 8  # R3

        # touch panel SPI settings
        _TP_SPI_HOST = 1
        _TP_SPI_FREQ = 1_000_000
        _TP_CS_PIN = 10 # gem Arduino CS=10
        # https://github.com/rzeldent/platformio-espressif32-sunton/blob/main/esp32-4827S043R.json
        _TP_INT_PIN = -1
        _TP_SPI_MOSI = 11
        _TP_SPI_MISO = 13
        _TP_SPI_CLK = 12

    if USE_5ZOLL_DISPLAY:
        _CTP_SCL = 20
        _CTP_SDA = 19
        _I2C_HOST = 1
        
        _LCD_FREQ = 13000000
        _PCLK_ACTIVE_NEG = 1

        _HSYNC_PULSE_WIDTH = 4
        _HSYNC_BACK_PORCH = 43
        _HSYNC_FRONT_PORCH = 8

        _VSYNC_PULSE_WIDTH = 4
        _VSYNC_BACK_PORCH = 12
        _VSYNC_FRONT_PORCH = 8

        # Die PIN Nummern stimmen mit dem Beispiel in https://pastebin.com/raw/aNBxmQhg überein
        _PCLK = 0
        _HSYNC = 39
        _VSYNC = 41
        _DE = 40
        _DISP = -1
        _BCKL = 2
        _DRST = None
        _DPWR = None

        # Display Anschlüsse
        _DATA15 = 14  # B7
        _DATA14 = 21  # B6
        _DATA13 = 47  # B5
        _DATA12 = 48  # B4
        _DATA11 = 45  # B3
        _DATA10 = 4  # G7
        _DATA9 = 16  # G6
        _DATA8 = 15  # G5
        _DATA7 = 7  # G4
        _DATA6 = 6  # G3
        _DATA5 = 5  # G2
        _DATA4 = 1  # R7
        _DATA3 = 9  # R6
        _DATA2 = 46  # R5
        _DATA1 = 3  # R4
        _DATA0 = 8  # R3

        _SD_MOSI = 11
        _SD_SCK = 12
        _SD_MISO = 13
        _SD_CS = 10
        _SPI_BUS_HOST = 2

    if USE_7ZOLL_DISPLAY:
        _CTP_SCL = 9
        _CTP_SDA = 8
        _I2C_HOST = 0
 
        _LCD_FREQ = 13000000 # bei 16000000 wandert der Pushbutton!
        _PCLK_ACTIVE_NEG = 1

        _HSYNC_PULSE_WIDTH = 4
        _HSYNC_BACK_PORCH = 8
        _HSYNC_FRONT_PORCH = 8

        _VSYNC_PULSE_WIDTH = 4
        _VSYNC_BACK_PORCH = 16 # oder 8
        _VSYNC_FRONT_PORCH = 16 # oder 8

        _PCLK = 7
        _HSYNC = 46
        _VSYNC = 3
        _DE = 5
        _DISP = -1
        _BCKL = 1
        _DRST = None
        _DPWR = None

        _DATA15 = 40
        _DATA14 = 41
        _DATA13 = 42
        _DATA12 = 2
        _DATA11 = 1
        _DATA10 = 21
        _DATA9 = 47
        _DATA8 = 48
        _DATA7 = 45
        _DATA6 = 0
        _DATA5 = 39
        _DATA4 = 10
        _DATA3 = 17
        _DATA2 = 18
        _DATA1 = 38
        _DATA0 = 14

        _SD_MOSI = 11
        _SD_SCK = 12
        _SD_MISO = 13
        # The SD card communicates via SPI, and it's important to note that the SD_CS pin needs to be driven by the EXIO4 of the CH422G.
        _SD_CS = None # EXT04
        _SPI_BUS_HOST = 2

    # touch drvier
    if USE_5ZOLL_DISPLAY or USE_7ZOLL_DISPLAY:
        from i2c import I2C
        import gt911
        I2C_BUS = I2C.Bus(
        host=_I2C_HOST,
        scl=_CTP_SCL,
        sda=_CTP_SDA,
        freq=400000,
        use_locks=False
        )

        TOUCH_DEVICE = I2C.Device(
            I2C_BUS,
            dev_id=gt911.I2C_ADDR,
            reg_bits=gt911.BITS
        )
    if USE_4ZOLL_DISPLAY:
        from machine import SPI
        # Create SPI bus
        SPI_BUS = SPI.Bus(
            host=_TP_SPI_HOST,
            miso=_TP_SPI_MISO,
            mosi=_TP_SPI_MOSI,
            sck=_TP_SPI_CLK
        )

        # Create touch controller SPI Device
        TOUCH_DEVICE = SPI.Device(
            spi_bus=SPI_BUS,
            freq=_TP_SPI_FREQ,
            cs=_TP_CS_PIN
        )

    display_bus = lcd_bus.RGBBus(
        hsync=_HSYNC,
        vsync=_VSYNC,
        de=_DE,
    #    disp=DISP,
        pclk=_PCLK,
        data0=_DATA0,
        data1=_DATA1,
        data2=_DATA2,
        data3=_DATA3,
        data4=_DATA4,
        data5=_DATA5,
        data6=_DATA6,
        data7=_DATA7,
        data8=_DATA8,
        data9=_DATA9,
        data10=_DATA10,
        data11=_DATA11,
        data12=_DATA12,
        data13=_DATA13,
        data14=_DATA14,
        data15=_DATA15,
        freq=_LCD_FREQ,
        hsync_front_porch=_HSYNC_FRONT_PORCH,
        hsync_back_porch=_HSYNC_BACK_PORCH,
        hsync_pulse_width=_HSYNC_PULSE_WIDTH,
        hsync_idle_low=True,
        vsync_front_porch=_VSYNC_FRONT_PORCH,
        vsync_back_porch=_VSYNC_BACK_PORCH,
        vsync_pulse_width=_VSYNC_PULSE_WIDTH,
        vsync_idle_low=True,
        de_idle_high=False,
        pclk_idle_high=False,
        pclk_active_low=_PCLK_ACTIVE_NEG,
    #     disp_active_low=False,
    #     refresh_on_demand=False
    )

    # lt kdschlosser wird der Buffer automatisch erzeugt
    # allenfalls hier kleiner Buffer wegen Geschwindigkeit
    # buf1 = bus.allocate_framebuffer(_WIDTH * _HEIGHT * 2, lcd_bus.MEMORY_SPIRAM)
    # buf2 = bus.allocate_framebuffer(_WIDTH * _HEIGHT * 2, lcd_bus.MEMORY_SPIRAM)

    import rgb_display  # NOQA

    display = rgb_display.RGBDisplay(
        data_bus=display_bus,
        display_width=_WIDTH,
        display_height=_HEIGHT,
    #     frame_buffer1=buf1,
    #     frame_buffer2=buf2,
        reset_pin=_DRST,
        reset_state=rgb_display.STATE_HIGH,
        power_pin=_DPWR,
        power_on_state=rgb_display.STATE_HIGH,
        backlight_pin=_BCKL,
        backlight_on_state=rgb_display.STATE_HIGH,
        color_space=lv.COLOR_FORMAT.RGB565,
        rgb565_byte_swap=False # sonst stimmen die Farben nicht
        #rgb565_byte_swap=True
    )

    if USE_4ZOLL_DISPLAY:
        class TouchCal:
            def __init__(self):
        #         self.alphaX = 1.088837
        #         self.betaX = 0.005908419
        #         self.deltaX = -7.80586
        #         self.alphaY = 0.00886263
        #         self.betaY = -1.136386
        #         self.deltaY = 353.614
                self.alphaX = 1.0
                self.betaX = 0.0
                self.deltaX = 0.0
                self.alphaY = 0.0
                self.betaY = 1.0
                self.deltaY = 0.0
                
                self.mirrorX = 0
                self.mirrorY = 0
                
                pass
            
            @staticmethod
            def save():
                pass

        from xpt2046 import XPT2046  # NOQA
        # indev = XPT2046(miso=_TP_MISO, mosi=_TP_MOSI, clk=_TP_CLK, cs=_TP_CS, host=_TP_HOST, freq=_TP_FREQ)
        cal = TouchCal()
        try:
            indev = XPT2046(
                TOUCH_DEVICE, startup_rotation=lv.DISPLAY_ROTATION._0, 
                touch_cal=cal, debug=True
            )
            print('is_calibrate is', indev.is_calibrated)

        except Exception as ex:
            sys.print_exception(ex)

    if USE_5ZOLL_DISPLAY:
        indev = gt911.GT911(device=TOUCH_DEVICE, startup_rotation=lv.DISPLAY_ROTATION._0)
    if USE_7ZOLL_DISPLAY:
        if _USE_SD_CARD:
            # Wenn Expander CH422G für CS benötigt wird:
            import ch422g
            # but we need to create a new device on the bus for the io_expander
            io_expander_device = I2C.Device(I2C_BUS, dev_id=ch422g.I2C_ADDR, reg_bits=ch422g.BITS)
            # Now we need to set the I2C device to the io expander driver
            ch422g.Pin.set_device(io_expander_device)

            tp_reset_pin =  ch422g.Pin(
                ch422g.EXIO1,  # sets the pin to use on the IO expander
                mode=ch422g.Pin.OUT,  # sets the mode as output
                # 0 if the pin needs to be high to to reset 
                # 1 if the state needs to be low to perform a reset 
                value=0)
            tp_lcdbl_pin =  ch422g.Pin(
                ch422g.EXIO2,  # sets the pin to use on the IO expander
                mode=ch422g.Pin.OUT,  # sets the mode as output
                # 0 if the pin needs to be high to to reset 
                # 1 if the state needs to be low to perform a reset 
                value=0)
            '''
            tp_lcdrst_pin =  ch422g.Pin(
                ch422g.EXIO3,  # sets the pin to use on the IO expander
                mode=ch422g.Pin.OUT,  # sets the mode as output
                # 0 if the pin needs to be high to to reset 
                # 1 if the state needs to be low to perform a reset 
                value=0)
            '''
            tp_sd_cs_pin =  ch422g.Pin(
                ch422g.EXIO4,  # sets the pin to use on the IO expander
                mode=ch422g.Pin.OUT,  # sets the mode as output
                value=0)
            # rest muss low sein, sonst geht I2C nicht
            tp_reset_pin.low()
            # lcdbl muss low sein, sonst ist display dunkel
            tp_lcdbl_pin.low()
            # cs muss high sein, sost geht SD nicht
            tp_sd_cs_pin.high()
            
        indev = gt911.GT911(device=TOUCH_DEVICE,interrupt_pin=4)

    if USE_5ZOLL_DISPLAY or USE_7ZOLL_DISPLAY:
        if indev.hw_size != (_WIDTH, _HEIGHT):
            fw_config = indev.firmware_config
            fw_config.width = _WIDTH
            fw_config.height = _HEIGHT
            fw_config.save()
            del fw_config

    #---------------------------------------------------------------------------
    #SD Card

    if _USE_SD_CARD:
        import machine
        import os, vfs
        from machine import SDCard, SPI
        import uos

        # Initialize the SPI bus with appropriate pins
        if USE_5ZOLL_DISPLAY or USE_7ZOLL_DISPLAY:
            spi_bus = SPI.Bus(
                host=_SPI_BUS_HOST,        # SPI bus host number (adjust based on your board)
                mosi=_SD_MOSI,       # Master Out Slave In (adjust based on your hardware)
                miso=_SD_MISO,       # Master In Slave Out (adjust based on your hardware)
                sck=_SD_SCK         # Clock pin (adjust based on your hardware)
            )
        if USE_4ZOLL_DISPLAY:
            # da wird der gleiche SPI Bus wie für das Touch verwendet
            # Re: [lvgl-micropython/lvgl_micropython] SD card and screen display conflict (Issue #322)
            spi_bus = SPI_BUS

        if USE_7ZOLL_DISPLAY:
            sd_cs_pin = -1
        if USE_5ZOLL_DISPLAY:
            sd_cs_pin = _SD_CS
        if USE_4ZOLL_DISPLAY:
            sd_cs_pin = _TP_CS_PIN
        
        sd = None
        while sd is None:
            try:
                sd = SDCard(
                    spi_bus=spi_bus,
                    cs=sd_cs_pin,
                    freq=10000000
                )
                # https://github.com/lvgl-micropython/lvgl_micropython/discussions/174
                # in order to have LVGL load anything from the file system you need to use the file system driver to do that.
                # import fs_driver
                # fs_drv = lv.fs_drv_t()  # This MUST not be garbage collected. It is best to do this in your main.py file at the module level. 
                # fs_driver.fs_register(fs_drv, 'S')
                # print(os.listdir('S'))

                vfs.mount(sd, "/sd")
                print('Flash Mounted')
                print(os.listdir('/sd'))
            except Exception as er:
                sd = None
                print(f'sd card failure {er}')
                time.sleep(5)

    #---------------------------------------------------------------------------

    if I2C_BUS is not None:
        print('Scan i2c bus...')
        devices = I2C_BUS.scan()

        if len(devices) == 0:
            print("No i2c device !")
        else:
            print('i2c devices found:',len(devices))
        
        for device in devices:  
            print("Decimal address: ",device," | Hexa address: ",hex(device))
        #---------------------------------------------------------------------------

    #---------------------------------------------------------------------------
