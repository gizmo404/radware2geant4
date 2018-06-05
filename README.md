Script to go from radware ascii gls \*.ags to geant4 compatible input for photon evaporation.

This is not ready yet.

## Requirements:
* Geant4.10.4 (input data files changed from 4.10.3->4.10.4)
* Qt (if you want visualisations)
* Root6 (needed if you use NPTool)
* [CADMesh](https://github.com/christopherpoole/CADMesh) (needed if you are using the Spede part of NPTool)
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

This generates the PhotonEvaporationFile to be used in Geant4 (E0 file is only needed if there are E0's!)

Optionally if the user is using NPTool and simulating e.g. a fusion-evaporation reaction where a distribution of states are being populated, Extractor.py and InititialPopCalculator.py can be used

`python Extractor.py` user will then be asked to input Z and A of nucleus and, assuming G4LEVELGAMMADATA is set, will get the file included with G4DATA

or

`python Extractor.py [filename]` user will then be asked to input Z and A of nucleus and the provided file will be used instead

Next for each transition the user will be asked to input an intensity. This generates an intensity file that can quickly be modified before the next step should intensities need tweaking.

`python InitialPopCalculator.py` user will then be asked to input Z and A of nucleus and script will then identify previously generated intensity file (you need to be in the right folder for it)

Next it will generate an initial_population_zXX.aXX file that can be read into NPTool. 

NB: This script is not yet clever and if you input intensities that don't balance it will all go horribly wrong

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

# Running Spede & Sage NPTool and also using user generated files
"[NPTool](nptool.org), which stands for Nuclear Physics Tool, is an open source and freely distributed data analysis and Monte Carlo simulation package for low-energy nuclear physics experiments. The NPTool package aims to offer an unified framework for preparing and analysing complex experiments, making an efficient use of Geant4 and ROOT toolkits."

It's a good way for running nuclear physics based Geant4 simulations because it skips the reinventing the wheel part of every simulation.

This is not a comprehensive tutorial but just some tips to run NPTool with these generated input files and also some specifics on the Sage and Spede simulations.

## Inputing user PhotonEvaporation files
In the event generator input file you need to add three flags to get NPTool to use your PhotonEvaporation file over the built in one.

Here is the section of the event generator file with the extra lines highlighted
```
TwoBodyReaction
 Beam= 188Pb
 Target= 2H
 Light= 2H
 Heavy= 188Pb
 **Z= 82**
 **A= 188**
 **PhotonEvaporation= correlation_z82.a188**
 **InitialPopulationHeavy= initial_population_z82.a188a**
 ExcitationEnergyLight= 0.0
 CrossSectionPath= flat.txt CSR
 ShootHeavy= 1
 ShootLight= 0
```
