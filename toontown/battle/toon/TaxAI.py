from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
import BattleStatusEffectGlobals
from direct.distributed.ClockDelta import *
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
import BossRewardAI

class TaxAI(BossRewardAI.BossRewardAI):
    
    def __init__(self, battle, target, toon, damage, healing, cooldown, turns):
        BossRewardAI.BossRewardAI.__init__(self, battle, target, toon, damage, healing, cooldown, turns)
        self.movie = [toon.doId, target.doId, damage, healing, 0, 0]
        self.rewardDepartment = 'cashbot'