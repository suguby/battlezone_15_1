#!/usr/bin/env python
# -*- coding: utf-8 -*-

from beegarden.core import Bee, Beegarden
from robogame_engine.geometry import Point
from robogame_engine.theme import theme

# теперь научи их кусаться - причем при укусе пчела теряет здоровье - задается константами
# default_theme/__init__.py:20
# но у своего улья действует защита - здоровье не теряется - "я в домике"
# предлагаю летать по двое-трое :) а если здоровья мало - лететь домой


class AlexBee(Bee):
    all_bees = []

    def on_born(self):
        self.in_hunt = True
        self.kill_them_all()
        self.choice_flower()
        self.move_at(target=self.my_flower)
        AlexBee.all_bees.append(self)


    def there_live_bees(self):
        for bee in self.bees:
            if isinstance(bee, self.__class__) or bee.dead:
                continue
            return True
        return False

    def kill_them_all(self):
        if self._health <= theme.STING_POWER:
            self.move_at(self.my_beehive)
            return
        near_bee, min_distance = None, 1000000
        for bee in self.bees:
            if isinstance(bee, self.__class__) or bee.dead or bee.distance_to(bee.my_beehive) < theme.BEEHIVE_SAFE_DISTANCE:
                continue
            distance_to_bee = self.distance_to(bee)
            if distance_to_bee < min_distance:
                near_bee = bee
                min_distance = distance_to_bee
        if near_bee is None:
            if not self.there_live_bees():
                self.in_hunt = False
            self.move_at(self.flowers[0])
        else:
            if min_distance < theme.NEAR_RADIUS:
                self.sting(near_bee)
            else:
                self.move_at(near_bee)

    def on_hearbeat(self):
        if self.in_hunt:
            self.kill_them_all()

    def choice_flower(self):
        for flower in self.flowers:
            if flower.honey > 0:
                for bee in AlexBee.all_bees:
                    if bee == self:
                        # не экономь на строках = снижает читаемость кода
                        continue
                    if bee.my_flower == flower:
                        break
                else:
                    self.my_flower = flower
                    break
        else:
            if not self.near(self.my_beehive):
                # Иначе, при пустых цветах пчелы пытаются летать из улья в улей (из своего в свой же)
                # и пусть летают :) но и так - норм
                self.move_at(target=self.my_beehive)

#    def nearest_flower(self):


    def on_stop_at_flower(self, flower):
        """Обработчик события 'остановка у цветка' """
#        self.sting()
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
        else:
            self.move_at(target=self.my_beehive)

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
