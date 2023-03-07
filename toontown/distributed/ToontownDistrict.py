from direct.distributed import DoInterestManager
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObject
from otp.distributed import DistributedDistrict
from direct.showbase import DirectObject
from direct.task import Task
from otp.distributed.OtpDoGlobals import *
_ToonTownDistrictInterest = None
_ToonTownDistrictInterestComplete = 0
_trashObject = DirectObject.DirectObject()

def EventName():
    return 'ShardPopulationSet'


def isOpen():
    global _ToonTownDistrictInterest
    return _ToonTownDistrictInterest is not None


def isComplete():
    global _ToonTownDistrictInterestComplete
    return _ToonTownDistrictInterestComplete


def open(event = None):
    global _trashObject
    global _ToonTownDistrictInterest
    if not isOpen():

        def _CompleteProc(event):
            global _ToonTownDistrictInterestComplete
            _ToonTownDistrictInterestComplete = 1
            if event is not None:
                messenger.send(event)

        _trashObject.acceptOnce(EventName(), _CompleteProc)
        _ToonTownDistrictInterest = base.cr.addInterest(OTP_DO_ID_TOONTOWN, OTP_ZONE_ID_DISTRICTS_STATS, EventName(), EventName())
    elif isComplete():
        messenger.send(EventName())


def refresh(event = None):
    global _ToonTownDistrictInterest
    if isOpen():
        if isComplete():
            messenger.send(EventName())
            if event is not none:
                messenger.send(event)
    else:

        def _CompleteProc(event):
            global _ToonTownDistrictInterestComplete
            _ToonTownDistrictInterestComplete = 1
            if event is not None:
                messenger.send(event)
            close()

        _trashObject.acceptOnce(EventName(), _CompleteProc, [event])
        _ToonTownDistrictInterest = base.cr.addInterest(OTP_DO_ID_TOONTOWN, OTP_ZONE_ID_DISTRICTS_STATS, EventName(), EventName())


def close():
    global _ToonTownDistrictInterest
    global _ToonTownDistrictInterestComplete
    if isOpen():
        _ToonTownDistrictInterestComplete = 0
        base.cr.removeInterest(_ToonTownDistrictInterest, None)
        _ToonTownDistrictInterest = None


class ToontownDistrict(DistributedDistrict.DistributedDistrict):
    notify = DirectNotifyGlobal.directNotify.newCategory('ToontownDistrict')
    neverDisable = 1

    def __init__(self, cr):
        DistributedDistrict.DistributedDistrict.__init__(self, cr)
        self.toontownDistrictId = 0
        self.avatarCount = 0
        self.newAvatarCount = 0
        self.invasionStatus = ('', 0, 0)
        self.isSpeedchatOnly = False

    def setToontownDistrictId(self, value):
        self.toontownDistrictId = value

    def setAvatarCount(self, avatarCount):
        self.avatarCount = avatarCount

    def setNewAvatarCount(self, newAvatarCount):
        self.newAvatarCount = newAvatarCount

    def setInvasionStatus(self, suitName, suitCount, suitSpecial):
        self.invasionStatus = (suitName, suitCount, suitSpecial)

    def setStats(self, avatarCount, newAvatarCount):
        self.setAvatarCount(avatarCount)
        self.setNewAvatarCount(newAvatarCount)

    def allowAHNNLog(self, allow):
        self.allowAHNN = allow

    def getAllowAHNNLog(self):
        return self.allowAHNN

    def setSpeedchatOnly(self, isChatless):
        self.isSpeedchatOnly = isChatless
