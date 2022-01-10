from src import make_data
from pathlib import Path
import pandas as pnd

# Folder to store all the data
DATA_FOLDER = Path("/opt/tiger/data/alphafold")
make_data.extract_data(DATA_FOLDER, DATA_FOLDER)

uniprot_folder = DATA_FOLDER / "uniprot_files"
if not uniprot_folder.exists():
    uniprot_folder.mkdir()
make_data.get_uniprot_info(DATA_FOLDER, uniprot_folder)

avg_scores, lengths_high_confidence, lengths_full = make_data.get_AF_protein_information(DATA_FOLDER)

# uniprot_folder = DATA_FOLDER / "uniprot_go"

AF_dataframe = pnd.concat([pnd.read_csv(filename, sep="\t") for filename in uniprot_folder.glob("UP*_uniprot.txt")])
AF_dataframe["Protein family"] = [str(val).split(",")[0] for val in AF_dataframe["Protein families"]] # Superfamily
AF_dataframe["Organism"] = [" ".join(str(val).split(" (")[0].split(" ")[:2]) for val in AF_dataframe["Organism"]]
AF_dataframe["ID"] = [f"AF-{k}-F1-model_v1.pdb" for k in AF_dataframe["Entry"]]
AF_dataframe["Avg. score"] = [avg_scores[key] if key in avg_scores else 40 for key in AF_dataframe["ID"]]
AF_dataframe["Length"] = [lengths_full[key] if key in lengths_full else 0 for key in AF_dataframe["ID"]]
AF_dataframe["High confidence length"] = [lengths_high_confidence[key] if key in lengths_high_confidence else 0 for key in AF_dataframe["ID"]]

AF_dataframe = AF_dataframe[[c for c in AF_dataframe.columns if not c.startswith("yourlist")]]
AF_dataframe.to_csv(DATA_FOLDER / "AF_dataframe.txt", sep="\t")
AF_dataframe = AF_dataframe.set_index("ID")