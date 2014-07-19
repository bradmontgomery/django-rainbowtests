#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.utils import termcolors
import random

happy_messages = []
sad_messages = []

happy_messages.append(
"""

        (づ｡◕‿‿◕｡)づ・。*。✧・゜・。
        ✧。*・゜゜・✧。・゜゜SUCCESS!!・。
        *。・゜*✧✿。*。✧・゜゜・✧。✧。*・

"""
)

happy_messages.append(
"""

        (☞ﾟ∀ﾟ)☞ You da Man!
        All tests passed.

"""
)

happy_messages.append(
"""

        ヽ(´▽`)/ Hallelujah!
        Praise FSM. Success.

"""
)

happy_messages.append(
"""

        (｡♥‿♥｡) ・。♥。✧・゜・✿
        ✧。*・Your code loves you.✧♥
        ✿。・ All tests passed!✿。*
        ✧・゜♥・✧。♥。*・。♥。✧・♥・✿
"""
)

sad_messages.append(
"""

        （╯°□°）╯︵ ┻━┻
        AAAAAAAAAARGGGGGGGGGG!!!

"""
)

sad_messages.append(
"""

        ლ(ಠ益ಠლ)
        Bloody tests failed AGAIN!

"""
)


def random_happy():
    return termcolors.colorize(random.choice(happy_messages), fg='green')


def random_sad():
    return termcolors.colorize(random.choice(sad_messages), fg='red')
