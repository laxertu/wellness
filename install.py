import sys
from repository import create_repository

try:
    csv_path = sys.argv[1]
    repository = create_repository()
    repository.init_db()
    repository.import_csv(csv_path)

except IndexError:
    print("missing csv path")
    exit(0)
