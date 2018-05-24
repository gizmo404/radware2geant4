import re
import subprocess
import xml.etree.ElementTree as ET
from math import log10, floor
import sys

# holder for information about the nucleus of interest
class Nucleus(object):
    def __init__(self, nucleus_name="Unknown",z=0,a=0,n=0):
        self.nucleus_name = nucleus_name
        self.z = z
        self.a = a
        self.n = z + a
    def __repr__(self):
        return '{} : {} {} {}'.format(self.__class__.__name__,
        self.nucleus_name,
        self.z,
        self.a)

# holder for the level info coming out of the ags file
class Level(object):
    def __init__(self, index=0, energy=0, Jpi="Unknown",n_gammas=0):
        self.index= index
        self.energy = energy
        self.Jpi = Jpi
        self.n_gammas = n_gammas
    
    def __repr__(self):
        return '{} : {} {} {} {}'.format(self.__class__.__name__,
                self.index,
                self.energy,
                self.Jpi,
                self.n_gammas)

# holder for the transition information coming out of the ags file
class Transition(object):
    def __init__(self, index=0, energy=0, energy_error=0,Multi="Unknown", ILev=0, FLev=0, intensity=0, ConvCoef=0, BrRatio=0, MixRatio=0, EILev=0, EFLev=0):
        self.index = index
        self.energy = energy
        self.energy_error = energy_error
        self.Multi = Multi
        self.ILev = ILev
        self.FLev = FLev
        self.intensity = intensity
        self.ConvCoef = ConvCoef
        self.BrRatio = BrRatio
        self.MixRatio = MixRatio
        self.EILev = EILev
        self.EFLev = EFLev

    def __repr__(self):
        return '{} : {} {} {} {} {} {} {} {} {} {} {} {}'.format(self.__class__.__name__,
                self.index,
                self.energy,
                self.energy_error,
                self.Multi,
                self.ILev,
                self.FLev,
                self.intensity,
                self.ConvCoef,
                self.BrRatio,
                self.MixRatio,
                self.EILev,
                self.EFLev)

# holder for the entries into the geant4 format level gamma data file
class G4LevelGammaEntry(object):
    def __init__(self, initialEnergy=0, transitionEnergy=0, transitionProb=0, polarity="Unknown", halfLife=0, angularMom=0, totalICC=0, fracKICC=0, fracL1ICC=0, fracL2ICC=0, fracL3ICC=0, fracM1ICC=0, fracM2ICC=0, fracM3ICC=0, fracM4ICC=0, fracM5ICC=0, fracOuterICC=0):
        self.initialEnergy = initialEnergy
        self.transitionEnergy = transitionEnergy
        self.transitionProb = transitionProb
        self.polarity = polarity
        self.halfLife = halfLife
        self.angularMom = angularMom
        self.totalICC = totalICC
        self.fracKICC = fracKICC
        self.fracL1ICC = fracL1ICC
        self.fracL2ICC = fracL3ICC
        self.fracL3ICC = fracL3ICC
        self.fracM1ICC = fracM1ICC
        self.fracM2ICC = fracM2ICC
        self.fracM3ICC = fracM3ICC
        self.fracM4ICC = fracM4ICC
        self.fracM5ICC = fracM5ICC
        self.fracOuterICC = fracOuterICC

    # def __repr__(self):
    #     return '{} : {} {} {} {} {} {}\n{} {}\n{} {} {}\n{} {} {} {} {} {}'.format(self.__class__.__name__,
    #             self.initialEnergy,
    #             self.transitionEnergy,
    #             self.transitionProb,
    #             self.polarity,
    #             self.halfLife,
    #             self.angularMom,
    #             self.totalICC,
    #             self.fracKICC,
    #             self.fracL1ICC,
    #             self.fracL2ICC,
    #             self.fracL3ICC,
    #             self.fracM1ICC,
    #             self.fracM2ICC,
    #             self.fracM3ICC,
    #             self.fracM4ICC,
    #             self.fracM5ICC,
    #             self.fracOuterICC)
    def __repr__(self):
        return '{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}'.format(
                self.initialEnergy,
                self.transitionEnergy,
                self.transitionProb,
                self.polarity,
                self.halfLife,
                self.angularMom,
                self.totalICC,
                self.fracKICC,
                self.fracL1ICC,
                self.fracL2ICC,
                self.fracL3ICC,
                self.fracM1ICC,
                self.fracM2ICC,
                self.fracM3ICC,
                self.fracM4ICC,
                self.fracM5ICC,
                self.fracOuterICC)

# holder for the level lines of the correlation file        
class LevelCorrelationEntry(object):
    def __init__(self, index=0, floating="Unknown", energy=0, halfLife=0, Jpi=0, n_gammas=0):
        self.index = index
        self.floating = floating
        self.energy = energy
        self.halfLife = halfLife
        self.Jpi = Jpi
        self.n_gammas = n_gammas

    #def __repr__(self):
    #    return '{} : {} {} {} {} {} {}'.format(self.__class__.__name__,
    #            self.index,
    #            self.floating,
    #            self.energy,
    #            self.halfLife,
    #            self.Jpi,
    #            self.n_gammas)

    def __repr__(self):
        return '{} {} {} {} {} {}'.format(
                self.index,
                self.floating,
                self.energy,
                self.halfLife,
                self.Jpi,
                self.n_gammas)

# holder for the transition lines of the correlation file
class GammaCorrelationEntry(object):
    def __init__(self, fLev=0, energy=0, intensity=0, multi=0, mixing=0, totalICC=0, fracKICC=0, fracL1ICC=0, fracL2ICC=0, fracL3ICC=0, fracM1ICC=0, fracM2ICC=0, fracM3ICC=0, fracM4ICC=0, fracM5ICC=0, fracOuterICC=0):
        self.fLev = fLev
        self.energy = energy
        self.intensity = intensity
        self.multi = multi
        self.mixing = mixing
        self.totalICC = totalICC
        self.fracKICC = fracKICC
        self.fracL1ICC = fracL1ICC
        self.fracL2ICC = fracL3ICC
        self.fracL3ICC = fracL3ICC

        self.fracM1ICC = fracM1ICC
        self.fracM2ICC = fracM2ICC
        self.fracM3ICC = fracM3ICC
        self.fracM4ICC = fracM4ICC
        self.fracM5ICC = fracM5ICC
        self.fracOuterICC = fracOuterICC

    #def __repr__(self):
    #    return '{} : {} {} {} {} {}\n{} {}\n{} {} {}\n{} {} {} {} {} {}'.format(self.__class__.__name__,
    #            self.fLev,
    #            self.energy,
    #            self.intensity,
    #            self.multi,
    #            self.mixing,
    #            self.totalICC,
    #            self.fracKICC,
    #            self.fracL1ICC,
    #            self.fracL2ICC,
    #            self.fracL3ICC,
    #            self.fracM1ICC,
    #            self.fracM2ICC,
    #            self.fracM3ICC,
    #            self.fracM4ICC,
    #            self.fracM5ICC,
    #            self.fracOuterICC)

    def __repr__(self):
        return '{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}'.format(
                self.fLev,
                self.energy,
                self.intensity,
                self.multi,
                self.mixing,
                self.totalICC,
                self.fracKICC,
                self.fracL1ICC,
                self.fracL2ICC,
                self.fracL3ICC,
                self.fracM1ICC,
                self.fracM2ICC,
                self.fracM3ICC,
                self.fracM4ICC,
                self.fracM5ICC,
                self.fracOuterICC)

###############################################################################
def fractionToFloat(fraction):
    num = 0
    mult = 1

    if fraction[:1] == "-":
        fraction = fraction[1:]     
        mult = -1

    if " " in fraction:
        a = fraction.split(" ")
        num = float(a[0])
        toSplit = a[1]
    else:
        toSplit = fraction

    frac = toSplit.split("/")
    num += float(frac[0]) / float(frac[1])

    return num * mult
def round_sig(x, sig=4):
  return round(x, sig-int(floor(log10(abs(x))))-1)
###############################################################################
def readInput():
    print('Reading file' +sys.argv[1])
    file = open(sys.argv[1],"r")
    
    #grab the file 
    #split the file into a list
    lines = file.read().splitlines()
    
    file.close()
    nucleus_info = lines[0].split()

    global nucleus
    nucleus.nucleus_name = nucleus_info[3]
    nucleus.z = nucleus_info[9]
    nucleus.a = nucleus_info[6]
    
    print('\nNucleus is '+nucleus.nucleus_name+'\n')


    # find the lines for level data, band data, gamma data and label data
    level_flag = [i for i, item in enumerate(lines) if re.search('\*\* Level', item)]
    band_flag = [i for i, item in enumerate(lines) if re.search('\*\* Band', item)]
    gamma_flag = [i for i, item in enumerate(lines) if re.search('\*\* Gamma', item)]
    label_flag = [i for i, item in enumerate(lines) if re.search('\*\* Label', item)]
    
    # create lists with all the level and gamma info in
    #for i in range (level_flag[0],band_flag[0]):
    #    level_lines.append(lines[i])
    global level_lines
    global gamma_lines
    level_lines = lines[level_flag[0]:band_flag[0]]
    gamma_lines = lines[gamma_flag[0]:label_flag[0]]
    print('File read\n')

###############################################################################
def generate_levels():
    print('Extracting levels', end='\r')
    for i in range(2,len(level_lines),2):
        level_data = level_lines[i].split()
        index =         int(level_data[0])
        energy =        float(level_data[1])
        s_Jpi =           str(level_data[3])
    
        s1_Jpi = s_Jpi.replace("+","")
        s2_Jpi = s1_Jpi.replace("-","")
        Jpi = fractionToFloat(s2_Jpi)
    
        levels.append(Level(index, energy, Jpi,0))
    print('Levels extracted ')
################################################################################
def generate_gammas():
    print('Extracting gammas', end='\r')
    for i in range(3,len(gamma_lines),3):
        gamma_data = gamma_lines[i].split()
        gamma_data2 = gamma_lines[i+1].split()
        index =         int(gamma_data[0])
        energy =        float(gamma_data[1])
        energy_error = float(gamma_data[2])
    
        # case of a good transition with all the useful bits
        if (gamma_data[3] == 'M') or (gamma_data[3] == 'E'):
            Multi =         str(gamma_data[3]+gamma_data[4])
            ILev =          int(gamma_data[5])
            FLev =          int(gamma_data[6])
            intensity =     float(gamma_data[7])
        else:
            Multi =         '0'
            ILev =          int(gamma_data[3])
            FLev =          int(gamma_data[4])
            intensity =     float(gamma_data[5])
    
        ConvCoef =      float(gamma_data2[1])
        BrRatio =       float(gamma_data2[3])
        MixRatio =      float(gamma_data2[5])
        
        # radware is a liar and will give a single multipolarity and a mixing ratio
        if MixRatio !=0:
           Multipolarity_dict = {
                   '0' : '0',
                   'M1' : 'M1+E2',
                   'M2' : 'M2+E3',
                   'M3' : 'M3+E4',
                   'M4' : 'M4+E5',
                   } #TODO expand this to include other combinations that can happen
           new_Multi = Multipolarity_dict.get(Multi)
           Multi = new_Multi
    
        # whilst we're already going through the gammas increment the counter for
        # number of gammas for each level
        levels[ILev-1].n_gammas +=1
        # the initial level energy will be useful later
        EILev = levels[ILev-1].energy 
    
        EFLev = levels[FLev-1].energy
    
        gammas.append(Transition(index,energy,energy_error,Multi,ILev,FLev,intensity,ConvCoef,BrRatio,MixRatio,EILev,EFLev))
    print('Gammas extracted \n')
################################################################################
def generate_g4_input():
    print('Generating Geant4 input',end='\r')
    sorted_levels = sorted(levels, key=lambda x: x.index)

    sorted_gammas = sorted(gammas, key=lambda x: x.EILev)

    for gamma in sorted_gammas:
        levelEnergy = sorted_levels[gamma.ILev-1].energy
        transitionEnergy = gamma.energy
        #transitionEnergyError = '-e '+str(gamma.energy_error)
        #transitionEnergyError = '-e +'+str(gamma.energy_error)+'-'+str(gamma.energy_error)
        #transitionEnergyError = '-e '+str(1)
        transitionEnergyError = '-e '+str(1)
        #transitionEnergyError = '-e 1'
        # TODO entering a non-integer number for the error breaks bricc
        intensity = gamma.intensity*10
        Jpi = sorted_levels[gamma.ILev-1].Jpi
    
        #print(gamma.Multi)
    
        # bricc_cmd = ['./briccs_osx.dms', '-Z 82', '-g 1063.656', '-e 3' ,'-L M4+E5', '-d +0.020', '-u 10', '-a', '-w BrIccFO']
    
        ICCs = []
        TotalIIC = 0
    
        # print(gamma.Multi+ ' do you have a flag?')
        # print(transitionEnergyError)
        if gamma.Multi !=str(0):
            # bricc_cmd = ['./briccs_osx.dms', '-Z '+nucleus_z, '-g '+str(transitionEnergy), '-e 1','-L '+gamma.Multi, '-a', '-w BrIccFO']
            bricc_cmd = ['./briccs.dms', '-Z '+nucleus.z, '-g '+str(transitionEnergy), transitionEnergyError ,'-L '+gamma.Multi, '-a', '-w BrIccFO']
            foo = subprocess.Popen(bricc_cmd, stdout=subprocess.PIPE)
    
            foo_string = foo.communicate()[0].decode("utf-8")
    
            # print(foo_string)
    
            root = ET.fromstring(foo_string)
    
            for child in root:
                if child.get('Shell') == 'Tot':
                    ICCs.append(float(child.text))
                    TotalICC = float(child.text)
                elif child.get('Shell') == 'K': 
                    ICCs.append(float(child.text)/TotalICC)
                elif child.get('Shell') == 'L1': 
                    ICCs.append(float(child.text)/TotalICC)
                elif child.get('Shell') == 'L2': 
                    ICCs.append(float(child.text)/TotalICC)
                elif child.get('Shell') == 'L3': 
                    ICCs.append(float(child.text)/TotalICC)
                elif child.get('Shell') == 'M1': 
                    ICCs.append(float(child.text)/TotalICC)
                elif child.get('Shell') == 'M2': 
                    ICCs.append(float(child.text)/TotalICC)
                elif child.get('Shell') == 'M3': 
                    ICCs.append(float(child.text)/TotalICC)
                elif child.get('Shell') == 'M4': 
                    ICCs.append(float(child.text)/TotalICC)
                elif child.get('Shell') == 'M5': 
                    ICCs.append(float(child.text)/TotalICC)
    
            G4LevelGamma.append(G4LevelGammaEntry(
                levelEnergy,# initial level energy
                transitionEnergy,# transition energy
                intensity,# transition probability
                "foo",# polarity change NOT USED
                0,# half life (useful?)
                Jpi,# spin of initial level NOT USED
                round_sig(ICCs[0]),
                round_sig(ICCs[1]),
                round_sig(ICCs[2]),round_sig(ICCs[3]), round_sig(ICCs[4]),
                round_sig(ICCs[5]),round_sig(ICCs[6]),round_sig(ICCs[7]),round_sig(ICCs[8]),round_sig(ICCs[9]),
                round_sig(1-ICCs[1]-ICCs[2]-ICCs[3]-ICCs[4]-ICCs[5]-ICCs[6]-ICCs[7]-ICCs[8]-ICCs[9])))
            # Total round(ICC, frac K, L1-3, M1-5, outer
        else:
            G4LevelGamma.append(G4LevelGammaEntry(
                levelEnergy,# initial level energy
                transitionEnergy,# transition energy
                intensity,# transition probability
                "foo",# polarity change NOT USED
                0,# half life (useful?)
                Jpi,# spin of initial level NOT USED
                0,
                0,
                0,0,0,
                0,0,0,0,0,
                0))
    
    sorted_G4LevelGamma = sorted(G4LevelGamma,key=lambda x: x.initialEnergy)
    filename = 'z'+nucleus.z+'.a'+nucleus.a
    f = open(filename,'w')
    for i in sorted_G4LevelGamma:
        print(i, file=f)

    print('Geant4 input file, '+filename+' generated')

################################################################################
def generate_correlation_g4_input():
    print('Generating Geant4 correlation input',end='\r')
    sorted_levels = sorted(levels, key=lambda x: x.energy)
    sorted_gammas = sorted(gammas, key=lambda x: x.ILev)
    index_dict = {}
    #sorted_levels.sort(key = lambda x: x.energy)
    #sorted_gammas.sort(key = lambda x: x.ILev)

    for counter, i in enumerate(sorted_levels):
        index_dict[sorted_levels[counter].index] = counter
        index = counter
        floating = '-'
        energy = sorted_levels[counter].energy
        if energy == 0:
            halfLife = -1
        else:
            halfLife = 0
        Jpi = sorted_levels[counter].Jpi
        n_gammas = sorted_levels[counter].n_gammas
        
        G4correlatedLevels.append(LevelCorrelationEntry(index, floating, energy, halfLife, Jpi, n_gammas))

    sorted_levels.sort(key = lambda x: x.energy)
    sorted_gammas.sort(key = lambda x: x.EILev)
    
    #for i in sorted_G4LevelGamma:
    #    print(i)
    #for i in sorted_gammas:
    #    print(i)
    
    Multi_dict = {'0' : 0,
            'E1' : 1, 'M1' : 2,
            'E2' : 3, 'M2' : 4,
            'E3' : 5, 'M3' : 6,
            'E4' : 7, 'M4' : 8,
            'E5' : 9, 'M5' : 10,
            'M1+E2' : 201,
            'M2+E3' : 405,
            'M3+E4' : 607,
            'M4+E5' : 809
            } # TODO expand this to include E0's and E0 components
    
    for counter, i in enumerate(sorted_gammas):
        index = 0 # index of daughter level 
        index = index_dict[sorted_gammas[counter].FLev]
        energy = sorted_gammas[counter].energy 
        intensity = sorted_gammas[counter].intensity*10 # relative intensity
    
        Multipolarity_string = sorted_gammas[counter].Multi
        Multipolarity = Multi_dict[Multipolarity_string]
    
        MixRatio = sorted_gammas[counter].MixRatio
    
        G4correlatedGamma.append(GammaCorrelationEntry(index, energy, intensity, Multipolarity, MixRatio,
            G4LevelGamma[counter].totalICC,
            G4LevelGamma[counter].fracKICC,
            G4LevelGamma[counter].fracL1ICC, G4LevelGamma[counter].fracL2ICC, G4LevelGamma[counter].fracL3ICC,
            G4LevelGamma[counter].fracM1ICC, G4LevelGamma[counter].fracM2ICC, G4LevelGamma[counter].fracM3ICC, G4LevelGamma[counter].fracM4ICC, G4LevelGamma[counter].fracM5ICC,
            G4LevelGamma[counter].fracOuterICC))
    
    filename = 'correlation_z'+nucleus.z+'.a'+nucleus.a
    f = open(filename,'w')
    
    tempcounter = 0
    for i in G4correlatedLevels:
        #print(i)
        print(i, file=f)
        for j in range(i.n_gammas):
            #print(sorted_gammas[tempcounter])
            #print(G4correlatedGamma[tempcounter])
            print(G4correlatedGamma[tempcounter], file=f)
            tempcounter+=1
    print('Geant4 correlation input file, '+filename+' generated')
################################################################################

# Gloabal lists and objects to be passed around between functions
nucleus = Nucleus("Unknown",0,0)
level_lines = []
gamma_lines = []

# lists to fill extracted levels and gammas with
levels = []
gammas = []

# list to fill with the generated level and gamma info to go into Geant4
G4LevelGamma = []

# lists to fill with the generated correlation info to go into Geant4
G4correlatedLevels = []
G4correlatedGamma = []

def main():
    print("Script to eventually convert .ags (ascii gls) files from Radware into Geant4 input files!")


    if len(sys.argv) == 1:
        print('\nWARNING NO INPUT GIVEN\n\nRun program with input .ags file e.g. python readfile.py Cs133.ags')
        sys.exit(-1)

    readInput()#TODO make this take an input so it's easier to debug    

    generate_levels()#TODO make this take an input so it's easier to debug
    generate_gammas()#TODO make this take an input so it's easier to debug

    generate_g4_input()#TODO make this take an input so it's easier to debug
    generate_correlation_g4_input()#TODO make this take an input so it's easier to debug

    print("\nGeant4 input file should be placed in 'Geant4/Data/Geant4.10.X/PhotonEvaporationX.X")
    print("Geant4 correlation input file should be editted to remove 'correlation_' prefix and placed in 'Geant4/Data/Geant4.10.X/PhotonEvaporationX.X/correlated_gamma'")
if __name__ == "__main__":
    main() 
