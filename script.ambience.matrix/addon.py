import xbmcaddon
import xbmcgui
import xbmc

if ( __name__ == "__main__" ):
    i = 1
    monitor = xbmc.Monitor()
    capture = xbmc.RenderCapture()
    fmt = capture.getImageFormat()
    xbmcgui.Dialog().notification("Test", fmt)

    while not monitor.abortRequested():
        xbmc.sleep(5000)
        i=i+1
        capture.capture(100,100)
        image = capture.getImage()
        count = len(image)
        xbmcgui.Dialog().notification("Test", str(i) + str(count))
    
    xbmcgui.Dialog().notification("Aborted", str(i))
