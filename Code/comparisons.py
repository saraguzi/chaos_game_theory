
from os import path
from itertools import combinations

from metrics import *
from datasets import *

#--------------------------------------------------------------------------

class Pairwise_Comparison:

    def __init__(self, matrix_1, matrix_2, metric):
        self.id_1 = matrix_1.id
        self.id_2 = matrix_2.id
        self.distance = metric(matrix_1.fcgr.flatten(), matrix_2.fcgr.flatten())

    def __str__(self):
        return "\t".join((self.id_1, self.id_2, str(self.distance)))

    def __eq__(self, other):
        return self.distance == other.distance
    
    def __lt__(self, other):
        return self.distance < other.distance

class Dataset_Comparison:

    def __init__(self, dataset_fcgr, metric):

        self.number_of_files = len(dataset_fcgr.matrices)
        self.k = dataset_fcgr.matrices[0].k
        self.metric = metric
        self.ids = [matrix.id for matrix in dataset_fcgr.matrices]
        self.comparisons = []

        for i, j in combinations(range(self.number_of_files), 2):
            matrix_1 = dataset_fcgr.matrices[i]
            matrix_2 = dataset_fcgr.matrices[j]
            comparison = Pairwise_Comparison(matrix_1, matrix_2, self.metric)
            self.comparisons.append(comparison)

        self.normalize()

    def normalize(self):
        mx = self.max_distance().distance
        for comparison in self.comparisons:
            comparison.distance /= mx
    
    def min_distance(self):
        return min(self.comparisons)

    def max_distance(self):
        return max(self.comparisons)

    def distance(self, id_1, id_2):
        if (id_1 == id_2):
            return 0
        
        for comparison in self.comparisons:
            if ((comparison.id_1 == id_1 and comparison.id_2 == id_2) or
                (comparison.id_2 == id_1 and comparison.id_1 == id_2)):
                return comparison.distance

        return -1

    def distance_matrix(self):
        distance_matrix = np.zeros((self.number_of_files, self.number_of_files))
        c = 0
        for i, j in combinations(range(self.number_of_files), 2):
            distance_matrix[i][j] = self.comparisons[c].distance
            distance_matrix[j][i] = self.comparisons[c].distance
            c += 1

        return distance_matrix

    def generate_TSV(self):
        file_name = f"{self.metric.__name__}_{self.k}_TSV.txt"
        with open(path.join(OUTPUT_PATH, file_name), 'w') as file:
            for comparison in self.comparisons:
                file.write(str(comparison) + "\n")

    def generate_PDM(self):
        distance_matrix = self.distance_matrix()
        file_name = f"{self.metric.__name__}_{self.k}_PDM.txt"
        with open(path.join(OUTPUT_PATH, file_name), 'w') as file:
            file.write(str(self.number_of_files) + "\n")
            for i in range(self.number_of_files):
                file.write(self.ids[i] + "\t")
                for j in range(self.number_of_files):
                    file.write("%.3f " % distance_matrix[i][j])
                file.write("\n")
