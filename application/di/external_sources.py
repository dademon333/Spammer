from application.external_sources.smsc.client import SMSCClient


def get_smsc_client() -> SMSCClient:
    return SMSCClient()
