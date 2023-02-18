#create a class called BattleAvatarAI and inherit from DistributedObjectAI

from direct.distributed.DistributedObjectAI import DistributedObjectAI
from statusEffect import BattleStatusEffectGlobals
import importlib

class BattleAvatarAI(DistributedObjectAI):

    def __init__(self, air, av):
        DistributedObjectAI.__init__(self, air)
        self.air = air
        self.av = av
        self.battle = None
        self.statusEffects = []
        self.statusEffectNames = []

        self.damageMultiplier = 1.0

    def appendStatusEffect(self, effectName):
        if effectName not in self.statusEffectNames:
            effectFile = importlib.import_module(BattleStatusEffectGlobals.STATUS_FOLDER + '.' + BattleStatusEffectGlobals.STATUS_NAME_2_FILE[effectName])
            effect = effectFile.BattleTargetStatusEffectAI(self.battle)
            effect.setStatusEffectTargetId(self.av)
            self.statusEffectNames.append(effectName)
            self.statusEffects.append(effect)
            self.av.sendUpdate('addStatusEffectVisual', [effectName])

    def calculateRound(self):
        for effect in self.statusEffects:
            if effect.getStatusEffectDuration() > 0 and not effect.effectedTarget:
                effect.doEffectOnBattle()
            effect.calculateDuration()
            print('Suit has status effect: ' + effect.getStatusEffectName())

            if effect.getStatusEffectDuration() <= 0:
                print('Suit status effect has worn off')
                effect.reset()
                self.statusEffects.remove(effect)
                self.statusEffectNames.remove(effect.getStatusEffectName())
                self.av.sendUpdate('removeStatusEffectVisual', [effect.getStatusEffectName()])