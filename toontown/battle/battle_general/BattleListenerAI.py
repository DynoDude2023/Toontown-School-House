from toontown.toonbase import ToontownBattleGlobals
from toontown.battle.BattleBase import *

class BattleListenerAI:
    
    def __init__(self, battle):
        self.killedSuits = []
        self.saddenedToons = []
        
        self.suitAttacksTracked = []
        self.toonAttacksTracked = []
        
    def trackKilledSuit(self, suit):
        self.killedSuits.append([suit.doId, suit.getLevel(), suit.dna.name, suit.dna.dept])
        print('Killed suit: ' + str(suit.doId) + ' ' + str(suit.getLevel()) + ' ' + str(suit.dna.name) + ' ' + str(suit.dna.dept))
    
    def trackSaddenedToon(self, toon):
        self.saddenedToons.append(toon.doId)
        print('Saddened toon: ' + str(toon.doId))
    
    def trackSuitAttack(self, attack):
        self.suitAttacksTracked.append([attack[SUIT_ID_COL], attack[SUIT_HP_COL], attack[SUIT_TAUNT_COL]])
        print('Suit attack: ' + str(attack[SUIT_ID_COL]) + ' ' + str(attack[SUIT_HP_COL]) + ' ' + str(attack[SUIT_TAUNT_COL]))
    
    def trackToonAttack(self, attack):
        self.toonAttacksTracked.append([attack[TOON_ID_COL], attack[TOON_HP_COL], attack[TOON_ACCBONUS_COL]])
        print('Toon attack: ' + str(attack[TOON_ID_COL]) + ' ' + str(attack[TOON_HP_COL]) + ' ' + str(attack[TOON_ACCBONUS_COL]))