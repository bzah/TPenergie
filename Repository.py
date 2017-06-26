import psycopg2


def connect():
    return psycopg2.connect(host="localhost", database="energie", user="postgres", password="postgres")


def select_or_insert_household(conn, household):
    select_stmt = """ SELECT id FROM household
                      WHERE id = %s"""
    insert_statement = """INSERT INTO household(id)
                                     VALUES (%s) RETURNING id"""
    cursor = conn.cursor()
    cursor.execute(select_stmt, (household,))
    if cursor.rowcount > 0:
        id = cursor.fetchone()[0]
    elif cursor.rowcount == 0:
        cursor.execute(insert_statement, (household,))
        id = cursor.fetchone()[0]
    else:
        print("ERROR (should throw exception")
        id = 0
    cursor.close()
    return id


def insert_measure(conn, appliance_id, measure):
    cursor = conn.cursor()
    measure_statement = """INSERT INTO measure(appliance,date,state,energy)
                                   VALUES (%s,%s,%s,%s) RETURNING id"""
    cursor.execute(measure_statement,
                   (appliance_id, measure.date + ":" + measure.time, measure.state, measure.energy))


def insert_measure_without_zero(conn, appliance_id, measure):
    cursor = conn.cursor()
    measure_statement = """INSERT INTO measure_without_zero(appliance,date,state,energy)
                                       VALUES (%s,%s,%s,%s) RETURNING id"""
    cursor.execute(measure_statement,
                   (appliance_id, measure.date + ":" + measure.time, measure.state, measure.energy))


def insert_measure_with_filtered_measures(conn, appliance_id, measure):
    cursor = conn.cursor()
    measure_statement = """INSERT INTO measure_with_filter(appliance,date,state,energy,recurrence)
                                           VALUES (%s,%s,%s,%s,%s) RETURNING id"""
    cursor.execute(measure_statement,
                   (appliance_id, measure.date + ":" + measure.time, measure.state, measure.energy, measure.recurrence))


def insert_appliance(conn, appliance, strategy):
    appliance_statement = """INSERT INTO appliance(name,project,household,file)
                             VALUES (%s,%s,%s,%s) RETURNING id"""

    household_id = select_or_insert_household(conn, appliance.household)
    cursor = conn.cursor()
    print("Inserting appliance --->  " + str(appliance))
    cursor.execute(appliance_statement, (appliance.name, appliance.project, household_id, appliance.filename))
    app_id = cursor.fetchone()[0]
    if app_id is not None:
        for measure in appliance.measures:
            if strategy == "SIMPLE":
                insert_measure(conn, app_id, measure)
            elif strategy == "NO_ZERO":
                insert_measure_without_zero(conn, app_id, measure)
            elif strategy == "FILTERED":
                insert_measure_with_filtered_measures(conn, app_id, measure)
        conn.commit()
    cursor.close()


def insert_appliances(appliances, strategy):
    conn = connect()
    for appliance in appliances:
        insert_appliance(conn, appliance, strategy)
    conn.close()
