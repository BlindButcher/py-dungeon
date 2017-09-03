import tkinter as tk

from creature import Hero, AttributeType
from game_message import MessageHolder
from location import SampleLocationGenerator, LocationComplex
from main import Main


class Application(tk.Frame):
    def __init__(self, main, master=None):
        super().__init__(master)
        self.pack()
        self.main = main
        self.hero_info = None
        self.next_button = None
        self.message_box = None
        self.quit = None
        self.create_widgets()
        self.cur_turn = 0

    def create_widgets(self):
        self.hero_info = tk.Label(self)

        desc = '\n'.join(map(str, self.main.hero_pool))
        self.hero_info['text'] = desc
        self.hero_info.pack(side="right")

        self.next_button = tk.Button(self)
        self.next_button["text"] = "Next"
        self.next_button["command"] = self.next_turn
        self.next_button.pack(side="top")

        self.message_box = tk.Text(root, height=150, width=150)
        self.message_box.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red", command=root.destroy)
        self.quit.pack(side="bottom")

    def next_turn(self):
        self.main.next_tick()
        desc = '\n'.join(map(str, self.main.all_heroes()))
        self.hero_info['text'] = desc

        self.cur_turn += 1

        messages = self.main.message_holder.flush()
        for m in reversed(messages):
            self.message_box.insert('1.0', '\n')
            self.message_box.insert('1.0', str(self.cur_turn) + ': ' + m)


dd_hero = Hero('hero', 'DD', {AttributeType.POWER: 4, AttributeType.TOUGHNESS: 1})
tank_hero = Hero('hero', 'Tank', {AttributeType.POWER: 2, AttributeType.TOUGHNESS: 4})
weak_hero = Hero('hero', 'Weak', {AttributeType.POWER: 2, AttributeType.TOUGHNESS: 2})

text_message_holder = MessageHolder()

heroes = [dd_hero, tank_hero, weak_hero]

root = tk.Tk()
dung_gen = SampleLocationGenerator(5, text_message_holder)
loc_complex = LocationComplex('city_dungeon', text_message_holder, dung_gen.generate)
app = Application(Main(heroes, text_message_holder, loc_complex), master=root)
app.mainloop()
