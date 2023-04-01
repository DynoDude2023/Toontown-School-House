from panda3d.core import *
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import ToontownBattleGlobals
from toontown.battle import SuitBattleGlobals
from toontown.toonbase import TTLocalizer
import HolidayDecorator
import HalloweenHolidayDecorator
import CrashedLeaderBoardDecorator
from direct.interval.IntervalGlobal import *
import calendar
from copy import deepcopy
from toontown.speedchat import TTSCJellybeanJamMenu
decorationHolidays = [ToontownGlobals.WINTER_DECORATIONS,
 ToontownGlobals.WACKY_WINTER_DECORATIONS,
 ToontownGlobals.HALLOWEEN_PROPS,
 ToontownGlobals.SPOOKY_PROPS,
 ToontownGlobals.HALLOWEEN_COSTUMES,
 ToontownGlobals.SPOOKY_COSTUMES,
 ToontownGlobals.CRASHED_LEADERBOARD]
promotionalSpeedChatHolidays = [ToontownGlobals.ELECTION_PROMOTION]

# Formatted by Jake S. - You're welcome!
SuitAttributes = {'f': {'name': TTLocalizer.SuitFlunky, # cog name
       'singularname': TTLocalizer.SuitFlunkyS, # cogs singular name, for tasks
       'pluralname': TTLocalizer.SuitFlunkyP, # cogs plural name, for tasks
       'level': 0, # level the cog starts at (level - 1)
       'hp':(6,12,20,30,42), # cogs hp (more numbers, more levels)
       'def':(2,5,10,12,15), # cogs defence (more numbers, more levels)
       'freq':(50,30,10,5,5), # cogs level frequency
       'acc':(35,40,45,50,55), # cogs accuracy (more numbers, more levels)
       'attacks':
                (('PoundKey',
                    (2,2,3,4,6), # attack damage
                    (75,75,80,80,90), # attack accuracy
                    (30,35,40,45,50)), # move frequency (all move frequency of each attack must add up to 100, for example 30,10,60 from level 1 of each attack)
                ('Shred',
                    (3,4,5,6,7),
                    (50,55,60,65,70),
                    (10,15,20,25,30)),
                ('ClipOnTie',
                    (1,1,2,2,3),
                    (75,80,85,90,95),
                    (60,50,40,30,20)))},
 'p': {'name': TTLocalizer.SuitPencilPusher,
       'singularname': TTLocalizer.SuitPencilPusherS,
       'pluralname': TTLocalizer.SuitPencilPusherP,
       'level': 1,
       'hp':(12,20,30,42,56),
       'def':(5,10,15,20,25),
       'freq':(50,30,10,5,5),
       'acc':(45,50,55,60,65),
       'attacks':
                (('FountainPen',
                    (2,3,4,6,9),
                    (75,75,75,75,75),
                    (20,20,20,20,20)),
                ('RubOut',
                    (4,5,6,8,12),
                    (75,75,75,75,75),
                    (20,20,20,20,20)),
                ('FingerWag',
                    (1,2,2,3,4),
                    (75,75,75,75,75),
                    (35,30,25,20,15)),
                ('WriteOff',
                    (4,6,8,10,12),
                    (75,75,75,75,75),
                    (5,10,15,20,25)),
                ('FillWithLead',
                    (3,4,5,6,7),
                    (75,75,75,75,75),
                    (20,20,20,20,20)))},
 'ym': {'name': TTLocalizer.SuitYesman,
        'singularname': TTLocalizer.SuitYesmanS,
        'pluralname': TTLocalizer.SuitYesmanP,
        'level': 2,
        'hp':(20,30,42,56,72),
        'def':(10,15,20,25,30),
        'freq':(50,30,10,5,5),
        'acc':(65,70,75,80,85),
        'attacks':
                (('RubberStamp',
                    (2,2,3,3,4),
                    (75,75,75,75,75),
                    (35,35,35,35,35)),
                ('RazzleDazzle',
                    (1,1,1,1,1),
                    (50,50,50,50,50),
                    (25,20,15,10,5)),
                ('Synergy',
                    (4,5,6,7,8),
                    (50,60,70,80,90),
                    (5,10,15,20,25)),
                ('TeeOff',
                    (3,3,4,4,5),
                    (50,60,70,80,90),
                    (35,35,35,35,35)))},
 'mm': {'name': TTLocalizer.SuitMicromanager,
        'singularname': TTLocalizer.SuitMicromanagerS,
        'pluralname': TTLocalizer.SuitMicromanagerP,
        'level': 3,
        'hp':(30,42,56,72,90),
        'def':(15,20,25,30,35),
        'freq':(50,30,10,5,5),
        'acc':(70,75,80,82,85),
        'attacks':
                (('Demotion',
                    (6,8,12,15,18),
                    (50,60,70,80,90),
                    (30,30,30,30,30)),
                ('FingerWag',
                    (4,6,9,12,15),
                    (50,60,70,80,90),
                    (10,10,10,10,10)),
                ('FountainPen',
                    (3,4,6,8,10),
                    (50,60,70,80,90),
                    (15,15,15,15,15)),
                ('BrainStorm',
                    (4,6,9,12,15),
                    (5,5,5,5,5),
                    (25,25,25,25,25)),
                ('BuzzWord',
                    (4,6,9,12,15),
                    (50,60,70,80,90),
                    (20,20,20,20,20)))},
 'ds': {'name': TTLocalizer.SuitDownsizer,
        'singularname': TTLocalizer.SuitDownsizerS,
        'pluralname': TTLocalizer.SuitDownsizerP,
        'level': 4,
        'hp':(42,56,72,90,110),
        'def':(20,25,30,35,40),
        'freq':(50,30,10,5,5),
        'acc':(35,40,45,50,55),
        'attacks':
                (('Canned',
                    (5,6,8,10,12),
                    (60,75,80,85,90),
                    (25,25,25,25,25)),
                ('Downsize',
                    (8,9,11,13,15),
                    (50,65,70,75,80),
                    (35,35,35,35,35)),
                ('PinkSlip',
                    (4,5,6,7,8),
                    (60,65,75,80,85),
                    (25,25,25,25,25)),
                ('Sacked',
                    (5,6,7,8,9),
                    (50,50,50,50,50),
                    (15,15,15,15,15)))},
 'hh': {'name': TTLocalizer.SuitHeadHunter,
        'singularname': TTLocalizer.SuitHeadHunterS,
        'pluralname': TTLocalizer.SuitHeadHunterP,
        'level': 5,
        'hp':(56,72,90,110,132),
        'def':(25,30,35,40,45),
        'freq':(50,30,10,5,5),
        'acc':(35,40,45,50,55),
        'attacks':
                (('FountainPen',
                    (5,6,8,10,12),
                    (60,75,80,85,90),
                    (15,15,15,15,15)),
                ('GlowerPower',
                    (7,8,10,12,13),
                    (50,60,70,80,90),
                    (20,20,20,20,20)),
                ('HalfWindsor',
                    (8,10,12,14,16),
                    (60,65,70,75,80),
                    (20,20,20,20,20)),
                ('HeadShrink',
                    (10,12,15,18,21),
                    (65,75,80,85,95),
                    (35,35,35,35,35)),
                ('Rolodex',
                    (6,7,8,9,10),
                    (60,65,70,75,80),
                    (10,10,10,10,10)))},
 'cr': {'name': TTLocalizer.SuitCorporateRaider,
        'singularname': TTLocalizer.SuitCorporateRaiderS,
        'pluralname': TTLocalizer.SuitCorporateRaiderP,
        'level': 6,
        'hp':(72,90,110,132,156),
        'def':(30,35,40,45,50),
        'freq':(50,30,10,5,5),
        'acc':(35,40,45,50,55),
        'attacks':
            (('Canned',
                (6,7,8,9,10),
                (60,75,80,85,90),
                (20,20,20,20,20)),
            ('EvilEye',
                (12,15,18,21,24),
                (60,70,75,80,90),
                (35,35,35,35,35)),
            ('PlayHardball',
                (7,8,12,15,16),
                (60,65,70,75,80),
                (30,30,30,30,30)),
            ('PowerTie',
                (10,12,14,16,18),
                (65,75,80,85,95),
                (15,15,15,15,15)))},
 'tbc': {'name': TTLocalizer.SuitTheBigCheese,
         'singularname': TTLocalizer.SuitTheBigCheeseS,
         'pluralname': TTLocalizer.SuitTheBigCheeseP,
         'level': 7,
         'hp':(90,110,132,156,200,462,992,1722,2652,3382,4112,4842,5572,6302),
         'def':(35,40,45,50,55,60,65,70,70,70,70,70,70,70),
         'freq':(50,30,10,5,5),
         'acc':(35,40,45,50,55,60,65,70,70,70,70,70,70,70),
         'attacks':
                (('CigarSmoke',
                    (10,12,15,18,20,22,23,24,25,26,27,28,29,30),
                    (55,65,75,85,95,95,95,95,95,95,95,95,95,95),
                    (20,20,20,20,20,20,20,20,20,20,20,20,20,20)),
                ('FloodTheMarket',
                    (14,16,18,20,22,23,23,24,25,26,27,28,29,30),
                    (70,75,85,90,95,95,95,95,95,95,95,95,95,95),
                    (10,10,10,10,10,10,10,10,10,10,10,10,10,10)),
                ('SongAndDance',
                    (14,15,17,19,20,21,22,23,24,25,26,27,28,29),
                    (60,65,70,75,80,85,90,90,90,90,90,90,90,90),
                    (20,20,20,20,20,20,20,20,20,20,20,20,20,20)),
                ('TeeOff',
                    (8,11,14,17,20,21,21,22,22,23,23,24,24,25),
                    (55,65,70,75,80,85,90,90,90,90,90,90,90,90),
                    (50,50,50,50,50,50,50,50,50,50,50,50,50,50)))},
 'cc': {'name': TTLocalizer.SuitColdCaller,
        'singularname': TTLocalizer.SuitColdCallerS,
        'pluralname': TTLocalizer.SuitColdCallerP,
        'level': 0,
        'hp':(6,12,20,30,42),
        'def':(2,5,10,12,15),
        'freq':(50,30,10,5,5),
        'acc':(35,40,45,50,55),
        'attacks':
                (('FreezeAssets',
                    (1,1,1,1,1),
                    (90,90,90,90,90),
                    (5,10,15,20,25)),
                ('PoundKey',
                    (2,2,3,4,5),
                    (75,80,85,90,95),
                    (25,25,25,25,25)),
                ('DoubleTalk',
                    (2,3,4,6,8),
                    (50,55,60,65,70),
                    (25,25,25,25,25)),
                ('HotAir',
                    (3,4,6,8,10),
                    (50,50,50,50,50),
                    (45,40,35,30,25)))},
 'tm': {'name': TTLocalizer.SuitTelemarketer,
        'singularname': TTLocalizer.SuitTelemarketerS,
        'pluralname': TTLocalizer.SuitTelemarketerP,
        'level': 1,
        'hp':(12,20,30,42,56),
        'def':(5,10,15,20,25),
        'freq':(50,30,10,5,5),
        'acc':(45,50,55,60,65),
        'attacks':
                (('ClipOnTie',
                    (2,2,3,3,4),
                    (75,75,75,75,75),
                    (15,15,15,15,15)),
                ('PickPocket',
                    (1,1,1,1,1),
                    (75,75,75,75,75),
                    (15,15,15,15,15)),
                ('Rolodex',
                    (4,6,7,9,12),
                    (50,50,50,50,50),
                    (30,30,30,30,30)),
                ('DoubleTalk',
                    (4,6,7,9,12),
                    (75,80,85,90,95),
                    (40,40,40,40,40)))},
 'nd': {'name': TTLocalizer.SuitNameDropper,
        'singularname': TTLocalizer.SuitNameDropperS,
        'pluralname': TTLocalizer.SuitNameDropperP,
        'level': 2,
        'hp':(20,30,42,56,72),
        'def':(10,15,20,25,30),
        'freq':(50,30,10,5,5),
        'acc':(65,70,75,80,85),
        'attacks':
                (('RazzleDazzle',
                    (4,5,6,9,12),
                    (75,80,85,90,95),
                    (30,30,30,30,30)),
                ('Rolodex',
                    (5,6,7,10,14),
                    (95,95,95,95,95),
                    (40,40,40,40,40)),
                ('Synergy',
                    (3,4,6,9,12),
                    (50,50,50,50,50),
                    (15,15,15,15,15)),
                ('PickPocket',
                    (2,2,2,2,2),
                    (95,95,95,95,95),
                    (15,15,15,15,15)))},
 'gh': {'name': TTLocalizer.SuitGladHander,
        'singularname': TTLocalizer.SuitGladHanderS,
        'pluralname': TTLocalizer.SuitGladHanderP,
        'level': 3,
        'hp':(30,42,56,72,90),
        'def':(15,20,25,30,35),
        'freq':(50,30,10,5,5),
        'acc':(70,75,80,82,85),
        'attacks':
                (('RubberStamp',
                    (4,3,3,2,1),
                    (90,70,50,30,10),
                    (40,30,20,10,5)),
                ('FountainPen',
                    (3,3,2,1,1),
                    (70,60,50,40,30),
                    (40,30,20,10,5)),
                ('Filibuster',
                    (4,6,9,12,15),
                    (30,40,50,60,70),
                    (10,20,30,40,45)),
                ('Schmooze',
                    (5,7,11,15,20),
                    (55,65,75,85,95),
                    (10,20,30,40,45)))},
 'ms': {'name': TTLocalizer.SuitMoverShaker,
        'singularname': TTLocalizer.SuitMoverShakerS,
        'pluralname': TTLocalizer.SuitMoverShakerP,
        'level': 4,
        'hp':(42,56,72,90,110),
        'def':(20,25,30,35,40),
        'freq':(50,30,10,5,5),
        'acc':(35,40,45,50,55),
        'attacks':
                (('BrainStorm',
                    (5,6,8,10,12),
                    (60,75,80,85,90),
                    (15,15,15,15,15)),
                ('HalfWindsor',
                    (6,9,11,13,16),
                    (50,65,70,75,80),
                    (20,20,20,20,20)),
                ('Quake',
                    (9,12,15,18,21),
                    (60,65,75,80,85),
                    (20,20,20,20,20)),
                ('Shake',
                    (6,8,10,12,14),
                    (70,75,80,85,90),
                    (25,25,25,25,25)),
                ('Tremor',
                    (5,6,7,8,9),
                    (50,50,50,50,50),
                    (20,20,20,20,20)))},
 'tf': {'name': TTLocalizer.SuitTwoFace,
        'singularname': TTLocalizer.SuitTwoFaceS,
        'pluralname': TTLocalizer.SuitTwoFaceP,
        'level': 5,
        'hp':(56,72,90,110,132),
        'def':(25,30,35,40,45),
        'freq':(50,30,10,5,5),
        'acc':(35,40,45,50,55),
        'attacks':
                (('EvilEye',
                    (10,12,14,16,18),
                    (60,75,80,85,90),
                    (30,30,30,30,30)),
                ('HangUp',
                    (7,8,10,12,13),
                    (50,60,70,80,90),
                    (15,15,15,15,15)),
                ('RazzleDazzle',
                    (8,10,12,14,16),
                    (60,65,70,75,80),
                    (30,30,30,30,30)),
                ('RedTape',
                    (6,7,8,9,10),
                    (60,65,75,85,90),
                    (25,25,25,25,25)))},
 'm': {'name': TTLocalizer.SuitTheMingler,
       'singularname': TTLocalizer.SuitTheMinglerS,
       'pluralname': TTLocalizer.SuitTheMinglerP,
       'level': 6,
       'hp':(72,90,110,132,156),
       'def':(30,35,40,45,50),
       'freq':(50,30,10,5,5),
       'acc':(35,40,45,50,55),
       'attacks':
               (('BuzzWord',
                    (10,11,13,15,16),
                    (60,75,80,85,90),
                    (20,20,20,20,20)),
                ('ParadigmShift',
                    (12,15,18,21,24),
                    (60,70,75,80,90),
                    (25,25,25,25,25)),
                ('PowerTrip',
                    (10,13,14,15,18),
                    (60,65,70,75,80),
                    (15,15,15,15,15)),
                ('Schmooze',
                    (7,8,12,15,16),
                    (55,65,75,85,95),
                    (30,30,30,30,30)),
                ('TeeOff',
                    (8,9,10,11,12),
                    (70,75,80,85,95),
                    (10,10,10,10,10)))},
 'mh': {'name': TTLocalizer.SuitMrHollywood,
        'singularname': TTLocalizer.SuitMrHollywoodS,
        'pluralname': TTLocalizer.SuitMrHollywoodP,
        'level': 7,
        'hp':(90,110,132,156,200,462,992,1722,2652,3382,4112,4842,5572,6302),
        'def':(35,40,45,50,55,60,65,70,70,70,70,70,70,70),
        'freq':(50,30,10,5,5),
        'acc':(35,40,45,50,55,60,65,70,70,70,70,70,70,70),
        'attacks':
                (('PowerTrip',
                    (10,12,15,18,20,22,24,26,28,30,32,34,36,38),
                    (55,65,75,85,95,95,95,95,95,95,95,95,95,95),
                    (50,50,50,50,50,50,50,50,50,50,50,50,50,50)),
                ('RazzleDazzle',
                    (8,11,14,17,20,22,24,26,28,30,32,34,36,38),
                    (70,75,85,90,95,95,95,95,95,95,95,95,95,95),
                    (50,50,50,50,50,50,50,50,50,50,50,50,50,50)))},
 'sc': {'name': TTLocalizer.SuitShortChange,
        'singularname': TTLocalizer.SuitShortChangeS,
        'pluralname': TTLocalizer.SuitShortChangeP,
        'level': 0,
        'hp':(6,12,20,30,42),
        'def':(2,5,10,12,15),
        'freq':(50,30,10,5,5),
        'acc':(35,40,45,50,55),
        'attacks':
                (('Watercooler',
                    (2,2,3,4,6),
                    (50,50,50,50,50),
                    (20,20,20,20,20)),
                ('BounceCheck',
                    (3,5,7,9,11),
                    (75,80,85,90,95),
                    (15,15,15,15,15)),
                ('ClipOnTie',
                    (1,1,2,2,3),
                    (50,50,50,50,50),
                    (25,25,25,25,25)),
                ('PickPocket',
                    (2,2,3,4,6),
                    (95,95,95,95,95),
                    (40,40,40,40,40)))},
 'pp': {'name': TTLocalizer.SuitPennyPincher,
        'singularname': TTLocalizer.SuitPennyPincherS,
        'pluralname': TTLocalizer.SuitPennyPincherP,
        'level': 1,
        'hp':(12,20,30,42,56),
        'def':(5,10,15,20,25),
        'freq':(50,30,10,5,5),
        'acc':(45,50,55,60,65),
        'attacks':
                (('BounceCheck',
                    (4,5,6,8,12),
                    (75,75,75,75,75),
                    (45,45,45,45,45)),
                ('FreezeAssets',
                    (2,3,4,6,9),
                    (75,75,75,75,75),
                    (20,20,20,20,20)),
                ('FingerWag',
                    (1,2,3,4,6),
                    (50,50,50,50,50),
                    (35,35,35,35,35)))},
 'tw': {'name': TTLocalizer.SuitTightwad,
        'singularname': TTLocalizer.SuitTightwadS,
        'pluralname': TTLocalizer.SuitTightwadP,
        'level': 2,
        'hp':(20,30,42,56,72),
        'def':(10,15,20,25,30),
        'freq':(50,30,10,5,5),
        'acc':(65,70,75,80,85),
        'attacks':
                (('Fired',
                    (3,4,5,5,6),
                    (75,75,75,75,75),
                    (75,5,5,5,5)),
                ('GlowerPower',
                    (3,4,6,9,12),
                    (95,95,95,95,95),
                    (10,15,20,25,30)),
                ('FingerWag',
                    (3,3,4,4,5),
                    (75,75,75,75,75),
                    (5,70,5,5,5)),
                ('FreezeAssets',
                    (3,4,6,9,12),
                    (75,75,75,75,75),
                    (5,5,65,5,30)),
                ('BounceCheck',
                    (5,6,9,13,18),
                    (75,75,75,75,75),
                    (5,5,5,60,30)))},
 'bc': {'name': TTLocalizer.SuitBeanCounter,
        'singularname': TTLocalizer.SuitBeanCounterS,
        'pluralname': TTLocalizer.SuitBeanCounterP,
        'level': 3,
        'hp':(30,42,56,72,90),
        'def':(15,20,25,30,35),
        'freq':(50,30,10,5,5),
        'acc':(70,75,80,82,85),
        'attacks':
                (('Audit',
                    (4,6,9,12,15),
                    (95,95,95,95,95),
                    (20,20,20,20,20)),
                ('Calculate',
                    (4,6,9,12,15),
                    (75,75,75,75,75),
                    (25,25,25,25,25)),
                ('Tabulate',
                    (4,6,9,12,15),
                    (75,75,75,75,75),
                    (25,25,25,25,25)),
                ('WriteOff',
                    (4,6,9,12,15),
                    (95,95,95,95,95),
                    (30,30,30,30,30)))},
 'nc': {'name': TTLocalizer.SuitNumberCruncher,
        'singularname': TTLocalizer.SuitNumberCruncherS,
        'pluralname': TTLocalizer.SuitNumberCruncherP,
        'level': 4,
        'hp':(42,56,72,90,110),
        'def':(20,25,30,35,40),
        'freq':(50,30,10,5,5),
        'acc':(35,40,45,50,55),
        'attacks':
                (('Audit',
                    (5,6,8,10,12),
                    (60,75,80,85,90),
                    (15,15,15,15,15)),
                ('Calculate',
                    (6,7,9,11,13),
                    (50,65,70,75,80),
                    (30,30,30,30,30)),
                ('Crunch',
                    (8,9,11,13,15),
                    (60,65,75,80,85),
                    (35,35,35,35,35)),
                ('Tabulate',
                    (5,6,7,8,9),
                    (50,50,50,50,50),
                    (20,20,20,20,20)))},
 'mb': {'name': TTLocalizer.SuitMoneyBags,
        'singularname': TTLocalizer.SuitMoneyBagsS,
        'pluralname': TTLocalizer.SuitMoneyBagsP,
        'level': 5,
        'hp':(56,72,90,110,132),
        'def':(25,30,35,40,45),
        'freq':(50,30,10,5,5),
        'acc':(35,40,45,50,55),
        'attacks':
                (('Liquidate',
                    (10,12,14,16,18),
                    (60,75,80,85,90),
                    (30,30,30,30,30)),
                ('MarketCrash',
                    (8,10,12,14,16),
                    (60,65,70,75,80),
                    (45,45,45,45,45)),
                ('PowerTie',
                    (6,7,8,9,10),
                    (60,65,75,85,90),
                    (25,25,25,25,25)))},
 'ls': {'name': TTLocalizer.SuitLoanShark,
        'singularname': TTLocalizer.SuitLoanSharkS,
        'pluralname': TTLocalizer.SuitLoanSharkP,
        'level': 6,
        'hp':(72,90,110,132,156),
        'def':(30,35,40,45,50),
        'freq':(50,30,10,5,5),
        'acc':(35,40,45,50,55),
        'attacks':
                (('Bite',
                    (10,11,13,15,16),
                    (60,75,80,85,90),
                    (30,30,30,30,30)),
                ('Chomp',
                    (12,15,18,21,24),
                    (60,70,75,80,90),
                    (35,35,35,35,35)),
                ('PlayHardball',
                    (9,11,12,13,15),
                    (55,65,75,85,95),
                    (20,20,20,20,20)),
                ('WriteOff',
                    (6,8,10,12,14),
                    (70,75,80,85,95),
                    (15,15,15,15,15)))},
 'rb': {'name': TTLocalizer.SuitRobberBaron,
        'singularname': TTLocalizer.SuitRobberBaronS,
        'pluralname': TTLocalizer.SuitRobberBaronP,
        'level': 7,
        'hp':(90,110,132,156,200,462,992,1722,2652,3382,4112,4842,5572,6302),
        'def':(35,40,45,50,55,60,65,70,70,70,70,70,70,70),
        'freq':(50,30,10,5,5),
        'acc':(35,40,45,50,55,60,65,70,70,70,70,70,70,70),
        'attacks':
                (('PowerTrip',
                    (11,14,16,18,21,22,23,24,25,26,27,28,29,30),
                    (60,65,70,75,80,80,80,85,90,90,90,90,90,90),
                    (50,50,50,50,50,50,50,50,50,50,50,50,50,50)),
                ('TeeOff',
                    (10,12,14,16,18,20,22,24,26,27,28,29,30,31),
                    (60,65,75,85,90,90,90,90,95,95,95,95,95,95),
                    (50,50,50,50,50,50,50,50,50,50,50,50,50,50)))},

 'bf': {'name': TTLocalizer.SuitBottomFeeder,
        'singularname': TTLocalizer.SuitBottomFeederS,
        'pluralname': TTLocalizer.SuitBottomFeederP,
        'level': 0,
        'hp':(6,12,20,30,42),
        'def':(2,5,10,12,15),
        'freq':(50,30,10,5,5),
        'acc':(35,40,45,50,55),
        'attacks':
                (('RubberStamp',
                    (2,3,4,5,6),
                    (75,80,85,90,95),
                    (20,20,20,20,20)),
                ('Shred',
                    (2,4,6,8,10),
                    (50,55,60,65,70),
                    (20,20,20,20,20)),
                ('Watercooler',
                    (3,4,5,6,7),
                    (95,95,95,95,95),
                    (10,10,10,10,10)),
                ('PickPocket',
                    (1,1,2,2,3),
                    (25,30,35,40,45),
                    (50,50,50,50,50)))},
 'b': {'name': TTLocalizer.SuitBloodsucker,
       'singularname': TTLocalizer.SuitBloodsuckerS,
       'pluralname': TTLocalizer.SuitBloodsuckerP,
       'level': 1,
       'hp':(12,20,30,42,56),
       'def':(5,10,15,20,25),
       'freq':(50,30,10,5,5),
       'acc':(45,50,55,60,65),
       'attacks':
                (('EvictionNotice',
                    (1,2,3,3,4),
                    (75,75,75,75,75),
                    (20,20,20,20,20)),
                ('RedTape',
                    (2,3,4,6,9),
                    (75,75,75,75,75),
                    (20,20,20,20,20)),
                ('Withdrawal',
                    (6,8,10,12,14),
                    (95,95,95,95,95),
                    (10,10,10,10,10)),
                ('Liquidate',
                    (2,3,4,6,9),
                    (50,60,70,80,90),
                    (50,50,50,50,50)))},
 'dt': {'name': TTLocalizer.SuitDoubleTalker,
        'singularname': TTLocalizer.SuitDoubleTalkerS,
        'pluralname': TTLocalizer.SuitDoubleTalkerP,
        'level': 2,
        'hp':(20,30,42,56,72),
        'def':(10,15,20,25,30),
        'freq':(50,30,10,5,5),
        'acc':(65,70,75,80,85),
        'attacks':
                (('RubberStamp',
                    (1,1,1,1,1),
                    (50,60,70,80,90),
                    (5,5,5,5,5)),
                ('BounceCheck',
                    (1,1,1,1,1),
                    (50,60,70,80,90),
                    (5,5,5,5,5)),
                ('BuzzWord',
                    (1,2,3,5,6),
                    (50,60,70,80,90),
                    (20,20,20,20,20)),
                ('DoubleTalk',
                    (6,6,9,13,18),
                    (50,60,70,80,90),
                    (25,25,25,25,25)),
                ('Jargon',
                    (3,4,6,9,12),
                    (50,60,70,80,90),
                    (25,25,25,25,25)),
                ('MumboJumbo',
                    (3,4,6,9,12),
                    (50,60,70,80,90),
                    (20,20,20,20,20)))},
 'ac': {'name': TTLocalizer.SuitAmbulanceChaser,
        'singularname': TTLocalizer.SuitAmbulanceChaserS,
        'pluralname': TTLocalizer.SuitAmbulanceChaserP,
        'level': 3,
        'hp':(30,42,56,72,90),
        'def':(15,20,25,30,35),
        'freq':(50,30,10,5,5),
        'acc':(65,70,75,80,85),
        'attacks':
                (('Shake',
                    (4,6,9,12,15),
                    (75,75,75,75,75),
                    (15,15,15,15,15)),
                ('RedTape',
                    (6,8,12,15,19),
                    (75,75,75,75,75),
                    (30,30,30,30,30)),
                ('Rolodex',
                    (3,4,5,6,7),
                    (75,75,75,75,75),
                    (20,20,20,20,20)),
                ('HangUp',
                    (2,3,4,5,6),
                    (75,75,75,75,75),
                    (35,35,35,35,35)))},
 'bs': {'name': TTLocalizer.SuitBackStabber,
        'singularname': TTLocalizer.SuitBackStabberS,
        'pluralname': TTLocalizer.SuitBackStabberP,
        'level': 4,
        'hp':(42,56,72,90,110),
        'def':(20,25,30,35,40),
        'freq':(50,30,10,5,5),
        'acc':(35,40,45,50,55),
        'attacks':
                (('GuiltTrip',
                    (8,11,13,15,18),
                    (60,75,80,85,90),
                    (40,40,40,40,40)),
                ('RestrainingOrder',
                    (6,7,9,11,13),
                    (50,65,70,75,90),
                    (25,25,25,25,25)),
                ('FingerWag',
                    (5,6,7,8,9),
                    (50,55,65,75,80),
                    (35,35,35,35,35)))},
 'sd': {'name': TTLocalizer.SuitSpinDoctor,
        'singularname': TTLocalizer.SuitSpinDoctorS,
        'pluralname': TTLocalizer.SuitSpinDoctorP,
        'level': 5,
        'hp':(56,72,90,110,132),
        'def':(25,30,35,40,45),
        'freq':(50,30,10,5,5),
        'acc':(35,40,45,50,55),
        'attacks':
                (('ParadigmShift',
                    (9,10,13,16,17),
                    (60,75,80,85,90),
                    (30,30,30,30,30)),
                ('Quake',
                    (8,10,12,14,16),
                    (60,65,70,75,80),
                    (20,20,20,20,20)),
                ('Spin',
                    (10,12,15,18,20),
                    (70,75,80,85,90),
                    (35,35,35,35,35)),
                ('WriteOff',
                    (6,7,8,9,10),
                    (60,65,75,85,90),
                    (15,15,15,15,15)))},
 'le': {'name': TTLocalizer.SuitLegalEagle,
        'singularname': TTLocalizer.SuitLegalEagleS,
        'pluralname': TTLocalizer.SuitLegalEagleP,
        'level': 6,
        'hp':(72,90,110,132,156),
        'def':(30,35,40,45,50),
        'freq':(50,30,10,5,5),
        'acc':(35,40,45,50,55),
        'attacks':
                (('EvilEye',
                    (10,11,13,15,16),
                    (60,75,80,85,90),
                    (20,20,20,20,20)),
                ('Jargon',
                    (7,9,11,13,15),
                    (60,70,75,80,90),
                    (15,15,15,15,15)),
                ('Legalese',
                    (11,13,16,19,21),
                    (55,65,75,85,95),
                    (35,35,35,35,35)),
                ('PeckingOrder',
                    (12,15,17,19,22),
                    (70,75,80,85,95),
                    (30,30,30,30,30)))},
 'bw': {'name': TTLocalizer.SuitBigWig,
        'singularname': TTLocalizer.SuitBigWigS,
        'pluralname': TTLocalizer.SuitBigWigP,
        'level': 7,
        'hp':(90,110,132,156,200,462,992,1722,2652,3382,4112,4842,5572,6302),
        'def':(35,40,45,50,55,60,65,70,70,70,70,70,70,70),
        'freq':(50,30,10,5,5),
        'acc':(35,40,45,50,55,60,65,70,70,70,70,70,70,70),
        'attacks':
                (('PowerTrip',
                    (10,11,13,15,16,18,20,21,23,24,25,25,26,27),
                    (75,80,85,90,95,95,95,95,95,95,95,95,95,95),
                    (50,50,50,50,50,50,50,50,50,50,50,50,50,50)),
                ('ThrowBook',
                    (13,15,17,19,21,23,25,27,29,32,34,36,38,40),
                    (80,85,85,85,90,90,90,90,95,95,95,95,95,95),
                    (50,50,50,50,50,50,50,50,50,50,50,50,50,50)))}}

class NewsManager(DistributedObject.DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('NewsManager')
    neverDisable = 1
    YearlyHolidayType = 1
    OncelyHolidayType = 2
    RelativelyHolidayType = 3
    OncelyMultipleStartHolidayType = 4

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        self.population = 0
        self.invading = 0
        self.decorationHolidayIds = []
        self.holidayDecorator = None
        self.holidayIdList = []
        base.cr.newsManager = self
        base.localAvatar.inventory.setInvasionCreditMultiplier(1)
        self.weeklyCalendarHolidays = []
        return

    def delete(self):
        self.cr.newsManager = None
        if self.holidayDecorator:
            self.holidayDecorator.exit()
        DistributedObject.DistributedObject.delete(self)
        return

    def setPopulation(self, population):
        self.population = population
        messenger.send('newPopulation', [population])

    def getPopulation(self):
        return population

    def sendSystemMessage(self, message, style):
        base.localAvatar.setSystemMessage(style, message)

    def setInvasionStatus(self, msgType, cogType, numRemaining, skeleton):
        self.notify.info('setInvasionStatus: msgType: %s cogType: %s, numRemaining: %s, skeleton: %s' % (msgType,
         cogType,
         numRemaining,
         skeleton))
        cogName = SuitAttributes[cogType]['name']
        cogNameP = SuitAttributes[cogType]['pluralname']
        if skeleton:
            cogName = TTLocalizer.Skeleton
            cogNameP = TTLocalizer.SkeletonP
        if msgType == ToontownGlobals.SuitInvasionBegin:
            msg1 = TTLocalizer.SuitInvasionBegin1
            msg2 = TTLocalizer.SuitInvasionBegin2 % cogNameP
            self.invading = 1
        elif msgType == ToontownGlobals.SuitInvasionUpdate:
            msg1 = TTLocalizer.SuitInvasionUpdate1 % numRemaining
            msg2 = TTLocalizer.SuitInvasionUpdate2 % cogNameP
            self.invading = 1
        elif msgType == ToontownGlobals.SuitInvasionEnd:
            msg1 = TTLocalizer.SuitInvasionEnd1 % cogName
            msg2 = TTLocalizer.SuitInvasionEnd2
            self.invading = 0
        elif msgType == ToontownGlobals.SuitInvasionBulletin:
            msg1 = TTLocalizer.SuitInvasionBulletin1
            msg2 = TTLocalizer.SuitInvasionBulletin2 % cogNameP
            self.invading = 1
        else:
            self.notify.warning('setInvasionStatus: invalid msgType: %s' % msgType)
            return
        if self.invading:
            mult = ToontownBattleGlobals.getInvasionMultiplier()
        else:
            mult = 1
        base.localAvatar.inventory.setInvasionCreditMultiplier(mult)
        Sequence(Wait(1.0), Func(base.localAvatar.setSystemMessage, 0, msg1), Wait(5.0), Func(base.localAvatar.setSystemMessage, 0, msg2), name='newsManagerWait', autoPause=1).start()

    def getInvading(self):
        return self.invading

    def startHoliday(self, holidayId):
        if holidayId not in self.holidayIdList:
            self.notify.info('setHolidayId: Starting Holiday %s' % holidayId)
            self.holidayIdList.append(holidayId)
            if holidayId in decorationHolidays:
                self.decorationHolidayIds.append(holidayId)
                if holidayId == ToontownGlobals.HALLOWEEN_PROPS:
                    if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                        base.localAvatar.chatMgr.chatInputSpeedChat.addHalloweenMenu()
                        self.setHalloweenPropsHolidayStart()
                elif holidayId == ToontownGlobals.SPOOKY_PROPS:
                    if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                        base.localAvatar.chatMgr.chatInputSpeedChat.addHalloweenMenu()
                        self.setSpookyPropsHolidayStart()
                elif holidayId == ToontownGlobals.WINTER_DECORATIONS:
                    if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                        base.localAvatar.chatMgr.chatInputSpeedChat.addWinterMenu()
                        self.setWinterDecorationsStart()
                elif holidayId == ToontownGlobals.WACKY_WINTER_DECORATIONS:
                    if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                        base.localAvatar.chatMgr.chatInputSpeedChat.addWinterMenu()
                        self.setWackyWinterDecorationsStart()
                if hasattr(base.cr.playGame, 'dnaStore') and hasattr(base.cr.playGame, 'hood') and hasattr(base.cr.playGame.hood, 'loader'):
                    if holidayId == ToontownGlobals.HALLOWEEN_COSTUMES or holidayId == ToontownGlobals.SPOOKY_COSTUMES:
                        self.holidayDecorator = HalloweenHolidayDecorator.HalloweenHolidayDecorator()
                    elif holidayId == ToontownGlobals.CRASHED_LEADERBOARD:
                        self.holidayDecorator = CrashedLeaderBoardDecorator.CrashedLeaderBoardDecorator()
                    else:
                        self.holidayDecorator = HolidayDecorator.HolidayDecorator()
                    self.holidayDecorator.decorate()
                    messenger.send('decorator-holiday-%d-starting' % holidayId)
            elif holidayId in promotionalSpeedChatHolidays:
                if hasattr(base, 'TTSCPromotionalMenu'):
                    base.TTSCPromotionalMenu.startHoliday(holidayId)
            elif holidayId == ToontownGlobals.MORE_XP_HOLIDAY:
                self.setMoreXpHolidayStart()
            elif holidayId == ToontownGlobals.JELLYBEAN_DAY:
                pass
            elif holidayId == ToontownGlobals.CIRCUIT_RACING_EVENT:
                self.setGrandPrixWeekendStart()
            elif holidayId == ToontownGlobals.HYDRANT_ZERO_HOLIDAY:
                self.setHydrantZeroHolidayStart()
            elif holidayId == ToontownGlobals.APRIL_FOOLS_COSTUMES:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.addAprilToonsMenu()
            elif holidayId == ToontownGlobals.WINTER_CAROLING:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.addCarolMenu()
                    self.setWinterCarolingStart()
            elif holidayId == ToontownGlobals.WACKY_WINTER_CAROLING:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.addCarolMenu()
            elif holidayId == ToontownGlobals.VALENTINES_DAY:
                messenger.send('ValentinesDayStart')
                base.localAvatar.setSystemMessage(0, TTLocalizer.ValentinesDayStart)
            elif holidayId == ToontownGlobals.SILLY_CHATTER_ONE:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.addSillyPhaseOneMenu()
            elif holidayId == ToontownGlobals.SILLY_CHATTER_TWO:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.addSillyPhaseTwoMenu()
            elif holidayId == ToontownGlobals.SILLY_CHATTER_THREE:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.addSillyPhaseThreeMenu()
            elif holidayId == ToontownGlobals.SILLY_CHATTER_FOUR:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.addSillyPhaseFourMenu()
            elif holidayId == ToontownGlobals.SILLY_CHATTER_FIVE:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.addSillyPhaseFiveMenu()
            elif holidayId == ToontownGlobals.VICTORY_PARTY_HOLIDAY:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.addVictoryPartiesMenu()
            elif holidayId == ToontownGlobals.SELLBOT_NERF_HOLIDAY:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    self.setSellbotNerfHolidayStart()
                    base.localAvatar.chatMgr.chatInputSpeedChat.addSellbotNerfMenu()
            elif holidayId == ToontownGlobals.JELLYBEAN_TROLLEY_HOLIDAY or holidayId == ToontownGlobals.JELLYBEAN_TROLLEY_HOLIDAY_MONTH:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.addJellybeanJamMenu(TTSCJellybeanJamMenu.JellybeanJamPhases.TROLLEY)
            elif holidayId == ToontownGlobals.JELLYBEAN_FISHING_HOLIDAY or holidayId == ToontownGlobals.JELLYBEAN_FISHING_HOLIDAY_MONTH:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.addJellybeanJamMenu(TTSCJellybeanJamMenu.JellybeanJamPhases.FISHING)
            elif holidayId == ToontownGlobals.JELLYBEAN_PARTIES_HOLIDAY:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    self.setJellybeanPartiesHolidayStart()
            elif holidayId == ToontownGlobals.JELLYBEAN_PARTIES_HOLIDAY_MONTH:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    self.setJellybeanMonthHolidayStart()
            elif holidayId == ToontownGlobals.BANK_UPGRADE_HOLIDAY:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    self.setBankUpgradeHolidayStart()
            elif holidayId == ToontownGlobals.BLACK_CAT_DAY:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    self.setBlackCatHolidayStart()
            elif holidayId == ToontownGlobals.SPOOKY_BLACK_CAT:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    self.setSpookyBlackCatHolidayStart()
            elif holidayId == ToontownGlobals.TOP_TOONS_MARATHON:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    self.setTopToonsMarathonStart()
            elif holidayId == ToontownGlobals.SELLBOT_INVASION:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.addSellbotInvasionMenu()
            elif holidayId == ToontownGlobals.SELLBOT_FIELD_OFFICE:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.addSellbotFieldOfficeMenu()
            elif holidayId == ToontownGlobals.IDES_OF_MARCH:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    self.setIdesOfMarchStart()
                    base.localAvatar.chatMgr.chatInputSpeedChat.addIdesOfMarchMenu()
            elif holidayId == ToontownGlobals.EXPANDED_CLOSETS:
                self.setExpandedClosetsStart()
            elif holidayId == ToontownGlobals.KARTING_TICKETS_HOLIDAY:
                self.setKartingTicketsHolidayStart()

    def endHoliday(self, holidayId):
        if holidayId in self.holidayIdList:
            self.notify.info('setHolidayId: Ending Holiday %s' % holidayId)
            self.holidayIdList.remove(holidayId)
            if holidayId in self.decorationHolidayIds:
                self.decorationHolidayIds.remove(holidayId)
                if holidayId == ToontownGlobals.HALLOWEEN_PROPS:
                    if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                        base.localAvatar.chatMgr.chatInputSpeedChat.removeHalloweenMenu()
                        self.setHalloweenPropsHolidayEnd()
                elif holidayId == ToontownGlobals.SPOOKY_PROPS:
                    if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                        base.localAvatar.chatMgr.chatInputSpeedChat.removeHalloweenMenu()
                        self.setSpookyPropsHolidayEnd()
                elif holidayId == ToontownGlobals.WINTER_DECORATIONS:
                    if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                        base.localAvatar.chatMgr.chatInputSpeedChat.removeWinterMenu()
                        self.setWinterDecorationsEnd()
                elif holidayId == ToontownGlobals.WACKY_WINTER_DECORATIONS:
                    if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                        base.localAvatar.chatMgr.chatInputSpeedChat.removeWinterMenu()
                if hasattr(base.cr.playGame, 'dnaStore') and hasattr(base.cr.playGame, 'hood') and hasattr(base.cr.playGame.hood, 'loader'):
                    if holidayId == ToontownGlobals.HALLOWEEN_COSTUMES or holidayId == ToontownGlobals.SPOOKY_COSTUMES:
                        self.holidayDecorator = HalloweenHolidayDecorator.HalloweenHolidayDecorator()
                    elif holidayId == ToontownGlobals.CRASHED_LEADERBOARD:
                        self.holidayDecorator = CrashedLeaderBoardDecorator.CrashedLeaderBoardDecorator()
                    else:
                        self.holidayDecorator = HolidayDecorator.HolidayDecorator()
                    self.holidayDecorator.undecorate()
                    messenger.send('decorator-holiday-%d-ending' % holidayId)
            elif holidayId in promotionalSpeedChatHolidays:
                if hasattr(base, 'TTSCPromotionalMenu'):
                    base.TTSCPromotionalMenu.endHoliday(holidayId)
            elif holidayId == ToontownGlobals.MORE_XP_HOLIDAY:
                self.setMoreXpHolidayEnd()
            elif holidayId == ToontownGlobals.JELLYBEAN_DAY:
                pass
            elif holidayId == ToontownGlobals.CIRCUIT_RACING_EVENT:
                self.setGrandPrixWeekendEnd()
            elif holidayId == ToontownGlobals.APRIL_FOOLS_COSTUMES:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.removeAprilToonsMenu()
            elif holidayId == ToontownGlobals.VALENTINES_DAY:
                messenger.send('ValentinesDayStop')
                base.localAvatar.setSystemMessage(0, TTLocalizer.ValentinesDayEnd)
            elif holidayId == ToontownGlobals.SILLY_CHATTER_ONE:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.removeSillyPhaseOneMenu()
            elif holidayId == ToontownGlobals.SILLY_CHATTER_TWO:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.removeSillyPhaseTwoMenu()
            elif holidayId == ToontownGlobals.SILLY_CHATTER_THREE:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.removeSillyPhaseThreeMenu()
            elif holidayId == ToontownGlobals.SILLY_CHATTER_FOUR:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.removeSillyPhaseFourMenu()
            elif holidayId == ToontownGlobals.SILLY_CHATTER_FIVE:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.removeSillyPhaseFiveMenu()
            elif holidayId == ToontownGlobals.VICTORY_PARTY_HOLIDAY:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.removeVictoryPartiesMenu()
            elif holidayId == ToontownGlobals.WINTER_CAROLING:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.removeCarolMenu()
            elif holidayId == ToontownGlobals.WACKY_WINTER_CAROLING:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.removeCarolMenu()
            elif holidayId == ToontownGlobals.SELLBOT_NERF_HOLIDAY:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    self.setSellbotNerfHolidayEnd()
                    base.localAvatar.chatMgr.chatInputSpeedChat.removeSellbotNerfMenu()
            elif holidayId == ToontownGlobals.JELLYBEAN_TROLLEY_HOLIDAY or holidayId == ToontownGlobals.JELLYBEAN_TROLLEY_HOLIDAY_MONTH:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.removeJellybeanJamMenu()
            elif holidayId == ToontownGlobals.JELLYBEAN_FISHING_HOLIDAY or holidayId == ToontownGlobals.JELLYBEAN_FISHING_HOLIDAY_MONTH:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.removeJellybeanJamMenu()
            elif holidayId == ToontownGlobals.JELLYBEAN_PARTIES_HOLIDAY or holidayId == ToontownGlobals.JELLYBEAN_PARTIES_HOLIDAY_MONTH:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    self.setJellybeanPartiesHolidayEnd()
                    base.localAvatar.chatMgr.chatInputSpeedChat.removeJellybeanJamMenu()
            elif holidayId == ToontownGlobals.BLACK_CAT_DAY:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    self.setBlackCatHolidayEnd()
            elif holidayId == ToontownGlobals.SPOOKY_BLACK_CAT:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    self.setSpookyBlackCatHolidayEnd()
            elif holidayId == ToontownGlobals.TOP_TOONS_MARATHON:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    self.setTopToonsMarathonEnd()
            elif holidayId == ToontownGlobals.SELLBOT_INVASION:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.removeSellbotInvasionMenu()
            elif holidayId == ToontownGlobals.SELLBOT_FIELD_OFFICE:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.removeSellbotFieldOfficeMenu()
            elif holidayId == ToontownGlobals.IDES_OF_MARCH:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.removeIdesOfMarchMenu()

    def setHolidayIdList(self, holidayIdList):

        def isEnding(id):
            return id not in holidayIdList

        def isStarting(id):
            return id not in self.holidayIdList

        toEnd = filter(isEnding, self.holidayIdList)
        for endingHolidayId in toEnd:
            self.endHoliday(endingHolidayId)

        toStart = filter(isStarting, holidayIdList)
        for startingHolidayId in toStart:
            self.startHoliday(startingHolidayId)

        messenger.send('setHolidayIdList', [holidayIdList])

    def getDecorationHolidayId(self):
        return self.decorationHolidayIds

    def getHolidayIdList(self):
        return self.holidayIdList

    def setBingoWin(self, zoneId):
        base.localAvatar.setSystemMessage(0, 'Bingo congrats!')

    def setBingoStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.FishBingoStart)

    def setBingoOngoing(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.FishBingoOngoing)

    def setBingoEnd(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.FishBingoEnd)

    def setCircuitRaceStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.CircuitRaceStart)

    def setCircuitRaceOngoing(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.CircuitRaceOngoing)

    def setCircuitRaceEnd(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.CircuitRaceEnd)

    def setTrolleyHolidayStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.TrolleyHolidayStart)

    def setTrolleyHolidayOngoing(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.TrolleyHolidayOngoing)

    def setTrolleyHolidayEnd(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.TrolleyHolidayEnd)

    def setTrolleyWeekendStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.TrolleyWeekendStart)

    def setTrolleyWeekendEnd(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.TrolleyWeekendEnd)

    def setRoamingTrialerWeekendStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.RoamingTrialerWeekendStart)
        base.roamingTrialers = True

    def setRoamingTrialerWeekendOngoing(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.RoamingTrialerWeekendOngoing)
        base.roamingTrialers = True

    def setRoamingTrialerWeekendEnd(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.RoamingTrialerWeekendEnd)
        base.roamingTrialers = False

    def setMoreXpHolidayStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.MoreXpHolidayStart)

    def setMoreXpHolidayOngoing(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.MoreXpHolidayOngoing)

    def setMoreXpHolidayEnd(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.MoreXpHolidayEnd)

    def setJellybeanDayStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.JellybeanDayHolidayStart)

    def setJellybeanDayEnd(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.JellybeanDayHolidayEnd)

    def setGrandPrixWeekendStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.GrandPrixWeekendHolidayStart)

    def setGrandPrixWeekendEnd(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.GrandPrixWeekendHolidayEnd)

    def setHydrantZeroHolidayStart(self):
        messenger.send('HydrantZeroIsRunning', [True])

    def setSellbotNerfHolidayStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.SellbotNerfHolidayStart)

    def setSellbotNerfHolidayEnd(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.SellbotNerfHolidayEnd)

    def setJellybeanTrolleyHolidayStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.JellybeanTrolleyHolidayStart)

    def setJellybeanTrolleyHolidayEnd(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.JellybeanTrolleyHolidayEnd)

    def setJellybeanFishingHolidayStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.JellybeanFishingHolidayStart)

    def setJellybeanFishingHolidayEnd(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.JellybeanFishingHolidayEnd)

    def setJellybeanPartiesHolidayStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.JellybeanPartiesHolidayStart)

    def setJellybeanMonthHolidayStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.JellybeanMonthHolidayStart)

    def setJellybeanPartiesHolidayEnd(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.JellybeanPartiesHolidayEnd)

    def setBankUpgradeHolidayStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.BankUpgradeHolidayStart)

    def setHalloweenPropsHolidayStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.HalloweenPropsHolidayStart)

    def setHalloweenPropsHolidayEnd(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.HalloweenPropsHolidayEnd)

    def setSpookyPropsHolidayStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.SpookyPropsHolidayStart)

    def setSpookyPropsHolidayEnd(self):
        pass

    def setBlackCatHolidayStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.BlackCatHolidayStart)

    def setBlackCatHolidayEnd(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.BlackCatHolidayEnd)

    def setSpookyBlackCatHolidayStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.SpookyBlackCatHolidayStart)
        for currToon in base.cr.toons.values():
            currToon.setDNA(currToon.style.clone())

    def setSpookyBlackCatHolidayEnd(self):
        for currToon in base.cr.toons.values():
            currToon.setDNA(currToon.style.clone())

    def setTopToonsMarathonStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.TopToonsMarathonStart)

    def setTopToonsMarathonEnd(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.TopToonsMarathonEnd)

    def setWinterDecorationsStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.WinterDecorationsStart)

    def setWinterDecorationsEnd(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.WinterDecorationsEnd)

    def setWackyWinterDecorationsStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.WackyWinterDecorationsStart)

    def setWinterCarolingStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.WinterCarolingStart)

    def setExpandedClosetsStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.ExpandedClosetsStart)

    def setKartingTicketsHolidayStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.KartingTicketsHolidayStart)

    def setIdesOfMarchStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.IdesOfMarchStart)

    def holidayNotify(self):
        for id in self.holidayIdList:
            if id == 19:
                self.setBingoOngoing()
            elif id == 20:
                self.setCircuitRaceOngoing()
            elif id == 21:
                self.setTrolleyHolidayOngoing()
            elif id == 22:
                self.setRoamingTrialerWeekendOngoing()

    def setWeeklyCalendarHolidays(self, weeklyCalendarHolidays):
        self.weeklyCalendarHolidays = weeklyCalendarHolidays

    def getHolidaysForWeekday(self, day):
        result = []
        for item in self.weeklyCalendarHolidays:
            if item[1] == day:
                result.append(item[0])

        return result

    def setYearlyCalendarHolidays(self, yearlyCalendarHolidays):
        self.yearlyCalendarHolidays = yearlyCalendarHolidays

    def getYearlyHolidaysForDate(self, theDate):
        result = []
        for item in self.yearlyCalendarHolidays:
            if item[1][0] == theDate.month and item[1][1] == theDate.day:
                newItem = [self.YearlyHolidayType] + list(item)
                result.append(tuple(newItem))
                continue
            if item[2][0] == theDate.month and item[2][1] == theDate.day:
                newItem = [self.YearlyHolidayType] + list(item)
                result.append(tuple(newItem))

        return result

    def setMultipleStartHolidays(self, multipleStartHolidays):
        self.multipleStartHolidays = multipleStartHolidays

    def getMultipleStartHolidaysForDate(self, theDate):
        result = []
        for theHoliday in self.multipleStartHolidays:
            times = theHoliday[1:]
            tempTimes = times[0]
            for startAndStopTimes in tempTimes:
                startTime = startAndStopTimes[0]
                endTime = startAndStopTimes[1]
                if startTime[0] == theDate.year and startTime[1] == theDate.month and startTime[2] == theDate.day:
                    fakeOncelyHoliday = [theHoliday[0], startTime, endTime]
                    newItem = [self.OncelyMultipleStartHolidayType] + fakeOncelyHoliday
                    result.append(tuple(newItem))
                    continue
                if endTime[0] == theDate.year and endTime[1] == theDate.month and endTime[2] == theDate.day:
                    fakeOncelyHoliday = [theHoliday[0], startTime, endTime]
                    newItem = [self.OncelyMultipleStartHolidayType] + fakeOncelyHoliday
                    result.append(tuple(newItem))

        return result

    def setOncelyCalendarHolidays(self, oncelyCalendarHolidays):
        self.oncelyCalendarHolidays = oncelyCalendarHolidays

    def getOncelyHolidaysForDate(self, theDate):
        result = []
        for item in self.oncelyCalendarHolidays:
            if item[1][0] == theDate.year and item[1][1] == theDate.month and item[1][2] == theDate.day:
                newItem = [self.OncelyHolidayType] + list(item)
                result.append(tuple(newItem))
                continue
            if item[2][0] == theDate.year and item[2][1] == theDate.month and item[2][2] == theDate.day:
                newItem = [self.OncelyHolidayType] + list(item)
                result.append(tuple(newItem))

        return result

    def setRelativelyCalendarHolidays(self, relativelyCalendarHolidays):
        self.relativelyCalendarHolidays = relativelyCalendarHolidays

    def getRelativelyHolidaysForDate(self, theDate):
        result = []
        self.weekDaysInMonth = []
        self.numDaysCorMatrix = [(28, 0), (29, 1), (30, 2), (31, 3)]

        for i in xrange(7):
            self.weekDaysInMonth.append((i, 4))

        for holidayItem in self.relativelyCalendarHolidays:
            item = deepcopy(holidayItem)

            newItem = []
            newItem.append(item[0])

            i = 1
            while i < len(item):
                sRepNum = item[i][1]
                sWeekday = item[i][2]
                eWeekday = item[i+1][2]

                while 1:
                    eRepNum = item[i+1][1]

                    self.initRepMatrix(theDate.year, item[i][0])
                    while self.weekDaysInMonth[sWeekday][1] < sRepNum:
                        sRepNum -= 1

                    sDay = self.dayForWeekday(theDate.year, item[i][0], sWeekday, sRepNum)

                    self.initRepMatrix(theDate.year, item[i+1][0])
                    while self.weekDaysInMonth[eWeekday][1] < eRepNum:
                        eRepNum -= 1

                    nDay = self.dayForWeekday(theDate.year, item[i+1][0], eWeekday, eRepNum)

                    if ((nDay > sDay and
                        item[i+1][0] == item[i][0] and
                        (item[i+1][1] - item[i][1]) <= (nDay - sDay + abs(eWeekday - sWeekday))/7) or
                        item[i+1][0] != item[i][0]):
                        break

                    if self.weekDaysInMonth[eWeekday][1] > eRepNum:
                        eRepNum += 1
                    else:
                        item[i+1][0] += 1
                        item[i+1][1] = 1

                newItem.append([item[i][0], sDay, item[i][3], item[i][4], item[i][5]])

                newItem.append([item[i+1][0], nDay, item[i+1][3], item[i+1][4], item[i+1][5]])

                i += 2

            if item[1][0] == theDate.month and newItem[1][1] == theDate.day:
                nItem = [self.RelativelyHolidayType] + list(newItem)
                result.append(tuple(nItem))
                continue

            if item[2][0] == theDate.month and newItem[2][1] == theDate.day:
                nItem = [self.RelativelyHolidayType] + list(newItem)
                result.append(tuple(nItem))

        return result

    def dayForWeekday(self, year, month, weekday, repNum):
        monthDays = calendar.monthcalendar(year, month)
        if monthDays[0][weekday] == 0:
            repNum += 1
        return monthDays[repNum - 1][weekday]

    def initRepMatrix(self, year, month):
        for i in xrange(7):
            self.weekDaysInMonth[i] = (i, 4)

        startingWeekDay, numDays = calendar.monthrange(year, month)
        if startingWeekDay > 6:
            import pdb
            pdb.set_trace()
        for i in xrange(4):
            if numDays == self.numDaysCorMatrix[i][0]:
                break

        for j in xrange(self.numDaysCorMatrix[i][1]):
            self.weekDaysInMonth[startingWeekDay] = (self.weekDaysInMonth[startingWeekDay][0], self.weekDaysInMonth[startingWeekDay][1] + 1)
            startingWeekDay = (startingWeekDay + 1) % 7

    def isHolidayRunning(self, holidayId):
        result = holidayId in self.holidayIdList
        return result
