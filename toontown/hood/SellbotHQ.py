import CogHood
from toontown.toonbase import ToontownGlobals
from toontown.coghq import SellbotCogHQLoader
from panda3d.core import *

class SellbotHQ(CogHood.CogHood):

    def __init__(self, parentFSM, doneEvent, dnaStore, hoodId):
        CogHood.CogHood.__init__(self, parentFSM, doneEvent, dnaStore, hoodId)
        self.id = ToontownGlobals.SellbotHQ
        self.cogHQLoaderClass = SellbotCogHQLoader.SellbotCogHQLoader
        self.storageDNAFile = None
        self.skyFile = 'phase_9/models/cogHQ/cog_sky'
        self.titleColor = (0.5, 0.5, 0.5, 1.0)
        self.whiteFogColor = Vec4(0.15, 0.15, 0.15, 1)
        return

    def load(self):
        CogHood.CogHood.load(self)
        self.sky.setScale(2.0)
        render.setColorScale(0.7, 0.7, 0.75, 1)
        self.sky.setFogOff()
        self.parentFSM.getStateNamed('SellbotHQ').addChild(self.fsm)
        self.fog = Fog('SellbotHQFog')

    def unload(self):
        self.parentFSM.getStateNamed('SellbotHQ').removeChild(self.fsm)
        render.setColorScale(1.0, 1.0, 1.0, 1)
        del self.cogHQLoaderClass
        CogHood.CogHood.unload(self)
        self.fog = None

    def enter(self, *args):
        CogHood.CogHood.enter(self, *args)
        localAvatar.setCameraFov(ToontownGlobals.CogHQCameraFov)
        base.camLens.setNearFar(ToontownGlobals.CogHQCameraNear, ToontownGlobals.CogHQCameraFar)

    def exit(self):
        localAvatar.setCameraFov(ToontownGlobals.DefaultCameraFov)
        base.camLens.setNearFar(ToontownGlobals.DefaultCameraNear, ToontownGlobals.DefaultCameraFar)
        CogHood.CogHood.exit(self)

    def setWhiteFog(self):
        if base.wantFog:
            self.fog.setColor(self.whiteFogColor)
            self.fog.setLinearRange(30.0, 800.0)
            render.clearFog()
            render.setFog(self.fog)
            self.sky.clearFog()
            self.sky.setFogOff()

    def setNoFog(self):
        if base.wantFog:
            render.clearFog()
            self.sky.clearFog()