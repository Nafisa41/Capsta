#code to get the risk values in a dictionary of "adult male night"
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import plotly.express as px
import pickle
import osmnx as ox
import math
import random
from collections import defaultdict
#-73.9004256
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

# def deserialize_one(filename):
#     dbfile = open('pkfiles/amn/' + filename, 'rb')    
#     obj = pickle.load(dbfile)
#     dbfile.close()
#     return obj
def deserialize_two(filename):
    dbfile = open('pkfiles/amn/correction/' + filename, 'rb')    
    obj = pickle.load(dbfile)
    dbfile.close()
    return obj
def serialize_one(obj, filename):
    dbfile = open('pkfiles/amn/correction/' + filename, 'wb')
    pickle.dump(obj, dbfile)
    dbfile.close()
dict_risk = {}
dict_crime = {42468222: 17.5, 561035378: 17.0, 1942053876: 20.0, 42435516: 11.0, 42745764: 21.0, 1942053941: 21.0}
file_name = "adult male night_26cf.pk"
obj = deserialize_two(file_name)
graph_assc = obj.graph
node_list = list(graph_assc.nodes())
for key in node_list:
  if key in dict_crime:
    dict_risk[key] = graph_assc.nodes[key]['risk']
print(dict_risk)
  

