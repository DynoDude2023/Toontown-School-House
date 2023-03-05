#create a class DistributedEvent that inherits from DistributedObject

from direct.distributed.DistributedObject import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM, State

class DistributedEvent(DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedEvent")

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)