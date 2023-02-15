#make a class called BattleAvatar and inherit from DistributedObject

from direct.distributed.DistributedObject import DistributedObject
from statusEffect import BattleStatusEffectGlobals

class BattleAvatar(DistributedObject):

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.cr = cr
        self.av = None
        self.battle = None
        self.statusEffects = []