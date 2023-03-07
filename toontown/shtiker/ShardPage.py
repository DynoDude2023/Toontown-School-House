from pandac.PandaModules import *
import ShtikerPage
from direct.task.Task import Task
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from toontown.toonbase import TTLocalizer
from direct.directnotify import DirectNotifyGlobal
from toontown.hood import ZoneUtil
from toontown.toonbase import ToontownGlobals
from toontown.distributed import ToontownDistrict
from toontown.toontowngui import TTDialog
from toontown.suit import Suit
from toontown.suit import SuitDNA
from toontown.battle import SuitBattleGlobals
import SuitPage
POP_COLORS_NTT = (Vec4(0.0, 1.0, 0.0, 1.0), Vec4(1.0, 1.0, 0.0, 1.0), Vec4(1.0, 0.0, 0.0, 1.0))
POP_COLORS = (Vec4(0.4, 0.4, 1.0, 1.0), Vec4(0.4, 1.0, 0.4, 1.0), Vec4(1.0, 0.4, 0.4, 1.0))
SC_ONLY_DISTRICTS_ENABLED = config.GetBool('want-sc-only-districts', False)

class ShardPage(ShtikerPage.ShtikerPage):
    notify = DirectNotifyGlobal.directNotify.newCategory('ShardPage')

    def __init__(self):
        ShtikerPage.ShtikerPage.__init__(self)
        self.shardButtonMap = {}
        self.shardButtons = []
        self.scrollList = None
        self.textRolloverColor = Vec4(1, 1, 0, 1)
        self.textDownColor = Vec4(0.5, 0.9, 1, 1)
        self.textDisabledColor = Vec4(0.4, 0.8, 0.4, 1)
        self.textSelectedColor = Vec4(0.9, 0.7, 0.5, 1)
        self.ShardInfoUpdateInterval = 5.0
        self.lowPop, self.midPop, self.highPop = base.getShardPopLimits()
        self.showPop = config.GetBool('show-total-population', 0)
        self.noTeleport = config.GetBool('shard-page-disable', 0)
        self.adminForceReload = 0
        self.selectedShard = None
        self.invasionStatus = None
        self.shardInvasionHead = None
        self.shardInvasionShadow = None

    def load(self):
        main_text_scale = 0.06
        title_text_scale = 0.12
        shard_text_scale = 0.09
        self.title = DirectLabel(parent=self, relief=None, text=TTLocalizer.ShardPageTitle, text_scale=title_text_scale, textMayChange=0, pos=(0, 0, 0.6))
        helpText_ycoord = 0.309
        self.helpText = DirectLabel(parent=self, relief=None, text='', text_scale=main_text_scale, text_wordwrap=12, text_align=TextNode.ALeft, textMayChange=1, pos=(0.06, 0, helpText_ycoord))
        goButton_ycoord = -1.0
        self.shardTitle = DirectLabel(parent=self, relief=None, text='', text_scale=shard_text_scale, text_wordwrap=12, textMayChange=1, pos=(0.41, 0, helpText_ycoord))
        self.shardPopulation = DirectLabel(parent=self, relief=None, text='', text_scale=main_text_scale, text_wordwrap=12, textMayChange=1, pos=(0.41, 0, helpText_ycoord - 0.03))
        self.totalPopulationText = DirectLabel(parent=self, relief=None, text=TTLocalizer.ShardPagePopulationTotal % 1, text_scale=main_text_scale, text_fg=(0.5, 0.1, 0.1, 1), text_wordwrap=20, textMayChange=1, text_align=TextNode.ACenter, pos=(0, 0, 0.52))
        iconGui = loader.loadModel('phase_3.5/models/gui/sos_textures')
        self.globeIcon = iconGui.find('**/district')
        self.globeIcon.reparentTo(self)
        self.globeIcon.setPos(0.415, 0, -0.09)
        self.globeIcon.setScale(0.4)
        iconGui.remove()
        self.shardInvasionText = DirectLabel(parent=self, relief=None, text='', text_scale=main_text_scale, text_fg=(0.5, 0.1, 0.09, 1), text_wordwrap=12, textMayChange=1, pos=(0.415, 0, -0.23))
        self.shardInvasionNode = self.attachNewNode('invasionNode')
        self.shardInvasionNode.setPos(0.415, 0, 0)
        suitGui = loader.loadModel('phase_3.5/models/gui/suitpage_gui')
        self.shadowModels = []
        for index in range(1, len(SuitDNA.suitHeadTypes) + 1):
            self.shadowModels.append(suitGui.find('**/shadow' + str(index)))

        suitGui.remove()
        goButtonGui = loader.loadModel('phase_4/models/parties/schtickerbookHostingGUI')
        goButtonPos = goButtonGui.find('**/startParty_text_locator').getPos()
        goButtonGuiList = (goButtonGui.find('**/startPartyButton_up'),
         goButtonGui.find('**/startPartyButton_down'),
         goButtonGui.find('**/startPartyButton_rollover'),
         goButtonGui.find('**/startPartyButton_inactive'))
        self.goButton = DirectButton(parent=self, relief=None, pos=(-0.215, 0, goButton_ycoord), geom=goButtonGuiList, geom_scale=1.6, geom3_pos=(0.085, 0, 0.06), geom3_scale=1.4, text=TTLocalizer.ShardPageGoTo, text_scale=TTLocalizer.EPpartyGoButton, text_pos=(goButtonPos[0] * 1.61, goButtonPos[2] * 1.53))
        goButtonGui.removeNode()
        self.gui = loader.loadModel('phase_3.5/models/gui/friendslist_gui')
        self.listXorigin = -0.02
        self.listFrameSizeX = 0.67
        self.listZorigin = -0.96
        self.listFrameSizeZ = 1.04
        self.arrowButtonScale = 1.3
        self.itemFrameXorigin = -0.237
        self.itemFrameZorigin = 0.365
        self.buttonXstart = self.itemFrameXorigin + 0.293
        self.regenerateScrollList()
        scrollTitle = DirectFrame(parent=self.scrollList, text=TTLocalizer.ShardPageScrollTitle, text_scale=main_text_scale, text_align=TextNode.ACenter, relief=None, pos=(self.buttonXstart, 0, self.itemFrameZorigin + 0.127))

    def unload(self):
        self.gui.removeNode()
        del self.title
        self.scrollList.destroy()
        del self.scrollList
        del self.shardButtons
        taskMgr.remove('ShardPageUpdateTask-doLater')
        ShtikerPage.ShtikerPage.unload(self)

    def regenerateScrollList(self):
        selectedIndex = 0
        if self.scrollList:
            selectedIndex = self.scrollList.getSelectedIndex()
            for button in self.shardButtons:
                button.detachNode()

            self.scrollList.destroy()
            self.scrollList = None
        self.scrollList = DirectScrolledList(parent=self, relief=None, pos=(-0.5, 0, -0.03), incButton_image=(self.gui.find('**/FndsLst_ScrollUp'),
         self.gui.find('**/FndsLst_ScrollDN'),
         self.gui.find('**/FndsLst_ScrollUp_Rllvr'),
         self.gui.find('**/FndsLst_ScrollUp')), incButton_relief=None, incButton_scale=(self.arrowButtonScale, self.arrowButtonScale, -self.arrowButtonScale), incButton_pos=(self.buttonXstart, 0, self.itemFrameZorigin - 0.999), incButton_image3_color=Vec4(1, 1, 1, 0.2), decButton_image=(self.gui.find('**/FndsLst_ScrollUp'),
         self.gui.find('**/FndsLst_ScrollDN'),
         self.gui.find('**/FndsLst_ScrollUp_Rllvr'),
         self.gui.find('**/FndsLst_ScrollUp')), decButton_relief=None, decButton_scale=(self.arrowButtonScale, self.arrowButtonScale, self.arrowButtonScale), decButton_pos=(self.buttonXstart, 0, self.itemFrameZorigin + 0.125), decButton_image3_color=Vec4(1, 1, 1, 0.2), itemFrame_pos=(self.itemFrameXorigin, 0, self.itemFrameZorigin), itemFrame_scale=1.0, itemFrame_relief=DGG.SUNKEN, itemFrame_frameSize=(self.listXorigin,
         self.listXorigin + self.listFrameSizeX,
         self.listZorigin,
         self.listZorigin + self.listFrameSizeZ), itemFrame_frameColor=(0.85, 0.95, 1, 1), itemFrame_borderWidth=(0.01, 0.01), numItemsVisible=15, forceHeight=0.065, items=self.shardButtons)
        self.scrollList.scrollTo(selectedIndex)

    def askForShardInfoUpdate(self, task = None):
        ToontownDistrict.refresh('shardInfoUpdated')
        taskMgr.doMethodLater(self.ShardInfoUpdateInterval, self.askForShardInfoUpdate, 'ShardPageUpdateTask-doLater')
        return Task.done

    def makeShardButton(self, shardId, shardName, shardPop):
        shardButtonParent = DirectFrame()
        shardButtonL = DirectButton(parent=shardButtonParent, relief=None, text=shardName, text_scale=0.06, text_align=TextNode.ALeft, text1_bg=self.textDownColor, text2_bg=self.textRolloverColor, text3_fg=self.textDisabledColor, textMayChange=1, command=self.selectShard, extraArgs=[shardId, shardName, shardPop])
        if self.showPop:
            popText = str(shardPop)
            if shardPop == None:
                popText = ''
            shardButtonR = DirectButton(parent=shardButtonParent, relief=None, text=popText, text_scale=0.06, text_align=TextNode.ALeft, text1_bg=self.textDownColor, text2_bg=self.textRolloverColor, text3_fg=self.textDisabledColor, textMayChange=1, pos=(0.5, 0, 0), command=self.choseShard, extraArgs=[shardId])
        else:
            model = loader.loadModel('phase_3.5/models/gui/matching_game_gui')
            button = model.find('**/minnieCircle')
            shardButtonR = DirectButton(parent=shardButtonParent, relief=None, image=button, image_scale=(0.3, 1, 0.3), image2_scale=(0.35, 1, 0.35), image_color=self.getPopColor(shardPop), pos=(0.6, 0, 0.0125), text=self.getPopText(shardPop), text_scale=0.06, text_align=TextNode.ACenter, text_pos=(-0.0125, -0.0125), text_fg=Vec4(0, 0, 0, 0), text1_fg=Vec4(0, 0, 0, 0), text2_fg=Vec4(0, 0, 0, 1), text3_fg=Vec4(0, 0, 0, 0), command=self.selectShard, extraArgs=[shardId, shardName, shardPop])
            del model
            del button
        if SC_ONLY_DISTRICTS_ENABLED:
            if base.cr.activeDistrictMap[shardId].isSpeedchatOnly:
                gui = loader.loadModel('phase_3.5/models/gui/chat_input_gui')
                shardButtonChat = DirectButton(parent=shardButtonParent, image=(gui.find('**/ChtBx_ChtBtn_UP'), gui.find('**/ChtBx_ChtBtn_RLVR'), gui.find('**/ChtBx_ChtBtn_RLVR')), pos=(0.51, 0, 0.013), scale=0.9, relief=None, image_color=Vec4(0.75, 1, 0.6, 1))
                return (shardButtonParent,
                 shardButtonR,
                 shardButtonL,
                 shardButtonChat)
        return (shardButtonParent, shardButtonR, shardButtonL)

    def getPopColor(self, pop):
        if config.GetBool('want-lerping-pop-colors', False):
            if pop < self.midPop:
                color1 = POP_COLORS_NTT[0]
                color2 = POP_COLORS_NTT[1]
                popRange = self.midPop - self.lowPop
                pop = pop - self.lowPop
            else:
                color1 = POP_COLORS_NTT[1]
                color2 = POP_COLORS_NTT[2]
                popRange = self.highPop - self.midPop
                pop = pop - self.midPop
            popPercent = pop / float(popRange)
            if popPercent > 1:
                popPercent = 1
            newColor = color2 * popPercent + color1 * (1 - popPercent)
        elif pop <= self.lowPop:
            newColor = POP_COLORS[0]
        elif pop <= self.midPop:
            newColor = POP_COLORS[1]
        else:
            newColor = POP_COLORS[2]
        return newColor

    def getPopText(self, pop):
        if pop <= self.lowPop:
            popText = TTLocalizer.ShardPageLow
        elif pop <= self.midPop:
            popText = TTLocalizer.ShardPageMed
        else:
            popText = TTLocalizer.ShardPageHigh
        return popText

    def getPopChoiceHandler(self, shardId, pop):
        if base.cr.productName == 'JP':
            handler = self.choseShard
        elif pop <= self.midPop:
            if self.noTeleport and not self.showPop:
                handler = self.shardChoiceReject
            elif SC_ONLY_DISTRICTS_ENABLED:
                if base.cr.activeDistrictMap[shardId].isSpeedchatOnly and base.cr.allowAnyTypedChat():
                    handler = self.shardChoiceSpeedchat
            else:
                handler = self.choseShard
        elif self.showPop:
            handler = self.choseShard
        else:
            handler = self.shardChoiceReject
        return handler

    def getCurrentZoneId(self):
        try:
            zoneId = base.cr.playGame.getPlace().getZoneId()
        except:
            zoneId = None

        return zoneId

    def getCurrentShardId(self):
        zoneId = self.getCurrentZoneId()
        if zoneId != None and ZoneUtil.isWelcomeValley(zoneId):
            return ToontownGlobals.WelcomeValleyToken
        else:
            return base.localAvatar.defaultShard

    def updateScrollList(self):
        curShardTuples = base.cr.listActiveShards()

        def compareShardTuples(a, b):
            if a[1] < b[1]:
                return -1
            elif b[1] < a[1]:
                return 1
            else:
                return 0

        curShardTuples.sort(compareShardTuples)
        if base.cr.welcomeValleyManager:
            curShardTuples.append((ToontownGlobals.WelcomeValleyToken,
             TTLocalizer.WelcomeValley[-1],
             0,
             0))
        currentShardId = self.getCurrentShardId()
        actualShardId = base.localAvatar.defaultShard
        actualShardName = None
        anyChanges = 0
        totalPop = 0
        totalWVPop = 0
        currentMap = {}
        self.shardButtons = []
        for i in range(len(curShardTuples)):
            shardId, name, pop, WVPop = curShardTuples[i]
            if shardId == actualShardId:
                actualShardName = name
            totalPop += pop
            totalWVPop += WVPop
            currentMap[shardId] = 1
            buttonTuple = self.shardButtonMap.get(shardId)
            if buttonTuple == None or self.adminForceReload:
                buttonTuple = self.makeShardButton(shardId, name, pop)
                self.shardButtonMap[shardId] = buttonTuple
                anyChanges = 1
            elif self.showPop:
                buttonTuple[1]['text'] = str(pop)
            else:
                buttonTuple[1]['image_color'] = self.getPopColor(pop)
                buttonTuple[1]['text'] = self.getPopText(pop)
                buttonTuple[1]['extraArgs'] = [shardId, name, pop]
                buttonTuple[2]['extraArgs'] = [shardId, name, pop]
            self.shardButtons.append(buttonTuple[0])
            buttonTuple[2]['text_fg'] = Vec4(0, 0, 0, 1)
            buttonTuple[1]['state'] = DGG.NORMAL
            buttonTuple[2]['state'] = DGG.NORMAL
            if shardId == currentShardId or self.book.safeMode:
                buttonTuple[2]['text_fg'] = self.textDisabledColor

        for shardId, buttonTuple in self.shardButtonMap.items():
            if shardId not in currentMap:
                buttonTuple[0].destroy()
                del self.shardButtonMap[shardId]
                anyChanges = 1

        buttonTuple = self.shardButtonMap.get(ToontownGlobals.WelcomeValleyToken)
        if buttonTuple:
            if self.showPop:
                buttonTuple[1]['text'] = str(totalWVPop)
            else:
                buttonTuple[1]['image_color'] = self.getPopColor(totalWVPop)
                buttonTuple[1]['text'] = self.getPopText(totalWVPop)
                buttonTuple[1]['extraArgs'] = [ToontownGlobals.WelcomeValleyToken, TTLocalizer.WelcomeValley[-1], totalWVPop]
                buttonTuple[2]['extraArgs'] = [ToontownGlobals.WelcomeValleyToken, TTLocalizer.WelcomeValley[-1], totalWVPop]
        if anyChanges or self.adminForceReload:
            self.regenerateScrollList()
        self.totalPopulationText['text'] = TTLocalizer.ShardPagePopulationTotal % totalPop
        helpText = TTLocalizer.ShardPageHelpIntro
        if actualShardName:
            if currentShardId == ToontownGlobals.WelcomeValleyToken:
                helpText += TTLocalizer.ShardPageHelpWelcomeValley % actualShardName
            else:
                helpText += TTLocalizer.ShardPageHelpWhere % actualShardName
        if not self.book.safeMode:
            helpText += TTLocalizer.ShardPageHelpMove
        self.helpText['text'] = helpText
        if self.selectedShard:
            self.selectShard(self.selectedShard[0], self.selectedShard[1], self.selectedShard[2])
        else:
            self.shardTitle['text'] = ''
            self.shardPopulation['text'] = ''
            self.goButton['state'] = DGG.DISABLED
            if self.shardInvasionHead and self.shardInvasionShadow:
                self.shardInvasionHead.remove()
                self.shardInvasionShadow.remove()
                self.shardInvasionText['text'] = ''
            self.globeIcon.hide()
        if self.adminForceReload:
            self.adminForceReload = 0

    def enter(self):
        self.askForShardInfoUpdate()
        self.updateScrollList()
        currentShardId = self.getCurrentShardId()
        buttonTuple = self.shardButtonMap.get(currentShardId)
        if buttonTuple:
            i = self.shardButtons.index(buttonTuple[0])
            self.scrollList.scrollTo(i, centered=1)
        ShtikerPage.ShtikerPage.enter(self)
        self.accept('shardInfoUpdated', self.updateScrollList)

    def exit(self):
        self.ignore('shardInfoUpdated')
        self.ignore('confirmDone')
        self.selectedShard = None
        self.invasionStatus = None
        if self.shardInvasionHead and self.shardInvasionShadow:
            self.shardInvasionHead.remove()
            self.shardInvasionShadow.remove()
            self.shardInvasionText['text'] = ''
        taskMgr.remove('ShardPageUpdateTask-doLater')
        ShtikerPage.ShtikerPage.exit(self)

    def shardChoiceReject(self, shardId, shardName):
        self.confirm = TTDialog.TTGlobalDialog(doneEvent='confirmDone', message=TTLocalizer.ShardPageChoiceReject, style=TTDialog.Acknowledge)
        self.confirm.show()
        self.accept('confirmDone', self.__handleConfirm)

    def shardChoiceSpeedchat(self, shardId, shardName):
        self.confirm = TTDialog.TTGlobalDialog(doneEvent='confirmDone', message=TTLocalizer.ShardPageChoiceSpeedchat % shardName, style=TTDialog.TwoChoice)
        self.confirm.show()
        self.accept('confirmDone', self.__handleConfirm, [shardId])

    def __handleConfirm(self, shardId = None):
        self.ignore('confirmDone')
        self.confirm.cleanup()
        del self.confirm
        if shardId != None:
            self.choseShard(shardId)

    def selectShard(self, shardId, shardName, shardPop):
        self.selectedShard = (shardId, shardName, shardPop)
        for otherShardId, buttonTuple in self.shardButtonMap.items():
            if otherShardId != self.getCurrentShardId():
                buttonTuple[2]['text3_fg'] = self.textDisabledColor
            buttonTuple[1]['state'] = DGG.NORMAL
            buttonTuple[2]['state'] = DGG.NORMAL

        buttonTuple = self.shardButtonMap.get(shardId)
        if buttonTuple:
            if shardId != self.getCurrentShardId():
                buttonTuple[2]['text3_fg'] = self.textSelectedColor
            buttonTuple[1]['state'] = DGG.DISABLED
            buttonTuple[2]['state'] = DGG.DISABLED
            self.helpText['text'] = ''
            self.shardTitle['text'] = shardName
            self.shardPopulation['text'] = TTLocalizer.ShardPagePopulationDistrict % str(shardPop)
        if shardId:
            if self.invasionStatus != base.cr.activeDistrictMap[self.selectedShard[0]].invasionStatus:
                self.invasionStatus = base.cr.activeDistrictMap[self.selectedShard[0]].invasionStatus
                if self.shardInvasionHead and self.shardInvasionShadow:
                    self.shardInvasionHead.remove()
                    self.shardInvasionShadow.remove()
                    self.shardInvasionText['text'] = ''
                suitName, suitCount, suitSpecial = base.cr.activeDistrictMap[self.selectedShard[0]].invasionStatus
                if suitName and shardId != ToontownGlobals.WelcomeValleyToken:
                    self.globeIcon.hide()
                    suitIndex = SuitDNA.suitHeadTypes.index(suitName)
                    shadow = self.shardInvasionNode.attachNewNode('shadow')
                    shadowModel = self.shadowModels[suitIndex]
                    shadowModel.copyTo(shadow)
                    coords = SuitPage.SHADOW_SCALE_POS[suitIndex]
                    shadow.setScale(coords[0])
                    shadow.setPos(coords[1], coords[2], coords[3])
                    self.shardInvasionShadow = shadow
                    self.shardInvasionHead = Suit.attachSuitHead(self.shardInvasionNode, suitName)
                    if suitSpecial == 1:
                        suitName = SuitBattleGlobals.SuitAttributes[suitName]['name'] + ' ' + TTLocalizer.SkeletonP
                    elif suitSpecial == 2:
                        suitName = TTLocalizer.SkeleReviveCogName % SuitBattleGlobals.SuitAttributes[suitName]['pluralname']
                    else:
                        suitName = SuitBattleGlobals.SuitAttributes[suitName]['pluralname']
                    if suitCount == ToontownGlobals.InvasionMegaNumSuits:
                        self.shardInvasionText['text'] = TTLocalizer.ShardPageMegaInvasionAlert % suitName
                    else:
                        self.shardInvasionText['text'] = TTLocalizer.ShardPageInvasionAlert % suitName
        if not self.shardInvasionHead:
            self.globeIcon.show()
        if self.selectedShard[0] != self.getCurrentShardId():
            self.goButton['state'] = DGG.NORMAL
            self.goButton['command'] = self.getPopChoiceHandler(self.selectedShard[0], self.selectedShard[2])
            self.goButton['extraArgs'] = [self.selectedShard[0], self.selectedShard[1]]

    def choseShard(self, shardId, shardName = None):
        zoneId = self.getCurrentZoneId()
        canonicalHoodId = ZoneUtil.getCanonicalHoodId(base.localAvatar.lastHood)
        currentShardId = self.getCurrentShardId()
        if shardId == currentShardId:
            return
        if shardId == ToontownGlobals.WelcomeValleyToken:
            self.doneStatus = {'mode': 'teleport',
             'hood': ToontownGlobals.WelcomeValleyToken}
            messenger.send(self.doneEvent)
        elif shardId == base.localAvatar.defaultShard:
            self.doneStatus = {'mode': 'teleport',
             'hood': canonicalHoodId}
            messenger.send(self.doneEvent)
        else:
            try:
                place = base.cr.playGame.getPlace()
            except:
                try:
                    place = base.cr.playGame.hood.loader.place
                except:
                    place = base.cr.playGame.hood.place

            place.requestTeleport(canonicalHoodId, canonicalHoodId, shardId, -1)