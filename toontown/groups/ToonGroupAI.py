from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import *
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.PyDatagram import PyDatagram
from panda3d.core import *

class ToonGroupAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('ToonGroupAI')

    def __init__(self, air, ownerId, maxMembers=4):
        DistributedObjectAI.__init__(self, air)
        self.air = air
        self.ownerId = ownerId
        self.members = []
        self.maxMembers = maxMembers
    
    def setOwnerId(self, ownerId):
        self.ownerId = ownerId
        self.sendUpdate('setOwnerId', [ownerId])
    
    def setMaxMembers(self, maxMembers):
        self.maxMembers = maxMembers
        self.sendUpdate('setMaxMembers', [maxMembers])
                                       
    def addMember(self, memberId):
        if memberId not in self.members:
            self.members.append(memberId)
            self.sendUpdate('addMember', [memberId])