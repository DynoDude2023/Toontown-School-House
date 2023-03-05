#make a class DistributedInvasionAI that inherits from DistributedEventAI

import DistributedEventAI

class DistributedInvasionAI(DistributedEventAI.DistributedEventAI):
    
    def __init__(self, air):
        DistributedEventAI.DistributedEventAI.__init__(self, air)
        self.cogNumber = 9999
        self.cogName = 'f'
        self.skelecog = 0
        self.v2 = 0
        self.waiter = 0
        self.level = 'any'
        self.isActive = 0