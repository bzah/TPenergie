import os, Measure, Appliance


# Get the second word (index 1) and remove the
def get_second_word(line):
    words = line.split(" : ")
    print(words)
    return words[1][:-2]


def read_appliance(filename):
    # Open 1 file
    filename = "1000080-2000900-3009900.txt"
    file = open(filename, "r")
    # Read the first line
    projectLine = file.readline()
    project = get_second_word(projectLine)
    # Read the second line
    householdLine = file.readline()
    household = get_second_word(householdLine)
    # Read the third line
    applianceLine = file.readline()
    appliance = get_second_word(applianceLine)
    appliance = Appliance.Appliance(filename, project, household, appliance)
    # Read the forth line
    file.readline()
    # Read the fifth line
    file.readline()
    measures = [Measure]
    # For each new line
    for line in file:
        splittedValue = line.split("\t")
        date = splittedValue[0]
        time = splittedValue[1]
        state = splittedValue[2]
        energy = splittedValue[3]
        measure = Measure.Measure(date, time, state, energy)
        measures.append(measure)
        print(date + " " + time + " --> " + state + " " + energy)

    return appliance
