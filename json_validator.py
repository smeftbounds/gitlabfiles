#!/usr/bin/env python3

# Author: K. Potamianos <karolos.potamianos@cern.ch>


# First step, validate the json
# We'll perform more complicated validation steps later

def validate_json(in_file, verbose=True):
    import json
    import jsonschema
    from json_schema import global_schema

    with open(in_file) as f:
        json_to_validate = json.load(f)
        if verbose: print(json.dumps(json_to_validate, indent=2))
        # Validate will raise exception if given json is not
        # what is described in schema.
        try:
            jsonschema.validate(instance=json_to_validate, schema=global_schema)
        except jsonschema.exceptions.SchemaError as e:
            print("ERROR: Exception caught:", e)
            return False
        except jsonschema.exceptions.ValidationError as e:
            print("ERROR: Exception caught:", e)
            return False

        return True


if __name__ == '__main__':
    import sys
    allgood = True
    for f in sys.argv[1:]:
        if not validate_json(f): allgood = False
    if allgood == False:
        print("ERROR: some of the files are not valid according to the schema. Plase fix it or contact the authors.")
    sys.exit(not allgood)
