#!/usr/bin/env python
# -*- coding: utf-8 -*-

# здесь разместить класс +пчелы
from beegarden.core import Bee, Beegarden
from robogame_engine.geometry import Point


class MyBeeRasswet(Bee):
    all_bees = []

    def on_born(self):


        xmy_behive = self.my_beehive.x
        ymy_behive = self.my_beehive.y
        dict_dist_flowers = {}
        for flower in self.flowers:
            xx = flower.x
            yy = flower.y
            dist = (abs(xx-xmy_behive)**2 + abs(yy-ymy_behive)**2)**0.5
            #print xx, '', yy, ' ', dist
            dict_dist_flowers[flower] = dist

        #print xmy_behive
        #print ymy_behive

        # здесь можно заюзать OrderedDict https://docs.python.org/2.7/library/collections.html?highlight=ordereddict#collections.OrderedDict

        sorted_keys = sorted(dict_dist_flowers, lambda x, y: cmp(dict_dist_flowers[x], dict_dist_flowers[y]))

        j = 0
        for i in sorted_keys:
            #print i, dict_dist_flowers[i]
            self.flowers.insert(j,i)
            # печалька в том, что self.flowers - системный обьект, а ты его изменяешь
            # согласен, что косяк архитектуры, исправлю... тогда твой код перестанет работать
            # заведи свой список цветков, например self.flowers_by_distance
            j += 1

        # а вообще никто не запрещает к обьекту Цветок поставить свой аттрибут, смотри
        for flower in self.flowers:
            xx = flower.x
            yy = flower.y
            dist = (abs(xx-xmy_behive)**2 + abs(yy-ymy_behive)**2)**0.5
            flower.rasswet_dist = dist
        # и тогда получить список цветов, упорядоченный по расстоянию до улья просто:
        flowers_by_distance = sorted(self.flowers, key=lambda flower: flower.rasswet_dist)


        for flower in self.flowers:
            if flower.honey > 0:
                for bees in MyBeeRasswet.all_bees:
                    if bees.my_flower == flower:
                        break
                else:
                    self.my_flower = flower
                    break
        self.move_at(target=self.my_flower)
        MyBeeRasswet.all_bees.append(self)

    def on_stop_at_flower(self, flower):
        """Обработчик события 'остановка у цветка' """
        self.load_honey_from(source=flower)

    def on_stop_at_beehive(self, beehive):
        """Обработчик события 'остановка у улья' """
        self.unload_honey_to(target=beehive)

    def on_honey_loaded(self):
        """Обработчик события 'мёд загружен' """
        if self.honey < 100:
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


    bee = MyBeeRasswet()
    bee.move_at(Point(1000, 1000))  # проверка на выход за границы экрана

    beegarden.go()
