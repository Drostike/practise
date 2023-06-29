class UsloviyaStrahovki:
    def __init__(self, vznos, period, max, franshiza, date):
        self.vznos = vznos
        self.period = period
        self.max = max
        self.franshiza = franshiza
        self.date = date

    def return_vznos(self):
        return self.vznos

    def return_period(self):
        return self.period

    def return_max(self):
        return self.max

    def return_franshiza(self):
        return self.franshiza

    def return_date(self):
        return self.date
