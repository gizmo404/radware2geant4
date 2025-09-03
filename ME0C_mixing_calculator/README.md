# ME0C (Mixed E0 Calculator for NPTool) #

_Author:_ Adrian Montes Plaza (email: amontesplaza@cns.s.u-tokyo.ac.jp) <br>
_Last update:_ Dec 9th, 2022 <br>
_Requirements:_ <br>
- Root (V5 and V6)
- BrIcc slave version installed (briccs)

## Explanation ##
- The input file needs:
1. Transition energy and multipolarity (mixed one with E0).
2. Experimental gamma intensity in RadWare units.
3. Experimental K-conversion coefficient.

- The output provides:
1. Useful intensities determined.
2. Line to be replaced in the user_zXX.aYY file so that NPTool/Geant4 knows how to treat the mixed E0 transitions.

# To Run #
(For the example file provided:)
```
$ root "ME0C.C(\"229_188Pb.txt\")" > 229_188Pb_ME0C.txt
```
