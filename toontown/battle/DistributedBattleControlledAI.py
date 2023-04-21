from otp.ai.AIBase import *
from BattleBase import *
from BattleCalculatorControlledAI import *
from toontown.toonbase.ToontownBattleGlobals import *
from SuitBattleGlobals import *
import DistributedBattleAI
from direct.task import Task
from direct.directnotify import DirectNotifyGlobal
import random

class DistributedBattleControlledAI(DistributedBattleAI.DistributedBattleAI):
    
    def __init__(self, air, battleMgr, pos, suit, toonId, zoneId, finishCallback=None, maxSuits=4, tutorialFlag=0, levelFlag=0, interactivePropTrackBonus=-1):
        DistributedBattleAI.DistributedBattleAI.__init__(self, air, battleMgr, pos, suit, toonId, zoneId, finishCallback, maxSuits, tutorialFlag, levelFlag, interactivePropTrackBonus)
        self.battleCalc = BattleCalculatorControlledAI(self, tutorialFlag)