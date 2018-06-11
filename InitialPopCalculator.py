import math
import numpy



def readFile(z, a):

    path = 'intensity_z'+str(z)+'.a'+str(a)
    intensity_file = open (path,'r')
    data = intensity_file.readlines()
    return data

def parseFile(_data, _levels, _transitions, _intensities):


    # read file line, by line and split into lists
    for level_line in _data:
        line = level_line.split()# split line
        print(line)
        _levels.append(line[0])
        _transitions.append(line[1])
        _intensities.append(line[2])


def findDepopulatingLevels(_levels, _unique_levels_out, _level_intensities_out, _intensities):
    # loop over the levels and find each unique level and the intensity of all transitions out of it
    for counter, level in enumerate(_levels):
        level = round(float(level),2)
        if level not in _unique_levels_out:
            _unique_levels_out.append(level)
            _level_intensities_out.append(float(_intensities[counter]))
        else:
            _level_intensities_out[_unique_levels_out.index(level)] += float(_intensities[counter])

    [round(float(i), 2) for i in _unique_levels_out]

    print('{}\n{}'.format('unique excited levels',_unique_levels_out))
    print('{}\n{}'.format('intensities out',_level_intensities_out))


def findPopulatingLevels(_levels, _unique_levels_in, _level_intensities_in, _transitions, _intensities):
    #loop over the levels and find each unique level with transitions into it and sum the incoming intensities
    for counter, level in enumerate(_levels):
        level = round(float(level),2)
        comparison_level = level - round(float(_transitions[counter]),2)
        comparison_level = round(comparison_level,2)
        if comparison_level != 0:
            if comparison_level not in _unique_levels_in:
                _unique_levels_in.append(comparison_level)
                _level_intensities_in.append(float(_intensities[counter]))
            else: 
                _level_intensities_in[_unique_levels_in.index(comparison_level)] += float(_intensities[counter])

    print('{}\n{}'.format('unique excited levels with transitions into them',_unique_levels_in))
    print('{}\n{}'.format('Intensities in',_level_intensities_in))

def calculateInitialPopulation(_unique_levels_in, _level_intensities_in, _unique_levels_out, _level_intensities_out, _initial_levels, _initial_population):
    
    total_initial_intensity = 0.
    for counter, level in enumerate(_unique_levels_out):
        if level not in _unique_levels_in:
            total_initial_intensity += _level_intensities_out[counter]
            _initial_levels.append(level)
            _initial_population.append(_level_intensities_out[counter])
        else:
            total_initial_intensity += _level_intensities_out[counter] - _level_intensities_in[_unique_levels_in.index(level)]
    
            _initial_levels.append(level)
            _initial_population.append(_level_intensities_out[counter] - _level_intensities_in[_unique_levels_in.index(level)])
    return total_initial_intensity
    
def generateInitialPopulationFile(_initial_population, _total_initial_intensity, _initial_levels, z, a):
    scaled_initial_population = []
    for x in _initial_population:
        scaled_initial_population.append(x/_total_initial_intensity)
    
    print('Levels with initial populations\n{}\nFractional initial population of levels\n{}'.format(_initial_levels, scaled_initial_population))
    
    path = 'initial_population_z'+str(z)+'.a'+str(a)
    initial_population_file = open(path, 'w')

    for counter, level in enumerate(_initial_levels):
        initial_population_file.write('{0} {1}\n'.format(level, scaled_initial_population[counter]))

def main():
    # read in Z of nucleus
    z = eval(input("Select Z:  "))
    # read in A of nucleus
    a = eval(input("Select A:  "))

    # get the extractor generated file
    # create lists to put the file contents in
    levels = []
    transitions = []
    intensities = []

    unique_levels_out = []
    level_intensities_out = []

    unique_levels_in = []
    level_intensities_in = []

    initial_levels = []
    initial_population = []

    data = readFile(z, a)
    parseFile(data, levels, transitions, intensities)
    findDepopulatingLevels(levels, unique_levels_out, level_intensities_out, intensities)
    findPopulatingLevels(levels, unique_levels_in, level_intensities_in, transitions, intensities)
    total_initial_intensity = calculateInitialPopulation(unique_levels_in, level_intensities_in, unique_levels_out, level_intensities_out, initial_levels, initial_population)
    print(total_initial_intensity)
    generateInitialPopulationFile(initial_population, total_initial_intensity, initial_levels, z, a)

if __name__ == "__main__":
    main()

#TODO make an object holding levels and intensities becauese they're used always together and all the time
#TODO make this smart enough to spot when numbers break and fractional intensities are negative
#TODO 
