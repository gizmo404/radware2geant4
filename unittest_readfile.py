import unittest
import numpy
from pytest import approx
from readfile import MathFuncs
from readfile import InputFuncs
from readfile import OutputFuncs

 
class TestReadFile(unittest.TestCase):
 
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
        bricc_output = OutputFuncs.parse_bricc(['./briccs.dms','-Z 82', '-g 200', '-e 3', '-L E2', '-a', '-w BrIccFO'])

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
        # self.assertIs( 
        bricc_output = OutputFuncs.parse_bricc(['./briccs.dms','-Z 82', '-g 200', '-e 3', '-L E0', '-a', '-w BrIccFO'])

        self.assertTrue( bricc_output == approx(numpy.array([2.045E+11,
                                                             3.554E+10,
                                                             7.251E+8,
                                                             2.408E+11]), rel=1e-2))
    def test_parse_bricc_mixed(self):
        # self.assertIs( 
        bricc_output = OutputFuncs.parse_bricc(['./briccs.dms','-Z 82', '-g 1063.656', '-e 3', '-L M4+E5', '-d +0.020', '-u 10', '-a', '-w BrIccFO'])

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
            

if __name__ == '__main__':
    unittest.main()
