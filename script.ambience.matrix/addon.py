from operator import le
import xbmcgui
import xbmc
import json
from websocket import create_connection

if ( __name__ == "__main__" ):

    monitor = xbmc.Monitor()
    capture = xbmc.RenderCapture()
    dialog = xbmcgui.Dialog()
    image_format = capture.getImageFormat()
    dialog.notification("Image format", image_format)
    ws = create_connection("ws://raspberrypi:1880/ws/ambience")
    dialog.notification("Web socket status", str(ws.getstatus()))
    while not monitor.abortRequested():
        xbmc.sleep(50)
        capture.capture(100,100)
        image = capture.getImage(50)
        image_len = len(image)
        hasImage = image_len > 0
        if not hasImage:
            continue
        B = 0
        G = 0
        R = 0
        A = 0

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
        ws.send(json.dumps({
            "R": int(R / iteration),
            "G": int(G / iteration),
            "B": int(B / iteration),
            "A": int(A / iteration)
        }))

    xbmcgui.Dialog().notification("Aborted", "XBMC monitor aborted'")
    ws.close()