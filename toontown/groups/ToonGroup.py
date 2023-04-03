from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import *
from direct.distributed.DistributedObject import DistributedObject
from direct.distributed.PyDatagram import PyDatagram
from panda3d.core import *

class ToonGroup(DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('ToonGroup')

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.cr = cr
        self.ownerId = None
        self.members = []
        self.maxMembers = 4
    
    def setOwnerId(self, ownerId):
        self.ownerId = ownerId
    
    def setMaxMembers(self, maxMembers):
        self.maxMembers = maxMembers
    
    def addMember(self, memberId):
        if memberId not in self.members:
            self.members.append(memberId)
            newToonMember = self.cr.doId2do.get(memberId)
            base.localAvatar.setSystemMessage(0, "A new member has joined your group: %s" % newToonMember.name)