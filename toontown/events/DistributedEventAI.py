#create a class DistributedEventAI that inherits from DistributedObjectAI

from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM, State
from toontown.toonbase import ToontownGlobals

class DistributedEventAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedEventAI")

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.isActive = 0
        self.nonIncludedZoneIds = []
    
    def setActive(self, isActive):
        self.isActive = isActive
    