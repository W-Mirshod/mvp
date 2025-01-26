class CampaignConstants:
    ID_MAX_LENGTH = 100
    TITLE_MAX_LENGTH = 255

    """MAILING TYPE  ->"""
    DEFAULT_MAILING_TYPE = 1
    SES_MAILING_TYPE = 2
    ANY_MAIL_MAILING_TYPE = 3
    SMTP_MAILING_TYPE = 4
    GMAIL_MAILING_TYPE = 5

    MAILING_TYPE_CHOICES = (
        (DEFAULT_MAILING_TYPE, "Default"),
        (SES_MAILING_TYPE, "SES"),
        (ANY_MAIL_MAILING_TYPE, "AnyMail 3"),
        (SMTP_MAILING_TYPE, "SMTP"),
        (GMAIL_MAILING_TYPE, "G-Mail 5"),
    )

    MAILING_TYPE_IDS = [i[0] for i in MAILING_TYPE_CHOICES]
    """< - MAILING TYPE """

    """ EMAIL BACKENDS ->"""

    EMAIL_BACKENDS = {
        DEFAULT_MAILING_TYPE: "post_office.EmailBackend",
        SES_MAILING_TYPE: "django_ses.SESBackend",
        SMTP_MAILING_TYPE: "post_office.EmailBackend",
        ANY_MAIL_MAILING_TYPE: "anymail.backends.amazon_ses.EmailBackend",
    }
    """<- EMAIL BACKENDS"""

    """SHIPPING TYPE  ->"""
    DEFAULT_SHIPPING_TYPE = 1
    SPEED_SHIPPING_TYPE = 2
    EXTRA_SPEED_SHIPPING_TYPE = 3

    SHIPPING_TYPE_CHOICES = (
        (DEFAULT_SHIPPING_TYPE, "Default"),
        (SPEED_SHIPPING_TYPE, "Speed"),
        (EXTRA_SPEED_SHIPPING_TYPE, "Extra speed"),
    )

    SHIPPING_TYPE_IDS = [i[0] for i in SHIPPING_TYPE_CHOICES]
    """< - SHIPPING TYPE """

    """ CAMPAIGN STATUS  ->"""
    NEW_CAMPAIGN_STATUS = 1
    COMPLETED_CAMPAIGN_STATUS = 2
    STOPPED_CAMPAIGN_STATUS = 3
    ERROR_CAMPAIGN_STATUS = 4
    AI_MAILING_CAMPAIGN_STATUS = 5
    SENDING_CAMPAIGN_STATUS = 6

    CAMPAIGN_STATUS_CHOICES = (
        (NEW_CAMPAIGN_STATUS, "New"),
        (COMPLETED_CAMPAIGN_STATUS, "Completed"),
        (STOPPED_CAMPAIGN_STATUS, "Stopped"),
        (ERROR_CAMPAIGN_STATUS, "Error"),
        (AI_MAILING_CAMPAIGN_STATUS, "AI mailing"),
        (SENDING_CAMPAIGN_STATUS, "Sending"),
    )

    CAMPAIGN_STATUS_IDS = [i[0] for i in CAMPAIGN_STATUS_CHOICES]
    """< - CAMPAIGN STATUS """
