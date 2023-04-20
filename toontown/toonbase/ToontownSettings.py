from direct.directnotify import DirectNotifyGlobal
from panda3d.core import loadPrcFileData

from otp.settings.Settings import Settings


class ToontownSettings(Settings):
    notify = DirectNotifyGlobal.directNotify.newCategory('ToontownSettings')

    def loadFromSettings(self):
        # Setting for toggling stretched screen.
        # Stretched screen forces the aspect ratio to be 4:3, or 1.333.
        stretchedScreen = self.getBool('game', 'stretched-screen', False)
        if stretchedScreen:
            loadPrcFileData('toonBase Settings Stretched Screen', 'aspect-ratio 1.333')
        else:
            self.updateSetting('game', 'stretched-screen', stretchedScreen)

        # Setting for a semi-custom Magic Word activator.
        # We will give players a list of which activators will work, and which will not.
        magicWordActivator = self.getInt('game', 'magic-word-activator', 0)
        loadPrcFileData('toonBase Settings Magic Word Activator', 'magic-word-activator %d' % magicWordActivator)
        self.updateSetting('game', 'magic-word-activator', magicWordActivator)

        # Setting for Interpolating Animations.
        smoothAnims = self.getBool('game', 'interpolate-animations', False)
        loadPrcFileData('toonBase Settings Interpolating Animations', 'interpolate-animations %s' % smoothAnims)
        self.updateSetting('game', 'interpolate-animations', smoothAnims)
        
        # Setting for Contrast Nametags.
        contrast_names = self.getBool('game', 'contrast-nametags', False)
        loadPrcFileData('toonBase Settings Contrast Nametags', 'contrast-nametags %s' % contrast_names)
        self.updateSetting('game', 'contrast-nametags', contrast_names)
        
        # Setting for Nametag Scale.
        scale_names = self.getFloat('game', 'nametag-scale', 1.4)
        loadPrcFileData('toonBase Settings Nametag Scale', 'nametag-scale %s' % scale_names)
        self.updateSetting('game', 'nametag-scale', scale_names)
