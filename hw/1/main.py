#!/usr/bin/python
"CYDF321 Spring 2019 Term Project #1"

# Mininet
from mininet.topo import Topo
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.clean import cleanup
from mininet.log import lg, info
from mininet.util import dumpNodeConnections
from mininet.cli import CLI

import numpy as np
import matplotlib as mpl
mpl.use('Agg') # Headless mode
import matplotlib.pyplot as plt

# Process
from subprocess import Popen, PIPE
from time import sleep, time
from multiprocessing import Process
from argparse import ArgumentParser

# General
import sys
import os
import math


class MininetTolpology(Topo):
    "Simple topology for CYDF321 Term Project."

    def build(self, bandwidth=100, delay=100):
        # Create the nodes to form the given topology
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        # Adds a switch to the topology for connecting the nodes
        s1 = self.addSwitch('s1')
        # Add links to the topology with appropriate characteristics
        self.addLink(h1,s1)
        self.addLink(h2,s1)
        print "Link Information\n"
        print "Bandwidth =", bandwidth * 1000.0, "Kbps\n"
        print "Network Delay =", 4 * delay, "ms"


def start_webserver(net):
    print "Starting webserver..."
    h1 = net.get('h1')
    proc = h1.popen("python -m SimpleHTTPServer 80", shell=True)
    sleep(1)
    return [proc]


def setup(bandwidth=100, delay=100):
    # Clean up existing mininet
    print "Cleaning up mininet..."
    cleanup()

    # Set congestion control to cubic (It is default congestion control algorithm)
    os.system("sysctl -w net.ipv4.tcp_congestion_control=cubic > /dev/null")

    # Timeout modifiers, throw it all away
    os.system("sysctl -w net.ipv4.tcp_retries1=100 > /dev/null")
    os.system("sysctl -w net.ipv4.tcp_retries2=100 > /dev/null")
    os.system("sysctl -w net.ipv4.tcp_frto=100 > /dev/null")
    os.system("sysctl -w net.ipv4.tcp_frto_response=100 > /dev/null")

    # Setup network topology
    print "Starting network..."
    topo = MininetTolpology(bandwidth=bandwidth, delay=delay / 4.0)
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    net.start()
    return net


def clean(net):
    print "Stopping network..."
    if net is not None:
        net.stop()

    Popen("pgrep -f webserver.py | xargs kill -9", shell=True).wait()
    Popen("killall -9 iperf", shell=True).wait()
    Popen("killall -9 ping", shell=True).wait()


def update_cwnd(host, initcwnd, initrwnd, mtu):
    rto_min = 1000

    route = host.cmd("ip route show").strip()
    print "route 1", route
    cmd = "sudo ip route change {} initcwnd {} initrwnd {} mtu {} rto_min {}".format(
        route, initcwnd, initrwnd, mtu, rto_min)
    print "$", cmd
    print "initcwnd", host.cmd(cmd)

#Generate figure function
def generate_figures(name, xaxis, xlabels, title, results):
    N, M = np.shape(results)
    abs_im = []
    per_im = []
    for i in range(N):
        a, b = results[i, :]
        abs_im += [(a - b) * 1000.0]
        per_im += [(a / b - 1) * 100]

    ind = np.arange(N)  # the x locations for the groups
    width = 0.35       # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, abs_im, width, bottom=1, color='#862633')

    # add some text for labels, title and axes ticks
    ax.set_ylim((1, 10000))
    ax.set_yscale('log')
    ax.set_ylabel('Improvement (ms)')
    ax.set_xlabel(xaxis)
    ax.set_title(title)
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(xlabels)

    ax2 = ax.twinx()
    ax2.set_ylim((0, 50.0))
    rects2 = ax2.bar(ind + width, per_im, width, bottom=0, color='#4169E1')

    ax.legend((rects1[0], rects2[0]),
              ('Absolute Improvement', 'Percentage Improvement'))

    fig.savefig('results/' + name + '.png')
    plt.close(fig)

#Generate initial figure function
#This function is used only once in init_cwnd_experiment()
def generate_init_figure(name, xaxis, xlabels, title, results):
    N = results.size
    yaxis = []
    for i in range(N):
        yaxis += [results[i]]
    
    ind = np.arange(N)
    width = 0.35

    #fig, ax = plt.subplots()
    p1 = plt.bar(ind, results, width, color='#862633')

    # add some text for labels, title and axes ticks
    plt.ylabel('RTT (ms)')
    plt.title(title)
    plt.xticks(ind, xlabels)
    plt.xlabel(xaxis)
    
    max_yaxis = int(max(yaxis))+1
    plt.yticks(np.arange(0, max_yaxis, (max_yaxis/10)+1))

    plt.savefig('results/' + name + '.png')
    plt.close()


#Set experiment parameter, links between hosts
#Measure latency 3 times
def experiment(bandwidth, delay, initcwnd, initrwnd, file=[
        "search/index.html", "search/1", "search/2", "search/3", "search/4"]):
    R = 3       # Number of concurrent curl experiments
    S = 0       # Time to sleep waiting for curl
    T = 30      # Time to run experiment
    mtu = 1500  # Max transmission unit

    # Setup
    net = setup(bandwidth=bandwidth, delay=delay)

    # Configuration
    h1 = net.get('h1')
    h2 = net.get('h2')
    times = []

    # Configure congestion window (only on the second experiment)
    update_cwnd(h1, initcwnd, initrwnd, mtu)
    update_cwnd(h2, initcwnd, initrwnd, mtu)

    # Check results
    print "H1 route:", h1.cmd("ip route show").strip()
    print "H2 route:", h2.cmd("ip route show").strip()

    # Experiment
    start_webserver(net)

    # Measure latency
    start_time = time()
    while True:
        for i in range(R):
            etime = 0
            for q in file:
                cmd = "curl -o /dev/null -s -w %{time_total} " + \
                    h1.IP() + "/http/" + q
                result = h2.cmd(cmd)
                print result
                etime += float(result)
            times += [etime]

        # do the measurement (say) 3 times.
        sleep(S)
        now = time()
        delta = now - start_time
        if delta > T:
            break
        print "%.1fs left..." % (T - delta)

    # Clean up
    clean(net)
    return np.mean(times)

"""
Experiment for measuring performance by changing bandwidth and mode
Tip: 'MODE' indicates conngestion control window size

This experiment sets X-axis as bandwidth and Y-axis as improvement ratio
Tip: There would be two bar since there are two modes (3,100) and (10, 100)
"""
def bandwidth_experiment():
    BW = (256, 512, 1000, 2000, 3000, 5000, 10000)#, 20000, 50000, 100000, 200000)
    MODE = (
        (3, 100),
        (10, 100)
    )

    N = len(BW)
    M = len(MODE)
    delay = 70

    results = np.zeros((N, M))

    # Run experiment
    # Use 'for' statement to change the 'BW' and 'MODE' and to store in 'results'
    """
    ***DO THIS***
    Hint: results[r, i] = experiment(*,*,*,*)
    """


    # Debugging
    print "Final results"
    print results

    # Save result
    generate_figures("Figure_Bandwidth_Experiment",
                     'Bandwidth (Kbps)',
                     BW,
                     'Average response latency for Web search bucketed by BW',
                     results)


"""
Experiment for measuring performance by changing network delay and mode
Tip: 'MODE' indicates conngestion control window size

This experiment sets X-axis as network delay and Y-axis as improvement ratio
Tip: There would be two bar since there are two modes (3,100) and (10, 100)
"""
def network_delay_experiment():
    delay = (20, 50, 100, 200, 500, 800, 1000) #800 is added _ 190321 wwjang
    MODE = (
        (3, 100),
        (10, 100)
    )

    M = len(MODE)
    N = len(delay)
    bandwidth = 1.2

    results = np.zeros((N, M))

    # Run experiment
    # Use 'for' statement to change the 'delay' and 'MODE' and to store in 'results'
    """
    ***DO THIS***
    Hint: results[r, i] = experiment(*,*,*,*)
    """

    # Debugging
    print "Final results"
    print results

    # Save result
    generate_figures("Figure_Network_Delay_Experiment",
                     'Network Delay (msec)',
                     delay,
                     'Average response latency for Web search bucketed by RTT',
                     results)


"""
Experiment for measuring performance by changing segment size and mode
Tip: Mininet does not support changing segment size, so you must use /http/*.html to change segment size

Tip: 'MODE' indicates conngestion control window size

This experiment sets X-axis as segment size and Y-axis as improvement ratio
Tip: There would be two bar since there are two modes (3,100) and (10, 100)
"""
def segment_size_experiment():
    SEG = (3, 4, 7, 10, 15, 30, 50)
    MODE = (
        (3, 100),
        (10, 100)
    )

    M = len(MODE)
    N = len(SEG)
    bandwidth = 1.2
    delay = 70
    results = np.zeros((N, M))

    # Run experiment
    # Use 'for' statement to change the 'delay' and 'MODE' and to store in 'results'
    """
    ***DO THIS***
    Hint: results[r, i] = experiment(*,*,*,*,file=[*])
    """
    
    # Debugging
    print "Final results"
    print results

    # Save result
    generate_figures("Figure_Segment_Size_Experiment",
                     'Segment size',
                     SEG,
                     'Average response latency for Web search bucketed by segmennt size',
                     results)

# Experiment for measuring performance by changing initial congestion window only
def init_cwnd_experiment():
    MODE = (
        (3, 100),
        (6, 100),
        (10, 100),
        (16, 100),
        (26, 100),
        (46, 100)
    )

    M = len(MODE)
    bandwidth = 1.2
    delay = 70
    results = np.zeros(M)

    # Run experiment
    for i in range(M):
        initcwnd, initrwnd = MODE[i]
        results[i] = experiment(bandwidth,
                                delay,
                                initcwnd,
                                initrwnd)
        print results

    # Debugging
    print "Final results"
    print results

    MODE_x = (3, 6, 10, 16, 26, 46)
    generate_init_figure("Figure_ICWND_Experiment",
                     'Initial Congestion Window Size (Segments)',
                     MODE_x,
                     'Average response latency for Web search only by initial congestion window',
                     results)

def generate_final_figure():
    '''
     ***DO THIS***
     1. Gather all results of each experiment (bandwidth, network_delay, segment_size)
     	Tip: You would need one data structure to gather/save all results
     	Tip: Using dictionary would be useful for gathering
     	Tip: Adding more code to each experiment function would be useful for gathering

     2. Draw box plot for improvement ratio according to each parameter
     	(bandwidth, network_delay, segment_size)
    	Set X-axis as each parameter and set Y-axis as improvement ratio

    Tips:   init_cwnd_experiment() is for showing why other factors have to be controlled and 
            getting the hang of this project. We recommend you to test only this function first.
    '''

if __name__ == "__main__":
    print "CYDF321 Computer Networks Term Project #1"

    # Setup
    if not os.path.exists("results"):
        os.makedirs("results")

    # Experiments to make figures 

    init_cwnd_experiment()
    #segment_size_experiment()
    #bandwidth_experiment()
    #network_delay_experiment()
    #generate_final_figure()
