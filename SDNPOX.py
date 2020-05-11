#NET 4005 - Assignment 4
#December 2, 2019
#Ishan Chaurasia - 101011068
#Reece Pillenger - 101013264
from pox.core import core
from pox.openflow import libopenflow_01 as of

class MyController(object):
        def __init__(self):
                core.openflow.addListeners(self)
        def _handle_ConnectionUp(self, event):
                L2Switch(event.connection)

class L2Switch(object):
        def __init__(self, connection):
                print "L2 Switch"
                self.mactable = {}
                self.connection = connection
                connection.addListeners(self)
        def _handle_PacketIn(self, pkt_in_event):
                packet = pkt_in_event.parse()
                print "pkt: src ", packet.src, " dst ", packet.dst, " port ",  pkt_in_event.port
                #L2 Machine Learning Switch Implementation
                if packet.src not in self.mactable: #Adds new MACs to table.
                        self.mactable[packet.src] = pkt_in_event.port
                if str(packet.src) in 'd4:13:1c:1b:76:a0' and str(packet.dst) in 'b8:94:91:62:f1:65': #If packet between H2 - H6 dropped.
                        self.drop(pkt_in_event)
                elif packet.dst in self.mactable: #Anything else sent according to MAC table if successful match.
                        self.forward(pkt_in_event, self.mactable.get(packet.dst))
                else: #If no match in MAC table. Floods packet.
                        self.flood(pkt_in_event)
        #Function to Flood the packet.
        def flood(self, pkt_in_event):
                msg = of.ofp_packet_out()
                msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
                msg.buffer_id = pkt_in_event.ofp.buffer_id
                msg.in_port = pkt_in_event.port
                self.connection.send(msg)
        #Function to Drop the packet.
        def drop(self, pkt_in_event):
                msg = of.ofp_packet_out()
                msg.buffer_id = pkt_in_event.ofp.buffer_id
                msg.in_port = pkt_in_event.port
                self.connection.send(msg)
        #Function to Forward the packet.
        def forward(self, pkt_in_event, to_port):
                packet = pkt_in_event.parse()
                msg = of.ofp_flow_mod()
                msg.match = of.ofp_match.from_packet(packet)
                msg.actions.append(of.ofp_action_output(port = to_port))
                msg.buffer_id = pkt_in_event.ofp.buffer_id
                self.connection.send(msg)
def launch():
        core.registerNew(MyController)
