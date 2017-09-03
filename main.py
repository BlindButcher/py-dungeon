from location import Temple


class Main:
    def __init__(self, hero_pool, message_holder, loc_complex):
        self.hero_pool = hero_pool
        self.message_holder = message_holder
        self.temple = Temple('temple', message_holder)
        self.loc_complex = loc_complex

    def handle_heal(self):
        wounded = filter(lambda _: _.wounded() or _.carried_hero is not None, self.hero_pool)
        for _ in wounded:
            self.temple.visit(_)

        for _ in wounded:
            self.hero_pool.remove(_)

    def next_tick(self):

        self.handle_heal()

        for _ in self.hero_pool:
            self.loc_complex.visit(_)

        self.hero_pool = []

        self.hero_pool.extend(self.temple.explorer()['return_heroes'])
        all_heroes = self.loc_complex.explorer()

        self.hero_pool.extend(all_heroes['return_heroes'])

    def game_over(self):
        return not self.hero_pool and not self.loc_complex.visiting_heroes

    def all_heroes(self):
        res = []
        res.extend(self.hero_pool)
        res.extend(self.loc_complex.visiting_heroes())

        return sorted(set(res), key=lambda h: h.name)
