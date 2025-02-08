from collections import namedtuple

class ProxiesConstants:

    DEFAULT_PROXY_JUDGE_URL =  "http://proxyjudge.us/azenv.php"
    DEFAULT_PROXY_JUDGE_MOJEIP_URL =  "http://mojeip.net.pl/asdfa/azenv.php"

    CHECKER_GET_IT_URL = "https://api.ipify.org/"
    CHECKER_GET_COUNTRY_URL = "https://ip2c.org/"

    """ ANONYMITY TYPE ->"""
    ANONYMITY_TYPE = namedtuple("ANONYMITY_TYPE", "transparent elite anonymous")._make(
        range(3)
    )

    ANONYMITY_CHOICES = [
        (ANONYMITY_TYPE.transparent, "Transparent"),
        (ANONYMITY_TYPE.elite, "Elite"),
        (ANONYMITY_TYPE.anonymous, "Anonymous"),
    ]
    """<- ANONYMITY TYPE"""