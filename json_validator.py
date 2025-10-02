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

wcxf_basis_data = {}
wcxf_valid_ops = {}

def wcxf_load_basis(in_file):
    print("Loading WCxF basis definitions")
    with open(in_file) as f:
        import json
        json_data = json.load(f)
        eft = json_data["eft"]
        basis = json_data["basis"]
        if eft not in wcxf_basis_data:
            wcxf_basis_data[eft] = {}
            wcxf_valid_ops[eft] = {}
        wcxf_basis_data[eft][basis] = json_data
        wcxf_valid_ops[eft][basis] = [ k 
                      for sector in wcxf_basis_data[eft][basis]["sectors"].keys() 
                      for k in wcxf_basis_data[eft][basis]["sectors"][sector].keys() ]
        print(f"Found {len(wcxf_valid_ops[eft][basis])} valid operators for {eft} {basis}")

def wcxf_check_operators(json_data):
    allgood = True
    for result in json_data["results"]:
        eft = result["wcxf_eft"]
        basis = result["wcxf_basis"]
        for c in result["bounds_coeffs"]:
            if c["coeff"] not in wcxf_valid_ops[eft][basis]:
                print(f"ERROR: operator {c['coeff']} isn't a valid name in WCxf {eft} {basis} definition.")
                allgood = False
    return allgood

def wcxf_validate_json(json_to_validate):
    wcxf_check_operators(json_to_validate)

# This is to add extra high-level validation that cannot easily be put into the schema
# Note that the alternative approach might be to augment the schema scriptically
def validate_content(in_file, verbose=True):
    if not wcxf_basis_data:
        import os, glob, wcxf
        for f in glob.glob(os.path.dirname(wcxf.__file__)+"/**/*.basis.json", recursive=True):
            wcxf_load_basis(f)
    with open(in_file) as f:
        import json
        json_to_validate = json.load(f)
        wcxf_validate_json(json_to_validate)
    return True

if __name__ == '__main__':
    import sys
    allgood = True
    for f in sys.argv[1:]:
        if not validate_json(f): allgood = False
        elif validate_content(f): allgood = False
    if allgood == False:
        print("ERROR: some of the files are not valid according to the schema. Plase fix it or contact the authors.")
    sys.exit(not allgood)
