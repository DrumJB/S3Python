# S3Python

### Commits
##### 8.11.2024 = V0.2
Finished first simple energy calibration with discussable fitting using normalization to usual Landau function intervals. Improvement needed using Langauss.
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