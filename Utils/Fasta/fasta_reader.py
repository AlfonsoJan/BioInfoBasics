#!/usr/bin/env python3

"""
A module for reading and processing FASTA files containing biological sequences.
"""

from pathlib import Path

class FastaReader:
    """
    A class for reading and processing FASTA files containing biological sequences.

    Args:
        file_path (str or Path): The path to the input FASTA file.

    Attributes:
        file_path (Path): The path to the input FASTA file.
        _sequences (dict): A dictionary storing sequence information.

    Methods:
        if_file_exist: Checks if the input file exists.
        read_file: Reads sequences from the input file.
        check_sequence_type: Determines the type of each sequence.
        sequences: Returns a list of dictionaries containing sequence information.
    """

    def __init__(self, file_path):
        """
        Initialize a FastaReader instance.

        Args:
            file_path (str or Path): The path to the input FASTA file.
        """
        self.file_path = Path(file_path)
        self.if_file_exist()
        self.read_file()

    def if_file_exist(self):
        """
        Checks if the input file exists. Raises FileNotFoundError if not.
        """
        if not self.file_path.is_file():
            raise FileNotFoundError(f'{self.file_path} does not exist')

    def read_file(self):
        """
        Reads sequences from the input file and processes them.
        """
        self._sequences = {}
        with open(self.file_path, "r", encoding="utf-8") as fasta_file:
            header = None
            for line in fasta_file:
                line = line.strip()
                if line.startswith('>'):
                    header = line[1:]
                    self._sequences[header] = {"sequence": "", "type": ""}
                else:
                    self._sequences[header]['sequence'] += line.upper()
        self.check_sequence_type()

    def check_sequence_type(self):
        """
        Determines the type of each sequence (DNA, RNA, or PROTEIN).
        """
        for info in self._sequences.values():
            seq_type = "UNK"
            if all(_ in 'ACGT' for _ in info["sequence"]):
                seq_type = "DNA"
            elif all(_ in 'ACGU' for _ in info["sequence"]):
                seq_type = "RNA"
            elif all(_ in 'ACDEFGHIKLMNPQRSTVWY' for _ in info["sequence"]):
                seq_type = "PROTEIN"
            info["type"] = seq_type

    def sequences(self):
        """
        Returns a list of dictionaries containing sequence information.

        Returns:
            list: A list of dictionaries with keys "header", "sequence", and "type".
        """
        return [
            {
                "header": header,
                "sequence": info["sequence"],
                "type": info["type"]
            }
            for header, info in self._sequences.items()
        ]

    def __repr__(self) -> str:
        """
        Returns a string representation of the FastaReader instance.
        """
        return f"{self.__class__}({self.__dict__})"

    def __str__(self):
        """
        Returns a human-readable summary of the FastaReader instance.
        """
        return f"FastaReader(file_path={self.file_path}, num_sequences={len(self.sequences)})"
