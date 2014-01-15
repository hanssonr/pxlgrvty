"""
Enumclass for the different sensors
"""
class Sensor(object):
    PLAYER_FOOTSENSOR = 0
    GRAVITYZONESENSOR = 1 #cant be same as TileType.GRAVITYZONE != 2
    PLAYER_DEATHSENSOR = 99