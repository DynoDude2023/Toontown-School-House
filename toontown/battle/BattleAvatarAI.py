#create a class called BattleAvatarAI and inherit from DistributedObjectAI

from direct.distributed.DistributedObjectAI import DistributedObjectAI
from statusEffect import BattleStatusEffectGlobals
from toontown.toonbase.ToontownBattleGlobals import *
from toontown.battle.BattleBase import *
import importlib, random

class BattleAvatarAI(DistributedObjectAI):

    def __init__(self, air, av):
        DistributedObjectAI.__init__(self, air)
        self.air = air
        self.av = av
        self.battle = None
        self.statusEffects = []
        self.statusEffectNames = []
        self.gagTrackDamages = {
            HEAL: 0,
            TRAP: 0,
            LURE: 0,
            SOUND: 0,
            THROW: 0,
            SQUIRT: 0,
            DROP: 0
        }
        self.damageMultiplier = 1.0
        self.comboDamage = 0
        self.damageDefense = 0
        self.attackDamages = {0: 0,
                              1: 0,
                              2: 0,
                              3: 0}
        self.wantedTargetId = 0

    def wantedTarget(self, targetId):
        self.wantedTargetId = targetId
        self.sendUpdate('wantedTarget', [targetId])
    
    def trackAttackDamages(self, damage, toonIndex):
        self.attackDamages[toonIndex] += damage
    
    def setComboDamage(self, damage):
        self.comboDamage += damage
        self.sendUpdate('setComboDamage', [damage])
    
    def addGagDamage(self, damage, gagTrack):
        damage -= self.damageDefense
        self.gagTrackDamages[gagTrack] += damage
        self.sendUpdate('setGagDamage', [damage, gagTrack])
    
    def appendStatusEffect(self, effectName):
        if effectName not in self.statusEffectNames:
            effectFile = importlib.import_module(BattleStatusEffectGlobals.STATUS_FOLDER + '.' + BattleStatusEffectGlobals.STATUS_NAME_2_FILE[effectName])
            effect = effectFile.BattleTargetStatusEffectAI(self.battle)
            effect.setStatusEffectTargetId(self.av)
            self.statusEffectNames.append(effectName)
            self.statusEffects.append(effect)
            self.av.sendUpdate('addStatusEffectVisual', [effectName])
    
    def hasStatusEffect(self, effectName):
        if effectName in self.statusEffectNames:
            return True
        return False

    def calculateRound(self):
        self.gagTrackDamages = {
            HEAL: 0,
            TRAP: 0,
            LURE: 0,
            SOUND: 0,
            THROW: 0,
            SQUIRT: 0,
            DROP: 0
        }
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