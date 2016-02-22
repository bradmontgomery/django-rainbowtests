#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import choice

from rainbowtests import colors

happy_messages = []
sad_messages = []

happy_messages.append("""

        (づ｡◕‿‿◕｡)づ・。*。✧・゜・。
        ✧。*・゜゜・✧。・゜゜SUCCESS!!・。
        *。・゜*✧✿。*。✧・゜゜・✧。✧。*・

""")

happy_messages.append("""

        (☞ﾟ∀ﾟ)☞ You rock!
        All tests passed.

""")

happy_messages.append("""

        ヽ(´▽`)/ Hallelujah!
        Praise FSM. Success.

""")

happy_messages.append("""

        (｡♥‿♥｡) ・。♥。✧・゜・✿
        ✧。*・Your code loves you.✧♥
        ✿。・ All tests passed!✿。*
        ✧・゜♥・✧。♥。*・。♥。✧・♥・✿
""")

sad_messages.append("""

        （╯°□°）╯︵ ┻━┻
        AAAAAAAAAARGGGGGGGGGG!!!

""")

sad_messages.append("""

        ლ(ಠ益ಠლ)
        Bloody tests failed AGAIN!

""")


def random_happy():
    return colors.green(choice(happy_messages))


def random_sad():
    return colors.red(choice(sad_messages))


def random(success):
    return random_happy() if success else random_sad()
