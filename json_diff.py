import sys
import json
from   pathlib import Path
from   jsondiff import diff

if len(sys.argv) == 3:
    old_file = Path(sys.argv[1])
    new_file = Path(sys.argv[2])
    if old_file.is_file() and new_file.is_file():
#       with open(old_file) as json_data:
        with old_file.open() as json_data:
            old_json = json.load(json_data)
#       with open(new_file) as json_data:
        with new_file.open() as json_data:
            new_json = json.load(json_data)
        if diff(old_json, new_json):
            sys.exit(1)
        else:
            sys.exit(0)

print(sys.argv)
print('json diff error: json_diff.py <new file> <old file>')
sys.exit(1)
