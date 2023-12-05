import json
import netsquid as ns

from basic_components import BasicConnection, BasicNode, BasicProtocol
from netsquid.components import ClassicalChannel
from netsquid.components.models import FibreDelayModel

def get_json_data(path):
    with open(path, "r") as read_file:
        json_data = json.load(read_file)
    return json_data

def get_json_node_by_id(nodes_json, id):
    return next(node for node in nodes_json if node["id"] == id)

def get_ns_node_by_id(ndoes_ns, id):
    return next(node for node in ndoes_ns if node.node_id == id)

def create_nodes(path):
    nodes = []
    json_nodes = get_json_data(path)
    
    for node in json_nodes:
        nodes.append(BasicNode(name=node["name"],
                               node_id=node["id"],
                               city=node["city"]))

    return nodes

def create_connections(path, nodes_json):
    connections = []
    json_connections = get_json_data(path)

    for connection in json_connections:
        node_A = get_json_node_by_id(nodes_json, connection['connection']['node_id_1'])
        node_B = get_json_node_by_id(nodes_json, connection['connection']['node_id_2'])

        delay_model = FibreDelayModel()
        channel_AB = ClassicalChannel(name=f"{node_A['city']} --> {node_B['city']}",
                                   length=connection["length"],
                                   models={"delay_model": delay_model})
        channel_BA = ClassicalChannel(name=f"{node_B['city']} --> {node_A['city']}",
                                   length=connection["length"],
                                   models={"delay_model": delay_model})
        connection = BasicConnection(f"{node_A['city']} <--> {node_B['city']}",
                                     id_A=connection['connection']['node_id_1'],
                                     id_B=connection['connection']['node_id_2'])
        connection.add_subcomponent(channel_AB, forward_input=[("A", "send")], forward_output=[("B", "recv")])
        connection.add_subcomponent(channel_BA, forward_input=[("B", "send")], forward_output=[("A", "recv")])
        connections.append(connection)
        
    return connections

def connect_nodes(nodes, connections):
    for connection in connections:
        node_A = get_ns_node_by_id(nodes, connection.id_A)
        node_B = get_ns_node_by_id(nodes, connection.id_B)
        port_name_A = f"classicalIO-to-{connection.id_B}"
        port_name_B = f"classicalIO-to-{connection.id_A}"
        node_A.add_ports([port_name_A])
        node_B.add_ports([port_name_B])
        node_A.ports[port_name_A].connect(connection.ports['A'])
        node_B.ports[port_name_B].connect(connection.ports['B'])

def main():
    nodes_path = "../data/nodes.json"
    edges_path = "../data/edges.json"
    nodes = create_nodes(nodes_path)
    connections = create_connections(edges_path, get_json_data(nodes_path))
    connect_nodes(nodes, connections)

    basic_protocol = BasicProtocol(nodes[0], initialize=True)
    basic_protocol.start()
    for node in nodes[1::]:
        basic_protocol = BasicProtocol(node)
        basic_protocol.start()

    run_stats = ns.sim_run(duration=300e+9)
    print(run_stats)

if __name__ == "__main__":
    main()