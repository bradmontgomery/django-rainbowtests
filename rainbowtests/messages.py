"""Fun messages for test results."""

from random import choice

from rainbowtests import colors

happy_messages: list[str] = [
    """

        (づ｡◕‿‿◕｡)づ・。*。✧・゜・。
        ✧。*・゜゜・✧。・゜゜SUCCESS!!・。
        *。・゜*✧✿。*。✧・゜゜・✧。✧。*・

""",
    """

        (☞ﾟ∀ﾟ)☞ You rock!
        All tests passed.

""",
    """

        ヽ(´▽`)/ Hallelujah!
        Praise FSM. Success.

""",
    """

        (｡♥‿♥｡) ・。♥。✧・゜・✿
        ✧。*・Your code loves you.✧♥
        ✿。・ All tests passed!✿。*
        ✧・゜♥・✧。♥。*・。♥。✧・♥・✿
""",
]

sad_messages: list[str] = [
    """

        （╯°□°）╯︵ ┻━┻
        AAAAAAAAAARGGGGGGGGGG!!!

""",
    """

        ლ(ಠ益ಠლ)
        Bloody tests failed AGAIN!

""",
]


def random_happy() -> str:
    return colors.green(choice(happy_messages))


def random_sad() -> str:
    return colors.red(choice(sad_messages))


def random(success: bool) -> str:
    return random_happy() if success else random_sad()
