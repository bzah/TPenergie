import sys, os.path
import timeit

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append('../src/')
sys.path.append('../src/Domain')

print(sys.path)

from src import Parsor, Repository


# #### MAIN #### #


# applianceTest = Parsor.read_appliance("data_example/sample.txt")
# connTest = connect()
# insert_appliance(connTest, applianceTest)
# connTest.close()

def execute(strat):
    # TODO Read the files only once when each strats are used
    start_time_reading = timeit.default_timer()
    appliances = Parsor.read_all_appliance(strat, async)
    reading_elapsed = timeit.default_timer() - start_time_reading

    start_time_inserting = timeit.default_timer()
    Repository.insert_appliances(appliances, strat, async)
    inserting_elapsed = timeit.default_timer() - start_time_inserting

    print("Reading file time : " + str(reading_elapsed) + " s")
    print("inserting values time : " + str(inserting_elapsed) + " s")

    return reading_elapsed + inserting_elapsed


async = False
if sys.argv.__len__() > 2 and sys.argv[2] == "async":
    async = True
if sys.argv[1] == '1':
    simpleTime = execute("SIMPLE")
elif sys.argv[1] == '2':
    noZeroTime = execute("NO_ZERO")
elif sys.argv[1] == '3':
    filteredTime = execute("FILTERED")
elif sys.argv[1] == '4':
    simpleTime = execute("SIMPLE")
    noZeroTime = execute("NO_ZERO")
    filteredTime = execute("FILTERED")
    print("SIMPLE strategy total time : " + str(simpleTime) + " s")
    print("NO_ZERO strategy total time : " + str(noZeroTime) + " s")
    print("FILTERED strategy total time : " + str(filteredTime) + " s")
else:
    print("Parameter required: ")
    print("1 - naive storage ")
    print("2 - no zero values storage ")
    print("3 - compressed storage")
    print("4 - every strategy")
