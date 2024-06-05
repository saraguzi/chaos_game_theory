
from matplotlib import pyplot as plt

from pylab import rcParams
rcParams['axes.xmargin'] = 0
rcParams['axes.ymargin'] = 0

from utils import *
from constants import *

#--------------------------------------------------------------------------

class Chaos_Game_Representation:

    def __init__(self, path):
        data = read_fasta_file(path)
            
        self.id = get_id_from_path(path)
        self.header = data[0]
        self.sequence = "".join(filter(lambda x: len(x) != 0 and x[0] != '>', data[1:]))
        self.length = len(self.sequence)
        self.cgr = self.numerical_cgr()

    def numerical_cgr(self):
        cgr = np.zeros((self.length + 1, 2))
        
        initial_point = np.array((0.5, 0.5))
        cgr[0] = initial_point
        
        for i, base in enumerate(self.sequence):
            if base == 'A':
                cgr[i + 1] = SF * (cgr[i] + ADENINE)
            elif base == 'T':
                cgr[i + 1] = SF * (cgr[i] + THYMINE)
            elif base == 'G':
                cgr[i + 1] = SF * (cgr[i] + GUANINE)
            elif base == 'C':
                cgr[i + 1] = SF * (cgr[i] + CYTOSINE)
                
        return np.delete(cgr, 0, axis=0)

    def visual_cgr(self):
        plt.plot(self.cgr[:, 0], self.cgr[:, 1], '.', ms = 1, mec = 'black', mfc = 'black')
        axes = plt.gca()
        axes.set_aspect('equal', adjustable='box')
        axes.get_xaxis().set_visible(False)
        axes.get_yaxis().set_visible(False)
        plt.title(f"Chaos game representation of {self.id}")
        plt.show()

    def __str__(self):
        return "\n".join(map(lambda x: str(x)[1:-1], self.cgr))

    def save(self):
        file_name = f"{self.id}_cgr.txt"
        with open(path.join(OUTPUT_PATH, file_name), 'w') as file:
            file.write(str(self))

class Frequency_Matrix_Representation:

    def __init__(self, representation, k):
        self.id = representation.id
        self.k = k
        self.fcgr = self.numerical_fcgr(representation.cgr, k)

    def numerical_fcgr(self, cgr, k):
        matrix_size = (2 ** k)
        square_size = 1 / matrix_size
        matrix = np.zeros((matrix_size, matrix_size))

        for point in cgr:
            row = int(point[0] / square_size)
            col = int(point[1] / square_size)
            if row == (2 ** k):
                row -= 1
            if col == (2 ** k):
                col -= 1
            matrix[row][col] += 1
            
        return np.rot90(matrix)

    def visual_fcgr(self):
        plt.imshow(self.fcgr, cmap='binary')
        axes = plt.gca()
        axes.set_aspect('equal', adjustable='box')
        axes.get_xaxis().set_visible(False)
        axes.get_yaxis().set_visible(False)
        plt.colorbar()
        plt.title(f"Frequency matrix representation of {self.id}")
        plt.show()
