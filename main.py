from crawler import get_page_text
from gemini_extractor import extract_speakers
from exporter import save_excel


def load_urls():

    with open(
        "urls.txt",
        "r",
        encoding="utf-8"
    ) as file:

        return [
            line.strip()
            for line in file
            if line.strip()
        ]


def main():

    urls = load_urls()

    all_speakers = []

    for url in urls:

        print(f"\nProcessing: {url}")

        try:

            page_text = get_page_text(url)
            print(page_text[:5000])

            speakers = extract_speakers(
                page_text
            )

            for speaker in speakers:

                speaker["source_url"] = url

                all_speakers.append(
                    speaker
                )

            print(
                f"Found {len(speakers)} speakers"
            )

        except Exception as e:

            print(
                f"Error processing {url}"
            )

            print(e)

    save_excel(all_speakers)


if __name__ == "__main__":
    main()
