from otp.ai.AIBaseGlobal import *
import random
from toontown.suit import SuitDNA
from direct.directnotify import DirectNotifyGlobal
from toontown.suit import DistributedSuitAI
import SuitBuildingGlobals, types

class SuitPlannerInteriorAI:
    notify = DirectNotifyGlobal.directNotify.newCategory('SuitPlannerInteriorAI')

    def __init__(self, numFloors, bldgLevel, bldgTrack, zone, respectInvasions=1):
        self.dbg_nSuits1stRound = config.GetBool('n-suits-1st-round', 0)
        self.dbg_4SuitsPerFloor = config.GetBool('4-suits-per-floor', 0)
        self.dbg_1SuitPerFloor = config.GetBool('1-suit-per-floor', 0)
        self.zoneId = zone
        self.numFloors = numFloors
        self.respectInvasions = respectInvasions
        dbg_defaultSuitName = simbase.config.GetString('suit-type', 'random')
        if dbg_defaultSuitName == 'random':
            self.dbg_defaultSuitType = None
        else:
            self.dbg_defaultSuitType = SuitDNA.getSuitType(dbg_defaultSuitName)
        if isinstance(bldgLevel, types.StringType):
            self.notify.warning('bldgLevel is a string!')
            bldgLevel = int(bldgLevel)
        self._genSuitInfos(numFloors, bldgLevel, bldgTrack)
        return

    def __genJoinChances(self, num):
        joinChances = []
        for currChance in xrange(num):
            joinChances.append(random.randint(1, 100))

        joinChances.sort(cmp)
        return joinChances

    def _genSuitInfos(self, numFloors, bldgLevel, bldgTrack):
        self.suitInfos = []
        self.notify.debug('\n\ngenerating suitsInfos with numFloors (' + str(numFloors) + ') bldgLevel (' + str(bldgLevel) + '+1) and bldgTrack (' + str(bldgTrack) + ')')
        for currFloor in xrange(numFloors):
            infoDict = {}
            lvls = self.__genLevelList(bldgLevel, currFloor, numFloors)
            activeDicts = self.__genActiveSuits(lvls, bldgTrack, currFloor, numFloors, bldgLevel)
            reserveDicts = self.__genReserveSuits(lvls, bldgTrack, currFloor, numFloors, bldgLevel, activeDicts)
            infoDict['activeSuits'] = activeDicts
            infoDict['reserveSuits'] = reserveDicts
            self.suitInfos.append(infoDict)

    def __genLevelList(self, bldgLevel, currFloor, numFloors):
        lvls = []
        for i in xrange(bldgLevel):
            if i == bldgLevel - 1 and currFloor + 1 == numFloors:
                lvls.append(SuitBuildingGlobals.SUIT_BLDG_INFO_BOSS_LVLS)
            else:
                lvls.append(random.choice(SuitBuildingGlobals.SuitBuildingInfo[i][SuitBuildingGlobals.SUIT_BLDG_INFO_BOSS_LVLS]))
        return lvls

    def __genNormalSuitType(self, level):
        return SuitDNA.getRandomSuitTypeSuitInterior(level)

    def __genActiveSuits(self, lvls, bldgTrack, currFloor, numFloors, bldgLevel):
        activeDicts = []
        maxActive = min(4, len(lvls))
        if self.dbg_nSuits1stRound:
            numActive = min(self.dbg_nSuits1stRound, maxActive)
        else:
            numActive = random.randint(1, maxActive)
        if currFloor + 1 == numFloors and len(lvls) > 1:
            origBossSpot = len(lvls) - 1
            if numActive == 1:
                newBossSpot = numActive - 1
            else:
                newBossSpot = numActive - 2
            lvls[newBossSpot], lvls[origBossSpot] = lvls[origBossSpot], lvls[newBossSpot]
        bldgInfo = SuitBuildingGlobals.SuitBuildingInfo[bldgLevel]
        revives = bldgInfo[SuitBuildingGlobals.SUIT_BLDG_INFO_REVIVES][0] if len(bldgInfo) > SuitBuildingGlobals.SUIT_BLDG_INFO_REVIVES else 0
        for currActive in xrange(numActive - 1, -1, -1):
            level = lvls[currActive]
            type = self.__genNormalSuitType(level)
            activeDicts.append({'type': type, 'track': bldgTrack, 'level': level, 'revives': revives})
        return activeDicts

    def __genJoinChances(self, numReserve):
        joinChances = []
        for i in xrange(numReserve):
            joinChances.append(random.randint(1, 100))
        return joinChances

    def __genReserveSuits(self, lvls, bldgTrack, currFloor, numFloors, bldgLevel, activeDicts):
        reserveDicts = []
        numReserve = len(lvls) - len(activeDicts)
        joinChances = self.__genJoinChances(numReserve)
        revives = 0
        for currReserve in xrange(numReserve):
            level = lvls[currReserve + len(activeDicts)]
            type = self.__genNormalSuitType(level)
            reserveDicts.append({'type': type, 'track': bldgTrack, 'level': level, 'revives': revives, 'joinChance': joinChances[currReserve]})
        return reserveDicts

    def __setupSuitInfo(self, suit, bldgTrack, suitLevel, suitType):
        suitName, skeleton = simbase.air.suitInvasionManager.getInvadingCog()
        if suitName and self.respectInvasions:
            if random.choice([0, 0, 1]) == 1:
                suitType = SuitDNA.getSuitType(suitName)
                bldgTrack = SuitDNA.getSuitDept(suitName)
                suitLevel = min(max(suitLevel, suitType), suitType + 7)
        dna = SuitDNA.SuitDNA()
        dna.newSuitRandom(suitType, bldgTrack)
        suit.dna = dna
        self.notify.debug('Creating suit type ' + suit.dna.name + ' of level ' + str(suitLevel) + ' from type ' + str(suitType) + ' and track ' + str(bldgTrack))
        suit.setLevel(suitLevel)
        return skeleton

    def __genSuitObject(self, suitZone, suitType, bldgTrack, suitLevel, revives=0):
        newSuit = DistributedSuitAI.DistributedSuitAI(simbase.air, None)
        skel = self.__setupSuitInfo(newSuit, bldgTrack, suitLevel, suitType)
        newSuit.generateWithRequired(suitZone)
        newSuit.node().setName('suit-%s' % newSuit.doId)
        if skel:
            newSuit.b_setSkelecog(1)
        newSuit.b_setSkeleRevives(revives)

        return newSuit

    def myPrint(self):
        self.notify.info('Generated suits for building: ')
        for currInfo in suitInfos:
            whichSuitInfo = suitInfos.index(currInfo) + 1
            self.notify.debug(' Floor ' + str(whichSuitInfo) + ' has ' + str(len(currInfo[0])) + ' active suits.')
            for currActive in xrange(len(currInfo[0])):
                self.notify.debug('  Active suit ' + str(currActive + 1) + ' is of type ' + str(currInfo[0][currActive][0]) + ' and of track ' + str(currInfo[0][currActive][1]) + ' and of level ' + str(currInfo[0][currActive][2]))

            self.notify.debug(' Floor ' + str(whichSuitInfo) + ' has ' + str(len(currInfo[1])) + ' reserve suits.')
            for currReserve in xrange(len(currInfo[1])):
                self.notify.debug('  Reserve suit ' + str(currReserve + 1) + ' is of type ' + str(currInfo[1][currReserve][0]) + ' and of track ' + str(currInfo[1][currReserve][1]) + ' and of lvel ' + str(currInfo[1][currReserve][2]) + ' and has ' + str(currInfo[1][currReserve][3]) + '% join restriction.')

    def genFloorSuits(self, floor):
        suitHandles = {}
        floorInfo = self.suitInfos[floor]
        activeSuits = []
        for activeSuitInfo in floorInfo['activeSuits']:
            suit = self.__genSuitObject(self.zoneId, activeSuitInfo['type'], activeSuitInfo['track'], activeSuitInfo['level'], activeSuitInfo['revives'])
            activeSuits.append(suit)

        suitHandles['activeSuits'] = activeSuits
        reserveSuits = []
        for reserveSuitInfo in floorInfo['reserveSuits']:
            suit = self.__genSuitObject(self.zoneId, reserveSuitInfo['type'], reserveSuitInfo['track'], reserveSuitInfo['level'], reserveSuitInfo['revives'])
            reserveSuits.append((suit, reserveSuitInfo['joinChance']))

        suitHandles['reserveSuits'] = reserveSuits
        return suitHandles

    def genSuits(self):
        suitHandles = []
        for floor in xrange(len(self.suitInfos)):
            floorSuitHandles = self.genFloorSuits(floor)
            suitHandles.append(floorSuitHandles)

        return suitHandles
