class item:
    name = ""
    quantity = 0
    frequency = 0
    weeks_past = 0
    unitType = ""

    def __init__(self, name ="Unknown", quantity = 1, frequency = 1,wW=0, units_cont="na"):
        self.name = name
        self.quantity = quantity
        self.frequency = frequency
        self.weeks_past = wW
        self.unitType = units_cont

    ##Make items comparable
    def __eq__(self, other):
        print("Comparison:")
        print("\t"+self.get_name())
        print("\t"+other.get_name())

        result = self.get_name() == other.get_name()

        print("\tResult: "+str(result))
        return result

    ##This fucntion looks at the frequnecy of need for this product. It then
    ##looks to see how many weeks have past. If it is time to order the item
    ##true will be return. The weeks_past will not be reset because there is
    ##no guarente the item makes it to the list at this point.
    def needed(self):
        if(self.weeks_past >= self.frequency):
            return True
        else:
            return False

    def reset_weeks_past(self):
        self.weeks_past = 0

    ##Basic Get Methods
    def get_unitType(self):
        return self.unitType

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
        return self.weeks_past

    def increment_weeks_past(self):
        self.weeks_past += 1

    def toString(self):
        if not(self.unitType == "na"):
            return str(self.quantity)+" "+self.unitType+" "+self.name
        else:
            return str(self.quantity)+" "+self.name
    ##To String Fucntionality
    def __str__(self):
        return self.toString()
    def __repr__(self):
        return self.__str__()
