from socket import socket, AF_INET, SOCK_DGRAM
from packet import *
from threading import Thread
import heapq
import sys

class udprouter():

        # All routers will know each other's routing tables
    
        def __init__(self, id, port):
                self.port = port
                self.id = id
                self.rt = { 'routes': [{'id': 101, 'ip': '192.168.1.1', 'gateway': '192.168.1.2', 'port':8880},
                {'id': 202, 'ip': '10.0.1.1', 'gateway': '10.0.1.0', 'port':8882}] }

        # Will Use the Destination received from the packet to find the appropriate destination address
        
        def search_dst_addr(self, dst):
                for x in range(len(self.rt['routes'])):
                        if self.rt['routes'][x]['id'] == dst:
                                return (self.rt['routes'][x]['ip'], self.rt['routes'][x]['port'])
                return ('10.0.1.1', 8882)

              
        #  Will send packet to the destination address     
              

        def handle_sending(self, packet, server):
                s = socket(AF_INET, SOCK_DGRAM)
                s.sendto(packet, server)
                print('Sending To: ', server)
                s.close()
                return 0
              
  # Dijkstra's algorithm is used to calculate the shortest path
  
  
                heap = [(0, self.id)]
                distances = {}
                while heap:
                    (dist, current_route) = heapq.heappop(heap)
                    if current_route in distances:
                        continue
                    distances[current_route] = dist
for neighbor in graph[current_route]:
                    if neighbor not in distances:
                        heapq.heappush(heap, (dist + graph[current_route][neighbor], neighbor))
   
  # Implementing Look Ahead to Improve BLCP
    
    def get_common_path(routing_table, source, destination):
   
  
    path = []
    current_node = source
    while current_node != destination:
        next_hop = routing_table[current_node][destination]
        if next_hop is None:
            # No path exists
            return None
        if next_hop != destination:
            # Look Ahead
            next_next_hop = routing_table[next_hop][destination]
            if next_next_hop is not None:
                # Check if there is a better path through next_hop
                current_to_next_hop = routing_table[current_node][next_hop]
                next_hop_to_dest = routing_table[next_hop][destination]
                current_to_next_next_hop = routing_table[current_node][next_next_hop]
                next_next_hop_to_dest = routing_table[next_next_hop][destination]
                if current_to_next_hop + next_hop_to_dest > current_to_next_next_hop + next_next_hop_to_dest:
                    next_hop = next_next_hop
        path.append(next_hop)
        current_node = next_hop
    return path
              
              
        # Implementation of BLCP
        
        def base_line_common_path(self):
                # Set up the graph
                graph = {}
                for route in self.rt['routes']:
                    graph[route['id']] = {}
                    for next_route in self.rt['routes']:
                        if next_route != route:
                            graph[route['id']][next_route['id']] = sys.maxsize

                # Link Cost Update
                
                for route in self.rt['routes']:
                    if route['id'] == self.id:
                        continue

                    server = (route['ip'], route['port'])
                    s = socket(AF_INET, SOCK_DGRAM)
                    s.sendto(b'get link cost', server)
                    response, addr = s.recvfrom(1024)
                    s.close()
                    cost = int(response.decode('utf-8'))
                    graph[self.id][route['id']] = cost

                # Routing Table(rt) Update
                
                self.rt['routes'][route['id']] = {
                    'id': route['id'],
                    'ip': route['ip'],
                    'gateway': self.rt['routes'][path[-2]]['ip'],
                    'port': self.rt['routes'][path[-2]]['port']
                }

    # listens for packets
    
    def listen_for_packets(self):
            s = socket(AF_INET, SOCK_DGRAM)
            s.bind(('0.0.0.0', self.port))
            while True:
                    packet, addr = s.recvfrom(1024)
                    t = Thread(target=self.handle_packet, args=(packet,))
                    t.start()

    # handles incoming packets
    def handle_packet(self, packet):
            # Parse the packet
            p = Packet()
            p.decode(packet)

            # Is the packet meant for this router?
            
            if p.dst == self.id:
                    print('Received Packet: ', packet)
                    return

            # Finds the next Hop for the packet
            
            dst_addr = self.search_dst_addr(p.dst)

            # Drops packet if the TTL is 0, decrements value
            
            p.ttl -= 1
            if p.ttl == 0:
                    print('Dropping Packet: ', packet)
                    return

            # Updates the packet to send to the next hop
            
            packet = p.encode()
            self.handle_sending(packet, dst_addr)
