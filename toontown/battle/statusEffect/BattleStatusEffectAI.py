from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
import BattleStatusEffectGlobals
from direct.distributed.ClockDelta import *
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer

class BattleStatusEffectAI(DistributedObjectAI):

    def __init__(self, battle):
        self.battle = battle
        self.statusType = BattleStatusEffectGlobals.BATTLE_STATUS_INFINITE
        self.statusEffectName = None
        self.statusEffectDuration = None
        self.statusEffectValues = {}
        self.statusEffectTargetId = None
        self.effectedTarget = 0

    def getStatusEffectName(self):
        return self.statusEffectName

    def getStatusEffectDuration(self):
        return self.statusEffectDuration

    def getStatusEffectValues(self):
        return self.statusEffectValues

    def getStatusEffectTargetId(self):
        return self.statusEffectTargetId

    def setStatusEffectName(self, statusEffectName):
        self.statusEffectName = statusEffectName

    def setStatusEffectDuration(self, statusEffectDuration):
        self.statusEffectDuration = statusEffectDuration

    def setStatusEffectValues(self, statusEffectValues):
        self.statusEffectValues = statusEffectValues

    def setStatusEffectTargetId(self, statusEffectTargetId):
        self.statusEffectTargetId = statusEffectTargetId

    def doEffectOnBattle(self):
        pass

    def calculateDuration(self):
        if self.statusType == BattleStatusEffectGlobals.BATTLE_STATUS_ROUND:
            self.statusEffectDuration -= 1