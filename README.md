# S3Python
This is code for analyzing data from S3 experiment. The main features are:
- reading the binary files from machine output
- exporting existing data to readable CSV format
- simple energy calibration using basic fitting algorithm (Landau distribution)


Now working on or improving these features:
- advanced fitting using Langauss and convolution minimization

### Docs
You can learn more about the code in the [Docs](./docs/homepage.md).

### Basic Usage
If you understand the purpose of the code, you can run the code with specifying custom settings in the JSON file. This needs to be added as parameter when running the code:
```bash
~$ python src/mainMP.py settings.json
```
Usually, modifying the first section `main`.

### Updates
##### 30.12.2024
Improved RAM memory handling. Complete folder now can be correctly processed and saved to many temporary CSV files. Further improvement to somehow merge those CSV files in plan.
##### 29.12.2024
Finding out the reason of interrupted RAW files. The issue is probably in missing part of the head - for some reason only `f0` header is added instead of `fff0` which should be correct. See analysis in `binaryFilesStructure.ipynb` notebook.
##### 17.11.2024
In notebook `fitting.ipynb` I have implemented the Landau, Langauss and Langauss with convolution fitting with some analysis of error. Criterion used is MSE (Mean Squared Error).
##### 14.11.2024
First Docs commit.
##### 10.11.2024
Now it is possible to export data from all events to CSV file. This means approximately 80% compression (100 MB to ~20 MB) and easier reading than from binary files. Also some energy spectra analysis added in notebooks. 
##### 8.11.2024 = V0.2
Finished first simple energy calibration with discussable fitting using normalization to usual Landau function intervals. Improvement needed using Langauss.

### Requirements
You need to have installed these programs or libraries. Some features are restricted to Linux or POSIX systems only, but the core should be working also on Windows and running the code there shouldn't cause an issues. The list is not completed yet.
```
python >= 3.10
matplotlib >= 2.11
```
The error message in case of missing library should be understandable enough for further installation.

### Updates Archive
##### 3.11.2024
Creating energy spectra, first attempts to fit with Landau.
##### 1.11.2024 = V0.1
Version 0.1, working multiprocessing and loading to `Event` classes. Some files can't be read, not solved fo now
##### 31.10.2024
RAM overflow handling and settings in JSON file.
##### 28.10.2024
Multiprocessing using `Pool` class and timing.
##### 22.10.2024
First sketch of multiprocessing, reading of multiple files in multiple processes. Might prove useful later.
##### 9.10.2024
Reading binary files as hex string and parsing it myself. Creating working class `Event`, which is able to successfully parse an event with given starting position. Looking for functions from some library to create more efficient code, if possible. All still in `binaryFilesStructure.ipynb`.
##### 6.10.2024
Binary files reading, event size found - 217 bytes. Can't parse the headers. All work done is in `binaryFilesStructure.ipynb`.