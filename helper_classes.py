class Workday:
    def __init__(self, date, day, time, position):
        self.date = date
        self.day = day
        self.time = time
        self.position = position
    
    def getDate(self):
        return self.date
    
    def getDay(self):
        return self.day
    
    def getTime(self):
        return self.time
    
    def getPosition(self):
        return self.position
    
    def print(self):
        print(f'Date: {self.date}, {self.day}')
        print(f'Time: {self.time}')
        print(f'Position: {self.position}')
        print('')
