# Mincraft 2D Online - Server
#version 0.1 (game equivalent to 2dMincraft version 0.4, without saveing.)
import Mincraft2DonlineLib
import socket
import json
print("Starting server...")
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.connect(("8.8.8.8", 80))
    MIP=s.getsockname()[0]
print(f"Your IP address is {MIP}.")
print('Reading settings...')
try:
    with open('Server_settings.json', 'r') as f:
        settings = json.load(f)
        if settings['localhost']:
            MIP='localhost'
        else:
            MIP=MIP
        name=settings['name']
except FileNotFoundError:
    print(F"No Server_settings.json found. Starting with default settings ({MIP}:12345).")
    name=input('Enter the name of the server (for display purposes): ')
    with open('Server_settings.json', 'w') as f:
        json.dump({"localhost": False, "name": name}, f)
s=Mincraft2DonlineLib.ser(MIP, 12345, name)
print("Loading server...")
s.start_server()
print("Running server...")
s.run_server()
print("Server stopped. Thanks for playing!")

if __name__ == "__main__":
    ...