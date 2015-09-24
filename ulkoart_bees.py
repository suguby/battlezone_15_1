#!/usr/bin/env python
# -*- coding: utf-8 -*-

# здесь разместить класс пчелы
from beegarden.core import Bee, Beegarden
from robogame_engine.geometry import Point


class UlkoArt(Bee):
    all_bees = []

    def on_born(self):
        for flower in self.flowers:
            if flower.honey > 0:
                for bees in UlkoArt.all_bees:
                    if bees.my_flower == flower:
                        break
                else:
                    self.my_flower = flower
                    break
        self.move_at(target=self.my_flower)
        UlkoArt.all_bees.append(self)

    def on_stop_at_flower(self, flower):
        """Обработчик события 'остановка у цветка' """
        self.load_honey_from(source=flower)

    def on_stop_at_beehive(self, beehive):
        """Обработчик события 'остановка у улья' """
        self.unload_honey_to(target=beehive)

    def on_honey_loaded(self):
        """Обработчик события 'мёд загружен' """
        if self.honey < 150:
            for i in self.flowers:
                if i.honey > 0:
                    self.move_at(target=i)
                    break

        else: self.move_at(target=self.my_beehive)

    def on_honey_unloaded(self):
        """Обработчик события 'мёд разгружен' """
        for i in self.flowers:
            if i.honey > 0:
                self.move_at(target=i)
                break



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


if __name__ == '__main__':
    beegarden = Beegarden(
        name="My little garden",
        flowers_count=5,
        speed=5,
        # field=(800, 600),
        # theme_mod_path='default_theme',
    )


    bee = UlkoArt()
    bee.move_at(Point(1000, 1000))  # проверка на выход за границы экрана

    beegarden.go()
