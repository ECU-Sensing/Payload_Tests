# Author: Colby Sawyer
# Dummy implementation of data. This used generate random "Weather" data. 
# It is recommended that you prepackage your data in a bytearray here so that you can have have a sketch for the decoder later

from logging import BufferingFormatter
from time import sleep
import struct
from datetime import datetime
import time
from tracemalloc import start
import pandas as pd
from csv import writer

ROUND_DEC = 3
DATA_SIZE = 16

def write_data_to_csv(buffer):
    #print(buffer)
    df = pd.DataFrame(buffer)
    date = datetime.now().strftime("%Y_%m_%d")
    #df.to_csv(f'stored/complete_metric_{date}.csv')
    
    # First, open the old CSV file in append mode, hence mentioned as 'a'
    # Then, for the CSV file, create a file object
    with open(f'stored/complete_metric_{date}.csv', 'a', newline='') as f_object:  
        # Pass the CSV  file object to the writer() function
        writer_object = writer(f_object)
        # Result - a writer object
        # Pass the data in the list as an argument into the writerow() function
        st = 0
        end = 15
        while end < len(buffer):
            vals_list = buffer[st:end:]
            writer_object.writerow(vals_list)
            st += DATA_SIZE
            end += DATA_SIZE
        # Close the file object
        f_object.close()

def get_agg_from_buffer(buffer):
    #[datetime, 18, 25, 100, 40.16, 5.87, 46.65, 6.21, 46.85, 6.21, 46.95, 6.21, 46.81, 6.21, 46.87, 172]
    start_val = 1
    increment = DATA_SIZE
    agg = []

    while start_val < increment:
        val_list = buffer[start_val::increment]
        val_max = round(float(max(val_list)),ROUND_DEC)
        val_min = round(float(min(val_list)),ROUND_DEC)
        val_avg = round(float((sum(val_list)/len(val_list))),ROUND_DEC)
        agg.extend([val_max,val_min,val_avg])
        start_val+=1

    return agg    

def float_list_to_bytes(floatlist):
    payload = bytearray()
    for flt in floatlist:
        payload.extend(bytearray(struct.pack("f", flt)))
    #print([ "0x%02x" % b for b in payload ])
    return payload

def get_data():
    # Instance Specific Info
    Feather_Id = 1.0
    # Add Start TimeStamp
    start_dt = datetime.now()
    buffer = []
    x = 0
    while x < 59:
        buffer.extend(read_sensor())
        #print(buffer)
        x = x + 1 
        sleep(1)

    # Save Seconds Data in CSV
    write_data_to_csv(buffer)

    # Create Aggregation Metrics from Buffer
    buffer = get_agg_from_buffer(buffer)

    # Add Timestamps
    end_dt = datetime.now()
    buffer.insert(0,time.mktime(start_dt.timetuple()) + start_dt.microsecond/1e6)
    buffer.extend([time.mktime(end_dt.timetuple()) + end_dt.microsecond/1e6])

    #Encode Minutes data to bytearray for transmission
    sensor_data = float_list_to_bytes(buffer)
    
    #print(len(sensor_data))
    return sensor_data

def read_sensor():
    #      [Temp_F, R_Hum, Batt, NC0_5, MC1_0, NC1_0, MC2_5, NC2_5, MC4_0, NC4_0, MC10_0, NC10_0, tVOC]
    dt = datetime.now()
    timestamp_float = time.mktime(dt.timetuple()) + dt.microsecond/1e6
    return [timestamp_float, 18, 25, 100, 40.16, 5.87, 46.65, 6.21, 46.85, 6.21, 46.95, 6.21, 46.81, 172]
