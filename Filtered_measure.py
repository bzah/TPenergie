import Measure


class Filtered_measure(Measure.Measure):
    def __init__(self, date, time, state, energy, recurrence):
        super().__init__(date, time, state, energy)
        self.recurrence = int(recurrence)
