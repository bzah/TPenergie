class Appliance:
    def __init__(self, filename, project, household, appliance):
        self.name = appliance
        self.project = project
        self.household = household
        self.filename = filename
        self.measures = []
