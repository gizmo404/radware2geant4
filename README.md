Script to go from radware ascii gls \*.ags to geant4 compatible input for photon evaporation.

This is not ready yet.

## Requirements:
* Geant4.10.4 (input data files changed from 4.10.3->4.10.4)
* Qt (if you want visualisations)
* Root6 (needed if you use NPTool)
* NPTool (if you want an easy way to input this files and spin populations)
* BrIcc and BrIccs (website is currently down so I can't link it here)
* Python3 (tested with 3.6.5)
* numpy (really useful python extension)

## Included files:
* readfile.py - main script for generating Geant4 PhotonEvaporation input files
* unittest_readfile.py - unit testing to try and catch my terrible coding
* Examples - folder of examlple ags schemes and generated files of varying complexity for testing and comparison
    * Single pure transition
    * Single mixed transition
    * Single E0 transition
    * single "rotational" band"
* Extractor.py - script to take a Geant4 input file and extract the level and gamma information and allow user to input intensities for each transition
* InitialPopCalculator.py - script to take the output of Extractor.py and calculate initial populations for all states

## Usage:
`python readfile.py [ags file] [E0 file]`

This generates the PhotonEvaporationFile to be used in Geant4

Optionally if the user is using NPTool and simulating e.g. a fusion-evaporation reaction where a distribution of states are being populated, Extractor.py and InititialPopCalculator.py can be used

`python Extractor.py` user will then be asked to input Z and A of nucleus and, assuming G4LEVELGAMMADATA is set, will get the file included with G4DATA

or

`python Extractor.py [filename]` user will then be asked to input Z and A of nucleus and the provided file will be used instead

### A little information on formatting
E0 transitions are not really a thing in radware, nor Geant4 for that matter.
So as a solution information about E0's can be added in to the program to generate an E0-like transition that Geant4 will be able to handle.

Here is an example of the header and a few E0 transitions;

| ## | energy | multipolarity | BranchingRatio | MixingRatio | e_Init | e_Final |
| --- | --- | --- | --- | --- | --- | --- |
|   | 150 | E0 | 0 | 0 | 150 | 0 |
|   | 200 | E0 | 0 | 0 | 350 | 150 |
|   | 500 | E0 | 0 | 0 | 500 | 0 |

Currently the transitions are being matched with their correct initial and final states based on their energies, as the level index assigned by radware is not something obvious to the user and would require parsing the file to generate the inputs (there is probably a better way to do this)

This is the only file the user will have to write for themselves and will likely only be a few lines long.

NB: the ## is a standard flag used in the .ags format so it's been carried over here for consistency.
