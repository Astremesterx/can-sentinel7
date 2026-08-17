import os
import time

while True:
    os.system("cansend vcan0 101#07D0000000000000")
    print("Engine ECU → RPM 2000 sent")
    time.sleep(1)

