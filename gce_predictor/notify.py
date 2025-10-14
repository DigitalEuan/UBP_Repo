from __future__ import annotations

import json
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any, Dict, Optional

import requests


def send_webhook(payload: Dict[str, Any], url: Optional[str] = None, timeout: int = 15) -> bool:
    """POST a JSON payload to a webhook URL (Slack/Discord/custom)."""
    hook = url or os.environ.get("GCE_WEBHOOK_URL")
    if not hook:
        return False
    try:
        r = requests.post(hook, json=payload, timeout=timeout)
        return r.status_code // 100 == 2
    except Exception:
        return False


def send_email(subject: str, body: str, to_addr: Optional[str] = None) -> bool:
    """Send an email via SMTP using environment configuration.

    Required env vars: SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, SMTP_FROM, SMTP_TO (or to_addr)
    """
    host = os.environ.get("SMTP_HOST")
    port = int(os.environ.get("SMTP_PORT", "587"))
    user = os.environ.get("SMTP_USER")
    pwd = os.environ.get("SMTP_PASS")
    from_addr = os.environ.get("SMTP_FROM")
    to = to_addr or os.environ.get("SMTP_TO")

    if not all([host, port, user, pwd, from_addr, to]):
        return False

    msg = MIMEMultipart()
    msg["From"] = from_addr
    msg["To"] = to
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(host, port, timeout=20) as server:
            server.starttls()
            server.login(user, pwd)
            server.sendmail(from_addr, [to], msg.as_string())
        return True
    except Exception:
        return False


def notify_new_prediction(prediction: Dict[str, Any]) -> Dict[str, bool]:
    """Send both webhook and email notifications if configured."""
    title = f"UBP GCE Prediction: {prediction.get('trigger_class')} [{prediction.get('prediction_id')}]"
    body = json.dumps(prediction, indent=2)

    results = {
        "webhook": send_webhook({"text": title, "prediction": prediction}),
        "email": send_email(title, body),
    }
    return results
