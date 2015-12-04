import time
import winsound

mp3 = u'sounds/BUZZ4.wav'
t = time.time()
for i in range(4):
    winsound.PlaySound(mp3, winsound.SND_NODEFAULT)
    #time.sleep(0.1)
print time.time() - t
