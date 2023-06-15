import xbmcgui
import xbmc
import json
import xbmcaddon
from websocket import create_connection
import socket

PI_HOST_NAME = "raspberrypi"
PI_IP = f"{socket.gethostbyname('raspberrypi')}:1880"

addon_icon_path = ''

def send_pixel(ws, R, G, B, A):
    ws.send(json.dumps({
            "R": int(R),
            "G": int(G),
            "B": int(B),
            "A": int(A)
        }))

def notify(dialog:xbmcgui.Dialog, heading: str, description: str):
    dialog.notification(heading, description, addon_icon_path, time=30)

if ( __name__ == "__main__" ):
    addon = xbmcaddon.Addon()
    monitor = xbmc.Monitor()
    capture = xbmc.RenderCapture()
    dialog = xbmcgui.Dialog()

    addon_icon_path = addon.getAddonInfo('path') + '/icon.png'
    notify(dialog, "Ambience", 'Activated')
    player = xbmc.Player()

    ws = create_connection(f"ws://{PI_IP}/ws/ambience")
    notify(dialog, "Ambience", 'Connected to module successfully.')

    pixel = 128
    sleep_time = 33

    was_playing = False
    while not monitor.abortRequested():
        xbmc.sleep(sleep_time)
        is_playing = player.isPlayingVideo()
        if not is_playing:
            if was_playing:
                send_pixel(ws, 0, 0, 0, 0)
                was_playing = False
            continue
        
        was_playing = True
        
        row = int(pixel * capture.getAspectRatio())
        col = pixel

        capture.capture(row, col)
        image = capture.getImage(sleep_time)
        image_len = len(image)
        hasImage = image_len > 0
        if not hasImage:
            continue

        B = G = R = A = 0

        b = 0
        g = 1
        r = 2
        a = 3

        iteration = image_len / 4
        while r < iteration:
            R += (image[r])
            G += (image[g])
            B += (image[b])
            A += (image[a])

            r = r + 4
            g = g + 4
            b = b + 4
            a = a + 4
        # notify(dialog, "Ambience", f'{int(R / iteration)} + {int(G /iteration)} + {int(B /iteration)} + {int(A /iteration)}')
        
        send_pixel(ws,
            R / iteration, 
            G / iteration,
            B / iteration,
            A / iteration)
    
    notify(dialog, "Ambience", "XBMC monitor aborted")
    ws.close()