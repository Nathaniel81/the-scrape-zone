from search import search_person
from email_finder import (
    extract_emails_from_url
)


def find_email(name, affiliation):

    urls = search_person(
        name,
        affiliation
    )

    for url in urls:

        emails = extract_emails_from_url(
            url
        )

        if emails:

            return {
                "email": emails[0],
                "source": url
            }

    return {
        "email": "",
        "source": ""
    }
