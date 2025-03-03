How to install
==============

1. Create a conda environment for Python 3.7 + pyrosetta <http://www.pyrosetta.org/dow>
    - You need to add a special channel to your .condarc
2. Download Rosetta <https://www.rosettacommons.org/software>
    - <ROSETTAROOT>/main/source/scripts/python/public/generic_potential/{Molecule,mol2genparams}.py must be patched so they import importlib.util instead of importlib.
3. Download EMBOSS Needle <http://emboss.sourceforge.net>
    - sudo apt install emboss
4. Apply for a license for OpenEye <https://www.eyesopen.com/> and set a `OE_LICENSE` env var pointing to your `oe_license.txt`, and download the suitable __application__ suite for your platform.
5. Install openbabel (either in the conda env or system-wide)