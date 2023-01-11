#code for optimal
#any any any
#eva = 0.7
#week 1
import osmnx as ox
import pickle
import math
import heapq
from scipy.interpolate import interp1d
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

def deserialize_one(filename):
    dbfile = open('pkfiles/week1Pk100/flushed/' + filename, 'rb')    
    obj = pickle.load(dbfile)
    dbfile.close()
    return obj
obj = deserialize_one("any any any.pk")
gr = obj.graph
node_list = list(gr.nodes())
edge_list = list(gr.edges(keys=True))
adj_dict = {}
weight = {}
m = interp1d([0.0, 1.0], [0.445, 4173.8189999999995])
for u, v, k in edge_list:
  d = 0.5 * m(gr[u][v][k]['risk']) + 0.5 * (gr[u][v][k]['length'])
  print(d)
  #only positive edges are here
  if(d < 0):
    continue
  if(u == v):
    continue
  test_tuple1 = (u, v)
  test_tuple2 = (v, u)
  if test_tuple1 in weight:
    if(d < weight[(u,v)]):
      weight[(u,v)] = d
  else:
    weight[(u,v)] = d
    if u in adj_dict:
      adj_dict[u].append(v)
    else:
      adj_dict[u] = []
      adj_dict[u].append(v)
  if(gr[u][v][k]['oneway'] == False):
    if test_tuple2 in weight:
      if(d < weight[(v,u)]):
        weight[(v,u)] = d
    else:
      weight[(v,u)] = d
      if v in adj_dict:
        adj_dict[v].append(u)
      else:
        adj_dict[v] = []
        adj_dict[v].append(u)
node_set = set()
for first, last in weight:
  node_set.add(first)
  node_set.add(last)
nodes = list(node_set)
for node in nodes:
  if node not in adj_dict:
    adj_dict[node] = []
#djkstra
start_node = 42467300
end_node = 766001495
distance ={}
prev = {}
distance[start_node] = 0.5 * m(gr.nodes[start_node]['risk'])
temp  = []
for node in nodes:
  if node != start_node:
    distance[node] = math.inf
    prev[node] = "undefined"
  temp.append((distance[node], node))
heapq.heapify(temp)
while len(list(temp)) != 0:
  d,n = heapq.heappop(temp)
  for neighbor in adj_dict[n]:
    alt = distance[n] + weight[(n,neighbor)] + 0.5 * gr.nodes[neighbor]['risk']
    if(alt < distance[neighbor]):
      distance[neighbor] = alt
      prev[neighbor] = n
      heapq.heappush(temp,(distance[neighbor], neighbor))
print(distance[end_node])
path = []
currnode = end_node
path.append(currnode)
while currnode != start_node:
  print(currnode)
  currnode = prev[currnode]
  path.append(currnode)
print(currnode)
path.append(currnode)
path.reverse()
lon = []
lat = []
for key in path:
  lat.append(gr.nodes[key]['y'])
  lon.append(gr.nodes[key]['x'])
print(lon)
print(lat)