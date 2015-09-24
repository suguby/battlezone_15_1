#!/usr/bin/env python
# -*- coding: utf-8 -*-

from my_bees import MyBee
from other_bees import OtherBee
from beegarden.core import Beegarden


if __name__ == '__main__':
    beegarden = Beegarden(
        name="My little garden",
        beehives_count=2,
        flowers_count=20,
        speed=5,
    )

    bees_count = 5

    team1 = [MyBee() for i in range(bees_count)]
    team2 = [OtherBee() for i in range(bees_count)]

    beegarden.go()
