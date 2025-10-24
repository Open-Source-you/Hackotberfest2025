import json
import os
DATA_FILE = "project_data.json"     # The file where current project data is stored
EXPORT_FILE = "exported_data.json"  # The file to which data will be exported/imported

def export_data():
    """
    Export project data to a JSON file (EXPORT_FILE).
    Reads data from 'project_data.json' and writes it to 'exported_data.json'.
    """
    if not os.path.exists(DATA_FILE):
        print(f"No data found in '{DATA_FILE}'. Please create or add data first.")
        return

    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    with open(EXPORT_FILE, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Data exported successfully to '{EXPORT_FILE}'")


def import_data():
    """
    Import project data from a JSON file (EXPORT_FILE).
    Reads data from 'exported_data.json' and writes it back into 'project_data.json'.
    """
    if not os.path.exists(EXPORT_FILE):
        print(f"No exported file found at '{EXPORT_FILE}' to import from.")
        return

    with open(EXPORT_FILE, "r") as f:
        data = json.load(f)

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Data imported successfully into '{DATA_FILE}'")


def main():
    print("Data Export/Import Tool")
    print("1.Export Data (project_data.json → exported_data.json)")
    print("2.Import Data (exported_data.json → project_data.json)")
    print("3.Exit")

    choice = input("Enter your choice ").strip()

    if choice == "1":
        export_data()
    elif choice == "2":
        import_data()
    elif choice == "3":
        print("Exiting...")
    else:
        print("Invalid choice! Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()