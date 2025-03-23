class Island:
    def __init__(self, x, y, numberOfConnections):
        self.row = x
        self.col = y
        self.numberOfConnections = numberOfConnections

    def getIndex(self):
        return (self.row, self.col)
    
    def getRow(self):
        return self.row

    def getCol(self):
        return self.col

    def getNumberOfConnections(self):
        return self.numberOfConnections

    def getInformation(self):
        return f"Index: ({self.row}, {self.col}), Number of Connections: {self.numberOfConnections}"

    def setIndex(self, x, y):
        self.row = x
        self.col = y
