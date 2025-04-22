# Konfiguration für das verwendete Displaypanel
# hier aktuell 5" Elecrow ESP32S3 N4R8, also 4 MB Flash und 8 MB RAM
# import lvgl_panel_config as cfg

# hier sind einige Hilfsfunktionen, ohne die Display und Touch Initialisierung

'''
Firmware build
    python3 make.py esp32 clean BOARD=ESP32_GENERIC_S3 BOARD_VARIANT=SPIRAM_OCT 
        --flash-size=4 DISPLAY=rgb_display INDEV=gt911 --enable-cdc-repl=n --enable-jtag-repl=n
'''
from micropython import const  # NOQA
import time
import sys
import gc
import lvgl as lv  # NOQA

lv.init()

# LVGL-Version durch Aufrufen der Funktionen anzeigen
def lvgl_info():
    major = lv.version_major()
    minor = lv.version_minor()
    patch = lv.version_patch()
    # Garbage Collector aufrufen, um unbenutzten Speicher freizugeben
    gc.collect()

    total_ram = gc.mem_alloc() + gc.mem_free()
    used_ram = gc.mem_alloc()
    free_ram = gc.mem_free()

    print("Gesamter RAM:", total_ram, "Bytes")
    print("Belegter RAM:", used_ram, "Bytes")
    print("Freier RAM:", free_ram, "Bytes")
    if sys.platform in ('esp', 'esp32'):
        import esp
        print(f"Flash Size: {esp.flash_size()}")
    print("LVGL Version:", major, ".", minor, ".", patch)
    print("---------------------------------------------------")
    print(sys.version)
    print("---------------------------------------------------")

# wo liegt dieses Modul im System
def get_script_path():
    try:
        script_path = __file__[:__file__.rfind('/')] if __file__.find('/') >= 0 else '.'
    except NameError: 
        script_path = ''
    print(f"script_path = {script_path}")
    return script_path

#---------------------------------------------------------------------------
# da gibts Speicherfehler, WFIFI for dem Displaytreiber laden !

def network_init():
    if sys.platform in ('esp', 'esp32'):
        import network

        def wifi_connect():
            ssid = 'MyNiceWlan'
            password = 'HANSIBLUDENZ1'
            
            wlan = network.WLAN(network.STA_IF)  # Create a WLAN object in station mode
            wlan.active(True)  # Activate the network interface
            wlan.connect(ssid, password)  # Connect to the specified WiFi network
            
            while not wlan.isconnected():  # Wait for the connection to be established
                print('Waiting for connection...')
                time.sleep(1)
            
            print('Connected on {ip}'.format(ip=wlan.ifconfig()[0]))  # Print the IP address

        wifi_connect()

#---------------------------------------------------------------------------
# rd write auf SD Karte

# write to a file
def sd_write_file(filename, data):
    with open("sd/" + filename, "wb") as file:
        file.write(data)
    print("Data has been written to file:", filename)

# Read file
def sd_read_file(filename):
    with open("sd/" + filename, "rb") as file:
        data = file.read()
    # print("readout:", data)
    return data

'''
# Hinweis von kdschlosser

def create_img_dsc(imgdata):
    imgdsc = lv.image_dsc_t({'data_size':len(imgdata), 'data':imgdata})
    return imgdsc
    
some_image_data = sd_read_file(YOURIMAGEFILENAME)
some_image_data_mv = memoryview(some_image_data)
some_img_dsc = create_img_dsc(some_image_data_mv)

image = lv.image(lv.screen_active())
image.set_src(some_img_dsc)

'''
#---------------------------------------------------------------------------
# Die Daten einen PNG Bildes von SD oder Filesystem lesen

def lvgl_get_image_desc(filename):
    # wenn das Programm auch unter WSL laufen soll
    print(f"Image {filename} laden ...")
    if sys.platform in ('linux', 'darwin'):
        # Bild vom assets Unterverzeichnis lesen
        # with open("sd/assets/" + filename, "rb") as file:
        #     png_data = file.read()
        png_data = sd_read_file("assets/" + filename)
    else: # wenn von ESP
        # Load the image von SD Karte
        # with open("sd/assets/" + filename, "rb") as file:
        #     png_data = file.read()
        png_data = sd_read_file("assets/" + filename)
        #with open("assets/" + filename, "rb") as file:
        #    png_data = file.read()
    png_image_dsc = lv.image_dsc_t({
        'data_size': len(png_data),
        'data': png_data 
    })
    print(f"Image {filename} geladen!")
    return png_image_dsc

# def read_image(
#                 # Bilddaten von der SD-Karte lesen
#     with open('S:HoPOS_small_320.bin', 'rb') as file:
#        img_data = file.read()
#  # Canvas-Objekt erstellen und Bilddaten darauf anzeigen
#     canvas = lv.canvas(screen)  # Canvas wird auf dem erstellten Bildschirm hinzugefügt
#     canvas.set_buffer(img_data, 320, 240, lv.COLOR_FORMAT.RGB565)  # Setzt Bildgröße und RGB565-Format
#     canvas.align(lv.ALIGN.CENTER, 0, 0)  # Zentriert das Bild auf dem Bildschirm


# )

#---------------------------------------------------------------------------

