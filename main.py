import subprocess
import time
import os
from pystray import Icon, Menu, MenuItem
from PIL import Image
import threading


lowest_brightness = 1

def decrease_brightness():
    subprocess.run(["brightnessctl", "set", f"{lowest_brightness}%"])
    print(f"brightness set to {lowest_brightness}")



def current_brightness():
    result = subprocess.run(["brightnessctl", "get"], capture_output=True, text=True)
    return result.stdout.strip()



def increase_brightness(brightness):
     subprocess.run(["brightnessctl", "set", f"{brightness}"])
     print(f"Increased screen brightness to {brightness}%")


interval = 20 #in minutes
delay = 20 #in seconds
toggle = True


def eyerest_loop():
    while toggle:
        print(f"waiting {interval} seconds")
        time.sleep(interval*60)
        print("done waiting")
        
        now_brightness = current_brightness()
        print(f"Current brightness = {now_brightness}")
    
        
        decrease_brightness()
        os.system("canberra-gtk-play --id='bell'")
    
        time.sleep(delay)
    
        os.system("canberra-gtk-play --id='complete'") #playes a bell sound on completion
        increase_brightness(now_brightness)
    

def setup_tray():
    image = Image.open("/home/linux4050/Projects/EyeRest/icon.png")
    
    menu = Menu(
        MenuItem("Exit", lambda: icon.stop())
    )
    
    icon = Icon("EyeRest", image, "EyeRest", menu)
    
    threading.Thread(target=eyerest_loop, daemon=True).start()

    icon.run()

if __name__ == "__main__":
    setup_tray()