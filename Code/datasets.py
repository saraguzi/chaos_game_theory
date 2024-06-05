
from os import scandir

from representations import *

#--------------------------------------------------------------------------

class Dataset_CGR:

    def __init__(self, path):

        self.representations = []

        for filename in scandir(path):
            if filename.is_file():
                representation = Chaos_Game_Representation(filename.path)
                self.representations.append(representation)

class Dataset_FCGR:

    def __init__(self, dataset_cgr, k):

        self.matrices = []
        
        for representation in dataset_cgr.representations:
            matrix = Frequency_Matrix_Representation(representation, k)
            self.matrices.append(matrix)
