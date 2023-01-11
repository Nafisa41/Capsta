#for visualizing crime of #adult male night
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import plotly.express as px
import pickle
import osmnx as ox
import math
import random
from collections import defaultdict
class Networkgraph:
  def __init__(self, graph, evaporation_rate):
        self.global_best = 0.0
        self.global_worst = -math.inf
        self.graph = graph
        self.evaporation_rate = evaporation_rate
  def update_global_best(self, new_severity_value):
    if self.global_best > new_severity_value:
      self.global_best = new_severity_value
  def update_global_worst(self, new_severity_value):
    if self.global_worst < new_severity_value:
      self.global_worst = new_severity_value

def deserialize_two(filename):
    dbfile = open('pkfiles/amn/' + filename, 'rb')    
    obj = pickle.load(dbfile)
    dbfile.close()
    return obj
obj = deserialize_two("adult male night_26" + ".pk")
graph_assc = obj.graph
node_list = list(graph_assc.nodes())
edge_list = list(graph_assc.edges(keys = True))
randomness = []
chosen = []
for key in node_list:
    if(len(graph_assc.nodes[key]['tempD']) >= 3):
      randomness.append(key)
chosen = random.sample(randomness, 6)
#visualizing with the chosen node
maxi = 0
maxi_key = ""
number = 1
value_avg = defaultdict(list)
value_risk = defaultdict(list)
for key in node_list:
    nonzero = 0
    for number in range(1, 27):
        print(number)
        file_name_normal = "adult male night_" + str(number)
        file_name_flush = "adult male night_" + str(number) + "f"
        obj = deserialize_two(file_name_normal + ".pk")
        graph_assc = obj.graph
        if(len(graph_assc.nodes[key]['tempD']) != 0):
            nonzero = nonzero + 1
            value_avg[key].append(sum(graph_assc.nodes[key]['tempD'])/len(graph_assc.nodes[key]['tempD']))
        else:
            value_avg[key].append(0.0)
        obj = deserialize_two(file_name_flush + ".pk")
        graph_assc = obj.graph
        value_risk[key].append(graph_assc.nodes[key]['risk'])
        number = number + 1
        if(nonzero > maxi):
          print("nonzero" + str(nonzero))
          print("key" + str(key))
          maxi = nonzero
          maxi_key = key

print(value_risk['key'])   

# print(value_avg)
# print(value_risk)

      