import os
import sys
import re

# list of elements for user friendliness
elementList=["H","He","Li","Be","B","C","N","O","F","Ne","Na","Mg","Al","Si",
        "P","S","Cl","Ar","K","Ca","Sc","Ti","V","Cr","Mn","Fe","Co","Ni","Cu",
        "Zn","Ga","Ge","As","Se","Br","Kr","Rb","Sr","Y","Zr","Nb","Mo","Tc",
        "Ru","Rh","Pd","Ag","Cd","In","Sn","Sb","Te","I","Xe","Cs","Ba","La",
        "Ce","Pr","Nd","Pm","Sm","Eu","Gd","Tb","Dy","Ho","Er","Tm","Yb","Lu",
        "Hf","Ta","W","Re","Os","Ir","Pt","Au","Hg","Tl","Pb","Bi","Po","At",
        "Rn","Fr","Ra","Ac","Th","Pa","U","Np","Pu","Am","Cm","Bk","Cf","Es",
        "Fm","Md","No","Lr","Rf","Db","Sg","Bh","Hs","Mt","Ds","Rg","Cn","Nh",
        "Fl","Mc","Lv","Ts","Og"]

def readFile(z, a, filename = None):
    if filename == None :
        # find where the data files are stored
        G4LevelGammaDataFolder=os.getenv('G4LEVELGAMMADATA')
        # select the file we want
        path = G4LevelGammaDataFolder+'/z'+str(z)+'.a'+str(a)
        # open file as read only
        data_file = open(path,"r")
        # fill a list with the lines of the file
        data = data_file.readlines()
        return data
    else :
        data_file = open(filename,"r")
        data = data_file.readlines()
        return data

def generateIntensityFile(data, z, a): # old data format reader
    new_path = 'intensity_z'+str(z)+'.a'+str(a)
    intensity_file = open (new_path,'w')

    #intensity_file.write('{0} {1}'.format(z,a)

    for level_line in data: 
        level_line = level_line.replace('\t', ' ') # remove annoying tabs
        line = level_line.split()# split line
        level = line[0]
        gamma = line[1]
        # get intensity from user
        intensity = eval(input("Enter intensity for {0}keV transition from level at {1}keV:  ".format(gamma,level)))
        #write level and gamma to a line in file
        intensity_file.write('{0} {1} {2}\n'.format(level, gamma,intensity))

class _RegExLib:
    """Set up regular expressions"""
    _reg_level = re.compile('\s*\d+\s+-.*')
    _reg_gamma = re.compile('\s*\d+\s+\d+.*')

    def __init__(self,line):
        self.level = self._reg_level.match(line)
        self.gamma = self._reg_gamma.match(line)

def extract(data, z, a):
    new_path = 'intensity_z'+str(z)+'.a'+str(a)
    intensity_file = open (new_path,'w')
    current_level = 0
    for line in data:
        reg_match = _RegExLib(line)
        if reg_match.level:
            level_line = line.split()
            current_level = level_line[2]
        if reg_match.gamma:
            print(line)
            gamma_line = line.split()
            gamma =  gamma_line[1]
            print(current_level, gamma)
            intensity = eval(input("Enter intensity for {0}keV transition from level at {1}keV:  ".format(gamma,current_level)))
            intensity_file.write('{0} {1} {2}\n'.format(current_level, gamma,intensity))
    

def main():
    
    # read in Z of nucleus
    z = eval(input("Select Z:  "))
    # read in A of nucleus
    a = eval(input("Select A:  "))

    # list element that is being used
    print('Reading file for isotope:    {0}-{1}'.format(elementList[z-1],a))

    if len(sys.argv) == 1: data = readFile(z, a)
    elif len(sys.argv) == 2: data = readFile(z,a,sys.argv[1])

    #generateIntensityFile(data, z, a)

    extract(data, z, a)

if __name__ == "__main__":
    main() 

