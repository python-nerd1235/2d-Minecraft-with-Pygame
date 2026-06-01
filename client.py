# Mincraft 2D Online - Client
#version 0.1 (game equivalent to 2dMincraft version 0.4, without saveing.)
import Mincraft2DonlineLib
c=Mincraft2DonlineLib.cli('localhost', 12345)
c.connect()
c.run_client()
print("Thanks for playing!")