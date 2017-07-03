import os

from src.Domain import Filtered_measure, Appliance, Measure


# Get the second word (index 1) and remove the
def get_second_word(line):
    words = line.split(" : ")
    return words[1][:-1]


def read_appliance_without_zeros(filename):
    file = open(filename, "r")
    print("Reading file --->  " + filename)
    project_line = file.readline()
    project = get_second_word(project_line)
    household_line = file.readline()
    household = get_second_word(household_line)
    appliance_line = file.readline()
    appliance = get_second_word(appliance_line)
    appliance = Appliance.Appliance(filename, project, household, appliance)
    file.readline()
    file.readline()
    for line in file:
        slitted_value = line.split("\t")
        measure = Measure.Measure(slitted_value[0], slitted_value[1],
                                  slitted_value[2], slitted_value[3])
        if measure.state != 0 or measure.energy != 0:
            appliance.measures.append(measure)
    return appliance


def read_appliance_with_filtered_measures(filename):
    file = open(filename, "r")
    print("Reading file --->  " + filename)
    project_line = file.readline()
    project = get_second_word(project_line)
    household_line = file.readline()
    household = get_second_word(household_line)
    appliance_line = file.readline()
    appliance = get_second_word(appliance_line)
    appliance = Appliance.Appliance(filename, project, household, appliance)
    file.readline()
    file.readline()
    first_measure_line = file.readline()
    first_measure_slitted = first_measure_line.split("\t")
    first_measure = Measure.Measure(first_measure_slitted[0], first_measure_slitted[1],
                                    first_measure_slitted[2], first_measure_slitted[3])
    previous_measure = first_measure
    recurrence = 1
    measure = None
    for line in file:
        slitted_value = line.split("\t")
        measure = Measure.Measure(slitted_value[0], slitted_value[1],
                                  slitted_value[2], slitted_value[3])
        if measure.state != previous_measure.state or measure.energy != previous_measure.energy:
            appliance.measures.append(
                Filtered_measure.Filtered_measure(previous_measure.date, previous_measure.time,
                                                  previous_measure.state, previous_measure.energy,
                                                  recurrence))
            previous_measure = measure
            recurrence = 0
        recurrence += 1
    if measure is not None:
        appliance.measures.append(
            Filtered_measure.Filtered_measure(measure.date, measure.time,
                                              measure.state, measure.energy,
                                              recurrence))
    return appliance


def read_appliance(filename):
    file = open(filename, "r")
    print("Reading file --->  " + filename)
    project_line = file.readline()
    project = get_second_word(project_line)
    household_line = file.readline()
    household = get_second_word(household_line)
    appliance_line = file.readline()
    appliance = get_second_word(appliance_line)
    appliance = Appliance.Appliance(filename, project, household, appliance)
    file.readline()
    file.readline()
    for line in file:
        slitted_value = line.split("\t")
        measure = Measure.Measure(slitted_value[0], slitted_value[1],
                                  slitted_value[2], slitted_value[3])
        appliance.measures.append(measure)
        #  print(measure.date + " " + measure.time + " --> "
        #       + measure.state + " " + measure.energy)
    return appliance


def read_all_appliance(strategy, async):
    appliances = []
    dir = '../data/'
    if async:
        dir = '../asyncData/'
    for filename in os.listdir(dir):
        if strategy == "SIMPLE":
            appliance = read_appliance(dir + filename)
        elif strategy == "NO_ZERO":
            appliance = read_appliance_without_zeros(dir + filename)
        elif strategy == "FILTERED":
            appliance = read_appliance_with_filtered_measures(dir + filename)
        else:
            appliance = None
            print("ERROR")
        appliances.append(appliance)
    return appliances
