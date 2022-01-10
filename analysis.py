import pickle
import pandas as pnd
from pathlib import Path
from collections import defaultdict, Counter
import numpy as np
import pdb

DATA_FOLDER = Path("/opt/tiger/data/alphafold")
AF_dataframe = pnd.read_csv(DATA_FOLDER / "AF_dataframe.txt", sep="\t")
AF_dataframe = AF_dataframe.set_index("ID")
most_common = set(x[0] for x in Counter(AF_dataframe["Protein family"]).most_common(21)[1:])
pdb.set_trace()