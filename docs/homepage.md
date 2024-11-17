# Docs for S3 Python Scripts
These are the docs for Python scripts for S3 project.

### Features & Purposes
The main code used for analyzing large amounts of data can be found in `./src`. If you decide to run it on multiple CPUs (highly recommended), you should run the `mainMP.py` file as suggested in README.
```bash
~$ python src/mainMP.py settings.json
```

Other part of this repo are the Jupyter Notebooks, very useful tool for instantaneous plotting and data analysis. I used them for demonstrations of results from the main code. There are often missing comments, while the code should be quite simple to understand when the purpose is known. I hope the content of each notebook should be understandable from the name of the file. If not, there should be description in the Docs in the future.

### Main Structure
This is the main structure of the main code. If you wonder about any part, you should be able to find more about it here in Docs or in comments directly in the code.
#### Main file
The main file `mainMP.py` automatically uses multiprocessing (could be changed in the future).