from src.importers.parsers.nahuatl_txt import (
    parse_nahuatl_txt
)


FILE_PATH = (
    "data/raw/nahuatl/"
    "source/nau-es.txt"
)


records, rejected = parse_nahuatl_txt(
    FILE_PATH,
    limit=50
)


print()
print("NAHUATL PARSER TEST")
print("=" * 60)

print(
    f"Parsed records: {len(records)}"
)

print(
    f"Rejected records: {len(rejected)}"
)

print()
print("FIRST 10 ENTRIES")
print("=" * 60)


for record in records[:10]:

    print()

    print(
        f"Line: {record.source_index}"
    )

    print(
        f"Headword: {record.headword}"
    )

    print(
        f"Spanish: {record.gloss_es}"
    )

    print(
        f"Sense: "
        f"{record.extra.get('sense_number')}"
    )