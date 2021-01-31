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
from toontown.toon import ToonHead
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

        # Copy player Toon attributes for preview Toon DNA and Accessories
        global toonDNA, toonAcc
        toonDNA = ToonDNA.ToonDNA(type='t', dna=base.localAvatar.style)
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
        global toonDNA
        self.wordsTabPage.unload()
        self.clothingTabPage.unload()
        self.acc1Page.unload()
        self.acc2Page.unload()
        del self.title
        del toonDNA
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
# TODO: Create copy DNA buttons
class ToonTabPageBase(DirectFrame):

    def __init__(self, parent = aspect2d):
        DirectFrame.__init__(self, parent=parent, relief=None, pos=(0.0, 0.0, 0.0), scale=(1.0, 1.0, 1.0))
        self.load()

    def load(self):
        global toonDNA
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
        self.resetToonButton = DirectButton(parent=self, state=DGG.DISABLED,
                                            image=(gui.find('**/QuitBtn_UP'),
                                                   gui.find('**/QuitBtn_DN'),
                                                    gui.find('**/QuitBtn_RLVR')), relief=None,
                                            text='Reset Toon', text_scale=0.05, text_pos=(0, -0.0125), scale=0.8,
                                            pos=(-0.25, 0, -0.6), command=self.resetToonPrompt)
        # TODO: Create functionality for Apply Changes button.
        self.applyChangesButton = DirectButton(parent=self, state=DGG.DISABLED,
                                            image=(gui.find('**/QuitBtn_UP'),
                                                   gui.find('**/QuitBtn_DN'),
                                                   gui.find('**/QuitBtn_RLVR')), relief=None,
                                            text='Apply Changes', text_scale=0.05, text_pos=(0, -0.0125), scale=0.8,
                                            pos=(-0.65, 0, -0.6))
        gui.removeNode()

    def unload(self):
        self.toon.delete()
        self.toonRotateSlider.destroy()
        self.resetToonButton.destroy()
        self.applyChangesButton.destroy()

    def enter(self):
        # Update Toon model to accomodate for any changes made on different tabs
        global toonRotation
        self.updateToon()
        self.toon.setH(toonRotation)

        # Update Toon Rotation Slider
        self.toonRotateSlider['state'] = DGG.NORMAL
        self.toonRotateSlider['value'] = toonRotation
        self.resetToonButton['state'] = DGG.NORMAL
        self.applyChangesButton['state'] = DGG.NORMAL
        self.show()

    def exit(self):
        self.toonRotateSlider['state'] = DGG.DISABLED
        self.resetToonButton['state'] = DGG.DISABLED
        self.applyChangesButton['state'] = DGG.DISABLED
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

    # Resets the preview Toon to that of the current player Toon.
    def resetToon(self, choice = 0):
        global toonDNA, toonAcc
        if choice == 1:
            toonDNA = ToonDNA.ToonDNA(type='t', dna=base.localAvatar.style)
            toonAcc = [base.localAvatar.getHat(), base.localAvatar.getGlasses(),
                       base.localAvatar.getBackpack(), base.localAvatar.getShoes()]
            self.updateToon()
        self.diag.destroy()

# Toon Body Customization Tab
class BodyTabPage(ToonTabPageBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('BodyTabPage')

    def __init__(self, parent = aspect2d):

        # Create UI lists
        self.speciesGui = []
        self.bodyGui = []
        self.headGui = []
        self.torsoGui = []
        self.legGui = []
        self.colorGui = []
        self.genderButtons = []
        self.idLabels = []

        # Create other variables
        self.focusType = 0 # Determines which part is being focused: 0 = Head, 1 = Torso, 2 = Legs
        self.colorTargetAll = True

        ToonTabPageBase.__init__(self, parent=parent)

    def load(self):
        ToonTabPageBase.load(self)

        # -= Create Species Section =-
        laffMeterGui = loader.loadModel('phase_3/models/gui/laff_o_meter')

        # Position multipliers for button positions, for versatility with species.
        x = 0
        z = 0

        # -= Create Species Section =-
        for species in ToonDNA.toonSpeciesTypes:
            head = ToonDNA.getSpeciesName(species)
            # Because the rabbit's laff meter model is called "bunnyhead", we change head to match that.
            if head == 'rabbit':
                head = 'bunny'
            button = DirectButton(parent=self, state=DGG.DISABLED, image=laffMeterGui.find('**/' + head + 'head'),
                                  relief=None, pos=(0.45 + (0.14 * x), 0, 0.6 - (0.125 * z)),
                                  image_scale=0.04, image2_scale=0.044, command=self.changeSpecies, extraArgs=[species])
            self.speciesGui.append(button)
            # Start a new row if we're starting a row higher than 3.
            x += 1
            if x > 2:
                x = 0
                z += 1

        # Species Section Label (vertically centered according to the amount of rows)
        zDiff = 0.0625 * z
        if x == 0:
            zDiff -= 0.0625

        speciesLabel = DirectLabel(parent=self, relief=None, text='Species', text_scale=0.07, text_align=TextNode.ACenter,
                                   pos=(0.2, 0, 0.6 - zDiff))
        self.speciesGui.append(speciesLabel)

        # -= Create Body Header =-
        bodyLabel = DirectLabel(parent=self, relief=None, text='Head', text_scale=0.07, text_align=TextNode.ACenter,
                                pos=(0.45, 0, 0.1875))
        self.bodyGui.append(bodyLabel)

        arrowGui = loader.loadModel('phase_3/models/gui/create_a_toon_gui')
        leftArrow = DirectButton(parent=self, state=DGG.DISABLED, geom=(arrowGui.find('**/CrtATn_R_Arrow_UP'),
                                                                        arrowGui.find('**/CrtATn_R_Arrow_DN'),
                                                                        arrowGui.find('**/CrtATn_R_Arrow_RLVR'),
                                                                        arrowGui.find('**/CrtATn_R_Arrow_DN')),
                                 scale=(0.5, 0.5, 0.5), relief=None, pos=(0.225, 0, 0.2), hpr=(180, 0, 0),
                                 command=self.changeFocusType, extraArgs=[-1])
        self.bodyGui.append(leftArrow)
        rightArrow = DirectButton(parent=self, state=DGG.DISABLED, geom=(arrowGui.find('**/CrtATn_R_Arrow_UP'),
                                                                        arrowGui.find('**/CrtATn_R_Arrow_DN'),
                                                                        arrowGui.find('**/CrtATn_R_Arrow_RLVR'),
                                                                        arrowGui.find('**/CrtATn_R_Arrow_DN')),
                                  scale=(-0.5, 0.5, 0.5), relief=None, pos=(0.675, 0, 0.2), hpr=(180, 0, 0),
                                  command=self.changeFocusType, extraArgs=[1])
        self.bodyGui.append(rightArrow)

        arrowGui.removeNode()

        # -= Create Head Section =-
        headFrame = DirectFrame(parent=self, pos=(0.45, 0, 0), relief=DGG.SUNKEN, frameSize=(-0.355, 0.355, -0.1, 0.1),
                                frameColor=(0.85, 0.95, 1, 1), borderWidth=(0.01, 0.01))
        self.headGui.append(headFrame)

        x = 0
        for headType in ['ls', 'ss', 'sl', 'll']:
            # Specifying a frame size due to the fact that the geom is going to change as the species changes.
            headButton = DirectButton(parent=headFrame, state=DGG.DISABLED, frameSize=(-0.0875, 0.0875, -0.1, 0.1),
                                      relief=None, pos=(-0.2625 + x, 0, 0), hpr=(180, 0, 0), command=self.changeHead,
                                      extraArgs=[headType])

            self.headGui.append(headButton)

            x += 0.175

        laffMeterGui.removeNode()

        # -= Create Torso Section =-
        torsoFrame = DirectFrame(parent=self, pos=(0.45, 0, 0), relief=DGG.SUNKEN,
                                 frameSize=(-0.355, 0.355, -0.1, 0.1), frameColor=(0.85, 0.95, 1, 1),
                                 borderWidth=(0.01, 0.01))
        torsoFrame.hide()
        self.torsoGui.append(torsoFrame)

        x = 0
        for torsoType in ['s', 'm', 'l']:
            # Create torso model and button. Torso won't have arms or neck, so it's kinda just a jellybean thing.
            size = torsoType.upper() + torsoType.upper()
            torsoModel = loader.loadModel('phase_3/models/char/dog%s_Naked-torso-1000' % size)
            torsoModel.find('**/arms').removeNode()
            torsoModel.find('**/hands').removeNode()
            torsoModel.find('**/neck').removeNode()
            torsoModel.setBin('unsorted', 0, 1)
            torsoModel.setDepthTest(True)
            torsoModel.setDepthWrite(True)

            torsoButton = DirectButton(parent=torsoFrame, state=DGG.DISABLED, geom=torsoModel, geom_scale=0.075,
                                       geom2_scale=0.0825, relief=None, pos=(-0.2 + x, 0, -0.05), hpr=(180, 0, 0),
                                       command=self.changeTorso, extraArgs=[torsoType])

            self.torsoGui.append(torsoButton)
            x += 0.2

        # -= Create Legs Section =-
        legFrame = DirectFrame(parent=self, pos=(0.45, 0, 0), relief=DGG.SUNKEN, frameSize=(-0.355, 0.355, -0.1, 0.1),
                               frameColor=(0.85, 0.95, 1, 1), borderWidth=(0.01, 0.01))
        legFrame.hide()
        self.legGui.append(legFrame)
        x = 0
        for legType in ['s', 'm', 'l']:
            # Create leg model and button. Legs won't have shoes.
            legModel = loader.loadModel('phase_3/models/char/tt_a_chr_dg%s_shorts_legs_1000' % legType)
            legModel.find('**/shoes').removeNode()
            legModel.find('**/boots_short').removeNode()
            legModel.find('**/boots_long').removeNode()
            legModel.setBin('unsorted', 0, 1)
            legModel.setDepthTest(True)
            legModel.setDepthWrite(True)
            legButton = DirectButton(parent=legFrame, state=DGG.DISABLED, geom=legModel, geom_scale=0.065,
                                     geom2_scale=0.0715, relief=None, pos=(-0.2 + x, 0, -0.09), hpr=(180, 0, 0),
                                     command=self.changeLegs, extraArgs=[legType])
            self.legGui.append(legButton)
            x += 0.2

        # -= Create Color Section =-
        colorLabel = DirectLabel(parent=self, relief=None, text='Color', text_scale=0.07, text_align=TextNode.ACenter,
                                 pos=(0.45, 0, -0.1625))
        self.colorGui.append(colorLabel)

        normalButtonGui = loader.loadModel('phase_3/models/gui/pick_a_toon_gui')
        colorTargetAllButton = DirectButton(parent=self, state=DGG.DISABLED,
                                            image=(normalButtonGui.find('**/QuitBtn_UP'),
                                                   normalButtonGui.find('**/QuitBtn_DN'),
                                                   normalButtonGui.find('**/QuitBtn_RLVR')), relief=None,
                                            text='Target All', text_scale=0.05, text_pos=(0, -0.0125), scale=0.8,
                                            pos=(0.45, 0, -0.3 - (z * 0.07)), command=self.toggleColorTarget)
        self.colorGui.append(colorTargetAllButton)

        minnieButtonGui = loader.loadModel('phase_3.5/models/gui/matching_game_gui')
        i = 0
        x = 0
        z = 0

        # Ensure that there are 3 rows of color buttons.
        rowNum = len(ToonDNA.allColorsList)
        rowLimit = 0.0
        while rowNum > 3:
            rowLimit += 1.0
            rowNum = len(ToonDNA.allColorsList) / rowLimit
            print str(rowLimit) + " " + str(rowNum)

        for color in ToonDNA.allColorsList:
            # Frame size specified due to how bad of a hitbox the image is on it's own in this case.
            colorButton = DirectButton(parent=self, state=DGG.DISABLED, relief=None,
                                       image=minnieButtonGui.find('**/minnieCircle'), image_scale=0.35,
                                       image2_scale=0.385, image_color=color, image_pos=(0.355 / rowLimit, 0, 0.035),
                                       frameSize=(0, 0.71 / rowLimit, 0, 0.07),
                                       pos=(0.095 + ((0.71 * x) / rowLimit), 0, -0.3 - (z * 0.07)),
                                       command=self.changeColors, extraArgs=[i])
            self.colorGui.append(colorButton)

            i += 1
            x += 1
            if x >= rowLimit:
                x = 0
                z += 1

        colorTargetAllButton.setZ(-0.3 - (z * 0.07))
        minnieButtonGui.removeNode()

        # -= Create Gender Buttons =-
        # Trans rights
        makeAToonGui = loader.loadModel('phase_3/models/gui/tt_m_gui_mat_mainGui')

        boyButton = DirectButton(parent=self, relief=None, image=(makeAToonGui.find('**/tt_t_gui_mat_boyUp'),
                                                                  makeAToonGui.find('**/tt_t_gui_mat_boyDown'),
                                                                  makeAToonGui.find('**/tt_t_gui_mat_boyUp')),
                                 pos=(0.15, 0, -0.6), image_scale=0.35, image2_scale=0.385, command=self.transGender,
                                 extraArgs=['m'])
        self.genderButtons.append(boyButton)

        girlButton = DirectButton(parent=self, relief=None, image=(makeAToonGui.find('**/tt_t_gui_mat_girlUp'),
                                                                   makeAToonGui.find('**/tt_t_gui_mat_girlDown'),
                                                                   makeAToonGui.find('**/tt_t_gui_mat_girlUp')),
                                  pos=(0.75, 0, -0.6), image_scale=0.35, image2_scale=0.385, command=self.transGender,
                                  extraArgs=['f'])
        self.genderButtons.append(girlButton)

        makeAToonGui.removeNode()

        # -= Create ID Labels =-
        # These will appear by the respective body parts with info about them.

        bodyIDLabel = DirectLabel(parent=self, relief=None, text='', text_scale=0.05, text_align=TextNode.ACenter,
                                  text_font=ToontownGlobals.getSignFont(), pos=(0.45, 0, 0.125))
        self.idLabels.append(bodyIDLabel)

        colorIDLabel = DirectLabel(parent=self, relief=None, text='', text_scale=0.05, text_align=TextNode.ACenter,
                                   text_font=ToontownGlobals.getSignFont(), pos=(0.45, 0, -0.2125))
        self.idLabels.append(colorIDLabel)

        # Create 3 pairs of labels for size and color labeling.
        ##for type in range(3):
        #    sizeLabel = DirectLabel(parent=self, relief=None, text='', text_scale=0.06,
        #                            text_font=ToontownGlobals.getSignFont(), text_align=TextNode.ARight,
        #                            pos=(-0.6, 0, 0), text_mayChange=True)
        #    self.idLabels.append(sizeLabel)
        #
        #    colorLabel = DirectLabel(parent=self, relief=None, text='', text_scale=0.06,
        #                             text_font=ToontownGlobals.getSignFont(), text_align=TextNode.ALeft,
        #                             pos=(-0.3, 0, 0), text_mayChange=True)
        #    self.idLabels.append(colorLabel)

    def unload(self):
        ToonTabPageBase.unload(self)
        # Destroy all GUI
        for list in [self.speciesGui, self.bodyGui, self.headGui, self.torsoGui, self.legGui, self.colorGui,
                     self.genderButtons, self.idLabels]:
            for button in list:
                button.destroy()
            del list

    def enter(self):
        ToonTabPageBase.enter(self)
        # Enable all general GUI, then enable the specific focus GUI.
        for list in [self.speciesGui, self.bodyGui, self.colorGui, self.genderButtons]:
            for button in list:
                button['state'] = DGG.NORMAL
        self.changeFocusType()

    def exit(self):
        ToonTabPageBase.exit(self)
        # Disable all GUI.
        for list in [self.speciesGui, self.bodyGui, self.headGui, self.torsoGui, self.legGui, self.colorGui,
                     self.genderButtons]:
            for button in list:
                button['state'] = DGG.DISABLED

    # When the preview Toon updates, update the buttons to match.
    def updateToon(self):
        global toonDNA
        ToonTabPageBase.updateToon(self)

        buttonToonDNA = ToonDNA.ToonDNA()
        # Update species buttons to match head color
        for button in self.speciesGui:
            button['image_color'] = toonDNA.getHeadColor()

        # Update head buttons to accommodate for species and head color.
        # This for loop is assuming that the buttons in self.headGui are in this order: ls, ss, sl, ll
        typeId = 0
        headTypes = ['ls', 'ss', 'sl', 'll']
        for button in self.headGui:
            # For each Toon Head button, replace the button geom with a new geom of the head.
            if isinstance(button, DirectButton):
                if not (typeId >= 2 and toonDNA.head[0] == 'm'):
                    # If the button is hidden, unhide it.
                    if button.isHidden():
                        button.show()
                        button['state'] = DGG.NORMAL
                    head = ToonHead.ToonHead()
                    # Copy preview Toon DNA, change the DNA head, then set up head.
                    buttonToonDNA.makeFromNetString(toonDNA.makeNetString())
                    buttonToonDNA.head = toonDNA.head[0] + headTypes[typeId]
                    head.setupHead(buttonToonDNA, forGui=True)
                    # If a head already exists on the button, get rid of it.
                    if button['geom']:
                        button['geom'].stopLookAroundNow()
                        button['geom'].removeNode()
                    # Set head as new button head.
                    button['geom'] = head
                    button['geom_scale'] = ToontownGlobals.toonBodyScales[buttonToonDNA.getAnimal()] / 8.5
                    button['geom2_scale'] = button['geom_scale'] * 1.1
                    button['geom_pos'] = (0, 0, -0.035)
                    typeId += 1
                else:
                    button.hide()
                    button['state'] = DGG.DISABLED
        del buttonToonDNA

        # Update torso buttons to accomodate for torso color.
        for button in self.torsoGui:
            if isinstance(button, DirectButton):
                button['geom_color'] = ToonDNA.allColorsList[toonDNA.armColor]

        # Update leg buttons to accomodate for torso color.
        for button in self.legGui:
            if isinstance(button, DirectButton):
                button['geom_color'] = ToonDNA.allColorsList[toonDNA.legColor]

        # Update size and color labeling
        self.updateIDLabels()

        # Update size and color labeling (old version, kept in here as a memento. Feel free to discard)

        #dataTypes = [toonDNA.head, toonDNA.headColor, toonDNA.torso, toonDNA.armColor, toonDNA.legs,
        #             toonDNA.legColor]
        #zPosList = [self.toon.getHeadParts()[0].getZ(self), self.toon.getTorsoParts()[0].getZ(self), -0.4]

        ## 0-1 = Head, 2-3 = Torso, 4-5 = Legs. First is size, second is color.
        #for type in range(6):
        #    # If this is a color label, label it as such. Otherwise, label the size.
        #    isColor = type % 2
        #    if isColor:
        #        self.idLabels[type]['text'] = '%s\n(%d)' % (TTLocalizer.NumToColor[dataTypes[type]], dataTypes[type])
        #        self.idLabels[type]['text_fg'] = ToonDNA.allColorsList[dataTypes[type]]
        #    else:
        #        # If the type is for head size, print the species name instead of a size. Otherwise, print the size.
        #        if type == 0:
        #            self.idLabels[type]['text'] = '%s\n(%s)' % (TTLocalizer.AnimalToSpecies[ToonDNA.getSpeciesName(dataTypes[type])], dataTypes[type])
        #        else:
        #            sizeNames = {'s':'Short', 'm':'Medium', 'l':'Long'}
        #            self.idLabels[type]['text'] = '%s\n(%s)' % (sizeNames[dataTypes[type][0]], dataTypes[type])
        #        self.idLabels[type]['text_fg'] = ToonDNA.allColorsList[dataTypes[type + 1]]

        #    # Position the Z pos to match that of the actual part positions.
        #    categoryType = int(math.floor(type / 2))
        #    print categoryType
        #    zPos = zPosList[categoryType]

        #    # Torso Adjustment
        #    if categoryType == 1:
        #        zPos += (0.2 if dataTypes[type - isColor][0] == 'l' else 0.1) * ToontownGlobals.toonBodyScales[toonDNA.getAnimal()]

        #    # Leg Adjustment
        #    if categoryType == 2:
        #        legPos = [0.1, 0.15, 0.2]
        #        zPos += legPos[ToonDNA.toonLegTypes.index(dataTypes[type - isColor])] * ToontownGlobals.toonBodyScales[toonDNA.getAnimal()]

        #    self.idLabels[type].setZ(zPos)

    # Change focused body type. Enables the current body section and disables all other body sections.
    def changeFocusType(self, typeChange=0):
        global toonDNA
        self.focusType = (self.focusType + typeChange) % 3
        labelNames = ['Head', 'Torso', 'Legs']
        # Change body section label
        self.bodyGui[0]['text'] = labelNames[self.focusType]

        i = 0
        b = 0
        for list in [self.headGui, self.torsoGui, self.legGui]:
            # If current ID matches the focus type, enable the buttons. Otherwise, disable them.
            if i == self.focusType:
                for button in list:
                    # Prevent long muzzle mouse head buttons from showing
                    button.show()
                    button['state'] = DGG.NORMAL
                    if i == 0 and isinstance(button, DirectButton):
                        if b >= 2 and toonDNA.head[0] == 'm':
                            button.hide()
                            button['state'] = DGG.DISABLED
                        b += 1
            else:
                for button in list:
                    button.hide()
                    button['state'] = DGG.DISABLED
            i += 1

        # Update size and color labeling
        self.updateIDLabels()

    # Changes the species of the preview Toon.
    def changeSpecies(self, type):
        global toonDNA
        # If the species type is valid, replace the DNA's head type with the species and update the preview Toon.
        # Otherwise, just notify console that the species is invalid.
        if type in ToonDNA.toonSpeciesTypes:
            newHead = type + toonDNA.head[1:]
            # If the current head type uses a long muzzle and the new species is mouse, change muzzle to short since
            # long mouse muzzles don't exist. (yet)
            if type == 'm' and newHead[2:] == 'l':
                newHead = newHead[:2] + 's'
            toonDNA.head = newHead
            self.updateToon()
        else:
            self.notify.warning("Species type '%s' does not exist" % type)

    # Changes the head of the preview Toon.
    def changeHead(self, type):
        global toonDNA
        toonDNA.head = toonDNA.head[0] + type
        self.updateToon()

    # Changes the torso of the preview Toon.
    def changeTorso(self, type):
        global toonDNA
        toonDNA.torso = type if len(toonDNA.torso) == 1 else type + toonDNA.torso[1]
        self.updateToon()

    # Changes the legs of the preview Toon.
    def changeLegs(self, type):
        global toonDNA
        toonDNA.legs = type
        self.updateToon()

    # Changes the colors of the preview Toon.
    def changeColors(self, id):
        global toonDNA

        # If the color buttons are targetting all parts, change all parts. If not, change only the one that's being focused.
        # There's probably a better way to do this.
        if self.colorTargetAll or self.focusType == 0:
            toonDNA.headColor = id
        if self.colorTargetAll or self.focusType == 1:
            toonDNA.armColor = id
        if self.colorTargetAll or self.focusType == 2:
            toonDNA.legColor = id

        self.updateToon()

    # Change the gender of the preview Toon.
    def transGender(self, newGender):
        global toonDNA
        newMaximum = (len(ToonDNA.BoyShorts) - 1) if newGender == 'm' else (len(ToonDNA.GirlBottoms) - 1)
        # Since we're still using separate bottoms lists, if the bottoms that the preview Toon has are of a higher id
        # than the new gender's list, then reset the bottom to 0 and notify the player.
        if (toonDNA.botTex > newMaximum):
            base.localAvatar.setSystemMessage(0,
                'Spellbook: The pants ID (%d) is higher than the maximum for %s (%d). Resetting to 0...' % (
                toonDNA.botTex, 'boys' if newGender == 'm' else 'girls', newMaximum))
            toonDNA.botTex = 0
        toonDNA.gender = newGender

        # Update Toon torso to match bottom.
        if len(toonDNA.torso) > 1:
            toonDNA.torso = toonDNA.torso[0] + 's'
            if newGender == 'f' :
                if ToonDNA.GirlBottoms[toonDNA.botTex][1] == 1:
                    toonDNA.torso = toonDNA.torso[0] + 'd'
        self.updateToon()

    # Toggles the target of the color buttons.
    def toggleColorTarget(self):
        self.colorTargetAll = not self.colorTargetAll
        self.colorGui[1]['text'] = 'Target All' if self.colorTargetAll else 'Target Selected'

    # Update ID labels
    def updateIDLabels(self):
        dataTypes = [toonDNA.head, toonDNA.torso, toonDNA.legs]
        dataTypeColors = [toonDNA.headColor, toonDNA.armColor, toonDNA.legColor]
        sizeNames = {'s': 'Short', 'm': 'Medium', 'l': 'Long'}

        # Size Label
        sizeName = sizeNames.get(dataTypes[self.focusType][0])
        if self.focusType == 0:
            sizeName = TTLocalizer.AnimalToSpecies[ToonDNA.getSpeciesName(dataTypes[0])]

        self.idLabels[0]['text'] = '%s (%s)' % (sizeName, dataTypes[self.focusType])
        self.idLabels[0]['text_fg'] = ToonDNA.allColorsList[dataTypeColors[self.focusType]]

        # Color Label
        self.idLabels[1]['text'] = '%s (%d)' % (
            TTLocalizer.NumToColor[dataTypeColors[self.focusType]], dataTypeColors[self.focusType])
        self.idLabels[1]['text_fg'] = ToonDNA.allColorsList[dataTypeColors[self.focusType]]

class ClothingTabPage(ToonTabPageBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('ClothingTabPage')

    def __init__(self, parent = aspect2d):

        # Create UI lists

        self.mainGui = []
        self.clothFrame = None
        self.clothButtons = []
        self.clothPages = None
        self.clothIDLabel = None
        self.subclothIDLabel = None
        self.leftPageButton = None
        self.rightPageButton = None
        self.colorGui = []
        self.colorIDLabel = None
        self.colorButtons = []
        self.gloveButtons = []

        # Other variables

        # Cloth Sections: 0 - Combined Shirts, 1 - TopTex, 2 - SleeveTex, 3 - Bottoms
        # Color Sections: 0 - Clothing Color, 1 - Glove Color

        self.clothSection = 0
        self.clothPage = 0
        self.maxClothPage = 0
        self.colorSection = 0
        self.spinIvals = []

        # Generate a chronological combined shirt list

        self.shirtStyles = []
        self.createShirtStyleList()


        ToonTabPageBase.__init__(self, parent=parent)

    # Generates a chronological combined shirt list
    def createShirtStyleList(self):
        for DNAShirtStyle in ToonDNA.ShirtStyles.values():
            # If the list is empty, add the first shirt.  Otherwise, go through the new list
            if len(self.shirtStyles) == 0:
                self.shirtStyles.append((DNAShirtStyle[0], DNAShirtStyle[1]))
            else:
                for i in range(0, len(self.shirtStyles)):
                    # If this DNA shirt ID matches with the current shirt ID, ditch this shirt
                    if self.shirtStyles[i][0] == DNAShirtStyle[0]:
                        break
                    # If we've reached the end of the list, append new shirt
                    elif i == len(self.shirtStyles):
                        self.shirtStyles.append((DNAShirtStyle[0], DNAShirtStyle[1]))
                        break
                    # If the DNA Shirt ID is smaller than the current registered ID, insert shirt at this position.
                    elif self.shirtStyles[i][0] > DNAShirtStyle[0]:
                        self.shirtStyles.insert(i, (DNAShirtStyle[0], DNAShirtStyle[1]))
                        break

    def load(self):
        ToonTabPageBase.load(self)

        # -= Clothing Section =-
        clothLabel = DirectLabel(parent=self, relief=None, text='Tops', text_scale=0.07, text_align=TextNode.ACenter,
                               pos=(0.45, 0, 0.51))
        self.mainGui.append(clothLabel)

        # Page label
        self.clothPages = DirectLabel(parent=self, relief=None, text='1/1', text_scale=0.045, text_align=TextNode.ACenter,
                                      pos=(0.45, 0, 0.46))
        self.mainGui.append(self.clothPages)

        # Cloth ID Label
        self.clothIDLabel = DirectLabel(parent=self, relief=None, text='Plain (0)', text_scale=0.045,
                                        text_align=TextNode.ACenter, text_fg=ToonDNA.ClothesColors[27],
                                        text_font=ToontownGlobals.getSignFont(), pos=(0.45, 0, -0.12))

        # "Subcloth" is mostly for the sleeve ID when using the combined shirt section
        self.subclothIDLabel = DirectLabel(parent=self, relief=None, text='Plain (0)', text_scale=0.035,
                                           text_align=TextNode.ACenter, text_fg=ToonDNA.ClothesColors[27],
                                           text_font=ToontownGlobals.getSignFont(), pos=(0.45, 0, -0.15))


        self.clothFrame = DirectFrame(parent=self, pos=(0.45, 0, 0.275), relief=DGG.SUNKEN, frameSize=(-0.3, 0.3, -0.35, 0.175),
                                      frameColor=(0.85, 0.95, 1, 1), borderWidth=(0.01, 0.01))

        # Clothing Tab buttons
        arrowGui = loader.loadModel('phase_3/models/gui/create_a_toon_gui')
        leftArrow = DirectButton(parent=self, state=DGG.DISABLED, geom=(arrowGui.find('**/CrtATn_R_Arrow_UP'),
                                                                        arrowGui.find('**/CrtATn_R_Arrow_DN'),
                                                                        arrowGui.find('**/CrtATn_R_Arrow_RLVR'),
                                                                        arrowGui.find('**/CrtATn_R_Arrow_DN')),
                                 scale=(0.5, 0.5, 0.5), relief=None, pos=(0.225, 0, 0.51), hpr=(180, 0, 0),
                                 command=self.changeFocusType, extraArgs=[-1])
        self.mainGui.append(leftArrow)
        rightArrow = DirectButton(parent=self, state=DGG.DISABLED, geom=(arrowGui.find('**/CrtATn_R_Arrow_UP'),
                                                                         arrowGui.find('**/CrtATn_R_Arrow_DN'),
                                                                         arrowGui.find('**/CrtATn_R_Arrow_RLVR'),
                                                                         arrowGui.find('**/CrtATn_R_Arrow_DN')),
                                  scale=(-0.5, 0.5, 0.5), relief=None, pos=(0.675, 0, 0.51), hpr=(180, 0, 0),
                                  command=self.changeFocusType, extraArgs=[1])
        self.mainGui.append(rightArrow)

        # Clothing Page buttons
        gui = loader.loadModel('phase_3.5/models/gui/friendslist_gui')
        self.leftPageButton = DirectButton(parent=self.clothFrame, state=DGG.DISABLED, pos=(-0.35, 0, -0.0875), relief=None,
                                           geom=(gui.find('**/FndsLst_ScrollUp'),
                                            gui.find('**/FndsLst_ScrollDN'),
                                            gui.find('**/FndsLst_ScrollUp_Rllvr'),
                                            gui.find('**/FndsLst_ScrollUp')), scale=(1.3, 1.3, -1.3),
                                           geom3_color=Vec4(1, 1, 1, 0.2), hpr=(0, 0, 90), command=self.setPage,
                                           extraArgs=[-1])
        self.rightPageButton = DirectButton(parent=self.clothFrame, state=DGG.DISABLED, pos=(0.35, 0, -0.0875), relief=None,
                                            geom=(gui.find('**/FndsLst_ScrollUp'),
                                            gui.find('**/FndsLst_ScrollDN'),
                                            gui.find('**/FndsLst_ScrollUp_Rllvr'),
                                            gui.find('**/FndsLst_ScrollUp')), scale=(1.3, 1.3, 1.3),
                                            geom3_color=Vec4(1, 1, 1, 0.2), hpr=(0, 0, 90), command=self.setPage,
                                            extraArgs=[1])
        self.mainGui.append(self.leftPageButton)
        self.mainGui.append(self.rightPageButton)
        gui.removeNode()

        # -= Color Section =-

        colorLabel = DirectLabel(parent=self, relief=None, text='Color', text_scale=0.07, text_align=TextNode.ACenter,
                                 pos=(0.45, 0, -0.25))
        self.colorGui.append(colorLabel)

        self.colorIDLabel = DirectLabel(parent=self, relief=None, text='White (27)', text_scale=0.05, text_align=TextNode.ACenter,
                                   text_font=ToontownGlobals.getSignFont(), pos=(0.45, 0, -0.3))

        # Color section arrow buttons

        leftColorArrow = DirectButton(parent=self, state=DGG.DISABLED, geom=(arrowGui.find('**/CrtATn_R_Arrow_UP'),
                                                                             arrowGui.find('**/CrtATn_R_Arrow_DN'),
                                                                             arrowGui.find('**/CrtATn_R_Arrow_RLVR'),
                                                                             arrowGui.find('**/CrtATn_R_Arrow_DN')),
                                      scale=(0.5, 0.5, 0.5), relief=None, pos=(0.15, 0, -0.24), hpr=(180, 0, 0),
                                      command=self.changeColorFocusType, extraArgs=[-1])
        self.colorGui.append(leftColorArrow)
        rightColorArrow = DirectButton(parent=self, state=DGG.DISABLED, geom=(arrowGui.find('**/CrtATn_R_Arrow_UP'),
                                                                              arrowGui.find('**/CrtATn_R_Arrow_DN'),
                                                                              arrowGui.find('**/CrtATn_R_Arrow_RLVR'),
                                                                              arrowGui.find('**/CrtATn_R_Arrow_DN')),
                                       scale=(-0.5, 0.5, 0.5), relief=None, pos=(0.75, 0, -0.24), hpr=(180, 0, 0),
                                       command=self.changeColorFocusType, extraArgs=[1])
        self.colorGui.append(rightColorArrow)

        arrowGui.removeNode()

        minnieButtonGui = loader.loadModel('phase_3.5/models/gui/matching_game_gui')

        # -- First, do clothing color
        i = 0
        x = 0
        z = 0

        # Ensure that there are 3 rows of color buttons.
        rowNum = len(ToonDNA.ClothesColors)
        rowLimit = 0.0
        while rowNum > 3:
            rowLimit += 1.0
            rowNum = len(ToonDNA.ClothesColors) / rowLimit

        for color in ToonDNA.ClothesColors:
            # Frame size specified due to how bad of a hitbox the image is on it's own in this case.
            colorButton = DirectButton(parent=self, state=DGG.DISABLED, relief=None,
                                       image=minnieButtonGui.find('**/minnieCircle'), image_scale=0.35,
                                       image2_scale=0.385, image_color=color, image_pos=(0.355 / rowLimit, 0, 0.035),
                                       frameSize=(0, 0.71 / rowLimit, 0, 0.07),
                                       pos=(0.095 + ((0.71 * x) / rowLimit), 0, -0.3875 - (z * 0.07)),
                                       command=self.updateClothes, extraArgs=[i, True])
            self.colorButtons.append(colorButton)

            i += 1
            x += 1
            if x >= rowLimit:
                x = 0
                z += 1

        # -- Second, do glove color
        i = 0
        x = 0
        z = 0

        # Ensure that there are 3 rows of color buttons.
        rowNum = len(ToonDNA.allColorsList)
        rowLimit = 0.0
        while rowNum > 3:
            rowLimit += 1.0
            rowNum = len(ToonDNA.allColorsList) / rowLimit

        for color in ToonDNA.allColorsList:
            # Frame size specified due to how bad of a hitbox the image is on it's own in this case.
            colorButton = DirectButton(parent=self, state=DGG.DISABLED, relief=None,
                                       image=minnieButtonGui.find('**/minnieCircle'), image_scale=0.35,
                                       image2_scale=0.385, image_color=color, image_pos=(0.355 / rowLimit, 0, 0.035),
                                       frameSize=(0, 0.71 / rowLimit, 0, 0.07),
                                       pos=(0.095 + ((0.71 * x) / rowLimit), 0, -0.3875 - (z * 0.07)),
                                       command=self.updateGloves, extraArgs=[i])
            self.gloveButtons.append(colorButton)

            i += 1
            x += 1
            if x >= rowLimit:
                x = 0
                z += 1

        minnieButtonGui.removeNode()

        # -= Create Buttons =-
        self.generateButtonGeom()


    def unload(self):
        ToonTabPageBase.unload(self)
        # Stop all spin intervals
        for ival in self.spinIvals:
            ival.finish()
        # Destroy all GUI
        for list in [self.mainGui, self.clothButtons, self.colorGui, self.colorButtons, self.gloveButtons]:
            for button in list:
                button.destroy()
            del list
        self.clothFrame.destroy()
        del self.clothFrame

    def enter(self):
        ToonTabPageBase.enter(self)
        # Enable all GUI
        for list in [self.mainGui, self.clothButtons, self.colorGui]:
            for button in list:
                button['state'] = DGG.NORMAL

        self.changeColorFocusType()
        self.generateButtonGeom()

    def exit(self):
        ToonTabPageBase.exit(self)
        # Disable all GUI
        for list in [self.mainGui, self.clothButtons, self.colorGui, self.colorButtons, self.gloveButtons]:
            for button in list:
                button['state'] = DGG.DISABLED

    # Change focused clothing type.
    def changeFocusType(self, typeChange=0):
        global toonDNA
        self.clothSection = (self.clothSection + typeChange) % 4
        labelNames = ['Tops', 'Shirts', 'Sleeves', 'Bottoms']
        # Change body section label
        self.mainGui[0]['text'] = labelNames[self.clothSection]

        # Update UI Elements
        self.generateButtonGeom()
        self.updateIDLabels()

    # Change focused clothing type.
    def changeColorFocusType(self, typeChange=0):
        global toonDNA
        self.colorSection = (self.colorSection + typeChange) % 2
        # Change label
        self.colorGui[0]['text'] = 'Clothing Color' if self.colorSection == 0 else 'Glove Color'

        # Update UI Elements
        for button in self.colorButtons:
            button['state'] = DGG.NORMAL if self.colorSection == 0 else DGG.DISABLED
            if self.colorSection == 1:
                button.hide()
            else:
                button.show()

        for button in self.gloveButtons:
            button['state'] = DGG.NORMAL if self.colorSection == 1 else DGG.DISABLED
            if self.colorSection == 0:
                button.hide()
            else:
                button.show()

        self.updateIDLabels()

    # Generate all 3D button / preview geometry and make them SPIN.
    def generateButtonGeom(self):
        global toonDNA
        # First, end every spin animation and reset the list
        for ival in self.spinIvals:
            ival.finish()
            del ival
        self.spinIvals = []

        # Destroy all clothing buttons and reset them to empty
        for button in self.clothButtons:
            button.destroy()
            del button
        self.clothButtons = []

        # Set max pages depending on what section is open
        topBase = len(ToonDNA.Shirts)
        if self.clothSection == 0 or self.clothSection == 2:
            topBase = len(self.shirtStyles) if self.clothSection == 0 else len(ToonDNA.Sleeves)
        if self.clothSection == 3:
            topBase = len(ToonDNA.GirlBottoms) if toonDNA.gender == 'f' else len(ToonDNA.BoyShorts)
        # If the pages divide evenly, create a difference of 1 to avoid a blank page.
        dif = 0
        if topBase % 9 == 0:
            dif = 1
        self.maxClothPage = math.ceil(topBase / 9) - dif

        # If the pages go over the maximum page limit (likely from transing gender), fix it
        if self.clothPage > self.maxClothPage:
            self.clothPage = self.maxClothPage

        # Update text on page labels
        self.clothPages['text'] = str(int(self.clothPage + 1)) + '/' + str(int(self.maxClothPage) + 1)

        # Enable/Disable page buttons according to the page
        self.leftPageButton['state'] = DGG.NORMAL if self.clothPage > 0 else DGG.DISABLED
        self.rightPageButton['state'] = DGG.NORMAL if self.clothPage < self.maxClothPage else DGG.DISABLED

        # Boolean that checks whether or not we're doing bottoms buttons
        bottoms = False if self.clothSection != 3 else True

        # Create 9 buttons
        for i in range(9):
            # Create value for button
            buttonID = int((self.clothPage * 9) + i)

            # If this button exceeds values in which exist in the game, skip this button.
            if (not bottoms and self.clothSection == 0 and buttonID >= len(self.shirtStyles)) or \
                (not bottoms and self.clothSection == 1 and buttonID >= len(ToonDNA.Shirts)) or \
                    (not bottoms and self.clothSection == 2 and buttonID >= len(ToonDNA.Sleeves)) or \
                    (bottoms and toonDNA.gender == 'f' and buttonID >= len(ToonDNA.GirlBottoms)) or \
                    (bottoms and toonDNA.gender == 'm' and buttonID >= len(ToonDNA.BoyShorts)):
                continue

            # If shirts, determine what pieces and values to use for it.
            if not bottoms:
                if self.clothSection == 0:
                    pieceNames = ('**/torso-top', '**/sleeves')
                else:
                    pieceNames = ('**/torso-top' if self.clothSection == 1 else '**/sleeves',)
            else:
                pieceNames = ('**/torso-bot',)

            # Set up texture values
            toptex = 0
            sleevetex = 0
            bottex = 0
            bottomType = 'shorts'

            # Set texture values
            if bottoms:
                # Set the pant texture
                bottex = buttonID
                # If Toon is girl and the bottom is a skirt, make the pant a skirt.
                if toonDNA.gender == 'f':
                    if ToonDNA.GirlBottoms[bottex][1] == 1:
                        bottomType = 'skirt'
            else:
                # Set the shirt texture if just the shirt, otherwise set it to the combined value.
                toptex = buttonID if (self.clothSection == 1) else self.shirtStyles[buttonID][0]

                # Set the sleeve texture if combined or just the sleeve, otherwise leave alone.
                if self.clothSection == 0 or self.clothSection == 2:
                    sleevetex = buttonID if self.clothSection == 2 or self.clothSection == 1 else self.shirtStyles[buttonID][1]
                # If the shirt tab is anything other than combined, change the other texture id to match the preview Toon.
                if self.clothSection == 1:
                    sleevetex = toonDNA.sleeveTex
                if self.clothSection == 2:
                    toptex = toonDNA.topTex

            toon = loader.loadModel('phase_3/models/char/tt_a_chr_dg%s_%s_torso_1000' % (toonDNA.torso[0], bottomType))
            nodeLabel = 'bot' if bottoms else 'top'
            model = NodePath(nodeLabel + str(i))

            for name in pieceNames:
                for piece in toon.findAllMatches(name):
                    # Set textures
                    if name == '**/torso-top':
                        piece.setTexture(loader.loadTexture(ToonDNA.Shirts[toptex]), 1)
                    elif name == '**/sleeves':
                        piece.setTexture(loader.loadTexture(ToonDNA.Sleeves[sleevetex]), 1)
                    elif name == '**/torso-bot':
                        piece.setTexture(loader.loadTexture(ToonDNA.BoyShorts[bottex] if toonDNA.gender == 'm' else ToonDNA.GirlBottoms[bottex][0]), 1)
                    piece.wrtReparentTo(model)

            model.setH(180)
            toon.removeNode()

            # Create button and spin interval
            button, spinIval = self.makeButtonModel(model, buttonID)

            # Create position values
            x = i % 3
            y = int(i / 3)

            # Reparent the button with the corresponding frame
            button.reparentTo(self.clothFrame)
            self.clothButtons.append(button)

            # Set button position
            button.setPos(-0.2 + (0.2 * x), 0, 0.075 - (0.1625 * y))
            button.setScale(0.06)

            # Start interval and add to spin list
            spinIval.loop()
            self.spinIvals.append(spinIval)


    # Create a single button model.  Modified port of makeFrameModel from toontown.catalog.CatalogItem
    def makeButtonModel(self, model, i):
        frame = None
        if type != 2:
            frame = DirectButton(parent=hidden, frameSize=(-1.0, 1.0, -1.0, 1.0), relief=None,
                                 command=self.updateClothes, extraArgs=[i, False])
        else:
            frame = DirectFrame(parent=hidden, frameSize=(-1.0, 1.0, -1.0, 1.0), relief=None)
        model.setDepthTest(1)
        model.setDepthWrite(1)
        pitch = frame.attachNewNode('pitch')
        rotate = pitch.attachNewNode('rotate')
        scale = rotate.attachNewNode('scale')
        model.reparentTo(scale)
        bMin, bMax = model.getTightBounds()
        center = (bMin + bMax) / 2.0
        model.setPos(-center[0], -center[1], -center[2])
        pitch.setP(20)
        bMin, bMax = pitch.getTightBounds()
        center = (bMin + bMax) / 2.0
        corner = Vec3(bMax - center)
        scale.setScale(1.0 / max(corner[0], corner[1], corner[2]))
        pitch.setY(2)
        ival = LerpHprInterval(rotate, 10, VBase3(-270, 0, 0), startHpr=VBase3(90, 0, 0))
        return (frame, ival)

    # Change the clothes of the preview Toon.
    def updateClothes(self, i, isColor):
        global toonDNA
        # Shirt
        if self.clothSection != 3:
            # If setting color, set the color. Otherwise, do textures.
            if isColor:
                if self.clothSection == 0 or self.clothSection == 1:
                    toonDNA.topTexColor = i
                if self.clothSection == 0 or self.clothSection == 2:
                    toonDNA.sleeveTexColor = i
            else:
                # If combined, set both shirt and sleeve from the compiled list.
                if self.clothSection == 0:
                    toonDNA.topTex = self.shirtStyles[i][0]
                    toonDNA.sleeveTex = self.shirtStyles[i][1]
                # If just the shirt, set the shirt.
                elif self.clothSection == 1:
                    toonDNA.topTex = i
                # If just the sleeves, set the sleeves.
                elif self.clothSection == 2:
                    toonDNA.sleeveTex = i
        # Pant
        elif self.clothSection == 3:
            # If setting color, set the color. Otherwise, do texture.
            if isColor:
                toonDNA.botTexColor = i
            else:
                toonDNA.botTex = i
                if toonDNA.gender == 'f':
                    toonDNA.torso = toonDNA.torso[0] + ('d' if ToonDNA.GirlBottoms[i][1] == 1 else 's')
                else:
                    toonDNA.torso = toonDNA.torso[0] + 's'
        # Update Toon
        self.updateToon()

    # Change glove color.
    def updateGloves(self, i):
        toonDNA.gloveColor = i
        self.updateToon()

    def updateToon(self):
        ToonTabPageBase.updateToon(self)
        self.updateIDLabels()

    # Update Labels
    def updateIDLabels(self):
        # TODO: Move these long ass lists to TTLocalizer
        # TODO: Make two bottoms lists
        ShirtToString = ['Plain',
                         'Single Stripe',
                         'Buttoned Collar',
                         'Double Stripe',
                         'Striped',
                         'Collar w/ Pocket',
                         'Flower Print',
                         'Flower Trim',
                         'Hawaiian',
                         'Collar w/ 2 Pockets',
                         'Bowling Shirt',
                         'Purple Vest',
                         'Denim Vest',
                         'Peasant',
                         'Ruffles',
                         'Peasant w/ Mid Stripe',
                         'Soccer Jersey',
                         'Lightning Bolt',
                         'No. 19',
                         'Guayabera',
                         'Hearts',
                         'Stars',
                         'Flower',
                         'Blue w/ Gold Wavy Stripes',
                         'Pink & Beige w/ Flower',
                         'Orange Hoodie',
                         'Blue Stripes',
                         'Palm Tree',
                         'Orange No. 1',
                         'Ghost',
                         'Pumpkin',
                         'Snowman',
                         'Snowflakes',
                         'Candy Cane Hearts',
                         'Scarf',
                         'Blue w/ Gold Wavy Stripes',
                         'Blue w/ Pink Ribbon',
                         'Lime Green w/ Stripe',
                         'Purple Stars',
                         'Red Kimono',
                         'Aqua Kimono',
                         'Pink w/ Red Heart',
                         'Red Hearts',
                         'Winged Heart',
                         'Flaming Heart',
                         'Tie Dye',
                         'Blue Stripes',
                         'Four Leaf Clover',
                         "Pot O' Gold",
                         'Fishing Vest',
                         'Fish Tank',
                         'Paw Print',
                         'Cowboy 1',
                         'Cowboy 2',
                         'Cowboy 3',
                         'Cowboy 4',
                         'Cowboy 5',
                         'Cowboy 6',
                         'USA Flag',
                         'Fireworks',
                         'Green',
                         'Pink Flower',
                         'Multicolor w/ Backpack',
                         'Lederhosen',
                         'Watermelon',
                         'Race Flag Shirt',
                         'Blue Banana Pajama',
                         'Red Bike Horn Pajama',
                         'Purple Hypno Pajama',
                         'Cupid',
                         'Patched Hearts',
                         'HD Double Stripe',
                         'Clown Fish',
                         'Old Boot',
                         'Mole',
                         'Farmer',
                         'Cupcake',
                         'Party Hat',
                         'Racer Goofy',
                         'Roadster',
                         'Cool Sun',
                         'Beach Ball',
                         'Golf 1',
                         'Golf 2',
                         'Bee',
                         'Supertoon',
                         'Marathon Winner',
                         'Anti-Cog Building',
                         'Building Lifesaver',
                         'HQ Completionist',
                         'Task Completionist',
                         'Dreamy Trolley',
                         'Cheery Trolley',
                         'Wintery Gift',
                         'Skeletoon',
                         'Webs',
                         'Red Bowed Angel',
                         'Prepostera',
                         'Surlee',
                         'Dimm',
                         'Silly Mailbox',
                         'Silly Trashcan',
                         'Loony Labs',
                         'Silly Fire Hydrant',
                         'Silly Meter',
                         'Cogbuster',
                         'Cog Destroyer',
                         'Anti-Cheese',
                         'Victory Party',
                         'Sellbot Icon',
                         'Anti-V.P.',
                         'Sellbot Crusher',
                         'Jellybean Jar',
                         'Doodle',
                         'Vampire',
                         'Turtle',
                         'Green Toon',
                         'Get Connected!',
                         'Grand Prix Suit',
                         'Lawbot Icon',
                         'Anti-C.J.',
                         'Lawbot Crusher',
                         'Bee',
                         'Pirate',
                         'Supertoon',
                         'Vampire',
                         'Dinosaur',
                         'Fisher',
                         'Golf 3',
                         'Cog Destroyer 2',
                         'Toontown Racing Suit',
                         'Anti-Cog Building 2',
                         'Trolley Rider',
                         'Old Boot 2',
                         'Golf 4',
                         'Witch',
                         'Sled',
                         'Flying Bats',
                         'Mittens',
                         'Pool Shark',
                         'Piano Fish',
                         'Golf 5',
                         'Toontown Racing Suit 2',
                         'Toontown Racing Suit 3',
                         'Cog Dummy',
                         'Cog Destroyer 3',
                         'Trolley Rider 2',
                         'Trolley Rider 3',
                         'Anti-Cog Building 3',
                         'Anti-Cog Building 4',
                         'Anniversary']
        BoyBotToString = []
        GirlBotToString = []
        NumToClothColor = ['Bright Red',
                           'Red',
                           'Maroon',
                           'Orange',
                           'Yellow',
                           'Lime',
                           'Sea Green',
                           'Teal',
                           'Aqua',
                           'Blue',
                           'Royal Blue',
                           'Slate Blue',
                           'Purple',
                           'Sienna',
                           'Brown',
                           'Tan',
                           'Coral',
                           'Orange',
                           'Lime',
                           'Teal',
                           'Aqua',
                           'Peach',
                           'Cream',
                           'Citrine',
                           'Periwinkle',
                           'Lavender',
                           'Pink',
                           'White',
                           'Solid Blue',
                           'Beet Red',
                           'Royal Purple']

        # Values
        id = 0
        sleeveID = 0
        colorID = 27
        colorSleeveID = 27
        clothName = None
        sleeveName = None

        # If shirt sections, set it to do shirt label
        if self.clothSection == 0 or self.clothSection == 1:
            # Try to do a custom label. If it doesn't exist, set it to the filename.
            try:
                clothName = ShirtToString[toonDNA.topTex]
            except:
                clothName = ToonDNA.Shirts[toonDNA.topTex]
            id = toonDNA.topTex
            colorID = toonDNA.topTexColor

        # If bottoms section, set it to do bottoms label
        if self.clothSection == 3:
            # Try to do a custom label. If it doesn't exist, set it to the filename.
            try:
                clothName = BoyBotToString[toonDNA.botTex] if toonDNA.gender == 'm' else GirlBotToString[toonDNA.botTex]
            except:
                clothName = ToonDNA.BoyShorts[toonDNA.botTex] if toonDNA.gender == 'm' else ToonDNA.GirlBottoms[toonDNA.botTex][0]
            id = toonDNA.botTex
            colorID = toonDNA.botTexColor

        # Figure out the sleeve name via the shirt list.
        sleeveID = toonDNA.sleeveTex
        colorSleeveID = toonDNA.sleeveTexColor
        for shirtStyle in self.shirtStyles:
            if toonDNA.sleeveTex == shirtStyle[1]:
                # Try to do a custom label. If it doesn't exist, set it to the filename.
                try:
                    sleeveName = ShirtToString[shirtStyle[0]]
                except:
                    sleeveName = ToonDNA.Sleeves[toonDNA.sleeveTex]
                break

        # If it's a sleeve that doesn't pair with a shirt, set it to the filename.
        if sleeveName == None:
            sleeveName = ToonDNA.Sleeves[toonDNA.sleeveTex]

        # If sleeve section, set the sleeve values to the normal values.
        if self.clothSection == 2:
            clothName = sleeveName
            id = sleeveID
            colorID = colorSleeveID

        # Set labels
        self.clothIDLabel['text'] = clothName + ' (' + str(id) + ')'
        self.clothIDLabel['text_fg'] = ToonDNA.ClothesColors[colorID]

        # If combined, show sleeve as well. If not, hide it.
        if self.clothSection == 0:
            self.subclothIDLabel['text'] = sleeveName + ' (' + str(sleeveID) + ')'
            self.subclothIDLabel['text_fg'] = ToonDNA.ClothesColors[colorSleeveID]
            self.subclothIDLabel.show()
        else:
            self.subclothIDLabel.hide()

        # Set color labels
        colorLabel, colorLabelID = (NumToClothColor[colorID], colorID) if self.colorSection == 0 else (TTLocalizer.NumToColor[toonDNA.gloveColor], toonDNA.gloveColor)

        self.colorIDLabel['text'] = '%s (%d)' % (colorLabel, colorLabelID)
        self.colorIDLabel['text_fg'] = ToonDNA.ClothesColors[colorID] if self.colorSection == 0 else ToonDNA.allColorsList[toonDNA.gloveColor]

    # Change the page value.
    def setPage(self, i):
        self.clothPage += i
        # If the page somehow ends up bigger than the max shirt page, set it to max shirt page.
        if self.clothPage > self.maxClothPage:
            self.clothPage = self.maxClothPage
        # Update button geom
        self.generateButtonGeom()


# TODO: Merge accessory tabs into a single Accessory tab, where a button swaps which accessories are being modified.
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
