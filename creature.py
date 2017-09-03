from enum import Enum, auto
from random import randrange


class AttributeType(Enum):
    POWER = auto()
    TOUGHNESS = auto()


class ValueByStats(Enum):
    SAVE_BY_TOUGHNESS = 5
    BASE_HERO_SAVE = 25
    BASE_PERCENT = 100


class CreatureStatus(Enum):
    DEAD = auto()
    UNCONSCIOUS = auto()
    WOUNDED = auto()
    ALIVE = auto()

    @staticmethod
    def disabled():
        return {CreatureStatus.DEAD, CreatureStatus.UNCONSCIOUS}


class CreatureEvents(Enum):
    NONE = auto()
    WOUND_HEALED = auto()
    HERO_TAKEN = auto()


class DealWoundResult:
    def __init__(self, creature, wound_received, toughness_negated, prev_status):
        self.creature = creature
        self.wound_received = wound_received
        self.toughness_negated = toughness_negated
        self.prev_status = prev_status
        self.cur_status = creature.status

    def report(self):
        if self.wound_received == 0:
            return f'{self.creature.name} receives no wounds'
        if self.wound_received == self.toughness_negated:
            return f'{self.creature.name} toughness negated all wound({self.wound_received})'

        message = f'{self.creature.name} receives {self.wound_received} wound'

        if self.toughness_negated > 0:
            message += f', toughness negated: {self.toughness_negated}'

        if self.prev_status != self.cur_status:
            message += f' and become {self.cur_status}'

        return message


class Creature:
    def __init__(self, creature_id, name, power):
        self.creature_id = creature_id
        self.name = name
        self.power = power
        self.status = CreatureStatus.ALIVE

    def deal_wounds(self, wounds):
        prev_status = self.status

        if wounds > 0:
            self.status = CreatureStatus.DEAD

        return DealWoundResult(self, wounds, 0, prev_status)

    def heal_wounds(self):
        assert self.status != CreatureStatus.DEAD, 'Dead can not be healed'
        if self.status == CreatureStatus.WOUNDED:
            self.status = CreatureStatus.ALIVE
            return self, CreatureEvents.WOUND_HEALED
        else:
            return self, CreatureEvents.NONE

    def revive(self):
        self.status = CreatureStatus.ALIVE

    def dead(self):
        return self.status == CreatureStatus.DEAD

    def disabled(self):
        return self.status in CreatureStatus.disabled()

    def wounded(self):
        return self.status == CreatureStatus.WOUNDED

    def __str__(self):
        return f'Name={self.name}, Power={self.power}, Status={str(self.status)}'


class Hero(Creature):
    def __init__(self, creature_id, name, attribute_map):
        super().__init__(creature_id, name, attribute_map[AttributeType.POWER])
        self.carried_treasure = []
        self.toughness = attribute_map[AttributeType.TOUGHNESS]
        self.carried_hero = None

    def obtain_treasure(self, treasure):
        self.carried_treasure.append(treasure)

    def deal_wounds(self, wounds):
        prev_status = self.status

        save = self.toughness * ValueByStats.SAVE_BY_TOUGHNESS.value + ValueByStats.BASE_HERO_SAVE.value
        status = CreatureStatus.ALIVE

        wounds_negated = 0

        status_dict = {CreatureStatus.ALIVE: CreatureStatus.WOUNDED, CreatureStatus.WOUNDED: CreatureStatus.UNCONSCIOUS,
                       CreatureStatus.UNCONSCIOUS: CreatureStatus.DEAD, CreatureStatus.DEAD: CreatureStatus.DEAD}

        for _ in range(0, wounds):
            if save > randrange(ValueByStats.BASE_PERCENT.value):
                status = status_dict[self.status]
            else:
                wounds_negated += 1

        self.status = status

        return DealWoundResult(self, wounds, wounds_negated, prev_status)

    def __str__(self):
        return super().__str__() + f',Toughness={self.toughness}'

    def take_disabled_hero(self, disabled_hero):
        assert disabled_hero.disabled(), f'{disabled_hero.name} is not disabled.'
        assert self.carried_hero is None, f'{self.name} already carries {self.carried_hero.name}.'

        self.carried_hero = disabled_hero


class MonsterGenerator:
    def generate(self):
        return Creature("monster", "my_monster", 2)
