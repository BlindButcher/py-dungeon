import tkinter as tk

from creature import Hero, AttributeType
from game_message import MessageHolder
from location import SampleLocationGenerator, LocationComplex
from main import Main


class Application(tk.Frame):
    def __init__(self, main, master=None, borderwidth=5, relief="sunken", width=800, height=600):
        super().__init__(master=master, borderwidth=borderwidth, relief=relief, width=width, height=height)
        self.main = main
        self.hero_info = None
        self.hero_list = None
        self.next_button = None
        self.message_box = None
        self.quit = None
        self.create_widgets()
        self.cur_turn = 0

    def create_widgets(self):
        # self.hero_info = tk.Label(self, text='Hero List')
        # self.hero_info.grid(row=0)

        self.hero_list = tk.Listbox(self)
        self.hero_list.grid(sticky=tk.W)

        for item in map(lambda _: _.name, self.main.all_heroes()):
            self.hero_list.insert(tk.END, item)

        # self.next_button = tk.Button(self)
        # self.next_button["text"] = "Next"
        # self.next_button["command"] = self.next_turn
        # self.next_button.grid(column=0, row=0, sticky=tk.W)
        #
        # self.message_box = tk.Text(root, height=150, width=150)
        # self.message_box.grid(column=0, row=0, sticky=tk.W)
        # self.message_box.insert('1.0', 'Welcome')
        #
        # self.quit = tk.Button(self, text="QUIT", fg="red", command=root.destroy)
        # self.quit.grid(column=3, row=3)

    def next_turn(self):
        self.main.next_tick()

        self.hero_list.delete(0, tk.END)

        for item in self.main.all_heroes():
            self.hero_list.insert(tk.END, item)

        desc = '\n'.join(map(str, self.main.all_heroes()))
        self.hero_info['text'] = desc

        self.cur_turn += 1

        messages = self.main.message_holder.flush()
        for m in reversed(messages):
            self.message_box.insert('1.0', '\n')
            self.message_box.insert('1.0', str(self.cur_turn) + ': ' + m)


dd_hero = Hero('DD', {AttributeType.POWER: 4, AttributeType.TOUGHNESS: 1})
tank_hero = Hero('Tank', {AttributeType.POWER: 2, AttributeType.TOUGHNESS: 4})
weak_hero = Hero('Weak', {AttributeType.POWER: 2, AttributeType.TOUGHNESS: 2})

text_message_holder = MessageHolder()

heroes = [dd_hero, tank_hero, weak_hero]

root = tk.Tk()
dung_gen = SampleLocationGenerator(5, text_message_holder)
loc_complex = LocationComplex('city_dungeon', text_message_holder, dung_gen.generate)
app = Application(Main(heroes, text_message_holder, loc_complex), master=root)

app.grid(column=0, row=0, columnspan=3, rowspan=2)

app.mainloop()
