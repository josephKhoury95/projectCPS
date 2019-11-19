"""
run.py
"""

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from minicps.mcps import MiniCPS
from topo import CpsTopo
from utils import IP, MAC, NETMASK

import sys, os
import gym
import gym_cps
import time


class CpsSimulation(MiniCPS):

    """Main container used to run the simulation."""

    def __init__(self, name, net):

        self.name = name
        self.net = net

        # c0 = self.net.addController(name='c0',
        #                   controller=Controller,
        #                   protocol='tcp',
        #                   port=6633)

        info( '*** Starting network\n')
        self.net.start()

        info( '*** Starting network\n')
        # self.net.build()

        info( '*** Starting controllers\n')
        for controller in self.net.controllers:
            controller.start()

        info( '*** Starting switches\n')
        self.net.get('s4').start([self.net.get('c0')])
        self.net.get('s2').start([self.net.get('c0')])
        self.net.get('s1').start([self.net.get('c0')])
        self.net.get('s3').start([self.net.get('c0')])

        info( '*** Post configure switches and hosts\n')

        ## Make the environment
        self.SimulateEnv(self.net)

        CLI(self.net)
        self.net.get('s4').stop()
        self.net.get('s2').stop()
        self.net.get('s1').stop()
        self.net.get('s3').stop()
        self.net.get('c0').stop()
        self.net.stop()
        # cmd(sys.executable + 'sudo mn -c &')

    def SimulateEnv(self, net):

        ## Output to file
        f = open('out.txt', 'w')

        env = gym.make('cps-v0')
        env.set_environment(net)

        done = False
        observation = env.observation
        steps = 0
        print env.render()
        print >>f, env.render()

        while not done:
            # print '****'
            print >>f, '****'
        # while steps < 1:
            steps += 1

            ## This is only used for attacker action sample..
            # action = env.attacker_action_space_sample(observation)

            ## This return a tuple
            ## index 0: Attacker action
            ## index 1: Defender action
            action = env.action_sample(observation)

            observation, reward_a, reward_d, done = env.step(action)
            # print 'Number of moves: ' + str(steps)
            # print 'Attacker action: ' + str(action[0][1].name) + ' - index: ' + str(action[0][2])
            # print 'Defender action: ' + str(action[1][1].name) + ' - index: ' + str(action[1][2]) + '\n'
            # print env.render()

            print >>f, 'Number of moves: ' + str(steps)
            print >>f, 'Attacker action: ' + str(action[0][1].name) + ' - index: ' + str(action[0][2])
            print >>f, 'Defender action: ' + str(action[1][1].name) + ' - index: ' + str(action[1][2]) + '\n'
            print >>f, env.render()

            if done:
                break

        print('Game lasted ' + str(steps) + ' moves.')
        print >>f, 'Game lasted ' + str(steps) + ' moves.'

        print('Attacker reward: ' + str(reward_a))
        print >>f, 'Attacker reward: ' + str(reward_a)

        print('Defender reward: ' + str(reward_d))
        print >>f, 'Defender reward: ' + str(reward_d)

        # print(env.render())
        # print >>f, env.render()


if __name__ == "__main__":

    topo = CpsTopo()
    net = Mininet(topo=topo ,ipBase='10.0.0.0/8')


    mycpstopo = CpsSimulation(
        name='mycpstopo',
        net=net)
