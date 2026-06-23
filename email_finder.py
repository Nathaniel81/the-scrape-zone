import re
import requests

EMAIL_REGEX = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"


def extract_emails_from_url(url):

    try:

        response = requests.get(
            url,
            timeout=15,
            headers={
                "User-Agent":
                "Mozilla/5.0"
            }
        )

        emails = set(
            re.findall(
                EMAIL_REGEX,
                response.text
            )
        )

        return list(emails)

    except Exception:

        return []
