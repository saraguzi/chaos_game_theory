
from scipy.spatial import distance

#--------------------------------------------------------------------------

def euclidean_distance(u, v):
    return distance.euclidean(u, v)

def manhattan_distance(u, v):
    return distance.cityblock(u, v)

def canberra_distance(u, v):
    return distance.canberra(u, v)

def cosine_distance(u, v):
    return distance.cosine(u, v)

def jensen_shannon_distance(u, v):
    return distance.jensenshannon(u, v)
