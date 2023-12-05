import netsquid as ns
import random

from netsquid.components.component import Port
from netsquid.nodes import Connection, Node
from netsquid.protocols import NodeProtocol


class BasicConnection(Connection):

    def __init__(self, name, id_A, id_B):
        super().__init__(name)
        self.id_A = id_A
        self.id_B = id_B

class BasicNode(Node):

    def __init__(self, name, node_id, city, ID=None, qmemory=None, port_names=None):
        super().__init__(name, ID, qmemory, port_names)
        self.node_id = node_id
        self.city = city

    def get_ports_names(self):
        port_names = [name for name in self.ports.filter_by_type(Port)]
        return port_names

class BasicProtocol(NodeProtocol):

    def __init__(self, node, initialize=False):
        super().__init__(node)
        self.initialize = initialize

    def run(self):

        ports = self.node.get_ports_names()

        if self.initialize:
            random_port = random.choice(ports)
            # Send Hello message
            self.node.ports[random_port].tx_output(f"Hello from {self.node.city}!")

        while True:
            input_event_expr = self.await_port_input(self.node.ports[ports[0]])
            for port in ports[1::]:
                input_event_expr = input_event_expr | self.await_port_input(self.node.ports[port])
            # Wait for a message
            yield input_event_expr
            # Recieve a message from appropriate port
            for port in ports:
                message_raw = self.node.ports[port].rx_input()
                if message_raw is not None:
                    break

            message = message_raw.items[0]
            yield self.await_timer(duration=10e+9)
            print(f"{ns.sim_time():5.1f}: {self.node.city} obtained a message: {message}")
            random_port = random.choice(ports)
            # Send Hello message
            self.node.ports[random_port].tx_output(f"Hello from {self.node.city}!")