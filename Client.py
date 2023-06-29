class Client:
    def __init__(self, name, fam, age, id):
        self.name = name
        self.fam = fam
        self.age = age
        self.id = id

    def return_name(self):
        return self.name

    def return_fam(self):
        return self.fam

    def return_age(self):
        return self.age

    def return_name_and_fam(self):
        return self.name + " " + self.fam
