import re
import subprocess
import xml.etree.ElementTree as ET
from math import log10, floor
from pytest import approx
import sys
import unittest
import numpy as np
from sys import platform

################################################################################
# holder for the transition information coming out of the intensity file 
################################################################################
class Transition(object):
    def __init__(self, index=0, energy=0., transition_energy=0., intensity=0., ILev=0, FLev=0):
        self.index = int(index)
        self.energy = float(energy)
        self.transition_energy = float(transition_energy)
        self.intensity = float(intensity)
        self.ILev = int(ILev)
        self.FLev = int(FLev)

    def __repr__(self):
        return '\n{} : {} {} {} {} {} {}'.format(self.__class__.__name__,
                self.index,
                self.energy,
                self.transition_energy,
                self.intensity,
                self.ILev,
                self.FLev)
    def __str__(self):
        return str(self.__dict__)
    def __eq__(self, other): 
        comparison = False
        if ((self.index == other.index) and
            #(np.float(self.energy) == approx(np.float(other.energy), rel=0.01)) and
            (self.FLev == other.FLev) and 
            (self.ILev == other.ILev)
        ):
            comparison = True
        return comparison
################################################################################
# holder for the initial population information to go into the output file
################################################################################
class Initial_Population(object):
    def __init__(self, energy=0., initial_population=0.):
        self.energy = energy
        self.initial_population = initial_population 

    def __repr__(self):
        return '\n{} : {} {}'.format(self.__class__.__name__,
                self.energy,
                self.initial_population)
    def __str__(self):
        return str(self.__dict__)
    def __eq__(self, other): 
        comparison = False
        if ((self.index== other.index) and
            (np.float(self.energy) == approx(np.float(other.energy), rel=0.01))
        ):
            comparison = True
        return comparison

################################################################################
# read in the intensity file and just store it line by line
################################################################################
def readFile(z, a):

    path = 'intensity_z'+str(z)+'.a'+str(a)
    intensity_file = open (path,'r')
    data = intensity_file.readlines()
    return data
################################################################################
# convert input file into transitions
################################################################################
def parseFile(_data, _transitions):
    index = 0
    for level_line in _data:
        line = level_line.split()
        new_transition = Transition(index, line[0], line[1], line[2], line[3], line[4])# temporary transitions for comparison
        if new_transition not in _transitions:# check there's not been a transitions from the same level energy before
            index = index + 1# this is a new level, show increment the index
        _transitions.append(Transition(index, line[0], line[1], line[2], line[3], line[4]))
################################################################################
# Find all unique levels and their corresponding depopulating intensity
################################################################################
def findDepopulatingLevels(_transitions, _unique_levels_out):
    for transition in _transitions:
        ILev = transition.ILev
        ILevs = []
        for trans in _unique_levels_out:
            ILevs.append(trans.ILev)
        if transition.ILev not in ILevs:
            _unique_levels_out.append(Transition(transition.ILev, transition.energy, 0, transition.intensity, transition.ILev, 0))
        else:
            transition_location = _unique_levels_out.index(Transition(ILev, transition.energy, 0, 0, ILev, 0))
            _unique_levels_out[transition_location].intensity = _unique_levels_out[transition_location].intensity +transition.intensity
    print('{}\n{}'.format('unique excited levels',_unique_levels_out))

################################################################################
# Find all levels with intensity going into them and sum it
################################################################################
def findPopulatingLevels(_transitions, _unique_levels_in):
    for transition in _transitions:
        FLev = transition.FLev
        FLevs = []
        for trans in _unique_levels_in:
            FLevs.append(trans.FLev)
        if FLev == "0": # is it the ground state? special case
            continue
        elif transition.FLev not in FLevs:# is it a new transition that's being populated?
            _unique_levels_in.append(Transition(transition.FLev, 0, 0, transition.intensity, 0, transition.FLev))
        else:# find the already existing populated level and add the intensity to it
            transition_location = _unique_levels_in.index(Transition(FLev, 0, 0, 0, 0, FLev))
            _unique_levels_in[transition_location].intensity = _unique_levels_in[transition_location].intensity + transition.intensity
    print('{}\n{}'.format('unique levels with transitions into them',_unique_levels_in))

################################################################################
# Find the total starting intensity in the system
################################################################################
def calculateInitialPopulation(_unique_levels_in, _unique_levels_out, _initial_population):
    total_intensity = 0
    ILevs = []
    FLevs = []
    ILevIntensities = []
    FLevIntensities = []
    ILevEnergies = []

    for transition in _unique_levels_out:
        ILevs.append(transition.ILev)
        ILevIntensities.append(transition.intensity)
        ILevEnergies.append(transition.energy)

    for transition in _unique_levels_in:
        FLevs.append(transition.FLev)
        FLevIntensities.append(transition.intensity)

    for x, i in enumerate(ILevs):
        if i in FLevs:
            location = FLevs.index(i)
            ILevIntensities[x] = ILevIntensities[x] - FLevIntensities[location]

    for x,i in enumerate(ILevs):
        _initial_population.append(Initial_Population(ILevEnergies[x], ILevIntensities[x]))
        total_intensity = total_intensity + ILevIntensities[x]

    print(_initial_population)
    
    return total_intensity
################################################################################
# Generate final output file
################################################################################
def generateInitialPopulationFile(_initial_population, _total_initial_intensity, z, a):
    scaled_initial_population = []
    for x in _initial_population:
        scaled_initial_population.append(Initial_Population(x.energy, x.initial_population/_total_initial_intensity))

    print('Fractional initial population of levels\n{}'.format(scaled_initial_population))

    path = 'initial_population_z'+str(z)+'.a'+str(a)
    initial_population_file = open(path, 'w')

    for counter, level in enumerate(_initial_population):
        initial_population_file.write('{0} {1}\n'.format(scaled_initial_population[counter].energy, scaled_initial_population[counter].initial_population))
    

def main():
    # read in Z of nucleus
    z = eval(input("Select Z:  "))
    # read in A of nucleus
    a = eval(input("Select A:  "))
    
    transitions = []# transitions read from file
    unique_levels_out = []# indices of unique depopulating levels and intensities

    unique_levels_in = []# indicies of uniqe levels being populated
    level_intensities_in = []# intensities into populated levels

    initial_population = []# Populations to be output

    data = readFile(z, a)
    parseFile(data, transitions)
    findDepopulatingLevels(transitions, unique_levels_out)
    findPopulatingLevels(transitions, unique_levels_in)
   
    total_intensity = calculateInitialPopulation(unique_levels_in, unique_levels_out, initial_population)
    generateInitialPopulationFile(initial_population, total_intensity, z, a)

if __name__ == "__main__":
    main()
