class BaseStrategy:
    def __init__(self, name):
        self.name = name
        self.position = None
    
    def analyze(self, data):
        pass
    
    def calculate_position_size(self, signal, balance):
        return balance * 0.01
