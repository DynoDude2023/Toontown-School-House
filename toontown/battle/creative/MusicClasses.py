from toontown.toonbase.ToontownBattleGlobals import *

class BattleMusicClass:
    file_paths = ['phase_3.5/audio/bgm/encntr_general_bg.ogg']
    audio_file_number = 1
    audi_file_name2Number = {'The Corporate Ladder': 1}
    
    def __init__(self, vol=0.9):
        self.battleThemes = []
        for path in self.file_paths:
            self.battleThemes.append(base.loadMusic(path))
        
        for theme in self.battleThemes:
            theme.setVolume(vol)
        
    def play(self):
        self.battleThemes[0].play()
        print('Playing music file number ' + str(self.audio_file_number) + "for the battle.")
    
    def stop(self):
        self.battleThemes[0].stop()
        print('Stopping music file number ' + str(self.audio_file_number) + "for the battle.")
    
    def swichToAnotherTheme(self, themeNumber):
        self.battleThemes[self.audio_file_number].stop()
        self.audio_file_number = themeNumber
        self.battleThemes[self.audio_file_number].play()
        print('Playing music file number ' + str(self.audio_file_number) + "for the battle.")
        
    
    