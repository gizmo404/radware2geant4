#import readfile
import unittest
import numpy
from pytest import approx
from readfile import MathFuncs
from readfile import InputFuncs
from readfile import OutputFuncs
from readfile import Nucleus, Level, Transition, G4LevelGammaEntry
from sys import platform

 
class TestReadFile(unittest.TestCase):
    maxDiff = None
 
    def setUp(self):
        pass
 
    def test_fraction(self):
        self.assertEqual( MathFuncs.fractionToFloat("1/2"), 0.5)
 
    def test_partial_fraction(self):
        self.assertEqual( MathFuncs.fractionToFloat("1 1/2"), 1.5)
    
    def test_not_fraction(self):
        self.assertEqual( MathFuncs.fractionToFloat("2"), 2)
    
    def test_round_sig(self):
        self.assertEqual( MathFuncs.round_sig(10001), 10000)
        self.assertEqual( MathFuncs.round_sig(1.9911,2), 2.0)
        self.assertEqual( MathFuncs.round_sig(0), 0)

    def test_parse_bricc_pure(self):
        # self.assertIs( 
        if platform == "linux" or platform == "linux2":
            bricc_output = OutputFuncs.parse_bricc(['./briccs_linux.dms','-Z 82', '-g 200', '-e 3', '-L E2', '-a', '-w BrIccFO'])
        elif platform == "darwin":
            bricc_output = OutputFuncs.parse_bricc(['./briccs_osx.dms','-Z 82', '-g 200', '-e 3', '-L E2', '-a', '-w BrIccFO'])

        self.assertTrue( bricc_output == approx(numpy.array([0.428,
                                                             0.168,
                                                             0.0234,
                                                             0.106,
                                                             0.064,
                                                             0.00559,
                                                             0.0274,
                                                             0.0172,
                                                             0.000203,
                                                             0.000131]), rel=1e-2))

    def test_parse_bricc_pure_E0(self):
        if platform == "linux" or platform == "linux2":
            bricc_output = OutputFuncs.parse_bricc(['./briccs_linux.dms','-Z 82', '-g 200', '-e 3', '-L E0', '-a', '-w BrIccFO'])
        elif platform == "darwin":
            bricc_output = OutputFuncs.parse_bricc(['./briccs_osx.dms','-Z 82', '-g 200', '-e 3', '-L E0', '-a', '-w BrIccFO'])

        self.assertTrue( bricc_output == approx(numpy.array([2.045E+11,
                                                             3.554E+10,
                                                             7.251E+8,
                                                             2.408E+11]), rel=1e-2))
    def test_parse_bricc_mixed(self):
        if platform == "linux" or platform == "linux2":
            bricc_output = OutputFuncs.parse_bricc(['./briccs_linux.dms','-Z 82', '-g 1063.656', '-e 3', '-L M4+E5', '-d +0.020', '-u 10', '-a', '-w BrIccFO'])
        elif platform == "darwin":
            bricc_output = OutputFuncs.parse_bricc(['./briccs_osx.dms','-Z 82', '-g 1063.656', '-e 3', '-L M4+E5', '-d +0.020', '-u 10', '-a', '-w BrIccFO'])

        self.assertTrue( bricc_output == approx(numpy.array([0.1257,
                                                             0.0942,
                                                             0.0183,
                                                             0.00375,
                                                             0.001667,
                                                             0.00441,
                                                             0.000995,
                                                             0.000473,
                                                             7.55E-6,
                                                             1.264E-6]), rel=1e-2))


    #def test_readInput(self):
    #    level_lines = []
    #    gamma_lines = []
    #    InputFuncs.readInput('test_input.txt')

    #    file = open('test_level_lines.txt')
    #    file_level_lines = file.read().splitlines()
    #    file.close()

    #    file = open ('test_gamma_lines.txt')
    #    file_gamma_lines = file.read().splitlines()
    #    file.close()

    #    self.assertEqual(level_lines, file_level_lines)

    def test_generate_levels(self):
        file = open('test_level_lines.txt')
        file_level_lines = file.read().splitlines()
        file.close()

        file = open('test_levels.txt')
        file_levels = file.readlines()
        file.close()

        file_LevelsRef = []
        for lines in file_levels:
            i = lines.split()
            file_LevelsRef.append(Level(int(i[0]),float(i[1]),i[2],int(i[3])))

        LevelsReturn = InputFuncs.generate_levels(file_level_lines)

        for i, entry in enumerate(LevelsReturn): 
            self.assertTrue(LevelsReturn[i] == LevelsRef[i])

    def test_generate_gammas(self):
        file = open ('test_gamma_lines.txt')
        file_gamma_lines = file.read().splitlines()
        file.close()

        file = open('test_gammas.txt')
        file_gammas = file.readlines()
        file.close()
        
        file_GammasRef = []
        for lines in file_gammas:
            i = lines.split()
            file_GammasRef.append(Transition(int(i[0]), float(i[1]), float(i[2]), i[3], int(i[4]), float(i[5]), float(i[6]), float(i[7]), float(i[8]), float(i[9]), float(i[10]), float(i[11])))

        file = open('test_levels.txt')
        file_levels = file.readlines()
        file.close()

        file_LevelsRef = []
        for lines in file_levels:
            i = lines.split()
            file_LevelsRef.append(Level(int(i[0]),float(i[1]),i[2],int(i[3])))

        GammasReturn = InputFuncs.generate_gammas(file_gamma_lines, file_LevelsRef)

        for i, entry in enumerate(GammasReturn):
            self.assertTrue(GammasReturn[i] == file_GammasRef[i])

    
    def test_generate_g4_input(self):
        file = open('test_generate_g4_entries.txt')
        file_g4_input= file.readlines()
        file.close()

        file_G4LevelGammaRef= []
        for lines in file_g4_input:
            i = lines.split()
            file_G4LevelGammaRef.append(G4LevelGammaEntry(float(i[0]),float(i[1]), float(i[2]),i[3],float(i[4]),float(i[5]),float(i[6]),float(i[7]),float(i[8]),float(i[9]),float(i[10]),float(i[11]),float(i[12]),float(i[13]),float(i[14]),float(i[15]),float(i[16])))

        file = open('test_level_lines.txt')
        file_level_lines = file.read().splitlines()
        file.close()

        file = open('test_levels.txt')
        file_levels = file.readlines()
        file.close()

        file_LevelsRef = []
        for lines in file_levels:
            i = lines.split()
            file_LevelsRef.append(Level(int(i[0]),float(i[1]),i[2],int(i[3])))

        file = open('test_gammas.txt')
        file_gammas = file.readlines()
        file.close()
        
        file_GammasRef = []
        for lines in file_gammas:
            i = lines.split()
            file_GammasRef.append(Transition(int(i[0]), float(i[1]), float(i[2]), i[3], int(i[4]), float(i[5]), float(i[6]), float(i[7]), float(i[8]), float(i[9]), float(i[10]), float(i[11])))

        nucleus = Nucleus("Pb",82,188)

        G4LevelGammaReturn = OutputFuncs.generate_g4_input(nucleus, file_LevelsRef, file_GammasRef)

        for i, entry in enumerate(G4LevelGammaReturn): 
            self.assertTrue(G4LevelGammaReturn[i] == file_G4LevelGammaRef[i])

    #def test_generate_g4_correlated_input(self):

    def test_extract_intensities(self):
    #   extract ags intensities and return a list with energy, intensity
        file = open('test_intensities.txt')
        file_intensities = file.readlines()
        file.close()

        IntensitiesRef = []
        for entry in file_intensities:
            i = entry.split()
            IntensitiesRef.append([float(i[0]),float(i[1]),float(i[2])])

        file = open('test_gammas.txt')
        file_gammas = file.readlines()
        file.close()

        file_GammasRef = []
        for lines in file_gammas:
            i = lines.split()
            file_GammasRef.append(Transition(int(i[0]), float(i[1]), float(i[2]), i[3], int(i[4]), float(i[5]), float(i[6]), float(i[7]), float(i[8]), float(i[9]), float(i[10]), float(i[11])))

        nucleus = Nucleus("Pb",82,188)

        IntensitiesReturn = OutputFuncs.generate_intensities(nucleus, file_GammasRef)

        self.assertEqual(IntensitiesRef,IntensitiesReturn)

if __name__ == '__main__':
    unittest.main()
