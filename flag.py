"""
    Based on flag different type of effect or features can be introduced.

    Character choice effect
"""
import random
from enum import Enum, auto, unique


@unique
class Flag(Enum):
    MEAN = auto()
    HELPFUL = auto()
    NEUTRAL = auto()


class HeroFlagGenerator:
    HELP_VALUES = [Flag.MEAN, Flag.NEUTRAL, Flag.HELPFUL]

    @staticmethod
    def generate():
        return [random.choice(HeroFlagGenerator.HELP_VALUES)]


@unique
class Help(Enum):
    KILL = auto()
    STEAL = auto()
    RESCUE = auto()
    NOTHING = auto()


class HeroDecisionService:
    BASE_HELP_CHANCE = 50
    HELP_MOD_DICT = {Flag.MEAN: -25, Flag.NEUTRAL: 0, Flag.HELPFUL: 25}

    HELP_RESULTS_DICT = {range(0, 25): Help.KILL,
                         range(25, 50): Help.STEAL,
                         range(50, 75): Help.NOTHING,
                         range(75, 100): Help.RESCUE}

    @staticmethod
    def disabled_hero(hero):
        base = max(random.randrange(100) + HeroDecisionService.HELP_MOD_DICT[hero.help_tag()], 99)

        for r, h in HeroDecisionService.HELP_RESULTS_DICT.items():
            if base in r:
                return h

        assert False, f'should not get here with {base}'
