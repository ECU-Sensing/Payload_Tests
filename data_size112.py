# Author: Colby Sawyer
# Dummy implementation of data. This used generate random "Weather" data. 
# It is recommended that you prepackage your data in a bytearray here so that you can have have a sketch for the decoder later

from csv import get_dialect
from itertools import count
import random
from datetime import datetime
from phonenumbers import country_code_for_valid_region

def get_data():
    # Here is where you can add your sensor specific information. The driving code will use whatever data is here
    payload =[item for item in range(0,112)]
    sensor_data = bytearray(payload)
    print("Byte Size:" + str(len(sensor_data)))
    return sensor_data
