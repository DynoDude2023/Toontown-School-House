from panda3d.core import *
from toontown.toonbase import ToontownGlobals
from toontown.toonbase.ToontownBattleGlobals import *
from direct.directnotify import DirectNotifyGlobal
import string
from toontown.toon import LaffMeter
from toontown.battle import BattleBase
from toontown.battle import BattleProps
from direct.task.Task import Task
from direct.gui.DirectGui import *
from toontown.toonbase import TTLocalizer

class TownBattleCogPanel(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('TownBattleCogPanel')
    healthColors = (Vec4(0, 1, 0, 1),
     Vec4(1, 1, 0, 1),
     Vec4(1, 0.5, 0, 1),
     Vec4(1, 0, 0, 1),
     Vec4(0.3, 0.3, 0.3, 1))
    healthGlowColors = (Vec4(0.25, 1, 0.25, 0.5),
     Vec4(1, 1, 0.25, 0.5),
     Vec4(1, 0.5, 0.25, 0.5),
     Vec4(1, 0.25, 0.25, 0.5),
     Vec4(0.3, 0.3, 0.3, 0))

    def __init__(self, id):
        gui = loader.loadModel('phase_3.5/models/gui/ttr_m_gui_bat_cogGUI')
        DirectFrame.__init__(self, relief=None, image=gui, image_color=Vec4(1, 1, 1, 0.95))
        self.setScale(0.05)
        self.initialiseoptions(TownBattleCogPanel)
        self.hidden = False
        self.cog = None
        self.healthText = DirectLabel(parent=self, text='', pos=(1.03302, 0, -1.88994), text_scale=0.055)
        button = gui.find('**/ttr_t_gui_bat_cogGUI_health_light_card')
        button.setScale(0.5)
        button.setH(180)
        button.setColor(Vec4(1, 0, 0, 1))
        self.accept('inventory-levels', self.__handleToggle)
        self.healthNode = self.attachNewNode('health')
        self.healthNode.setPos(-0.06, 0, 0.05)
        glow = BattleProps.globalPropPool.getProp('glow')
        glow.reparentTo(button)
        glow.setScale(0.0)
        glow.setPos(-0.005, 0.01, 0.015)
        glow.setColor(Vec4(0.25, 1, 0.25, 0.5))
        self.button = button
        self.glow = glow
        self.head = None
        self.blinkTask = None
        self.hide()
        gui.removeNode()

    def setCogInformation(self, cog):
        self.cog = cog
        self.updateHealthBar()
        if self.head:
            self.head.removeNode()
        self.head = self.attachNewNode('head')
        for part in cog.headParts:
            copyPart = part.copyTo(self.head)
            copyPart.setDepthTest(1)
            copyPart.setDepthWrite(1)

        p1, p2 = Point3(), Point3()
        self.head.calcTightBounds(p1, p2)
        d = p2 - p1
        biggest = max(d[0], d[1], d[2])
        s = 0.1 / biggest
        self.head.setPosHprScale(-1.58605, -0.1, -0.747626, 180, 0, 0, s, s, s)
        self.head.setScale(1.2)
        self.setLevelText(cog.getActualLevel(), cog.getSkeleRevives())

    def setLevelText(self, hp, revives = 0):
        if revives > 0:
            self.healthText['text'] = TTLocalizer.DisguisePageCogLevel % str(hp) + TTLocalizer.SkeleRevivePostFix
        else:
            self.healthText['text'] = TTLocalizer.DisguisePageCogLevel % str(hp)

    def updateHealthBar(self):
        condition = self.cog.healthCondition
        if condition == 4:
            self.blinkTask = Task.loop(Task(self.__blinkRed), Task.pause(0.75), Task(self.__blinkGray), Task.pause(0.1))
            taskMgr.add(self.blinkTask, self.uniqueName('blink-task'))
        elif condition == 5:
            self.blinkTask = Task.loop(Task(self.__blinkRed), Task.pause(0.25), Task(self.__blinkGray), Task.pause(0.1))
            taskMgr.add(self.blinkTask, self.uniqueName('blink-task'))
        else:
            taskMgr.remove(self.uniqueName('blink-task'))
            self.button.setColor(self.healthColors[condition], 1)
            self.glow.setColor(self.healthGlowColors[condition], 1)

    def show(self):
        if self.cog:
            self.updateHealthBar()
        self.hidden = False
        DirectFrame.show(self)
    
    def __handleToggle(self):
        if self.cog:
            if self.hidden:
                self.show()
            else:
                self.hide()

    def __blinkRed(self, task):
        self.button.setColor(self.healthColors[3], 1)
        self.glow.setColor(self.healthGlowColors[3], 1)
        return Task.done

    def __blinkGray(self, task):
        self.button.setColor(self.healthColors[4], 1)
        self.glow.setColor(self.healthGlowColors[4], 1)
        return Task.done

    def hide(self):
        if self.blinkTask:
            taskMgr.remove(self.blinkTask)
            self.blinkTask = None
        self.hidden = True
        DirectFrame.hide(self)

    def cleanup(self):
        self.ignoreAll()
        if self.head:
            self.head.removeNode()
            del self.head
        if self.blinkTask:
            taskMgr.remove(self.blinkTask)
        del self.blinkTask
        self.button.removeNode()
        self.glow.removeNode()
        DirectFrame.destroy(self)
