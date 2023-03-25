#make a class called BattleAvatar and inherit from DistributedObject

from direct.distributed import DistributedObject
from statusEffect import BattleStatusEffectGlobals
from toontown.battle.BattleBase import *

class BattleAvatar(DistributedObject.DistributedObject):

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        self.cr = cr
        self.av = None
        self.battle = None
        self.statusEffects = []
        self.comboDamage = 0
        self.gagTrackDamages = {
            HEAL: 0,
            TRAP: 0,
            LURE: 0,
            SOUND: 0,
            THROW: 0,
            SQUIRT: 0,
            DROP: 0
        }
    
    def setGagDamage(self, damage, gagTrack):
        self.gagTrackDamages[gagTrack] = damage
    
    def setComboDamage(self, damage):
        self.comboDamage = damage