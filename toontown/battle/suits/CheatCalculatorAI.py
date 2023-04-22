import random

class CheatCalculatorAI:
    
    def __init__(self, suit):
        self.suit = suit
        self.battle = suit.battle
    
    def doCheatCalculation(self):
        pass

class OvertimeCheatCalculator(CheatCalculatorAI):
    
    def __init__(self, suit):
        CheatCalculatorAI.__init__(self, suit)
    
    def doCheatCalculation(self):
        overtimeSuitChoices = []
        self.suit.wantedTarget(0)
        suitAttackOvertime = [self.suit.doId,
                            3,
                            0,
                            [0, 0, 0, 0],
                            0,
                            0,
                            0]
        for suitChoice in self.battle.activeSuits:
            if suitChoice != self.suit:
                overtimeSuitChoices.append(suitChoice)
        pickedSuitId = None
        pickedSuit = None
        if overtimeSuitChoices:
            pickedSuit = random.choice(overtimeSuitChoices)
            pickedSuitId = pickedSuit.doId
        if pickedSuit and not self.battle.battleCalc.combatantDead(pickedSuitId, toon=0):
            self.suit.wantedTarget(pickedSuitId)
            self.battle.battleCalc.addCustomAttack(self.suit, suitAttackOvertime, 0)
            pickedSuit.setHP(pickedSuit.getHP() + (pickedSuit.getActualLevel() * 3))