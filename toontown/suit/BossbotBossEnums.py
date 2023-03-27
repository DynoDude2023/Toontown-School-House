from enum import Enum

class WaiterRound(Enum):
    LOWEST_LEVEL = 9
    HIGHEST_LEVEL = 12
    PLANNER_COG_AMT_POOL = 206
    SKELE_REVIVE_CHANCE = 0.20

class DinerBattleRound(Enum):
    COG_LEVEL = 12
    SKELE_REVIVE_CHANCE = 0.20
    TIER_2_COG = ['hh',
                  'hh',
                  'cr',
                  'cr',
                  'tbc']