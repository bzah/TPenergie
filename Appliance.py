class Appliance:
    def __init__(self, filename, project, household, appliance):
        self.name = appliance
        self.project = project
        self.household = household
        self.filename = filename
        self.measures = []

    def __str__(self):
        return "date : " + self.name \
               + " time : " + self.project \
               + " state : " + self.household \
               + " energy : " + self.filename \
               + " measure count : " + str(self.measures.__len__())
