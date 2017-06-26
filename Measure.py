class Measure:
    def __init__(self, date, time, state, energy):
        self.date = date
        self.time = time
        self.state = int(state)
        self.energy = int(energy)

    def __str__(self):
        return "date : " + self.date \
               + " time : " + self.time \
               + " state : " + self.state \
               + " energy : " + self.energy
