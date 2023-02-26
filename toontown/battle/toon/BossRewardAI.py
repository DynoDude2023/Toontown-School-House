from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
import BattleStatusEffectGlobals
from direct.distributed.ClockDelta import *
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer

class BossRewardAI(DistributedObjectAI):
    
    def __init__(self, battle, target, toon, damage, healing, cooldown, turns):
        self.toon = toon
        self.target = target
        self.battle = battle
        self.damage = damage
        self.healing = healing
        self.cooldown = cooldown
        self.turns = turns
        self.rewardDepartment = 's'
        self.movie = []
    
    def getDamage(self):
        return self.damage
    
    def getHealing(self):
        return self.healing
    
    def getCooldown(self):
        return self.cooldown
    
    def setMovie(self, movie):
        self.movie = movie