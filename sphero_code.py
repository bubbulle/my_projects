import time
from pysphero.core import Sphero
from pysphero.driving import Direction
import sys
from enum import Enum
from pysphero.device_api.sensor import CoreTime, Quaternion, AmbientLight
from pysphero.device_api import DeviceApiABC, DeviceId
from pysphero.packet import Flag
from pysphero.bluetooth.bluepy_adapter import BluepyAdapter
import abc
from concurrent.futures import Future
from typing import Callable
from pysphero.packet import Packet
from pysphero.packet import Flag
import contextlib
import logging
from typing import List, Optional
from bluepy.btle import DefaultDelegate, Peripheral, ADDR_TYPE_RANDOM, Characteristic, Descriptor
from pysphero.bluetooth.ble_adapter import AbstractBleAdapter
from pysphero.bluetooth.packet_collector import PacketCollector
from pysphero.constants import SpheroCharacteristic, GenericCharacteristic

#maybe too much imports, need to cleen all these

#modify this function to wait less time after giving an order to sphero
def my_write(self, packet: Packet, *, timeout: float = 10, raise_api_error: bool = True) -> Optional[Packet]:
        logger.debug(f"Send {packet}")
        self.ch_api_v2.write(packet.build(), withResponse=False) #changed to false
        #return self.packet_collector.get_response(packet, raise_api_error, timeout=timeout)

#I love python
BluepyAdapter.write = my_write

#total time for the robot running
RUNNING_TIME=10
#the lab's robots' adresses
addresses=["E4:C9:D4:82:B8:4A", "CF:A1:99:E6:60:CA", "EA:16:30:8A:40:0A"]
#change the adress here depanding which robot you want to use
robot_adress=addresses[1]

def drive(addresses, starting_time
    with Sphero(mac_address=robot_address) as sphero:
        print('robot connected')
        try:
            sphero.power.wake()
            print('robot awake')
        except:
            sphero.power.enter_soft_sleep()
            print('go back to sleep')
            sphero.power.wake()
            print("now you're awake ?")
        current_time=time.time()
        #constantly print the bot's gyroscope info
        try:
            sphero.sensor.set_notify(notify_callback, CoreTime, Quaternion)
            print('sensor on')
        except:
            print("sensor doesn't want to work ;_;")
        while(current_time-starting_time<RUNNING_TIME):
            light=300
            try:
                light = sphero.sensor.get_ambient_light_sensor_value()
                print(light)
            except:
                print("sensor doesn't want to work ;_;")
            try:
                if light >= 300:
                    sphero.driving.drive_with_heading(100, 0, Direction.forward)
                else:
                    sphero.driving.drive_with_heading(0, 0, Direction.forward)
            except:
                print("robot won't move >:(")
            current_time=time.time()
        print('time over')
        sphero.power.enter_soft_sleep()
    return True

#in case the robot disconnects we need to know when we started
def call_the_robot(starting_time):
    end=False
    try:
        end=drive(addresses, starting_time)

    except:
        #sometimes the robot disconnects, we need to reconnect it
        if not end:
            print("robot disconnected")
            call_the_robot(starting_time)

call_the_robot(time.time())

#nothing necessary there, but I don't feel like ereasing it

#trying to make the animatronics.play_animation function working
#it does not work but I keep it there
"""
def my_play_animation(self, animation_id: int, target_id=0x12):
        self.request(
            AnimatronicsCommand.play_animation,
            target_id=target_id,
            data=[*animation_id.to_bytes(2, "big")],
        )

Animatronics.play_animation = my_play_animation
"""

#first try to make the bot responds quicker after giving an order
#it does work but it wasn't perfect
"""
def my_request(self, command_id: Enum, timeout: float = 0.5, raise_api_error: bool = True, **kwargs) -> Packet:
    return self.ble_adapter.write(
        self.packet(command_id=command_id.value, **kwargs),
        raise_api_error=raise_api_error,
        timeout=timeout,
    )

DeviceApiABC.request=my_request
"""
