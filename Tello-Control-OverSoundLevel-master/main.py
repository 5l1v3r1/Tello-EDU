import sounddevice as sd
import numpy as np
import socket
import time

# Tello Connecting
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tello_address = ("192.168.10.1", 8889)
sock.bind(('', 9000))

# Activating the commands
msg = "command"
msg = msg.encode()
print(msg)
sent = sock.sendto(msg, tello_address)

# Streaming the video to the python
# msg = "streamon"
# msg = msg.encode()
# print(msg)
# sent = sock.sendto(msg, tello_address)

# Taking the drone off the ground
msg = "takeoff"
msg = msg.encode()
print(msg)
sent = sock.sendto(msg, tello_address)

msg = "up 25"
msg = msg.encode()
print(msg)
sent = sock.sendto(msg, tello_address)


def print_sound(indata, outdata, frames, time, status):
    global volume_norm
    volume_norm = np.linalg.norm(indata)*10

    print(int(volume_norm))

    if volume_norm >= 100:
        for i in range(40):
            msg = "land"
            msg = msg.encode()
            print(msg)
            sent = sock.sendto(msg, tello_address)


with sd.Stream(callback=print_sound):
    global volume_norm
    sd.sleep(100000000)