# ManInAGarden 2014
#
import sqlitepersist as sqlp
import datetime

METRICS = {0.0000000001:'n',
           0.000001: 'u',
           0.001:'m',
           1.0:'',
           1000.0:'k',
           1000000.0:'M',
           1000000000.0:'T'}

class Series(sqlp.PBaseTimed):
    TableName = "SERIES"
    TypeDict = sqlp.PBaseTimed.TypeDict.copy()
    TypeDict.update({"Name": sqlp.Text(30),
        "Description": sqlp.Text(255)})

        
    def __init__(self):
        super().__init__()
        self.Name = "series with no name"
        self.Description = ""

    def __str__(self):
        return "Series: Id=" + str(self.Id) + " Name=" + self.Name + " Description=" + self.Description + " Created=" + str(self.Created)

    

class Value(sqlp.PBaseTimed):
    TableName="VALUE"
    TypeDict = sqlp.PBaseTimed.TypeDict.copy()
    TypeDict.update({"t": sqlp.DateTime(),
                     "Name" : sqlp.Text(30),
                     "Value": sqlp.Number(),
                     "SeriesId":sqlp.ForeignKeyId(),
                     "UnitId": sqlp.ForeignKeyId()})
    
    def __init__(self):
        super().__init__()
        self.t = datetime.datetime.now()
        self.Value = 0


class Unit(sqlp.PBaseTimed):
    TableName = "UNIT"
    TypeDict = sqlp.PBaseTimed.TypeDict.copy()
    TypeDict.update({"Name": sqlp.Text(15),
                     "FactorToBase": sqlp.Number(),
                     "BaseName": sqlp.Text(15)})
    
    @classmethod
    def create_vanilla_data(cls):
        print("creating vanilla data for units")
        cls.create_units('V', -3, 3) #volt
        cls.create_units('A', -3, 3) #ampere
        cls.create_units('s', -6, 0) #seconds
        cls.create_units('Ah', -3, 3)
        cls.create_units('°C', 0, 2) #degrees celsius
        cls.create_units('cd', 0, 2) #candela
        cls.create_units('lx', 0, 2) #lux
        cls.create_units('lm', 0, 2) #lumend
        cls.create_units('W', -3, 3)
        cls.create_units('VA', -3, 3)

    @classmethod
    def create_units(cls, base, minexp, maxexp):
        print("creating for base", base)
        for i in range(minexp, maxexp+1, 3):
            fact = pow(10,i)
            unit = Unit()
            unit.Name = METRICS[fact] + base
            unit.FactorToBase = fact
            unit.BaseName = base
            unit.flush()
            print("created new unit", unit.Name)

    def __init__(self):
        super().__init__()
        self.Name = ""
        self.FactorToBase = 1.0
        self.BaseName = ""

    def __str__(self):
        return self.Name
