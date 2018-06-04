Script to go from radware ascii gls \*.ags to geant4 compatible input for photon evaporation.

This is not ready yet.

Requirements:
* Geant4.10.4 (input data files changed from 4.10.3->4.10.4)
* Qt (if you want visualisations)
* Root6 (needed if you use NPTool)
* NPTool (if you want an easy way to input this files and spin populations)
* BrIcc and BrIccs (website is currently down so I can't link it here)
* Python3 (tested with 3.6.5)
* numpy (really useful python extension)

Included files:
* readfile.py - main script
* unittest_readfile.py - unit testing to try and catch my terrible coding
* Examples - folder of examlple ags schemes and generated files of varying complexity for testing and comparison
    * Single pure transition
    * Single mixed transition
    * Single E0 transition
    * single "rotational" band"

Usage:
`python readfile.py [ags file] (optional) [E0 file]`


A little information on formatting
* E0 
||##||energy||multipolarity||BranchingRatio||MixingRatio||e_Init||e_Final||

