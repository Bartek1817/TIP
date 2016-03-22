from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel
from mininet.link import TCLink
from mininet.node import RemoteController


import random
import sys 

class CustomTopo(Topo):
	"Simple Data Center Topology"
	"linkopts - (1:core, 2:aggregation, 3: edge) parameters"
	"fanout - number of child switch per parent switch"
	def __init__(self, linkopts1, linkopts2, linkopts3, fanout=2, **opts):
        # Initialize topology and default options
		Topo.__init__(self, **opts)
        # Add your logic here ...
		core = self.addSwitch('c0')
		for i in range(1, fanout+1):
			switchA = self.addSwitch('a%s' % i)
			self.addLink(core, switchA, **linkopts1)
			for j in range(1, fanout+1):
				switchE = self.addSwitch('e%s' % ((i-1)*fanout+j))
				self.addLink(switchA, switchE, **linkopts2)
				for k in range(1, fanout+1):
					host = self.addHost('h%s' % ((((i-1)*fanout+j)-1)*fanout+k))
					self.addLink(switchE, host, **linkopts3)


                    
topos = { 'custom': ( lambda: CustomTopo() ) }


def simpleTest():
   #Create and test a simple network
   #Set up link parameters
	print "a. Setting link parameters"
    #--- core to aggregation switches
	linkopts1 = {'bw':50, 'delay':'5ms'}
    #--- aggregation to edge switches
	linkopts2 = {'bw':30, 'delay':'10ms'}
    #--- edge switches to hosts
	linkopts3 = {'bw':10, 'delay':'15ms'}
  
    #Creating network and run simple performance test
	print "b. Creating Custom Topology"
	topo = CustomTopo(linkopts1, linkopts2, linkopts3, fanout=2)

	controller = RemoteController(name='c0', port=6633) 
	print "c. Firing up Mininet"
	net = Mininet(topo=topo, link=TCLink, controller=controller)
	net.start()
    
	print "Dumping host connections"
	dumpNodeConnections(net.hosts)
	print "Testing network connectivity"

  
    # enter command line for the mininet
	print "d. Command line"
	CLI(net)

	print "e. Stopping Mininet"
	net.stop()
    

if __name__ == '__main__':
   # Tell mininet to print useful information
   setLogLevel('info')
   simpleTest()
