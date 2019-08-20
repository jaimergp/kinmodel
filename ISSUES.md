# Observed issues

- Not installable - package structure needed with explicit dependencies
- Refactor scripts -> library/app layers
- Lots of absolute paths (shebang, executables, in-house datasets)
- Uncouple IO from calculation
- It relies on applications rather than libraries. For example, the
  OpenEye toolkits could be used instead of the applications.
- No error control. If one step does not produce any results, the script
  goes on, resulting in either a exception or a silent termination with no
  output.
- Script 01: mol2params script relies on parts of Rosetta written for Py2.
  Everything under <ROSETTA>/main/source/scripts/python/public/rosetta_py
  must be updated to use `print()`, `range`, `zip` and `io.IOBase`.
- Script 02: Input Fasta filenames cannot contain underscores.

# Questions

- What does `bou-min-ubo-nrg-jump` do? Reading through the source code, it provides
  the difference of energy (score) between bound/unbound poses, with optional
  minimization first. Can we replicate that with single point potential energies
  or do we need to compute free energies?


# Proposed architecture

- ligands/
    - io.py -> read files
    - alignment.py -> structural alignment (ROCS)
    - conformers.py -> generate conformers (OMEGA)
    - parameterize.py -> assign parameters (OFF?)
    - similarity.py -> fingerprints, graph-edition?
- proteins/
    - sequence.py -> sequence alignment (EMBOSS)
    - build.py -> models the 3D structure (PyRosetta)
    - energy.py -> minimization and energy retrieval
- app.py -> applies protocol


Python stub

```python

# Step 1

smiles = '<arbitrary SMILES>'
ligand = Ligand.from_smiles(smiles)
ligand.generate_conformers(n=1000)

actives = datasets.load('active_kinase_ligand')
aligned_conformations = align(actives, ligand, conformers=ligand.conformers)

aligned_ligand = copy(ligand)
aligned_ligand.conformers = aligned_conformations[:100]

aligned_ligand.parameterize()
aligned_ligand.minimize(inplace=True, all_conformers=True)

aligned_ligands = aligned_ligands.conformers_to_structures()

# Step 2

fasta = '<arbitrary protein sequence>'
sequence = Sequence(fasta)

templates = datasets.load('active_kinase_sequences')
aligned_sequences, aligned_templates = sequence.align(templates)

server = DaskServer()
models = server.map(rosetta_modeling, zip(aligned_sequences[:10], aligned_templates[:10]))
server.

# Step 3

server = DaskServer()
complexes = [prot + lig for (prot, lig) in product(models[0], aligned_ligands[:100])]
minimized_complexes = server.map(minimize, complexes)


# The rest of the steps would be similar


```