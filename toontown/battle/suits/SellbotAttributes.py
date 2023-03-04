from toontown.toonbase import TTLocalizer

SellbotAttributes = {'cc': {'name': TTLocalizer.SuitColdCaller,
        'singularname': TTLocalizer.SuitColdCallerS,
        'pluralname': TTLocalizer.SuitColdCallerP,
        'level': 0,
        'hp':(6,12,20,30,42,56,72,90),
        'def':(2,5,10,12,15,15,15,15),
        'freq':(50,30,10,5,5,5,5,5),
        'acc':(35,40,45,50,55,60,65,70),
        'attacks':
                (('FreezeAssets',
                    (1,1,1,1,1,1,1,1),
                    (90,90,90,90,90,90,90,90),
                    (5,10,15,20,25,25,25,25)),
                ('PoundKey',
                    (2,2,3,4,5,6,7,8),
                    (75,80,85,90,95,95,95,95),
                    (25,25,25,25,25,25,25,25)),
                ('DoubleTalk',
                    (2,3,4,6,8,8,10,12),
                    (50,55,60,65,70,75,80,85),
                    (25,25,25,25,25,25,25,25)),
                ('HotAir',
                    (3,4,6,8,10,12,14,15),
                    (50,50,50,50,50,50,50,50),
                    (45,40,35,30,25,25,25,25)))},
 'tm': {'name': TTLocalizer.SuitTelemarketer,
        'singularname': TTLocalizer.SuitTelemarketerS,
        'pluralname': TTLocalizer.SuitTelemarketerP,
        'level': 1,
        'hp':(12,20,30,42,56,72,90,110),
        'def':(5,10,15,20,25,25,25,25),
        'freq':(50,30,10,5,5,5,5,5),
        'acc':(45,50,55,60,65,70,75,80),
        'attacks':
                (('ClipOnTie',
                    (2,2,3,3,4,4,5,5),
                    (75,75,75,75,75),
                    (15,15,15,15,15)),
                ('PickPocket',
                    (1,1,1,1,1,1,1,1),
                    (75,75,75,75,75,75,75,75),
                    (15,15,15,15,15,15,15,15)),
                ('Rolodex',
                    (4,6,7,9,12,13,15,18),
                    (50,50,50,50,50,50,50,50),
                    (30,30,30,30,30,30,30,30)),
                ('DoubleTalk',
                    (4,6,7,9,12,13,15,18),
                    (75,80,85,90,95,95,95,95),
                    (40,40,40,40,40,40,40,40)))},
 'nd': {'name': TTLocalizer.SuitNameDropper,
        'singularname': TTLocalizer.SuitNameDropperS,
        'pluralname': TTLocalizer.SuitNameDropperP,
        'level': 2,
        'hp':(20,30,42,56,72,90,110,132),
        'def':(10,15,20,25,30,30,30,30),
        'freq':(50,30,10,5,5,5,5,5),
        'acc':(65,70,75,80,85,90,95,95),
        'attacks':
                (('RazzleDazzle',
                    (1,1,1,1,1,1,1,1),
                    (50,50,50,50,50,50,50,50),
                    (30,30,30,30,30,30,30,30)),
                ('Rolodex',
                    (5,6,7,10,14,15,16,19),
                    (95,95,95,95,95,95,95,95),
                    (40,40,40,40,40,40,40,40)),
                ('Synergy',
                    (3,4,6,9,12,13,15,18),
                    (50,50,50,50,50,50,50,50),
                    (15,15,15,15,15,15,15,15)),
                ('PickPocket',
                    (2,2,2,2,2,3,4,5),
                    (95,95,95,95,95,95,95,95),
                    (15,15,15,15,15,15,15,15)))},
 'gh': {'name': TTLocalizer.SuitGladHander,
        'singularname': TTLocalizer.SuitGladHanderS,
        'pluralname': TTLocalizer.SuitGladHanderP,
        'level': 3,
        'hp':(30,42,56,72,90,110,132,156),
        'def':(15,20,25,30,35,35,35,35),
        'freq':(50,30,10,5,5,5,5,5),
        'acc':(70,75,80,82,85,88,90,92),
        'attacks':
                (('RubberStamp',
                    (1,2,3,4,5,6,7,8),
                    (90,70,50,30,10,10,10,10),
                    (40,30,20,10,5,5,5,5)),
                ('FountainPen',
                    (1,2,3,4,5,6,7,8),
                    (70,60,50,40,30,30,30,30),
                    (40,30,20,10,5,5,5,5)),
                ('Filibuster',
                    (4,6,9,12,15,17,20,23),
                    (30,40,50,60,70,80,90,90),
                    (10,20,30,40,45,45,45,45)),
                ('Schmooze',
                    (5,7,11,15,20,22,26,29),
                    (55,65,75,85,95,95,95,95),
                    (10,20,30,40,45,45,45,45)))},
 'ms': {'name': TTLocalizer.SuitMoverShaker,
        'singularname': TTLocalizer.SuitMoverShakerS,
        'pluralname': TTLocalizer.SuitMoverShakerP,
        'level': 4,
        'hp':(42,56,72,90,110,132,156,196),
        'def':(20,25,30,35,40,40,40,40),
        'freq':(50,30,10,5,5,5,5,5),
        'acc':(35,40,45,50,55,60,65,70),
        'attacks':
                (('BrainStorm',
                    (5,6,8,10,12,13,15,17),
                    (60,75,80,85,90,90,90,90),
                    (15,15,15,15,15,15,15,15)),
                ('HalfWindsor',
                    (6,9,11,13,16,19,21,24),
                    (50,65,70,75,80,85,90,95),
                    (20,20,20,20,20,20,20,20)),
                ('Quake',
                    (9,12,15,18,21,24,27,30),
                    (60,65,75,80,85,90,95,95),
                    (20,20,20,20,20,20,20,20)),
                ('Shake',
                    (6,8,10,12,14,16,18,20),
                    (70,75,80,85,90,95,95,95),
                    (25,25,25,25,25,25,25,25)),
                ('Tremor',
                    (5,6,7,8,9,10,11,12),
                    (50,50,50,50,50,50,50,50),
                    (20,20,20,20,20,20,20,20)))},
 'tf': {'name': TTLocalizer.SuitTwoFace,
        'singularname': TTLocalizer.SuitTwoFaceS,
        'pluralname': TTLocalizer.SuitTwoFaceP,
        'level': 5,
        'hp':(56,72,90,110,132,156,196,224),
        'def':(25,30,35,40,45,45,45,45),
        'freq':(50,30,10,5,5,5,5,5),
        'acc':(35,40,45,50,55,60,65,70),
        'attacks':
                (('EvilEye',
                    (10,12,14,16,18,20,22,24),
                    (60,75,80,85,90,90,90,90),
                    (30,30,30,30,30,30,30,30)),
                ('HangUp',
                    (7,8,10,12,13,15,17,18),
                    (50,60,70,80,90,90,90,90),
                    (15,15,15,15,15,15,15,15)),
                ('RazzleDazzle',
                    (8,10,12,14,16,18,20,22),
                    (60,65,70,75,80,85,90,95),
                    (30,30,30,30,30,30,30,30)),
                ('RedTape',
                    (6,7,8,9,10,11,12,13),
                    (60,65,75,85,90,90,90,90),
                    (25,25,25,25,25,25,25,25)))},
 'm': {'name': TTLocalizer.SuitTheMingler,
       'singularname': TTLocalizer.SuitTheMinglerS,
       'pluralname': TTLocalizer.SuitTheMinglerP,
       'level': 6,
       'hp':(72,90,110,132,156,196,224,254),
       'def':(30,35,40,45,50,50,50,50),
       'freq':(50,30,10,5,5,5,5,5),
       'acc':(35,40,45,50,55,60,65,70),
       'attacks':
               (('BuzzWord',
                    (10,11,13,15,16,17,19,21),
                    (60,75,80,85,90,90,90,90),
                    (20,20,20,20,20,20,20,20)),
                ('RazzleDazzle',
                    (12,15,18,21,24,27,30,33),
                    (60,70,75,80,90,90,90,90),
                    (25,25,25,25,25,25,25,25)),
                ('PowerTrip',
                    (10,13,14,15,18,19,20,23),
                    (60,65,70,75,80,85,90,95),
                    (15,15,15,15,15,15,15,15)),
                ('Schmooze',
                    (7,8,12,15,16,20,23,24),
                    (55,65,75,85,95,95,95,95),
                    (15,15,15,15,15,15,15,15)),
                ('ParadigmShift',
                    (7,8,12,15,16,20,23,24),
                    (55,65,75,85,95,95,95,95),
                    (15,15,15,15,15,15,15,15)),
                ('TeeOff',
                    (8,9,10,11,12,13,14,15),
                    (70,75,80,85,95,95,95,95),
                    (10,10,10,10,10,10,10,10)))},
 'mh': {'name': TTLocalizer.SuitMrHollywood,
        'singularname': TTLocalizer.SuitMrHollywoodS,
        'pluralname': TTLocalizer.SuitMrHollywoodP,
        'level': 7,
        'hp':(90,110,132,156,196,224,254,286),
        'def':(35,40,45,50,55,55,55,55),
        'freq':(50,30,10,5,5,5,5,5),
        'acc':(35,40,45,50,55,60,65,70),
        'attacks':
                (('PowerTrip',
                    (10,12,15,18,20,22,25,28),
                    (55,65,75,85,95,95,95,95),
                    (50,50,50,50,50,50,50,50)),
                ('RazzleDazzle',
                    (8,11,14,17,20,23,26,29),
                    (70,75,85,90,95,95,95,95),
                    (50,50,50,50,50,50,50,50)))}}