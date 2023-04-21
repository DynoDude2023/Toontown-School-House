from panda3d.core import *
from libotp import *
from direct.interval.IntervalGlobal import *
from BattleBase import *
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import ToontownBattleGlobals
import DistributedBattle
from direct.directnotify import DirectNotifyGlobal
import MovieUtil
from toontown.suit import Suit
from direct.actor import Actor
from toontown.toon import TTEmote
from otp.avatar import Emote
import SuitBattleGlobals
from toontown.distributed import DelayDelete
import random

class DistributedBattleControlled(DistributedBattle.DistributedBattle):
    
    def __init__(self, cr):
        self.cr = cr
        DistributedBattle.DistributedBattle.__init__(self, cr)