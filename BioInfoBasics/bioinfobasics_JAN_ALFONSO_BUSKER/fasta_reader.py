from pathlib import Path
from collections import namedtuple

class FastaReader:
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.if_file_exist()
        self.sequences = {}
    
    def if_file_exist(self):
        if not self.file_path.is_file():
            raise FileNotFoundError(f'{self.file_path} does not exist')
    
    def read_sequences(self):
        SeqInfo = namedtuple("SeqInfo", "sequence type")

        self.sequences = {}
        with open(self.file_path, 'r') as fasta_file:
            header = None
            for line in fasta_file:
                line = line.strip()
                if line.startswith('>'):
                    header = line[1:]
                    self.sequences[header] = SeqInfo("", "")
                else:
                    self.sequences[header] = self.sequences[header]._replace(sequence=self.sequences[header].sequence + line.upper())
        self.check_sequence_type()

    def check_sequence_type(self):
        for header in self.sequences.keys():
            seq_type = "UNK"
            if all(base in 'ACGT' for base in self.sequences[header].sequence):
                seq_type = "DNA"
            elif all(base in 'ACGU' for base in self.sequences[header].sequence):
                seq_type = "RNA"
            elif all(base in 'ACDEFGHIKLMNPQRSTVWY' for base in self.sequences[header].sequence):
                seq_type = "PROTEIN"
            self.sequences[header] = self.sequences[header]._replace(type=seq_type)

f = FastaReader("D:\Desktop\multi_dna.fasta")
f.read_sequences()

# Seq = namedtuple("Seq", "sequence type")

# sequences = {}
# with open("D:\Desktop\multi_dna.fasta", 'r') as fasta_file:
#     header = None
#     for line in fasta_file:
#         line = line.strip()
#         if line.startswith('>'):
#             header = line[1:]
#             sequences[header] = Seq("", "")
#         else:
#             sequences[header] = sequences[header]._replace(sequence=sequences[header].sequence + line.upper())