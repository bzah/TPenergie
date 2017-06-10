import os, Measure, Appliance, psycopg2


# Get the second word (index 1) and remove the
def get_second_word(line):
    words = line.split(" : ")
    return words[1][:-2]


def read_appliance(filename):
    file = open(filename, "r")
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


def read_all_appliance():
    appliances = [Appliance]
    for filename in os.listdir('/data/'):
        print(filename)
        appliance = read_appliance(filename)
        appliances.append(appliance)
    return appliances


def connect():
    return psycopg2.connect(host="localhost", database="energie", user="postgres", password="postgres")


def insert_appliance(conn, appliance):
    # print("insertion into DB Energie")
    appliance_statement = """INSERT INTO appliance(name,project,household,file)
                             VALUES (%s,%s,%s,%s) RETURNING id"""

    measure_statement = """INSERT INTO measure(appliance,date,state,energy)
                           VALUES (%s,%s,%s,%s) RETURNING id"""

    cursor = conn.cursor()
    cursor.execute(appliance_statement, (appliance.name, appliance.project, appliance.household, appliance.filename))
    app_id = cursor.fetchone()[0]
    if app_id is not None:
        for measure in appliance.measures:
            cursor.execute(measure_statement,
                           (app_id, measure.date + ":" + measure.time, measure.state, measure.energy))
        conn.commit()
    cursor.close()


def insert_appliances(appliances):
    conn = connect()
    for appliance in appliances:
        insert_appliance(conn, appliance)
    conn.close()


# #### MAIN #### #
applianceTest = read_appliance("data/sample.txt")
connTest = connect()
insert_appliance(connTest, applianceTest)
connTest.close()
