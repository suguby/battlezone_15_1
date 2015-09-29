#!/usr/bin/env python
# -*- coding: utf-8 -*-

# здесь разместить класс пчелы
from beegarden.core import Bee, Beegarden
from robogame_engine.geometry import Point


class AlexBee1(Bee):
    all_bees = []
    perspective_flowers = []

    def on_born(self):
        AlexBee1.perspective_flowers = self.flowers[:]
        self.choice_flower()
        self.move_at(target=self.my_flower)
        AlexBee1.all_bees.append(self)

    def choice_flower(self):
        for flower in self.flowers:
            if flower.honey > 0:
                for bee in AlexBee1.all_bees:
                    if bee == self: continue
                    if bee.my_flower == flower:
                        break
                else:
                    self.my_flower = flower
                    break
        else:
            if not self.near(self.my_beehive): # Иначе, при пустых цветах пчелы пытаются летать из улья в улей (из своего в свой же)
                self.move_at(target=self.my_beehive)

#    def nearest_flower(self):


    def on_stop_at_flower(self, flower):
        """Обработчик события 'остановка у цветка' """
        self.my_flower = None

        self.load_honey_from(source=flower)

    def on_stop_at_beehive(self, beehive):
        """Обработчик события 'остановка у улья' """
        self.unload_honey_to(target=beehive)

    def on_honey_loaded(self):
        """Обработчик события 'мёд загружен' """
        if self.honey < 100:
            self.choice_flower()
            if self.my_flower:
                self.move_at(target=self.my_flower)
        else: self.move_at(target=self.my_beehive)

    def on_honey_unloaded(self):
        """Обработчик события 'мёд разгружен' """
        self.choice_flower()
        if self.my_flower:
            self.move_at(target=self.my_flower)


    # self.flowers - список всех цветков
    # self.my_beehive - наш улей, туда надо носить мёд
    
    # self.move_at(target_pos)
    #    """ Задать движение к указанному <объекту/точке> """

    # self.load_honey_from(source)
    #    """Загрузить мёд от ... """

    # self.unload_honey_to(target)
    #    """Разгрузить мёд в ... """
        
    # self.is_full()
    #    """полностью заполнен?"""


# if __name__ == '__main__':
#     beegarden = Beegarden(
#         name="My little garden",
#         flowers_count=5,
#         speed=5,
#         # field=(800, 600),
#         # theme_mod_path='default_theme',
#     )
#
#
#     bee = AlexBee()
#     bee.move_at(Point(1000, 1000))  # проверка на выход за границы экрана
#
#     beegarden.go()
