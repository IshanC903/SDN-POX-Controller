
from mininet.topo import Topo
class SDNTOP(Topo):
        def __init__(self):
                Topo.__init__(self)

                s1 = self.addSwitch('s1')
                s2 = self.addSwitch('s2')
                s3 = self.addSwitch('s3')
                s4 = self.addSwitch('s4')
                s5 = self.addSwitch('s5')
                s6 = self.addSwitch('s6')
                s7 = self.addSwitch('s7')

                self.addLink(s1,s2)
                self.addLink(s1,s3)
                self.addLink(s2,s4)
                self.addLink(s2,s5)
                self.addLink(s3,s6)
                self.addLink(s3,s6)

topos = {'SDNTOP':(lambda: SDNTOP())}