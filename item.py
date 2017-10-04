class item:
    name = ""
    quantity = 0
    frequency = 0
    weeks_past = 0

    def __init__(self, name, quantity = 1, frequency = 1):
        self.name = name
        self.quantity = quantity
        self.frequency = frequency

    ##This fucntion looks at the frequnecy of need for this product. It then
    ##looks to see how many weeks have past. If it is time to order the item
    ##true will be return. The weeks_past will not be reset because there is
    ##no guarente the item makes it to the list at this point.
    def needed(self):
        if(weeks_past >= frequency):
            return True
        else:
            return False
    ##Basic Get Methods
    def get_name(self):
        return self.name

    def get_quantity(self):
        return self.quantity

    def get_frequency(self):
        return self.frequency

    ##Basic Set Methods
    def set_frequency(self, f):
        self.frequency = f
    def set_name(self, n):
        self.name = n
    def set_quantity(self, q):
        self.quantity = q

    ##Weeks_past functionality
    def get_weeks_past(self):
        return weeks_past

    def a_week_has_past(self):
        weeks_past += 1

    ##To String Fucntionality
    def __str__(self):
        return self.name+":"+str(self.quantity)
    def __repr__(self):
        return self.__str__()
