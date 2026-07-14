import os
import json

DATA_FOLDER = "C:/Users/vishu/Downloads/ipl data pipeline/raw data"
files = os.listdir(DATA_FOLDER)
print(f"Total Files Found: {len(files)}")

success = 0
failed = 0
for filename in files:
    if not filename.endswith(".json"):
        print(f"Skipped: {filename}")
        continue
    file_path = os.path.join(DATA_FOLDER, filename)
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            match_data = json.load(file)
        success += 1
    except Exception as e:
        failed += 1
        print(f"Failed to read {filename}")
        print(e)

print("\n========== REPORT ==========")
print(f"Successfully Read : {success}")
print(f"Failed            : {failed}")