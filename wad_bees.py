#!/usr/bin/env python
# -*- coding: utf-8 -*-

from beegarden.core import Bee
from robogame_engine.theme import theme


class WadBee(Bee):

    def on_born(self):
        self.in_hunt = True
        self.kill_them_all()

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

    def on_stop_at_flower(self, flower):
        self.load_honey_from(flower)

    def on_stop_at_beehive(self, beehive):
        self.unload_honey_to(beehive)

    def on_honey_loaded(self):
        if self.is_full():
            self.move_at(self.my_beehive)
        else:
            self.go_flower()

    def on_honey_unloaded(self):
        self.go_flower()

    def go_flower(self):
        for flower in self.flowers:
            if flower.honey:
                self.move_at(flower)
                break
        else:
            self.move_at(self.my_beehive)


class WadBee2(WadBee):
    pass


class WadBee3(WadBee):
    pass


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


