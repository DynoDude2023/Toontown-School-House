from panda3d.core import *
from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
from direct.distributed import DistributedObject
from direct.gui.DirectGui import *
from otp.otpbase import PythonUtil
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from toontown.toon import Toon
from toontown.toon import ToonDNA
from toontown.toontowngui import TTDialog
from toontown.spellbook.MagicWordIndex import *
import ShtikerPage
PageMode = PythonUtil.Enum('Words, Body, IDs, Acc1, Acc2')

# Create global Toon variables for customization pages
toonRotation = 180
toonDNA = None
toonAcc = []

class WordPage(ShtikerPage.ShtikerPage):
    notify = DirectNotifyGlobal.directNotify.newCategory('WordPage')

    def __init__(self):
        ShtikerPage.ShtikerPage.__init__(self)

    def load(self):
        ShtikerPage.ShtikerPage.load(self)

        # Set global Toon variables for Toon DNA and Accessories
        global toonDNA, toonAcc
        toonDNA = base.localAvatar.getStyle()
        toonAcc = [base.localAvatar.getHat(), base.localAvatar.getGlasses(),
                   base.localAvatar.getBackpack(), base.localAvatar.getShoes()]

        # Load pages
        self.wordsTabPage = WordsTabPage(self)
        self.wordsTabPage.hide()
        self.bodyTabPage = BodyTabPage(self)
        self.bodyTabPage.hide()
        self.clothingTabPage = ClothingTabPage(self)
        self.clothingTabPage.hide()
        self.acc1Page = AccTabPage1(self)
        self.acc1Page.hide()
        self.acc2Page = AccTabPage2(self)
        self.acc2Page.hide()

        titleHeight = 0.61
        self.title = DirectLabel(parent=self, relief=None, text=TTLocalizer.SpellbookPageTitle, text_scale=0.12, pos=(0, 0, titleHeight))
        normalColor = (1, 1, 1, 1)
        clickColor = (0.8, 0.8, 0, 1)
        rolloverColor = (0.15, 0.82, 1.0, 1)
        diabledColor = (1.0, 0.98, 0.15, 1)

        # Load tabs
        gui = loader.loadModel('phase_3.5/models/gui/fishingBook')
        self.wordsTab = DirectButton(parent=self, relief=None, text=TTLocalizer.WordPageTabTitle, text_scale=0.063,
                                     text_align=TextNode.ACenter, text_pos=(0.125, 0.0, 0.0),
                                     image=gui.find('**/tabs/polySurface1'), image_pos=(0.55, 1, -0.91),
                                     image_hpr=(0, 0, -90), image_scale=(0.033, 0.033, 0.035), image_color=normalColor,
                                     image1_color=clickColor, image2_color=rolloverColor, image3_color=diabledColor,
                                     text_fg=Vec4(0.2, 0.1, 0, 1), command=self.setMode, extraArgs=[PageMode.Words],
                                     pos=(-0.93, 0, 0.77))

        # TODO: Any strings that should go into the localizer need to go into the localizer when porting over.
        self.bodyTab = DirectButton(parent=self, relief=None, text="Body", text_scale=0.063,
                                     text_align=TextNode.ACenter, text_pos=(0.125, 0.0, 0.0),
                                     image=gui.find('**/tabs/polySurface1'), image_pos=(0.55, 1, -0.91),
                                     image_hpr=(0, 0, -90), image_scale=(0.033, 0.033, 0.035), image_color=normalColor,
                                     image1_color=clickColor, image2_color=rolloverColor, image3_color=diabledColor,
                                     text_fg=Vec4(0.2, 0.1, 0, 1), command=self.setMode, extraArgs=[PageMode.Body],
                                     pos=(-0.53, 0, 0.77))
        self.clothingTab = DirectButton(parent=self, relief=None, text=TTLocalizer.ClothingPageTitle, text_scale=0.065,
                                   text_align=TextNode.ACenter, text_pos=(0.125, 0.0, 0.0),
                                   image=gui.find('**/tabs/polySurface2'), image_pos=(0.12, 1, -0.91),
                                   image_hpr=(0, 0, -90), image_scale=(0.033, 0.033, 0.035), image_color=normalColor,
                                   image1_color=clickColor, image2_color=rolloverColor, image3_color=diabledColor,
                                   text_fg=Vec4(0.2, 0.1, 0, 1), command=self.setMode, extraArgs=[PageMode.IDs],
                                   pos=(-0.13, 0, 0.77))
        self.acc1Tab = DirectButton(parent=self, relief=None, text=TTLocalizer.AccessoriesPageHeadTab, text_scale=0.045,
                                   text_align=TextNode.ACenter, text_pos=(0.125, 0.035, 0.0),
                                   image=gui.find('**/tabs/polySurface2'), image_pos=(0.12, 1, -0.91),
                                   image_hpr=(0, 0, -90), image_scale=(0.033, 0.033, 0.035), image_color=normalColor,
                                   image1_color=clickColor, image2_color=rolloverColor, image3_color=diabledColor,
                                   text_fg=Vec4(0.2, 0.1, 0, 1), command=self.setMode, extraArgs=[PageMode.Acc1],
                                   pos=(0.27, 0, 0.77))
        self.acc2Tab = DirectButton(parent=self, relief=None, text=TTLocalizer.AccessoriesPageBodyTab, text_scale=0.045,
                                    text_align=TextNode.ACenter, text_pos=(0.125, 0.035, 0.0),
                                    image=gui.find('**/tabs/polySurface2'), image_pos=(0.12, 1, -0.91),
                                    image_hpr=(0, 0, -90), image_scale=(0.033, 0.033, 0.035), image_color=normalColor,
                                    image1_color=clickColor, image2_color=rolloverColor, image3_color=diabledColor,
                                    text_fg=Vec4(0.2, 0.1, 0, 1), command=self.setMode, extraArgs=[PageMode.Acc2],
                                    pos=(0.67, 0, 0.77))
        return

    def enter(self):
        self.setMode(PageMode.Words, updateAnyways=1)
        ShtikerPage.ShtikerPage.enter(self)

    def exit(self):
        self.clothingTabPage.exit()
        self.wordsTabPage.exit()
        self.acc1Page.exit()
        self.acc2Page.exit()
        ShtikerPage.ShtikerPage.exit(self)

    def unload(self):
        self.wordsTabPage.unload()
        self.clothingTabPage.unload()
        self.acc1Page.unload()
        self.acc2Page.unload()
        del self.title
        ShtikerPage.ShtikerPage.unload(self)

    def setMode(self, mode, updateAnyways = 0):
        messenger.send('wakeup')
        if not updateAnyways:
            if self.mode == mode:
                return
            else:
                self.mode = mode
        if mode == PageMode.Words:
            self.mode = PageMode.Words
            self.title['text'] = TTLocalizer.WordPageTabTitle
            self.wordsTab['state'] = DGG.DISABLED
            self.wordsTabPage.enter()
            self.bodyTab['state'] = DGG.NORMAL
            self.bodyTabPage.exit()
            self.clothingTab['state'] = DGG.NORMAL
            self.clothingTabPage.exit()
            self.acc1Tab['state'] = DGG.NORMAL
            self.acc1Page.exit()
            self.acc2Tab['state'] = DGG.NORMAL
            self.acc2Page.exit()

            # Reset Toon Rotation if not in customization tabs
            global toonRotation
            toonRotation = 180
        elif mode == PageMode.Body:
            self.mode = PageMode.Body
            self.title['text'] = "Body"
            self.wordsTab['state'] = DGG.NORMAL
            self.wordsTabPage.exit()
            self.bodyTab['state'] = DGG.DISABLED
            self.bodyTabPage.enter()
            self.clothingTab['state'] = DGG.NORMAL
            self.clothingTabPage.exit()
            self.acc1Tab['state'] = DGG.NORMAL
            self.acc1Page.exit()
            self.acc2Tab['state'] = DGG.NORMAL
            self.acc2Page.exit()
        elif mode == PageMode.IDs:
            self.mode = PageMode.IDs
            self.title['text'] = TTLocalizer.ClothingPageTitle
            self.wordsTab['state'] = DGG.NORMAL
            self.wordsTabPage.exit()
            self.bodyTab['state'] = DGG.NORMAL
            self.bodyTabPage.exit()
            self.clothingTab['state'] = DGG.DISABLED
            self.clothingTabPage.enter()
            self.acc1Tab['state'] = DGG.NORMAL
            self.acc1Page.exit()
            self.acc2Tab['state'] = DGG.NORMAL
            self.acc2Page.exit()
        elif mode == PageMode.Acc1:
            self.mode = PageMode.Acc1
            self.title['text'] = TTLocalizer.AccessoriesPageHead
            self.wordsTab['state'] = DGG.NORMAL
            self.wordsTabPage.exit()
            self.bodyTab['state'] = DGG.NORMAL
            self.bodyTabPage.exit()
            self.clothingTab['state'] = DGG.NORMAL
            self.clothingTabPage.exit()
            self.acc1Tab['state'] = DGG.DISABLED
            self.acc1Page.enter()
            self.acc2Tab['state'] = DGG.NORMAL
            self.acc2Page.exit()
        elif mode == PageMode.Acc2:
            self.mode = PageMode.Acc2
            self.title['text'] = TTLocalizer.AccessoriesPageBody
            self.wordsTab['state'] = DGG.NORMAL
            self.wordsTabPage.exit()
            self.bodyTab['state'] = DGG.NORMAL
            self.bodyTabPage.exit()
            self.clothingTab['state'] = DGG.NORMAL
            self.clothingTabPage.exit()
            self.acc1Tab['state'] = DGG.NORMAL
            self.acc1Page.exit()
            self.acc2Tab['state'] = DGG.DISABLED
            self.acc2Page.enter()
        else:
            raise StandardError, 'WordPage::setMode - Invalid Mode %s' % mode

# NOTICE: This is an old version of WordsTabPage. Discard this version when porting over.
class WordsTabPage(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('WordsTabPage')

    def __init__(self, parent = aspect2d):
        self._parent = parent
        self.currentSizeIndex = None
        DirectFrame.__init__(self, parent=self._parent, relief=None, pos=(0.0, 0.0, 0.0), scale=(1.0, 1.0, 1.0))
        self.load()

    def load(self):
        self.magicWords = []
        self.hiddenMagicWords = []
        self.shownMagicWords = []
        self.setupWords()

        gui = loader.loadModel('phase_3.5/models/gui/friendslist_gui')
        coolbutton = loader.loadModel('phase_3/models/gui/pick_a_toon_gui')
        guiButton = loader.loadModel('phase_3/models/gui/quit_button')
        cdrGui = loader.loadModel('phase_3.5/models/gui/tt_m_gui_sbk_codeRedemptionGui')
        guiClose = loader.loadModel('phase_3.5/models/gui/avatar_panel_gui')
        self.helpLabel = DirectLabel(parent=self, relief=None, text=TTLocalizer.WordPageHelp, text_scale=0.06,
                                     text_wordwrap=12, text_align=TextNode.ALeft, textMayChange=1,
                                     pos=(0.058, 0, 0.403))
        self.searchLabel = DirectLabel(parent=self, relief=None, text=TTLocalizer.WordPageSearch, text_scale=0.06,
                                       text_wordwrap=12, text_align=TextNode.ACenter, textMayChange=1,
                                       pos=(0.439, 0, -0.2))
        self.searchBarFrame = DirectFrame(parent=self, relief=None, image=cdrGui.find('**/tt_t_gui_sbk_cdrCodeBox'),
                                          pos=(0.439, 0.0, -0.3225), scale=0.7)
        self.searchBarEntry = DirectEntry(parent=self, relief=None, text_scale=0.06, width=7.75, textMayChange=1,
                                          pos=(0.209, 0, -0.3325), text_align=TextNode.ALeft, backgroundFocus=0,
                                          focusInCommand=self.toggleEntryFocus)
        self.searchBarEntry.bind(DGG.TYPE, self.updateWordSearch)
        self.searchBarEntry.bind(DGG.ERASE, self.updateWordSearch)
        self.activatorLabel = DirectLabel(parent=self, relief=None,
                                          text=TTLocalizer.WordPageActivator + TTLocalizer.WordPageNA,
                                          text_scale=0.06, text_wordwrap=12, text_align=TextNode.ALeft, textMayChange=1,
                                          pos=(0.058, 0, 0.15))
        self.totalLabel = DirectLabel(parent=self, relief=None,
                                      text=TTLocalizer.WordPageTotal + str(len(self.shownMagicWords)), text_scale=0.06,
                                      text_wordwrap=12, text_align=TextNode.ALeft, textMayChange=1,
                                      pos=(0.058, 0, 0.05))
        self.currentLabel = DirectLabel(parent=self, relief=None,
                                        text=TTLocalizer.WordPageCurrent + TTLocalizer.WordPageNA, text_scale=0.06,
                                        text_wordwrap=12, text_align=TextNode.ALeft, textMayChange=1,
                                        pos=(0.058, 0, -0.05))
        self.copyToChatButton = DirectButton(parent=self, relief=None, image=(guiButton.find('**/QuitBtn_UP'),
                                                                              guiButton.find('**/QuitBtn_DN'),
                                                                              guiButton.find('**/QuitBtn_RLVR')),
                                             image_scale=(0.7, 1, 1), text=TTLocalizer.WordPageCopyToChat,
                                             text_scale=0.04, text_pos=(0, -0.01), pos=(0.629, 0.0, -0.5325),
                                             command=self.copyToChat)
        self.infoButton = DirectButton(parent=self, relief=None, image=(guiButton.find('**/QuitBtn_UP'),
                                                                        guiButton.find('**/QuitBtn_DN'),
                                                                        guiButton.find('**/QuitBtn_RLVR')),
                                       image_scale=(0.7, 1, 1), text=TTLocalizer.WordPageMoreInfo,
                                       text_scale=0.04, text_pos=(0, -0.01), pos=(0.249, 0.0, -0.5325),
                                       command=self.showInfoPanel)
        self.scrollList = DirectScrolledList(parent=self, forceHeight=0.07, pos=(-0.5, 0, 0),
                                             incButton_image=(gui.find('**/FndsLst_ScrollUp'),
                                                              gui.find('**/FndsLst_ScrollDN'),
                                                              gui.find('**/FndsLst_ScrollUp_Rllvr'),
                                                              gui.find('**/FndsLst_ScrollUp')),
                                             incButton_relief=None, incButton_scale=(1.3, 1.3, -1.3),
                                             incButton_pos=(0.08, 0, -0.60), incButton_image3_color=Vec4(1, 1, 1, 0.2),
                                             decButton_image=(gui.find('**/FndsLst_ScrollUp'),
                                                              gui.find('**/FndsLst_ScrollDN'),
                                                              gui.find('**/FndsLst_ScrollUp_Rllvr'),
                                                              gui.find('**/FndsLst_ScrollUp')),
                                             decButton_relief=None,  decButton_scale=(1.3, 1.3, 1.3),
                                             decButton_pos=(0.08, 0, 0.52), decButton_image3_color=Vec4(1, 1, 1, 0.2),
                                             itemFrame_pos=(-0.237, 0, 0.41), itemFrame_scale=1.0,
                                             itemFrame_relief=DGG.SUNKEN,
                                             itemFrame_frameSize=(-0.05, 0.66, -0.98, 0.07),
                                             itemFrame_frameColor=(0.85, 0.95, 1, 1),
                                             itemFrame_borderWidth=(0.01, 0.01),
                                             numItemsVisible=14, items=self.shownMagicWords)
        self.slider = DirectSlider(parent=self, range=(len(self.shownMagicWords), 0),
                                   scale=(0.7, 0.7, 0.515), pos=(-0.1, 0, -0.045),
                                   pageSize=1, orientation=DGG.VERTICAL, command=self.scrollListTo,
                                   thumb_geom=(coolbutton.find('**/QuitBtn_UP'),
                                                coolbutton.find('**/QuitBtn_DN'),
                                                coolbutton.find('**/QuitBtn_RLVR'),
                                                coolbutton.find('**/QuitBtn_UP')),
                                   thumb_relief=None, thumb_geom_hpr=(0, 0, -90), thumb_geom_scale=(0.5, 1, 0.5))
        self.magicWordInfo = DirectFrame(parent=self, relief=None, pos=(0.0, 0.0, -0.05), scale=0.9,
                                         geom=DGG.getDefaultDialogGeom(), geom_scale=(1.4, 1, 1),
                                         geom_color=ToontownGlobals.GlobalDialogColor)
        self.magicWordTitle = DirectLabel(parent=self.magicWordInfo, relief=None, text=TTLocalizer.WordPageNA,
                                          text_scale=0.12,  textMayChange=1, pos=(0, 0, 0.3500))
        self.magicWordInfoLabel = DirectLabel(parent=self.magicWordInfo, relief=None, text=TTLocalizer.WordPageNA,
                                         text_scale=0.06, text_wordwrap=20, text_align=TextNode.ALeft, textMayChange=1,
                                         pos=(-0.6, 0, 0.2))
        self.magicWordQuitButton = DirectButton(parent=self.magicWordInfo,
                                                image=(guiClose.find('**/CloseBtn_UP'),
                                                       guiClose.find('**/CloseBtn_DN'),
                                                       guiClose.find('**/CloseBtn_Rllvr'),
                                                       guiClose.find('**/CloseBtn_UP')),
                                                relief=None, scale=1.5, pos=(0.6, 0, -0.4),
                                                command=self.hideInfoPanel)
        self.magicWordInfo.hide()
        gui.removeNode()
        coolbutton.removeNode()
        guiButton.removeNode()
        cdrGui.removeNode()
        guiClose.removeNode()

    def unload(self):
        for word in self.magicWords + self.hiddenMagicWords + self.shownMagicWords:
            word.destroy()
            del word

        gui = [self.helpLabel, self.searchLabel, self.searchBarFrame, self.searchBarEntry, self.activatorLabel,
               self.totalLabel, self.currentLabel, self.copyToChatButton, self.infoButton, self.scrollList,
               self.slider, self.magicWordTitle, self.magicWordInfoLabel, self.magicWordQuitButton, self.magicWordInfo]

        for dgui in gui:
            dgui.destroy()
            del dgui

    def exit(self):
        for word in self.magicWords:
            if word['state'] != DGG.NORMAL:
                word['state'] = DGG.NORMAL

        self.activatorLabel['text'] = TTLocalizer.WordPageActivator + base.cr.magicWordManager.chatPrefix + ' (' + str(MagicWordConfig.PREFIX_ALLOWED.index(base.cr.magicWordManager.chatPrefix)) + ')'
        self.currentLabel['text'] = TTLocalizer.WordPageCurrent + TTLocalizer.WordPageNA
        self.ignore('mouse1')
        self.toggleEntryFocus(True)
        self.searchBarEntry.set('')
        self.updateWordSearch()
        self.hideInfoPanel()
        self.hide()

    def enter(self):
        for word in self.magicWords:
            if word['state'] != DGG.NORMAL:
                word['state'] = DGG.NORMAL

        self.activatorLabel['text'] = TTLocalizer.WordPageActivator + base.cr.magicWordManager.chatPrefix + ' (' + str(MagicWordConfig.PREFIX_ALLOWED.index(base.cr.magicWordManager.chatPrefix)) + ')'
        self.currentLabel['text'] = TTLocalizer.WordPageCurrent + TTLocalizer.WordPageNA
        self.accept('mouse1', self.toggleEntryFocus, extraArgs=[True])
        self.searchBarEntry.set('')
        self.updateWordSearch()
        self.hideInfoPanel()
        self.show()

    def scrollListTo(self):
        self.scrollList.scrollTo(int(self.slider['value']))

    def toggleEntryFocus(self, lose=False):
        if lose:
            self.searchBarEntry['focus'] = 0
            base.localAvatar.chatMgr.fsm.request('mainMenu')
        else:
            base.localAvatar.chatMgr.fsm.request('otherDialog')

    def setupWords(self, returnWords=False):
        words = []

        for wordName in magicWordIndex:
            word = magicWordIndex[wordName]
            if word['classname'] not in words:
                if not word['hidden']:
                    words.append(word['classname'])

        sortedWords = sorted(words)

        numWords = len(sortedWords)
        if returnWords:
            return numWords

        currentWordIndex = 0
        while currentWordIndex < numWords:
            newWordButton = DirectButton(parent=self, relief=None, text=sortedWords[currentWordIndex],
                                         text_align=TextNode.ALeft, text_scale=0.05, text1_bg=Vec4(0.5, 0.9, 1, 1),
                                         text2_bg=Vec4(1, 1, 0, 1), text3_fg=Vec4(0.4, 0.8, 0.4, 1), textMayChange=0,
                                         command=self.showWordInfo, extraArgs=[currentWordIndex])
            self.magicWords.append(newWordButton)
            self.shownMagicWords.append(newWordButton)
            currentWordIndex += 1

    def showWordInfo(self, wordNum):
        for word in self.magicWords:
            if word['state'] != DGG.NORMAL:
                word['state'] = DGG.NORMAL

        wordName = self.magicWords[wordNum]
        wordName['state'] = DGG.DISABLED
        self.currentLabel['text'] = TTLocalizer.WordPageCurrent + wordName['text']

    def updateWordSearch(self, extraArgs=None):
        self.hiddenMagicWords = []
        searchTerm = self.searchBarEntry.get().lower()
        for word in self.magicWords + self.hiddenMagicWords:
            wordLabel = word['text'].lower()
            if searchTerm not in wordLabel and word in self.magicWords:
                self.hiddenMagicWords.append(word)
                if word['state'] != DGG.NORMAL:
                    self.currentLabel['text'] = TTLocalizer.WordPageCurrent + TTLocalizer.WordPageNA
                    word['state'] = DGG.NORMAL
                word.hide()
            elif searchTerm in wordLabel and word in self.hiddenMagicWords:
                self.hiddenMagicWords.remove(word)
                word.show()

        self.shownMagicWords = []
        for word in self.magicWords:
            if word not in self.hiddenMagicWords:
                self.shownMagicWords.append(word)

        magicWordCount = len(self.shownMagicWords)
        if magicWordCount == 0:
            magicWordCount = 1

        self.totalLabel['text'] = TTLocalizer.WordPageTotal + str(len(self.shownMagicWords))
        self.scrollList['items'] = self.shownMagicWords
        self.slider['range'] = (magicWordCount, 0)

    def copyToChat(self):
        wordName = None
        for word in self.magicWords:
            if word['state'] != DGG.NORMAL:
                wordName = word['text']
                break

        if not wordName:
            return

        phrase = base.cr.magicWordManager.chatPrefix + wordName + ' '
        localAvatar.book.closeBook()
        localAvatar.chatMgr.fsm.request('mainMenu')
        localAvatar.chatMgr.chatInputNormal.typeCallback(None)
        localAvatar.chatMgr.chatInputNormal.chatEntry.enterText(phrase)

    def showInfoPanel(self):
        wordName = None
        for word in self.magicWords:
            if word['state'] != DGG.NORMAL:
                wordName = word['text']
                break

        if not wordName:
            return

        wordInfo = magicWordIndex[wordName.lower()]
        wordText = TTLocalizer.WordPageDescription + wordInfo['desc']
        prefix = base.cr.magicWordManager.chatPrefix
        if not wordInfo['example']:
            exampleText = TTLocalizer.WordPageExample + prefix + wordName.lower()
        else:
            exampleText = TTLocalizer.WordPageExample + prefix + wordName.lower() + ' ' + wordInfo['example']
        aliasText = TTLocalizer.WordPageAliases
        for alias in wordInfo['aliases']:
            aliasText += alias
            if wordInfo['aliases'].index(alias) != len(wordInfo['aliases']) - 1:
                aliasText += ', '
        accessLevelText = TTLocalizer.WordPageAccessLevel + wordInfo['access'] + ' (' + str(OTPGlobals.AccessLevelName2Int.get(wordInfo['access'])) + ')'

        lineBreak = '\n\n'
        infoText = wordText + lineBreak + exampleText + lineBreak + aliasText + lineBreak + accessLevelText

        self.magicWordTitle['text'] = wordName
        self.magicWordInfoLabel['text'] = infoText

        self.magicWordInfo.show()

    def hideInfoPanel(self):
        self.magicWordTitle['text'] = TTLocalizer.WordPageNA
        self.magicWordInfoLabel['text'] = TTLocalizer.WordPageNA

        self.magicWordInfo.hide()

# Base class for Toon customization tabs
class ToonTabPageBase(DirectFrame):

    def __init__(self, parent = aspect2d):
        DirectFrame.__init__(self, parent=parent, relief=None, pos=(0.0, 0.0, 0.0), scale=(1.0, 1.0, 1.0))
        self.load()

    def load(self):
        # Create Toon
        self.toon = Toon.Toon()
        self.toon.setDNA(toonDNA)
        self.toon.loop('neutral')

        # Put Toon on page
        self.toon.reparentTo(self)
        self.toon.setScale(0.18)
        self.toon.setPos(-0.45, 0, -0.425)
        self.toon.setBin('unsorted', 0, 1)
        self.toon.setDepthTest(True)
        self.toon.setDepthWrite(True)

        # Create Toon Rotation Slider and Reset Button
        gui = loader.loadModel('phase_3/models/gui/pick_a_toon_gui')
        self.toonRotateSlider = DirectSlider(parent=self, state=DGG.DISABLED, pos=(-0.45, 0, -0.5), range=(0.0, 360.0),
                                             value=toonRotation, scale=(0.4, 0.7, 0.7),
                                             thumb_geom=(gui.find('**/QuitBtn_UP'),
                                                         gui.find('**/QuitBtn_DN'),
                                                         gui.find('**/QuitBtn_RLVR'),
                                                         gui.find('**/QuitBtn_UP')), thumb_relief=None,
                                             thumb_geom_scale=(0.75, 1, 0.75), command=self.setToonRotation)
        self.resetToonButton = DirectButton(parent=self,
                                            image=(gui.find('**/QuitBtn_UP'),
                                                   gui.find('**/QuitBtn_DN'),
                                                    gui.find('**/QuitBtn_RLVR')), relief=None,
                                            text='Reset Toon', text_scale=0.05, text_pos=(0, -0.0125), scale=0.8,
                                            pos=(-0.25, 0, -0.6), command=self.resetToonPrompt)
        # TODO: Create functionality for Apply Changes button.
        self.applyChangesButton = DirectButton(parent=self,
                                            image=(gui.find('**/QuitBtn_UP'),
                                                   gui.find('**/QuitBtn_DN'),
                                                   gui.find('**/QuitBtn_RLVR')), relief=None,
                                            text='Apply Changes', text_scale=0.05, text_pos=(0, -0.0125), scale=0.8,
                                            pos=(-0.65, 0, -0.6))
        gui.removeNode()

    def unload(self):
        self.toon.delete()
        self.toonRotateSlider.removeNode()

    def enter(self):
        # Update Toon model to accomodate for any changes made on different tabs
        global toonRotation
        self.updateToon()
        self.toon.setH(toonRotation)

        # Update Toon Rotation Slider
        self.toonRotateSlider['state'] = DGG.NORMAL
        self.toonRotateSlider['value'] = toonRotation
        self.show()

    def exit(self):
        self.toonRotateSlider['state'] = DGG.DISABLED
        self.hide()

    # Updates the Toon model
    def updateToon(self):
        global toonDNA, toonAcc
        self.toon.updateToonDNA(toonDNA, 1)
        # Replay Toon neutral animation due to a bug with forcing DNA changes causing the legs to not animate.
        self.toon.loop('neutral')
        self.toon.setHat(toonAcc[0][0], toonAcc[0][1], toonAcc[0][2])
        self.toon.setGlasses(toonAcc[1][0], toonAcc[1][1], toonAcc[1][2])
        self.toon.setBackpack(toonAcc[2][0], toonAcc[2][1], toonAcc[2][2])
        self.toon.setShoes(toonAcc[3][0], toonAcc[3][1], toonAcc[3][2])

        # In case the Toon's head change results in the Toon looking around
        self.toon.stopLookAroundNow()

    # Changes the global Toon rotation value to the slider value, then sets the Toon's rotation to it.
    def setToonRotation(self):
        global toonRotation
        toonRotation = self.toonRotateSlider.getValue()
        self.toon.setH(toonRotation)

    # Prompts the user asking if they want to reset the preview Toon
    def resetToonPrompt(self):
        self.diag = TTDialog.TTDialog(parent=aspect2d, text="This will set the preview Toon's DNA and accessories to that of your current Toon. Any unapplied changes will be lost. Are you sure you want to reset the preview Toon?",
                                      style=TTDialog.YesNo, fadeScreen=0.5, command=self.resetToon)
        self.diag.show()

    # Resets the Toon
    def resetToon(self, choice = 0):
        global toonDNA, toonAcc
        if choice == 1:
            toonDNA = base.localAvatar.getStyle()
            toonAcc = [base.localAvatar.getHat(), base.localAvatar.getGlasses(),
                       base.localAvatar.getBackpack(), base.localAvatar.getShoes()]
            self.updateToon()
        self.diag.destroy()

# Toon Body Customization Tab
class BodyTabPage(ToonTabPageBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('BodyTabPage')

    def __init__(self, parent = aspect2d):
        self.speciesButtons = []
        ToonTabPageBase.__init__(self, parent=parent)

    def load(self):
        ToonTabPageBase.load(self)

        # Create Species Buttons
        gui = loader.loadModel('phase_3/models/gui/laff_o_meter')

        # Position multipliers, for versatility with species.
        x = 0
        y = 0
        for species in ToonDNA.toonSpeciesTypes:
            head = ToonDNA.getSpeciesName(species)
            # Because the rabbit's laff meter model is called "bunnyhead", we change head to match that.
            if head == 'rabbit':
                head = 'bunny'
            # TODO: Add functionality for the buttons.
            button = DirectButton(parent=self, state=DGG.DISABLED, geom=gui.find('**/' + head + 'head'),
                                  relief=None, pos=(0.1 + ((0.7 / 5) * x), 0, 0.45 - (0.1 * y)),
                                  scale=0.04)
            button.hide()
            self.speciesButtons.append(button)
            # Start a new row if we're starting a row higher than 6.
            x += 1
            if x > 5:
                x = 0
                y += 1
        gui.removeNode()

        # Create Head Buttons
        # TODO: Create a Direct Frame that encapsulates 4 ToonHeads (2 for mouse) that act as buttons to change the head. Do a similar thing for Torsos and Legs.

    def unload(self):
        ToonTabPageBase.unload(self)

    def enter(self):
        ToonTabPageBase.enter(self)
        for button in self.speciesButtons:
            button.show()
            button['state'] = DGG.NORMAL

    def exit(self):
        ToonTabPageBase.exit(self)
        for button in self.speciesButtons:
            button.hide()
            button['state'] = DGG.DISABLED

    # When the preview Toon updates, update the buttons to match.
    def updateToon(self):
        global toonDNA
        ToonTabPageBase.updateToon(self)
        for button in self.speciesButtons:
            button['geom_color'] = toonDNA.getHeadColor()

# TODO: Create different sections for shirts. Section 1: Combined TopTex and SleeveTex combos. Section 2: All TopTex. Section 3: All SleeveTex
class ClothingTabPage(ToonTabPageBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('ClothingTabPage')

    def __init__(self, parent = aspect2d):
        ToonTabPageBase.__init__(self, parent=parent)

    def load(self):
        ToonTabPageBase.load(self)

    def unload(self):
        ToonTabPageBase.unload(self)

    def enter(self):
        ToonTabPageBase.enter(self)

    def exit(self):
        ToonTabPageBase.exit(self)

class AccTabPage1(ToonTabPageBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('AccTabPage1')

    def __init__(self, parent = aspect2d):
        ToonTabPageBase.__init__(self, parent=parent)

    def load(self):
        ToonTabPageBase.load(self)

    def unload(self):
        ToonTabPageBase.unload(self)

    def enter(self):
        ToonTabPageBase.enter(self)

    def exit(self):
        ToonTabPageBase.exit(self)

class AccTabPage2(ToonTabPageBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('AccTabPage2')

    def __init__(self, parent = aspect2d):
        ToonTabPageBase.__init__(self, parent=parent)

    def load(self):
        ToonTabPageBase.load(self)

    def unload(self):
        ToonTabPageBase.unload(self)

    def enter(self):
        ToonTabPageBase.enter(self)

    def exit(self):
        ToonTabPageBase.exit(self)
