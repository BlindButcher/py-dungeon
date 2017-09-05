import abc
from enum import Enum, auto
from random import randrange

from creature import MonsterGenerator, CreatureEvents, CreatureStatus
from fight import Fight
from flag import HeroDecisionService, Help
from hero_assign import HeroAssignment


class Location:
    def __init__(self, name, holder):
        self.name = name
        self.next_loc = None
        self.message_holder = holder

    @abc.abstractmethod
    def visit(self, hero):
        """""Handles hero visiting location"""

    def set_next_loc(self, loc):
        self.next_loc = loc


class LocationComplex(Location):
    HERO_RESCUE_LOC_CHANCE = 25

    def __init__(self, name, holder, loc_generator):
        super().__init__(name, holder)
        self.loc_generator = loc_generator
        self.unique_locations = []
        self.hero_assignment = set()

    def visit(self, hero):
        new_loc = self.loc_generator

        new_assign = HeroAssignment(hero, new_loc())

        assert new_assign not in self.hero_assignment, 'Hero is already in the list'

        self.hero_assignment.add(new_assign)

    def visiting_heroes(self):
        return list(map(lambda _: _.hero, self.hero_assignment))

    def explorer(self):
        return_heroes = []
        new_assignment = set()

        for a in self.hero_assignment:
            l = a.assign_loc
            h = a.hero

            l.visit(h)

            if h.disabled():
                self.message_holder.append(f'{h.name} disabled and waiting for help')

                self.unique_locations.append(HeroRoom(self.message_holder, h))

            elif l.next_loc is not None:
                self.try_hero_rescue(l, h)
                new_assignment.add(HeroAssignment(h, l.next_loc))
            else:
                self.message_holder.append(f'{h.name} has cleaned the dungeon and is back to pool')
                return_heroes.append(h)

        self.hero_assignment = new_assignment

        return {'dead': [], 'return_heroes': return_heroes}

    def try_hero_rescue(self, loc, h):
        if self.unique_locations and h.carried_hero is None and randrange(
                100) <= LocationComplex.HERO_RESCUE_LOC_CHANCE:
            next_loc = loc.next_loc
            hero_loc = self.unique_locations.pop()
            hero_loc.next_loc = next_loc
            loc.next_loc = hero_loc


class Treasure:
    def __init__(self, val):
        self.value = val


class TreasureRoom(Location):
    def __init__(self, name, treasure, holder):
        super().__init__(name, holder)
        self.treasure = treasure

    def visit(self, hero):
        self.message_holder.append(f"Treasure obtained {self.treasure}")
        hero.obtain_treasure(self.treasure)
        return hero


class EmptyRoom(Location):
    def visit(self, hero):
        self.message_holder.append('Empty room')
        return hero


class HeroRoom(Location):
    def __init__(self, holder, disabled_hero):
        super().__init__('Hero room', holder)
        self.disabled_hero = disabled_hero

    def visit(self, hero):

        decision = HeroDecisionService.disabled_hero(hero)

        if decision == Help.RESCUE:
            self.message_holder.append(f'{hero.name} sees ${self.disabled_hero.name} and tries to help him.')
            hero.take_disabled_hero(self.disabled_hero)
            self.disabled_hero = None
            return hero, CreatureEvents.HERO_TAKEN
        elif decision == Help.NOTHING:
            self.message_holder.append(f'{hero.name} sees ${self.disabled_hero.name} and ignores him.')
            return hero, CreatureEvents.NONE
        elif decision == Help.STEAL:
            self.message_holder.append(f'{hero.name} sees ${self.disabled_hero.name} and steals all his treasures.')
            to_steal = self.disabled_hero.carried_treasures
            hero.carried_treasure.extend(to_steal)
            self.disabled_hero.carried_treasures = []
            return hero, CreatureEvents.NONE
        elif decision == Help.KILL:
            self.message_holder.append(f'{hero.name} sees ${self.disabled_hero.name} and kills him.')
            self.disabled_hero.status = CreatureStatus.DEAD
            return hero, CreatureEvents.HERO_DEAD

        assert False, f'Should not get here with decision:{decision}'


class MonsterDan(Location):
    def __init__(self, name, monster_gen, holder):
        super().__init__(name, holder)
        self.monster_gen = monster_gen

    def visit(self, hero):
        mon = self.monster_gen.generate()
        f = Fight(hero, mon)

        res = f.process()

        self.message_holder.append(f'Monster generated in dan: {mon.name}')
        self.message_holder.append(f'Fight: {mon.name} vs {hero.name}')

        self.message_holder.append(res[0].report())
        self.message_holder.append(res[1].report())

        return res


class Temple(Location):
    def __init__(self, name, holder):
        super().__init__(name, holder)
        self.heroes = []

    def visit(self, hero):
        self.heroes.append(hero)

    def explorer(self):
        return_heroes = []

        for h in self.heroes:
            h.heal_wounds()
            self.message_holder.append(f'{h.name} healed his wound in temple')

            if h.carried_hero is not None:
                self.message_holder.append(f'{h.carried_hero.name} is healed and back to life')
                return_heroes.append(h.carried_hero)
                h.carried_hero.revive()
                h.carried_hero = None

            return_heroes.append(h)

        self.heroes = []

        return {'dead': [], 'return_heroes': return_heroes}


class SampleLocationGenerator:
    def __init__(self, depth, message_holder):
        self.depth = depth
        self.message_holder = message_holder

    def generate(self):
        head = EmptyRoom('Empty', self.message_holder)
        cur = head
        for _ in range(self.depth):
            num = randrange(3)
            if num == 0:
                cur.next_loc = EmptyRoom('Empty', self.message_holder)
            elif num == 1:
                cur.next_loc = MonsterDan('monsterRoom', MonsterGenerator(), self.message_holder)
            elif num == 2:
                cur.next_loc = TreasureRoom('treasureRoom', Treasure(randrange(50) + 1), self.message_holder)
            else:
                raise Exception('no value defined for', num)
            cur = cur.next_loc

        return head
