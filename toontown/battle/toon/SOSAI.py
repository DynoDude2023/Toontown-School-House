from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
import BattleStatusEffectGlobals
from direct.distributed.ClockDelta import *
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
import BossRewardAI

class SOSAI(BossRewardAI.BossRewardAI):
    
    def __init__(self, battle, target, toon, damage, healing, cooldown, turns, npcId, SOS_ID):
        BossRewardAI.BossRewardAI.__init__(self, battle, target, toon, damage, healing, cooldown, turns)
        self.movie = [toon.doId, target.doId, damage, healing, npcId, SOS_ID]
        self.rewardDepartment = 'sellbot'