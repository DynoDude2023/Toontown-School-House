from direct.directnotify import DirectNotifyGlobal
from BattleStatusEffectAI import BattleStatusEffectAI
import BattleStatusEffectGlobals
from direct.distributed.ClockDelta import *
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer

class BattleTargetStatusEffectAI(BattleStatusEffectAI):

    def __init__(self, battle):
        BattleStatusEffectAI.__init__(self, battle)
        self.battle = battle
        self.statusType = BattleStatusEffectGlobals.BATTLE_STATUS_ROUND
        self.statusEffectName = 'comboDamage'
        self.statusEffectDuration = 2
        self.statusEffectValues = {'20%': 0.20}
        self.statusEffectTargetId = None

    def doEffectOnBattle(self):
        if self.statusEffectTargetId and self.statusEffectDuration > 0:
            target = self.statusEffectTargetId
            if target:
                self.effectedTarget = 1
                target.setComboDamage(target.getActualLevel()*3)

    def reset(self):
        self.statusEffectTargetId.comboDamage = 0