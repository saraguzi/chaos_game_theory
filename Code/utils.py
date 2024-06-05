
from pathlib import Path

#--------------------------------------------------------------------------

def get_id_from_path(path):
    return Path(path).name.split('.')[0]

def read_fasta_file(path):
    if path.lower().endswith('.fasta'):
    
        with open(path, 'r') as file:
            return file.read().split("\n")

    raise ValueError('Wrong file format, extension must be .fasta')
