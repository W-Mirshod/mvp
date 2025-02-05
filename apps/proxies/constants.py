from collections import namedtuple


ANONYMITY_TYPE = namedtuple("ANONYMITY_TYPE", "transparent elite anonymous")._make(range(3))

ANONYMITY_CHOICES = [
    (ANONYMITY_TYPE.transparent, "Transparent"),
    (ANONYMITY_TYPE.elite, "Elite"),
    (ANONYMITY_TYPE.anonymous, "Anonymous"),
]