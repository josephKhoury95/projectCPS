"""
toy topology
"""

from mininet.topo import Topo
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf

from utils import IP, MAC, NETMASK


class CpsTopo(Topo):

    def build(self):

        # info( '*** Adding controller\n' )
        # c0=self.addController(name='c0',
        #                   controller=Controller,
        #                   protocol='tcp',
        #                   port=6633)

        info( '*** Add switches\n')
        s4 = self.addSwitch('s4', cls=OVSKernelSwitch)
        s2 = self.addSwitch('s2', cls=OVSKernelSwitch)
        s1 = self.addSwitch('s1', cls=OVSKernelSwitch)
        s3 = self.addSwitch('s3', cls=OVSKernelSwitch)

        info( '*** Add hosts\n')
        h5 = self.addHost('h5', cls=Host, ip='10.0.0.5', defaultRoute=None)      ## Computer 2
        h1 = self.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)      ## Email Server
        h9 = self.addHost('h9', cls=Host, ip='10.0.0.9', defaultRoute=None)      ## SCADA Historian
        h7 = self.addHost('h7', cls=Host, ip='10.0.0.7', defaultRoute=None)      ## SCADA Server
        h10 = self.addHost('h10', cls=Host, ip='10.0.0.10', defaultRoute=None)   ## PLC
        h6 = self.addHost('h6', cls=Host, ip='10.0.0.6', defaultRoute=None)      ## Computer 3
        h2 = self.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)      ## Web Server
        h4 = self.addHost('h4', cls=Host, ip='10.0.0.4', defaultRoute=None)      ## Computer 1
        h8 = self.addHost('h8', cls=Host, ip='10.0.0.8', defaultRoute=None)      ## SCADA HMI
        h3 = self.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute=None)      ## Database Server

        info( '*** Add links\n')
        self.addLink(h4, s2)
        self.addLink(h5, s2)
        self.addLink(h6, s2)
        self.addLink(h7, s3)
        self.addLink(h8, s3)
        self.addLink(h9, s3)
        self.addLink(h10, s4)
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s1)
        self.addLink(s1, s2)
        self.addLink(s2, s3)
        self.addLink(s3, s4)

        # c0 = self.addController('c0', controller=RemoteController)

        # ## Switch 1
        # s1 = self.addSwitch('s1')
        #
        # #### DMZ
        # ## Email Server
        # eml_server = self.addHost(
        #     'eml_server',
        #     ip=IP['eml_server'] + NETMASK,
        #     mac=MAC['eml_server'])
        # self.addLink(eml_server, switch1)
        #
        # ## Web Server
        # web_server = self.addHost(
        #     'web_server',
        #     ip=IP['web_server'] + NETMASK,
        #     mac=MAC['web_server'])
        # self.addLink(web_server, switch1)
        #
        # ## Database Server
        # db_server = self.addHost(
        #     'db_server',
        #     ip=IP['db_server'] + NETMASK,
        #     mac=MAC['db_server'])
        # self.addLink(db_server, switch1)
        #
        # ## Switch 2
        # s2 = self.addSwitch('s2')
        # self.addLink(eml_server, switch2)
        # self.addLink(web_server, switch2)
        # self.addLink(db_server, switch2)
        #
        #### Computers Offices
        ## Computer1
        # computer1 = self.addHost(
        #     'computer1',
        #     ip=IP['computer1'] + NETMASK,
        #     mac=MAC['computer1'])
        # # self.addLink(computer1, switch2)
        #
        # ## Computer2
        # computer2 = self.addHost(
        #     'computer2',
        #     ip=IP['computer2'] + NETMASK,
        #     mac=MAC['computer2'])
        # # self.addLink(computer2, switch2)
        #
        # ## Computer3
        # computer3 = self.addHost(
        #     'computer3',
        #     ip=IP['computer3'] + NETMASK,
        #     mac=MAC['computer3'])
        # # self.addLink(computer3, switch2)
        # #
        # # ## Switch 3
        # s3 = self.addSwitch('s3')
        # self.addLink(computer1, switch3)
        # self.addLink(computer2, switch3)
        # self.addLink(computer3, switch3)
        #
        # #### SCADA
        # ## SCADA Server
        # scada_ser = self.addHost(
        #     'scada_ser',
        #     ip=IP['scada_ser'] + NETMASK,
        #     mac=MAC['scada_ser'])
        # self.addLink(scada_ser, switch3)
        #
        # ## SCADA HMI
        # scada_hmi = self.addHost(
        #     'scada_hmi',
        #     ip=IP['scada_hmi'] + NETMASK,
        #     mac=MAC['scada_hmi'])
        # self.addLink(scada_hmi, switch3)
        #
        # ## SCADA Historian
        # scada_his = self.addHost(
        #     'scada_his',
        #     ip=IP['scada_his'] + NETMASK,
        #     mac=MAC['scada_his'])
        # self.addLink(scada_his, switch3)
        #
        # ## Switch 4
        # s4 = self.addSwitch('s4')
        # self.addLink(scada_ser, switch4)
        # self.addLink(scada_hmi, switch4)
        # self.addLink(scada_his, switch4)
        #
        # #### Field devices
        # ## PLC1
        # plc1 = self.addHost(
        #     'plc1',
        #     ip=IP['plc1'] + NETMASK,
        #     mac=MAC['plc1'])
        # self.addLink(plc1, switch4)

        # switch1.start([c0])
        # switch2.start([c0])
        # switch3.start([c0])
        # switch4.start([c0])

        # self.addLink(scada_ser, switch4)
        # self.addLink(scada_hmi, switch4)
        # self.addLink(scada_his, switch4)


        # switch = self.addSwitch('s1')
        #
        # plc1 = self.addHost(
        #     'plc1',
        #     ip=IP['plc1'] + NETMASK,
        #     mac=MAC['plc1'])
        # self.addLink(plc1, switch)
        #
        # # switch2 = self.addSwitch('s2')
        #
        # scada_ser = self.addHost(
        #     'scada_ser',
        #     ip=IP['scada_ser'] + NETMASK,
        #     mac=MAC['scada_ser'])
        # self.addLink(scada_ser, switch)
