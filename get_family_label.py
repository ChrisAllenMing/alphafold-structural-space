import os, sys
import pickle as pkl
import pandas as pnd
from pathlib import Path
from collections import defaultdict, Counter
import numpy as np
import pdb

# Read the AF dataframe
DATA_FOLDER = Path("/opt/tiger/data/alphafold")
AF_dataframe = pnd.read_csv(DATA_FOLDER / "AF_dataframe.txt", sep="\t")
AF_dataframe = AF_dataframe.set_index("ID")
most_common = list(x[0] for x in Counter(AF_dataframe["Protein family"]).most_common(21)[1:])

# Get protein family label
filename_dir = Path("/opt/tiger/data/af_split_filenames")
output_dir = Path("/opt/tiger/data/af_family_labels")
if not os.path.exists(output_dir):
    os.mkdir(output_dir)
for name in os.listdir(filename_dir):
    if name.endswith(".pkl"):
        file_path = filename_dir / name
        pkl_file = open(file_path, "rb")
        filenames = pkl.load(pkl_file)

        family_labels = []
        for filename in filenames:
            try:
                family = AF_dataframe.loc[filename]["Protein family"]
                try:
                    family_label = most_common.index(family) if family in most_common else -1
                except:
                    family = family.iloc[0]
                    family_label = most_common.index(family) if family in most_common else -1
            except:
                family_label = -1
            family_labels.append(family_label)
        family_labels = np.array(family_labels)
        output_name = name.split(".")[0] + ".npy"
        output_name = output_dir / output_name
        np.save(output_name, family_labels)
        print("Save to: ", output_name)
