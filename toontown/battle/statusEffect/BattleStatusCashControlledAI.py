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
        self.statusType = BattleStatusEffectGlobals.BATTLE_STATUS_INFINITE
        self.statusEffectName = 'cash_controlled'
        self.statusEffectDuration = 2
        self.statusEffectValues = {'20%': 0.20}
        self.statusEffectTargetId = None

    def doEffectOnBattle(self):
        if self.statusEffectTargetId and not self.effectedTarget:
            target = self.statusEffectTargetId
            if target:
                target.damageDefense += 8
                self.effectedTarget = 1
                target.damageMultiplier += .25

    def reset(self):
        self.damageDefense -= 8
        self.damageMultiplier -= .25