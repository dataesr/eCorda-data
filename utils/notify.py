import os
import requests


def notify(name, msg, e=None):
    color = '#ff5655' if e else '#27a658'
    fields = [{'short': False, 'value': e}] if e else []
    attachments = [{'color': color, 'text': msg, 'fields': fields}]
    body = {'username': name, 'channel': os.getenv(
        'MM_CHANNEL'), 'attachments': attachments}
    requests.post(os.getenv('MM_WEBHOOK_URL'), json=body)
