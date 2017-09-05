"""
Hero/Assignment holder, with specific based on hero_id hash code behavior

"""


class HeroAssignment:
    def __init__(self, hero, assign_loc):
        self.hero = hero
        self.assign_loc = assign_loc

    def __eq__(self, other):
        return self.hero.creature_id == other.hero.creature_id

    def __hash__(self):
        return hash(self.hero.creature_id)
