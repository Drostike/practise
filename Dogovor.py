class Dogovor:
    def __init__(self, client, id, usloviya, thing, date, time):
        self.client = client
        self.id = id
        self.usloviya = usloviya
        self.thing = thing
        self.date = date
        self.time = time

    def return_client(self):
        return self.client

    def return_id(self):
        return self.id

    def return_usloviya(self):
        return self.usloviya

    def return_thing(self):
        return self.thing

    def return_date(self):
        return self.date

    def return_time(self):
        return self.time
