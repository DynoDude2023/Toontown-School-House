import colors
from QuestPoster import *

class QuestBookPoster(QuestPoster):
    IMAGE_SCALE_LARGE = 0.15
    IMAGE_SCALE_SMALL = 0.1
    POSTER_WIDTH = 0.7
    TEXT_SCALE = TTLocalizer.QPtextScale * 0.7
    TEXT_WORDWRAP = TTLocalizer.QPtextWordwrap * 0.8
    NORMAL_TEXT_COLOR = (0.3, 0.25, 0.2, 1)
    CONFIRM_DELETE_BUTTON_EVENT = 'confirmDeleteButtonEvent'

    def __init__(self, parent=aspect2d, **kw):
        bookModel = loader.loadModel('phase_3.5/models/gui/stickerbook_gui')
        questCard = bookModel.find('**/questCard')
        optiondefs = (
            ('relief', None, None),
            ('reverse', False, None),
            ('mapIndex', 0, None),
            ('image', questCard, None),
            ('image_scale', (0.8, 1.0, 0.58), None),
            ('state', DGG.NORMAL, None)
        )
        self.defineoptions(kw, optiondefs)
        QuestPoster.__init__(self, relief=None)
        self.initialiseoptions(QuestBookPoster)
        self._deleteCallback = None
        self.questFrame = DirectFrame(parent=self, relief=None)
        gui = loader.loadModel('phase_4/models/parties/schtickerbookHostingGUI')
        icon = gui.find('**/startPartyButton_inactive')
        iconNP = aspect2d.attachNewNode('iconNP')
        icon.reparentTo(iconNP)
        icon.setX((-12.0792 + 0.2) / 30.48)
        icon.setZ((-9.7404 + 1) / 30.48)
        self.mapIndex = DirectLabel(
            parent=self.questFrame,
            relief=None,
            text='%s' % self['mapIndex'],
            text_fg=colors.WHITE,
            text_scale=0.035,
            text_align=TextNode.ACenter,
            image=iconNP,
            image_scale=0.3,
            image_color=colors.RED,
            pos=(-0.3, 0, 0.15)
        )
        self.mapIndex.hide()
        iconNP.removeNode()
        gui.removeNode()
        bookModel.removeNode()
        self.reverseBG(self['reverse'])

    def reverseBG(self, reverse=False):
        if reverse:
            self['image_scale'] = (-abs(self['image_scale'][0]), self['image_scale'][1], self['image_scale'][2])
            self.questFrame.setX(0.015)
        else:
            self['image_scale'] = (abs(self['image_scale'][0]), self['image_scale'][1], self['image_scale'][2])