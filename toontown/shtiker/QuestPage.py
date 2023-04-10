from panda3d.core import *
import ShtikerPage
from direct.gui.DirectGui import *
from toontown.quest import Quests
from toontown.toon import NPCToons
from toontown.hood import ZoneUtil
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from toontown.quest import QuestBookPoster, QuestSideBookPoster
from direct.directnotify import DirectNotifyGlobal

class QuestPage(ShtikerPage.ShtikerPage):
    notify = DirectNotifyGlobal.directNotify.newCategory('QuestPage')

    def __init__(self):
        ShtikerPage.ShtikerPage.__init__(self)
        self.quests = {0: None,
         1: None,
         2: None,
         3: None}
        self.side_quests = {0: None,
         1: None,
         2: None,
         3: None}
        self.textRolloverColor = Vec4(1, 1, 0, 1)
        self.textDownColor = Vec4(0.5, 0.9, 1, 1)
        self.textDisabledColor = Vec4(0.4, 0.8, 0.4, 1)
        self.onscreen = 0
        self.lastQuestTime = globalClock.getRealTime()
        return

    def load(self):
        self.title = DirectLabel(parent=self, relief=None, text=TTLocalizer.QuestPageToonTasks, text_scale=0.12, textMayChange=0, pos=(0, 0, 0.6))
        questFramePlaceList = ((-0.45,
          0,
          0.25,
          0,
          0,
          0),
         (-0.45,
          0,
          -0.35,
          0,
          0,
          0),
         (0.45, 0, 0.25, 0, 0, 0),
         (0.45,
          0,
          -0.35,
          0,
          0,
          0))
        sideQuestFramePlaceList = ((-1.45,
          0,
          0.25,
          0,
          0,
          0),
         (-1.45,
          0,
          -0.35,
          0,
          0,
          0),
         (1.45, 0, 0.25, 0, 0, 0),
         (1.45,
          0,
          -0.35,
          0,
          0,
          0))
        self.questFrames = []
        self.sideQuestFrames = []
        for i in xrange(ToontownGlobals.MaxQuestCarryLimit):
            frame = QuestBookPoster.QuestBookPoster(reverse=i > 1, mapIndex=i + 1)
            frame.reparentTo(self)
            frame.setPosHpr(*questFramePlaceList[i])
            frame.setScale(1.06)
            self.questFrames.append(frame)
        for i in xrange(ToontownGlobals.MaxQuestCarryLimit):
            frame = QuestSideBookPoster.QuestBookPoster(reverse=i > 1, mapIndex=i + 1)
            frame.reparentTo(self)
            frame.setPosHpr(*sideQuestFramePlaceList[i])
            frame.setScale(0.6)
            self.sideQuestFrames.append(frame)

        self.accept('questsChanged', self.updatePage)
        self.accept('sideQuestsChanged', self.updateSidePage)
        return

    def acceptOnscreenHooks(self):
        self.accept(ToontownGlobals.QuestsHotkeyOn, self.showQuestsOnscreen)
        self.accept(ToontownGlobals.QuestsHotkeyOff, self.hideQuestsOnscreen)

    def ignoreOnscreenHooks(self):
        self.ignore(ToontownGlobals.QuestsHotkeyOn)
        self.ignore(ToontownGlobals.QuestsHotkeyOff)

    def unload(self):
        self.ignore('questsChanged')
        del self.title
        del self.quests
        del self.questFrames
        loader.unloadModel('phase_3.5/models/gui/stickerbook_gui')
        ShtikerPage.ShtikerPage.unload(self)

    def clearQuestFrame(self, index):
        self.questFrames[index].clear()
        self.quests[index] = None
        return

    def fillQuestFrame(self, questDesc, index):
        self.questFrames[index].update(questDesc)
        self.quests[index] = questDesc
    
    def clearSideQuestFrame(self, index):
        self.sideQuestFrames[index].clear()
        self.side_quests[index] = None
        return

    def fillSideQuestFrame(self, questDesc, index):
        self.sideQuestFrames[index].update(questDesc)
        self.side_quests[index] = questDesc

    def getLowestUnusedIndex(self):
        for i in xrange(ToontownGlobals.MaxQuestCarryLimit):
            if self.quests[i] == None:
                return i

        return -1
    
    def getLowestUnusedSideIndex(self):
        for i in xrange(ToontownGlobals.MaxQuestCarryLimit):
            if self.quests[i] == None:
                return i

        return -1

    def updatePage(self):
        self.notify.debug('updatePage()')
        newQuests = base.localAvatar.quests
        carryLimit = base.localAvatar.getQuestCarryLimit()
        for i in xrange(ToontownGlobals.MaxQuestCarryLimit):
            if i < carryLimit:
                self.questFrames[i].show()
            else:
                self.questFrames[i].hide()

        for index, questDesc in self.quests.items():
            if questDesc is not None and list(questDesc) not in newQuests:
                self.clearQuestFrame(index)

        for questDesc in newQuests:
            newQuestDesc = tuple(questDesc)
            if newQuestDesc not in self.quests.values():
                index = self.getLowestUnusedIndex()
                self.fillQuestFrame(newQuestDesc, index)

        for i, questDesc in self.quests.iteritems():
            if questDesc:
                if self.canDeleteQuest(questDesc):
                    self.questFrames[i].setDeleteCallback(self.__deleteQuest)
                else:
                    self.questFrames[i].setDeleteCallback(None)
                self.questFrames[i].update(questDesc)
            else:
                self.questFrames[i].unbindMouseEnter()

        messenger.send('questPageUpdated')
        return
    
    def updateSidePage(self):
        self.notify.debug('updatePage()')
        newQuests = base.localAvatar.side_quests
        carryLimit = base.localAvatar.getQuestCarryLimit()
        for i in xrange(ToontownGlobals.MaxQuestCarryLimit):
            if i < carryLimit:
                self.sideQuestFrames[i].show()
            else:
                self.sideQuestFrames[i].hide()

        for index, questDesc in self.side_quests.items():
            if questDesc is not None and list(questDesc) not in newQuests:
                self.clearSideQuestFrame(index)

        for questDesc in newQuests:
            newQuestDesc = tuple(questDesc)
            if newQuestDesc not in self.side_quests.values():
                index = self.getLowestUnusedSideIndex()
                self.fillSideQuestFrame(newQuestDesc, index)

        for i, questDesc in self.side_quests.iteritems():
            if questDesc:
                if self.canDeleteQuest(questDesc):
                    self.sideQuestFrames[i].setDeleteCallback(self.__deleteQuest)
                else:
                    self.sideQuestFrames[i].setDeleteCallback(None)
                self.sideQuestFrames[i].update(questDesc)
            else:
                self.sideQuestFrames[i].unbindMouseEnter()

        messenger.send('questPageUpdated')
        return

    def enter(self):
        self.updatePage()
        self.updateSidePage()
        ShtikerPage.ShtikerPage.enter(self)

    def exit(self):
        ShtikerPage.ShtikerPage.exit(self)

    def showQuestsOnscreenTutorial(self):
        self.setPos(0, 0, -0.2)
        self.showQuestsOnscreen()

    def showQuestsOnscreen(self):
        messenger.send('wakeup')
        timedif = globalClock.getRealTime() - self.lastQuestTime
        if timedif < 0.7:
            return
        self.lastQuestTime = globalClock.getRealTime()
        if self.onscreen or base.localAvatar.invPage.onscreen:
            return
        self.onscreen = 1
        for i in xrange(ToontownGlobals.MaxQuestCarryLimit):
            if hasattr(self.questFrames[i], 'mapIndex'):
                self.questFrames[i].mapIndex.show()
        
        for i in xrange(ToontownGlobals.MaxQuestCarryLimit):
            if hasattr(self.questFrames[i], 'mapIndex'):
                self.sideQuestFrames[i].mapIndex.show()

        self.updatePage()
        self.updateSidePage()
        self.reparentTo(aspect2d)
        self.title.hide()
        self.show()

    def hideQuestsOnscreenTutorial(self):
        self.setPos(0, 0, 0)
        self.hideQuestsOnscreen()

    def hideQuestsOnscreen(self):
        if not self.onscreen:
            return
        self.onscreen = 0
        for i in xrange(ToontownGlobals.MaxQuestCarryLimit):
            if hasattr(self.questFrames[i], 'mapIndex'):
                self.questFrames[i].mapIndex.hide()
        
        for i in xrange(ToontownGlobals.MaxQuestCarryLimit):
            if hasattr(self.questFrames[i], 'mapIndex'):
                self.sideQuestFrames[i].mapIndex.hide()

        self.reparentTo(self.book)
        self.title.show()
        self.hide()

    def canDeleteQuest(self, questDesc):
        return Quests.isQuestJustForFun(questDesc[0], questDesc[3]) and self.onscreen == 0

    def __deleteQuest(self, questDesc):
        base.localAvatar.d_requestDeleteQuest(questDesc)
