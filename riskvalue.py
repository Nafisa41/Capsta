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
    dbfile = open('pkfiles/amn/correction0.5/' + filename, 'rb')    
    obj = pickle.load(dbfile)
    dbfile.close()
    return obj
def deserialize_one(filename):
    dbfile = open('pkfiles/amn/' + filename, 'rb')

    obj = pickle.load(dbfile)
    dbfile.close()
    return obj
def serialize_one(obj, filename):
    dbfile = open('pkfiles/amn/correction0.5/' + filename, 'wb')
    pickle.dump(obj, dbfile)
    dbfile.close()
weekly_risk = {}
for i in range(1, 27):
    print(i)
    file_name1 = "adult male night_" + str(i) + ".pk"
    file_name2 = "adult male night_" + str(i) + "cf.pk"
    obj = deserialize_one(file_name1)
    obj_up = deserialize_two(file_name2)
    gr = obj.graph
    node_list = list(gr.nodes()) 
    edge_list = list(gr.edges(keys=True))
    total = len(node_list) + len(edge_list)
    risk1 = 0
    risk2 = 0
    for key in node_list:
        risk1 = risk1 + gr.nodes[key]['risk']
    for u, v, k in edge_list:
        risk1 = risk1 + gr[u][v][k]['risk']
    gr = obj_up.graph
    node_list = list(gr.nodes()) 
    edge_list = list(gr.edges(keys=True))
    for key in node_list:
        risk2 = risk2 + gr.nodes[key]['risk']
    for u, v, k in edge_list:
        risk2 = risk2 + gr[u][v][k]['risk']
    weekly_risk[i] = (risk1 - risk2)/total
    
print(weekly_risk)   
        
        

    

  

