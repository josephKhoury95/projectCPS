"""
scada.py
"""

from minicps.devices import SCADAServer
from utils import SCADA_PROTOCOL, STATE
from utils import PLC_PERIOD_SEC
from utils import IP, CO_0_2a, HR_0_2a, DI_0_2a, IR_0_2a

import time

# PLC1_ADDR = IP['plc1'] + ':502'
# SCADA_ADDR = IP['scada_ser'] + ':502'


PLC1_ADDR = '10.0.0.10:502'
SCADA_ADDR = '10.0.0.7:502'

SENSOR3_1 = ('SENSOR3', 1)

class SCADAServer(SCADAServer):

    def pre_loop(self, sleep=0.5):
        """scada pre loop.
            - sleep
        """

        time.sleep(sleep)

    def main_loop(self):
        """scada main loop.
        For each RTU in the network
            - Read the pump status
        """
        count = 0
        while(True):

            tt = self.receive(SENSOR3_1, '10.0.0.10')
            print tt

            # if count < 10:
            # #co_00_2a = self.receive(CO_0_2a, RTU2A_ADDR)
            #     tt = self.receive(CO_0_2a, SCADA_ADDR)
            #     print tt
            # else:
            #     self.send(CO_0_2a, False, IP['rtu1'] + ':502')
            #     print CO_0_2a[1]

            # hh = self.receive(HR_0_2a, SCADA_ADDR)
            # ff = self.receive(IR_0_2a, SCADA_ADDR)
            # dd = self.receive(DI_0_2a, SCADA_ADDR)
            # tt = self.receive(SENSOR3_2, SCADA_ADDR)
            # print 'aaaaa ', tt
            # print 'bbbbb ', hh
            # print 'ccccc ', ff
            # print 'ddddd ', dd

            # NOTE: used for testing first challenge
            #print('DEBUG scada from rtu2a: CO 0-0 2a: {}'.format(co_00_2a))

            # NOTE: used for testing second challenge
            # NOTE: comment out
            # hr_03_2a = self.receive(HR_0_2a, RTU2B_ADDR, count=3)
            # print('DEBUG scada from rtu2b: HR 0-2 2a: {}'.format(hr_03_2a))


            # print("DEBUG: scada main loop")
            # time.sleep(PLC_PERIOD_SEC)

            time.sleep(1)
            count += 1


if __name__ == "__main__":

    scada_ser = SCADAServer(
        name='scada_ser',
        state=STATE,
        protocol=SCADA_PROTOCOL)
