from cvxpower import *
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
# import graphviz
# import agraph


def optimize_static_network(json_body):
    g = nx.DiGraph()
    
    devices = []
    
    for load in json_body["loads"]:
      load_obj = FixedLoad(power=load["power"], name=load["name"])
      g.add_node(load["name"], cvxp_obj = load_obj) 
      devices.append(load_obj) 
    
    for gen in json_body["generators"]:
      gen_obj = Generator(power_max=gen["power_max"], alpha=gen["alpha"],
                          beta=gen["beta"], name=gen["name"])
      g.add_node(gen_obj.name, cvxp_obj = gen_obj)
      devices.append(gen_obj) 
    
    for line in json_body["lines"]:
      line_obj = TransmissionLine(power_max=line["power_max"], name=line["name"])
      g.add_node(line_obj.name, cvxp_obj = line_obj)
      devices.append(line_obj)
    
    nets = []
    for net in json_body["nets"]:
      net_terminals = [nx.get_node_attributes(g, "cvxp_obj")[terminal["device"]]
                       .terminals[terminal["terminal"]] 
                       for terminal in net["terminals"]]
      net_obj = Net(net_terminals, name=net["name"])
      g.add_node(net_obj.name, cvxp_obj=net_obj)
      for terminal in net["terminals"]:
        g.add_edge(net["name"], terminal["device"])
    
      nets.append(net_obj)
      
    g_nodes = g.nodes()
    color_map = []
    for n in g:
      if type(g_nodes[n]['cvxp_obj']) == FixedLoad:
        color_map.append('lightgray')
      elif type(g_nodes[n]['cvxp_obj']) == Generator:
        color_map.append('lightgray')
      elif type(g_nodes[n]['cvxp_obj']) == TransmissionLine:
        color_map.append('lightgray')
      elif type(g_nodes[n]['cvxp_obj']) == Net: 
        color_map.append('gray')
    
    
    network = Group(devices, 
                    nets)
    
    network.init_problem()
    network.optimize(solver="ECOS")
    return network.results.summary()
    
    
json_body = {
    "loads": [{"name":"load1", "power": 50}, {"name": "load2", "power": 100}],
    "generators": [{"name": "gen1", "power_max":1000, "alpha": 0.02, "beta": 30},
                   {"name": "gen2", "power_max": 100, "alpha": 0.2, "beta": 0}],
    "lines": [{"name": "line1", "power_max": 50}, {"name": "line2", "power_max": 10},
              {"name": "line3", "power_max": 50}],
    "nets": [{"name": "net1", 
              "terminals": [{"device": "load1", "terminal": 0}, 
                            {"device": "gen1", "terminal": 0},
                            {"device": "line1", "terminal": 0},
                            {"device": "line2", "terminal": 0}]},
             {"name": "net2",
              "terminals": [{"device": "load2", "terminal": 0},
                            {"device": "line1", "terminal": 1},
                            {"device": "line3", "terminal": 0}]},
             {"name": "net3",
              "terminals": [{"device": "gen2", "terminal": 0},
                            {"device": "line2", "terminal": 1},
                            {"device": "line3", "terminal": 1}]}]
}
def application():
    result = optimize_static_network(json_body)
    print(result)

if __name__ == '__main__':
    application()