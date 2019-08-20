#!/home/kiruba/softwares/miniconda3/bin/python

import os
import glob
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--folder", required=True, help="Enter into the folder")
args = vars(ap.parse_args())


ROSETTA_ROOT = os.environ.get('ROSETTA_ROOT', os.path.expanduser('~/.local/rosetta_bin_linux_2019.22.60749_bundle'))

rosetta_mini_app = f"{ROSETTA_ROOT}/main/source/bin/minimize_ppi.static.linuxgccrelease"
rosetta_db = f"{ROSETTA_ROOT}/main/database"
# This binary is only available if compiled from source using the development versio (not public!)
rosetta_mini_score_app = f"{ROSETTA_ROOT}/main/source/bin/bou-min-ubo-nrg-jump.default.linuxgccrelease"

# First minimization of protein ligand complex

def first_minimization(rosetta_mini_app, rosetta_db, protein_ligand_path, lig_params_path):

    dict_prtn_lig_with_params = {}
    for p_l_path in protein_ligand_path:
        params_file = "_".join(os.path.splitext(os.path.basename(p_l_path))[0].split("_")[3:-1])
        params_file_with_ext = "{0}.params".format(params_file)
        dict_prtn_lig_with_params[params_file_with_ext] = p_l_path

    for params in lig_params_path:
        params_basename = os.path.basename(params)
        if params_basename in dict_prtn_lig_with_params:
            protein_ligand = os.path.basename(dict_prtn_lig_with_params[params_basename])
            protein_ligand_without_ext = os.path.splitext(os.path.basename(dict_prtn_lig_with_params[params_basename]))[0]
            print('{0} -database {1} -ignore_unrecognized_res -s {2}/{3} -extra_res_fa {2}/{4} > {2}/mini_protein_ligand_complex_top_1_comp_model/mini_{5}.log'.format(rosetta_mini_app, rosetta_db, os.getcwd(), dict_prtn_lig_with_params[params_basename], params, protein_ligand_without_ext))
            os.system('{0} -database {1} -ignore_unrecognized_res -s {2}/{3} -extra_res_fa {2}/{4} > {2}/mini_protein_ligand_complex_top_1_comp_model/mini_{5}.log'.format(rosetta_mini_app, rosetta_db, os.getcwd(), dict_prtn_lig_with_params[params_basename], params, protein_ligand_without_ext))

# First minimization score_only

def first_minimization_score_only(rosetta_mini_score_app, mini_protein_ligand_path, lig_params_path):

    dict_prtn_lig_with_params = {}
    for mini_p_l_path in mini_protein_ligand_path:
        params_file = "_".join(os.path.splitext(os.path.basename(mini_p_l_path))[0].split("_")[4:-1])
        params_file_with_ext = "{0}.params".format(params_file)
        dict_prtn_lig_with_params[params_file_with_ext] = mini_p_l_path

    for params in lig_params_path:
        params_basename = os.path.basename(params)
        if params_basename in dict_prtn_lig_with_params:
            protein_ligand = os.path.basename(dict_prtn_lig_with_params[params_basename])
            protein_ligand_without_ext = os.path.splitext(os.path.basename(dict_prtn_lig_with_params[params_basename]))[0]
            print('{0} -ignore_unrecognized_res -s {1}/{2} -extra_res_fa {1}/{3} > {1}/mini_protein_ligand_complex_top_1_comp_model/{4}.score'.format(rosetta_mini_score_app, os.getcwd(), dict_prtn_lig_with_params[params_basename], params, protein_ligand_without_ext))
            os.system('{0} -ignore_unrecognized_res -s {1}/{2} -extra_res_fa {1}/{3} > {1}/mini_protein_ligand_complex_top_1_comp_model/{4}.score'.format(rosetta_mini_score_app, os.getcwd(), dict_prtn_lig_with_params[params_basename], params, protein_ligand_without_ext))

currentWD = os.getcwd()
os.chdir(args['folder'])

os.makedirs("mini_protein_ligand_complex_top_1_comp_model", exist_ok=True)
first_minimization(rosetta_mini_app, rosetta_db, glob.glob('protein_ligand_complex_top_1_comp_model/*.pdb'), glob.glob('sdf2params/*.params'))
os.system("mv mini_*.pdb mini_protein_ligand_complex_top_1_comp_model/")

first_minimization_score_only(rosetta_mini_score_app, glob.glob('mini_protein_ligand_complex_top_1_comp_model/*.pdb'), glob.glob('sdf2params/*.params'))

os.chdir(currentWD)
