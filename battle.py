#!/usr/bin/env python
# -*- coding: utf-8 -*-
from beegarden.core import Beegarden

from rasswet_bee import MyBeeRasswet
from alex_bees import AlexBee

if __name__ == '__main__':
    beegarden = Beegarden(
        name="My little garden",
        beehives_count=2,
        flowers_count=20,
        speed=5,
    )

    bees_count = 5

    team1 = [MyBeeRasswet() for i in range(bees_count)]
    team2 = [AlexBee() for i in range(bees_count)]

    beegarden.go()
