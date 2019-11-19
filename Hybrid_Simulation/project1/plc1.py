"""
toy plc1.py
"""

from minicps.devices import PLC
from utils import PLC1_DATA, IP, STATE
from utils import PLC1_PROTOCOL

import time
import sys


SENSOR1_1 = ('SENSOR1', 1)
SENSOR2_1 = ('SENSOR2', 1)
SENSOR3_1 = ('SENSOR3', 1)
ACTUATOR1_1 = ('ACTUATOR1', 1)
ACTUATOR2_1 = ('ACTUATOR2', 1)

PLC1_ADDR = '10.0.0.10:502'
SCADA_ADDR = '10.0.0.7:502'


class CpsPlc(PLC):

    def pre_loop(self, sleep=0.6):
        print 'DEBUG: toy plc1 enters pre_loop'
        print

        # TODO

        # wait for the other plcs
        time.sleep(sleep)

    def main_loop(self, sleep=0.0):
        print 'DEBUG: toy plc2 enters main_loop'
        print

        count = 0
        END = 6e6
        while(True):
            set_s31 = self.set(SENSOR3_1, count)
            print 'DEBUG: toy plc1 set SENSOR3_1: ', set_s31
            self.send(SENSOR3_1, count, '10.0.0.10')

            time.sleep(1)
            count += 1

            if count > END:
                print 'DEBUG toy plc1 shutdown'
                break


if __name__ == "__main__":

    # notice that memory init is different form disk init
    plc1 = CpsPlc(
        name='plc1',
        state=STATE,
        protocol=PLC1_PROTOCOL,
        memory=PLC1_DATA,
        disk=PLC1_DATA)
