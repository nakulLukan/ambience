import xbmcaddon
import xbmcgui
import xbmc
from websocket import create_connection

if ( __name__ == "__main__" ):
    i = 1
    monitor = xbmc.Monitor()
    capture = xbmc.RenderCapture()
    dialog = xbmcgui.Dialog()
    image_format = capture.getImageFormat()
    dialog.notification("Image format", image_format)

    ws = create_connection("ws://localhost:1880/ws/ambience")
    dialog.notification("Web socket status", str(ws.getstatus()))

    while not monitor.abortRequested():
        xbmc.sleep(2000)
        i=i+1
        capture.capture(100,100)
        image = capture.getImage()
        count = len(image)
        dialog.notification("Data", str(i) + str(count))
        ws.send("Hello, World")


    xbmcgui.Dialog().notification("Aborted", str(i))
    ws.close()