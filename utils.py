import csv

def extract_csv_data(path: str, movies: list) -> list[dict]:
    with open(path, mode="r", encoding="utf-8") as archive:
        reader = csv.DictReader(archive)

        for row in reader:
            movies.append({
                "id": int(row["ID"]),
                "film": row["Film"],
                "genre": row["Genre"],
                "studio": row["Studio"],
                "score": int(row["Score"]),
                "year": int(row["Year"])
            })
        
    return movies