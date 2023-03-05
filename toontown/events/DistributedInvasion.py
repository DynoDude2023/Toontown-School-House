#make a class DistributedInvasion that inherits from DistributedEvent

import DistributedEvent
from direct.directnotify import DirectNotifyGlobal

class DistributedInvasion(DistributedEvent.DistributedEvent):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedInvasion")

    def __init__(self, cr):
        DistributedEvent.DistributedEvent.__init__(self, cr)
        