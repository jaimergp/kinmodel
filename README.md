# 1. Conformers generation and ligand alignment (`01_modeling_script.py`)

1. The maximum number of conformers will be generated for a given SMILES using OMEGA. The output will be a single SDF file with the maximum number of conformers.
2. The single SDF file will be used for the alignment of a query (Molecule of interest) and database (in-house active kinase ligand template library) molecules using ROCS. The output will be each template aligned query molecule.
3. Combining the report files of each template aligned query molecule into a single report file.
4. Based on the single report file, the top 100 conformers for the given SMILES are selected.
5. SDF to PARAMS will be generated using 100 conformers for Rosetta Minimization step.

# 2. Sequence alignment and protein modeling (`02_new_protein_modeling.py`)

1. Target-template sequence alignment will be performed using in-house active kinase sequence template library (EMBOSS Needleman-Wunsch algorithm)
2. Selection of top hit templates will be applied using sequence and ligand similarity approach (defined as Template Score). Based on this approach, the top 10 templates for the given sequence will be selected.
3. 10 predicted models of target protein will be performed using PyRosetta.
4. Using the top first model we concatenate the 100 conformers from ligand alignment and this results into an unrefined protein-ligand complex of 100 comparative models.

# 3. Minimization of protein-ligand complex (`03_minimization.py`)

1. The input files for Rosetta minimization process will be generated for parallel computing.
2. Once minimization finished, the energy for each model will be calculated similarly to the first step.

# 4. Analysis (`04_analysis_1.py`)

Here, I will generate the table for 100 minimized structures. It contains the name and energy attributes of those models. Out of 100, the top 10 models will be selected using Rosetta energy values.

# 5. Complex modeling of remaining protein models (`05_top_comp_prtn_lig_modeling.py`) (from step 2, third point)

Here, the PARAMS files of top 10 ligands will be taken from step 1, fifth point.
Concatenation of protein-ligand complex (this will again result into 100 complex models)

# 6. Minimization (`06_top_comp_prtn_lig_modeling_minimization.py`)

The minimization process is same as step 3.

# 7. Analysis (`analysis_2.py`)

The analysis process is same as step 4.
The top 1 model will be reported as the best prediction.