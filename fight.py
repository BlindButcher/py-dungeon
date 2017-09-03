from random import randrange


class Fight:
    def __init__(self, right, left):
        self.right = right
        self.left = left

    def process(self):
        f_res = 0
        s_res = 0

        for _ in [1, 2, 3]:
            f = randrange(self.right.power)
            s = randrange(self.left.power)
            if s > f:
                f_res += 1
            elif f > s:
                s_res = 1

        return self.right.deal_wounds(f_res), self.left.deal_wounds(s_res)
