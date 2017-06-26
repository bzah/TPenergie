import timeit, Parsor, Repository, sys

# #### MAIN #### #


# applianceTest = Parsor.read_appliance("data_example/sample.txt")
# connTest = connect()
# insert_appliance(connTest, applianceTest)
# connTest.close()

param = sys.argv[1]


def execute(strat):
    start_time_reading = timeit.default_timer()
    appliances = Parsor.read_all_appliance(strat)
    reading_elapsed = timeit.default_timer() - start_time_reading

    start_time_inserting = timeit.default_timer()
    Repository.insert_appliances(appliances, strat)
    inserting_elapsed = timeit.default_timer() - start_time_inserting

    print("Reading file time : " + str(reading_elapsed) + " s")
    print("inserting values time : " + str(inserting_elapsed) + " s")

    print("total time : " + str(reading_elapsed + inserting_elapsed) + " s")

    return reading_elapsed + inserting_elapsed


if param == '1':
    execute("SIMPLE")
elif param == '2':
    execute("NO_ZERO")
elif param == '3':
    execute("FILTERED")
elif param == '4':
    execute("SIMPLE")
    execute("NO_ZERO")
    execute("FILTERED")
else:
    print("Parameter required: ")
    print("1 - naive storage ")
    print("2 - no zero values storage ")
    print("3 - compressed storage")
    print("4 - every strategy")
