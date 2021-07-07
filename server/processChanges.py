# This script makes changes in database based on sent JSON request
# NOTE: check if typeform questions are the same as col names.
import sys
import importlib
from pathlib import Path
import json

# Add parent directory to PYTHONPATH to be able to find package.
if __name__ == '__main__' and __package__ is None:
    file = Path(__file__).resolve()
    parent, top = file.parent, file.parents[2]

    sys.path.append(str(top))
    try:
        sys.path.remove(str(parent))
    except ValueError:
        pass

    __package__ = '.'.join(parent.parts[len(top.parts):])
    importlib.import_module(__package__)

# print(sys.path)
from tech_team_database.dependencies.DatabaseSQLOperations import TpSQL

db = TpSQL()
# print(db.listTableNames())

# Get data
with open('sample.json') as json_file:
    data = json.load(json_file)

for request in data["requests"]:
    # Determine table to modify and make sure it exists:

    # checkTblName()
    tableName = ""

    # Before editing, check if there are multiple oldVal entries for the checkColName:
    colData = db.getColData(tableName, [request["submission_q"]])

    # Modify specific table:
    # db.editTable(tableName, colName, checkColName, oldVal, newVal)
    db.editTable(tableName, request["change_q"], request["submission_q"], request["submission_a"], request["change_a"])

    # Check if modified (just for testing):

