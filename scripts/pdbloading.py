import subprocess as sp
import pandas as pd
from Bio import PDB
import os
import shlex
import time


# This script is designed for loading files from PDB with 30 seconds delay after each loading
# This delay is according to robots.txt file from PDB, where you can find conventions about working conditions with
# database via programs
# Biopython contains function to load all files from list, yet there is no specified delay between loads and you can be
# banned for loading numerous files without timeouts
#
# Script loads an entries.idx
# Creates pdb_index file - clean file for dataframe
# Creates directory with loaded pdb files
#
# Note: at this script, I`ve loaded files contained RNA in their title
# To change subset of files you should change line with 'mask' variable assignment

# Absolute or relative path for directory to store pdbs
path = input("Enter path to directory to store files: ")
os.makedirs(path, exist_ok=True)

# Initialize loading class
load_struct = PDB.PDBList()


# Parse command to load pdb index file
command = shlex.split('wget ftp://ftp.wwpdb.org/pub/pdb/derived_data/index/entries.idx')
# Run command
sp.check_output(command, universal_newlines=True)

# Delete junk --lines in file, make header tab-separated as main part of file
with open('entries.idx', 'r') as source, open('pdb_index', 'w') as target:
    for ind, line in enumerate(source):
        if ind == 0:
            line = line.replace(', ', '\t')
        if not line.startswith('-'):
            target.write(line)


# Create dataframe from full file with pdb index
with open('pdb_index', 'r') as source:
    data = pd.read_csv(source, sep='\t')

print(data.shape, data.columns)


# Checking data
print(data.isnull().any(), data.shape)

# Drop files with empty header
data.dropna(subset=['HEADER'], inplace=True)
print(data.shape)

# Filter subset of data with RNA in header
mask = data['HEADER'].str.contains('RNA')
rna = data[mask]

# Create list with PDB ids of files with RNA
rna_ids = rna['IDCODE'].unique().tolist()
rna_length = len(rna_ids)
rna_length, rna.head(), rna_ids


with open('rna_ids', 'w') as file:
    for entry in rna_ids:
        file.write('{}\n'.format(entry))


# Load 1 pdb file from RNA list, wait 30 seconds
for ind, file in enumerate(rna_ids, 1):
    load_struct.retrieve_pdb_file(file, file_format='pdb',pdir=path)
    print("{} is loaded, {} from {}".format(file, ind, rna_length))
    time.sleep(30)

