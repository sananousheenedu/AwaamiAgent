import csv
import os
import requests


SOURCES_FILE = os.path.join(
    os.path.dirname(__file__),
    "sources.csv"
)

OUTPUT_DIR = os.path.join(
    os.path.dirname(__file__),
    "documents"
)


def download_sources():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(SOURCES_FILE, "r", encoding="utf-8") as file:
        sources = csv.DictReader(file)

        for source in sources:
            source_id = source["source_id"]
            source_name = source["source_name"]
            source_url = source["source_url"]

            safe_name = "".join(
                c if c.isalnum() or c in (" ", "-", "_")
                else "_"
                for c in source_name
            ).strip()

            filename = f"{source_id}_{safe_name}.pdf"
            output_path = os.path.join(OUTPUT_DIR, filename)

            print(f"Downloading: {source_name}")

            try:
                response = requests.get(
                    source_url,
                    timeout=60,
                    headers={
                        "User-Agent": "AwaamiAgent/1.0"
                    }
                )

                response.raise_for_status()

                content_type = response.headers.get(
                    "Content-Type",
                    ""
                ).lower()

                if "pdf" not in content_type and not response.content.startswith(b"%PDF"):
                    print(f"Skipped: {source_name} - not a PDF")
                    continue

                with open(output_path, "wb") as output_file:
                    output_file.write(response.content)

                print(f"Saved: {output_path}")

            except requests.RequestException as error:
                print(f"Failed: {source_name}")
                print(f"Error: {error}")

            except Exception as error:
                print(f"Unexpected error for {source_name}: {error}")


if __name__ == "__main__":
    download_sources()
