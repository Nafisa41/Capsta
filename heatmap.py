#for visualizing crime of #adult male night
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import plotly.express as px
import pickle
import osmnx as ox
import math
import random
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
    dbfile = open('pkfiles/amn/correction0.5/' + filename, 'rb')    
    obj = pickle.load(dbfile)
    dbfile.close()
    return obj
def serialize_one(obj, filename):
    dbfile = open('pkfiles/amn/correction/' + filename, 'wb')
    pickle.dump(obj, dbfile)
    dbfile.close()
obj = deserialize_two("adult male night_26cf" + ".pk")
graph_assc = obj.graph
node_list = list(graph_assc.nodes())
edge_list = list(graph_assc.edges(keys = True))
dict_risk = {}
edge_list_chosen = [(7661878383, 7661878384, 0), (588114966, 5487927870, 0), (42437354, 42455396, 0), (42479840, 42476963, 0), (42502482, 42525161, 0), (1942054127, 42497249, 0)]
maxi = -math.inf
temp = []
for u,v,k in edge_list_chosen:
  dict_risk[(u,v,k)] = graph_assc[u][v][k]['risk']
print(dict_risk)