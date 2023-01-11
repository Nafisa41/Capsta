import osmnx as ox
import matplotlib.pyplot as plt
import pickle 
import math 
import networkx as nx
import sys
import copy
import pandas as pd
import os

#this section removes the nodes that are completely disconnected
#list of the nodes to be removed
def remove_isolated_nodes(G):
  nodes_to_be_removed = []
  for node in G.nodes:
    if(G.out_degree(node) == 0 and G.in_degree(node) == 0):
      nodes_to_be_removed.append(node)
  G.remove_nodes_from(nodes_to_be_removed)
  return G

#modifying the graph and adding prev_mean, crime_count, risk
def add_attributes(G):
  #for nodes
  for key in G.nodes().keys():
    G.nodes[key]['prev_mean'] = 0.0
    G.nodes[key]['crime_count'] = 0
    G.nodes[key]['risk'] = 0.0
    G.nodes[key]['tempD'] = []
  #for edges
  for u,v,d in G.edges(data=True):
    d['prev_mean'] = 0.0
    d['crime_count'] = 0
    d['risk'] = 0.0
    d['tempD'] = []
  return G

#initializing networkgraph class(for every feature combination there is a graph)
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

#getting the keys for the networkgraph objects
def get_tree_leaf_list():
  leaf_list = []
  for i in age_values:
    for j in gender_values:
      for k in time_of_the_day_values:
        leaf_list.append(i + " " + j + " " + k)
        print(i + " " + j + " " + k)
  return leaf_list

#data structure initialization
def init_ds():
    leaf_list = get_tree_leaf_list()
    print(len(leaf_list))
    count = 0
    for key in leaf_list:    
        newG = deserialize_one('graph.pk')
        obj_initial = Networkgraph(newG, 0.0)
        serialize_one(obj_initial, key + ".pk")
        count = count + 1
        print(count)
        # ds[key] = obj_initial

def gen_all_branch(input_features_str):
    output = []
    for i in range(8):
        str = ""
        if (i & 1) > 0:
            str += "any "
        else:
            str += input_features_str[0] + " "
        
        if (i & 2) > 0:
            str += "any "
        else:
            str += input_features_str[1] + " "

        if (i & 4) > 0:
            str += "any"
        else:
            str += input_features_str[2]
        output.append(str)
    return output

def report_crime(filename, input_features_str, severity):
  square_graph = deserialize_latlng(filename)
  if(square_graph == "not found"):
    print("not found")
    return
  node_list = list(square_graph.nodes())
  edge_list = list(square_graph.edges(keys=True))
  input_features_str_list = input_features_str.split()
  output_list = gen_all_branch(input_features_str_list)
  #for adult male night
  output_list = ["adult male night"]
  #for adult male night
  for key in output_list:
    obj = deserialize_one(key + ".pk")
    graph_assc = obj.graph
    for keyvalue in node_list:
      try:
        lst_tempD = graph_assc.nodes[keyvalue]['tempD']
        lst_tempD.append(severity)
      except:
        continue
    for u, v, k in edge_list:
      try:
        graph_assc[u][v][k]['tempD'].append(severity)
      except:
        continue
    # obj_updated = Networkgraph(graph_assc, 0.0)
    obj.update_global_best(severity)
    obj.update_global_worst(severity)
    serialize_one(obj, key + ".pk")

def report_call(csv_file):
  df = pd.read_csv(csv_file)
  week_cnt = 26
  row_number = len(df.index)
  for i in range(0, row_number):
    week_number_current_row = df.iloc[i]['week_number']
    if(week_cnt == week_number_current_row):
      input_features_str = df.iloc[i]['age'] + " " + df.iloc[i]['gender'] + " " + df.iloc[i]['time_of_the_day']
      if(input_features_str == 'adult male night'):
        report_crime("row" + str(i), input_features_str, df.iloc[i]['severity'])
        print(i)
    elif(week_number_current_row > week_cnt):
      break

def step_update():
  file_name_list = get_tree_leaf_list()
  #for adult male night
  file_name_list = ["adult male night"]
  #for adult male night
  for file_name in file_name_list:
    obj = deserialize_one(file_name + ".pk")
    graph_assc = obj.graph
    node_list = list(graph_assc.nodes())
    edge_list = list(graph_assc.edges(keys=True))
    for keyvalue in node_list:
      try:
        lst_tempD = graph_assc.nodes[keyvalue]['tempD']
        sum_tempD = sum(lst_tempD)
        if(graph_assc.nodes[keyvalue]['prev_mean'] == 0.0 and len(lst_tempD) == 0.0):
          continue
        favg = (graph_assc.nodes[keyvalue]['prev_mean'] * 0.7 * graph_assc.nodes[keyvalue]['crime_count'] + sum_tempD) / (graph_assc.nodes[keyvalue]['crime_count'] + len(lst_tempD))
        # if(file_name == 'teen male morning' and keyvalue == 267089071):
        #   print(favg)
        risk_value = abs(favg - obj.global_best) / (abs(favg - obj.global_worst) + abs(favg - obj.global_best))
        graph_assc.nodes[keyvalue]['risk'] = risk_value
        graph_assc.nodes[keyvalue]['prev_mean'] = favg
        graph_assc.nodes[keyvalue]['crime_count'] = graph_assc.nodes[keyvalue]['crime_count'] + len(lst_tempD)
        #flush
        graph_assc.nodes[keyvalue]['tempD'].clear()
      except:
        continue
    for u, v, k in edge_list:
      try:
        lst_tempD = graph_assc[u][v][k]['tempD']
        sum_tempD = sum(lst_tempD)
        if(graph_assc.nodes[keyvalue]['prev_mean'] == 0.0 and len(lst_tempD) == 0.0):
          continue
        favg = (graph_assc[u][v][k]['prev_mean'] * 0.7 * graph_assc[u][v][k]['crime_count'] + sum_tempD) / (graph_assc[u][v][k]['crime_count'] + len(lst_tempD))
        risk_value = abs(favg - obj.global_best) / (abs(favg - obj.global_worst) + abs(favg - obj.global_best))
        graph_assc[u][v][k]['risk'] = risk_value
        graph_assc[u][v][k]['prev_mean'] = favg
        graph_assc[u][v][k]['crime_count'] = graph_assc[u][v][k]['crime_count'] + len(lst_tempD)
        #flush
        graph_assc[u][v][k]['tempD'].clear()
      except:
        continue
    serialize_one(obj, file_name + ".pk")
  
def serialize_one(obj, filename):
    dbfile = open('pkfiles/amn/' + filename, 'wb')
    pickle.dump(obj, dbfile)
    dbfile.close()

def deserialize_one(filename):
    dbfile = open('pkfiles/amn/' + filename, 'rb')    
    obj = pickle.load(dbfile)
    dbfile.close()
    return obj

def deserialize_latlng(filename):
  path = "/mnt/d/ResearchGit/latlng/" + filename
  isExist = os.path.exists(path)
  if(isExist == True):
    dbfile = open('latlng/' + filename, 'rb')  
    obj = pickle.load(dbfile)
    dbfile.close()
    return obj
  else:
    return "not found"

def get_graph(city_name):
  G = ox.graph.graph_from_place(city_name, network_type='drive', retain_all = True)
  # ox.plot_graph(G)
  G = remove_isolated_nodes(G)
  ox.plot_graph(G)
  G = add_attributes(G)
  serialize_one(G, 'graph.pk')

# get_graph('New York, United States')
#-------------------------------------------------------
#data structure initialization
features = ['age', 'gender', 'time_of_the_day']
age_values = ['teen', 'young_adult', 'adult', 'middle_age','old', 'any']
gender_values = ['male', 'female', 'diverse', 'enby', 'any']
time_of_the_day_values = ['morning', 'afternoon', 'evening', 'night', 'any']
feature_val_dict = {}
feature_val_dict['age'] = age_values
feature_val_dict['gender'] = gender_values
feature_val_dict['time_of_the_day'] = time_of_the_day_values
#init_ds()
report_call('dataset/finaldata.csv')
#step_update()
#--------------------------------------------------------
#testing 
# input_features_str = 'teen male morning'
# severity = 2
# lat = 40.594909125
# lng = -73.955384213
# tempList = report_crime(lat, lng, input_features_str,severity)
# step_update()
# obj = deserialize_one(input_features_str+".pk")
# graph_assc = obj.graph
# for u, v, k in tempList:
#     print(graph_assc[u][v][k]['tempD'])
# print("global best" + str(obj.global_best) + " " + "global worst" + str(obj.global_worst))
# print(graph_assc[267089071][642632761][0]['prev_mean'])
# print(graph_assc[267089071][642632761][0]['risk'])
# print("--------------------")
# obj = deserialize_one('any any any'+".pk")
# graph_assc = obj.graph
# for u, v, k in tempList:
#     print(graph_assc[u][v][k]['tempD'])
# print("global best" + str(obj.global_best) + " " + "global worst" + str(obj.global_worst))
# print('--------------------')
# obj = deserialize_one('teen female morning'+".pk")
# graph_assc = obj.graph
# for u, v, k in tempList:
#     print(graph_assc[u][v][k]['tempD'])
# print("global best" + str(obj.global_best) + " " + "global worst" + str(obj.global_worst))
# print("--------------------")
# print(graph_assc[267089071][642632761][0]['tempD'])
#checking if the actual graph stayed non updated
# global_graph = deserialize_one("graph.pk")
# edge_list = list(global_graph.edges(data=True))
# node_list = list(global_graph.nodes(data=True))
# for i in range(0, 10):
#   print(edge_list[i])