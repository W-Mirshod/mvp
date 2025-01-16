from factory import Faker
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyInteger, FuzzyText

from apps.mail_servers import ServerType
from apps.mail_servers import (
    IMAPServer,
    ProxyServer,
    SMTPServer,
)


class SMTPServerFactory(DjangoModelFactory):
    """
    SMTP Server Factory
    """

    type = ServerType.SMTP
    url = FuzzyText(length=20, prefix="http://smtp.")
    port = FuzzyInteger(1, 65535)
    password = Faker("password")
    username = FuzzyText(length=15, suffix="_smtp@example.com")
    email_use_tls = Faker("boolean", chance_of_getting_true=75)
    is_active = True

    class Meta:
        model = SMTPServer


class IMAPServerFactory(DjangoModelFactory):
    """
    IMAP Server Factory
    """

    type = ServerType.IMAP
    url = FuzzyText(length=20, prefix="http://imap.")
    port = FuzzyInteger(1, 65535)
    password = Faker("password")
    username = FuzzyText(length=15, suffix="_imap@example.com")
    email_use_tls = Faker("boolean", chance_of_getting_true=75)
    is_active = True

    class Meta:
        model = IMAPServer


class ProxyServerFactory(DjangoModelFactory):
    """
    Proxy Server Factory
    """

    type = ServerType.PROXY
    url = FuzzyText(length=20, prefix="http://proxy.")
    port = FuzzyInteger(1, 65535)
    password = Faker("password")
    username = FuzzyText(length=15, suffix="_proxy@example.com")
    email_use_tls = Faker("boolean", chance_of_getting_true=75)
    is_active = True

    class Meta:
        model = ProxyServer


# class MessageTemplateFactory(DjangoModelFactory):
#     """
#     Message Template Factory
#     """
#
#     from_address = FuzzyText(length=20, suffix="_template@example.com")
#     template = FuzzyText(length=20, prefix="template_")
#     message = {"message": FuzzyText(length=20, prefix="message_").fuzz()}
#
#     class Meta:
#         model = MessageTemplate
