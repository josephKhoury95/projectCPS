"""
toy plc1.py
"""

from minicps.devices import RTU
from utils import PLC1_DATA, STATE
from utils import RTU1_PROTOCOL, IP
from utils import CO_0_2a, HR_0_2a, DI_0_2a, IR_0_2a

import time
import os
import sys


# constant tag addresses
SENSOR1_1 = ('SENSOR1', 1)
SENSOR2_1 = ('SENSOR2', 1)
SENSOR3_1 = ('SENSOR3', 1)
ACTUATOR1_1 = ('ACTUATOR1', 1)
ACTUATOR2_1 = ('ACTUATOR2', 1)

SENSOR3_2 = ('SENSOR3', 2)

SCADA_ADDR = IP['scada'] + ':502'


# TODO: decide how to map what tuples into memory and disk
class ToyPLC1(RTU):

    def pre_loop(self, sleep=0.1):
        print 'DEBUG: toy rtu1 enters pre_loop'
        print

        # sensor1 = self.set(SENSOR1_1, 2)
        # print 'DEBUG: toy plc1 sensor1: ', self.get(SENSOR1_1)
        # self.memory['SENSOR1'] = sensor1

        # self.send(SENSOR3_1, 2, IP['plc1'])
        # self.send(CO_0_2a, True, SCADA_ADDR)

        time.sleep(sleep)

    def main_loop(self, sleep=0.5):
        print 'DEBUG: toy rtu1 enters main_loop'
        print

        count = 0
        END = 6e6
        while(True):

            self.set(CO_0_2a, True)
            self.send(CO_0_2a, True, SCADA_ADDR)

            get_s32 = self.get(SENSOR3_2)
            print 'Value gotten from plc2 is ', get_s32

            # v = self.get(CO_0_2a)
            # print v

            # if count < 10:
            # ## Read-Write
            #     self.send(CO_0_2a, True, SCADA_ADDR)
            #     print CO_0_2a
            # else:
            #     tt = self.receive(CO_0_2a, IP['rtu1'] + ':502')
            #     print tt

            # self.send(HR_0_2a, '9', SCADA_ADDR)
            # ## Read-only
            # self.set(DI_0_2a, '10')
            # self.set(IR_0_2a, True)

            # get_s32 = self.get(SENSOR3_2)
            # rec_s31 = self.receive(SENSOR3_2, IP['plc2'])
            # print 'Value gotten from plc2 is ', rec_s31

            # rec_s31 = self.receive(SENSOR3_1, IP['plc1'])
            # # print 'DEBUG: toy plc1 receive SENSOR3_1: ', rec_s31
            # get_s32 = self.get(SENSOR3_2)
            # print 'DEBUG: toy plc1 get SENSOR3_2: ', get_s32
            #
            # self.send(SENSOR3_2, get_s32, IP['scada'])

            time.sleep(1)
            count += 1

            if count > END:
                print 'DEBUG toy plc1 shutdown'
                break


if __name__ == "__main__":

    # notice that memory init is different form disk init
    rtu1 = ToyPLC1(
        name='rtu1',
        state=STATE,
        protocol=RTU1_PROTOCOL)
