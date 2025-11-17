#!/usr/bin/env python3
# Author: K. Potamianos <karolos.potamianos@cern.ch>
# Updated for WCxf-style JSON with Level-0 required keys {eft, basis, scale, metadata, values}
#
# Step 1: validate JSON structure against json_schema.global_schema
# Step 2: validate that all operator names in "values" are valid WCxf operators
#         for the given (eft, basis), using basis files from the wilson package.

wcxf_basis_data = {}
wcxf_valid_ops = {}


def validate_json(in_file, verbose=True):
    """
    Validate the JSON file against the global_schema definition.
    Returns True if it passes, False otherwise.
    """
    import json
    import jsonschema
    from json_schema import global_schema

    with open(in_file) as f:
        json_to_validate = json.load(f)

    if verbose:
        import json as _json
        print(_json.dumps(json_to_validate, indent=2))

    try:
        jsonschema.validate(instance=json_to_validate, schema=global_schema)
    except jsonschema.exceptions.SchemaError as e:
        print("ERROR: Schema error:", e)
        return False
    except jsonschema.exceptions.ValidationError as e:
        print("ERROR: Validation error:", e)
        return False

    return True


def wcxf_load_basis(in_file):
    """
    Load a WCxf basis definition (*.basis.json) and cache the list of valid operators
    for that (eft, basis).
    """
    import json

    with open(in_file) as f:
        json_data = json.load(f)

    eft = json_data["eft"]
    basis = json_data["basis"]

    if eft not in wcxf_basis_data:
        wcxf_basis_data[eft] = {}
        wcxf_valid_ops[eft] = {}

    wcxf_basis_data[eft][basis] = json_data

    # Flatten all operator names across sectors
    wcxf_valid_ops[eft][basis] = [
        op_name
        for sector in json_data.get("sectors", {}).values()
        for op_name in sector.keys()
    ]

    print(f"Found {len(wcxf_valid_ops[eft][basis])} valid operators for {eft} {basis} (from {in_file})")


def wcxf_check_operators(json_data):
    """
    Check that all operator names in json_data["values"] are valid WCxf operators
    for the given (eft, basis).

    Expects:
      json_data["eft"]   : string
      json_data["basis"] : string
      json_data["values"]: object mapping operator_name -> [lower, upper]

    Returns True if all operators are valid, False otherwise.
    """
    allgood = True

    eft = json_data.get("eft")
    basis = json_data.get("basis")

    if eft is None or basis is None:
        print("ERROR: JSON is missing 'eft' and/or 'basis' fields at top level.")
        return False

    if eft not in wcxf_valid_ops or basis not in wcxf_valid_ops[eft]:
        print(f"ERROR: EFT {eft} with basis {basis} not defined in WCxF basis definitions. Please check.")
        return False

    valid_ops = set(wcxf_valid_ops[eft][basis])

    values = json_data.get("values", {})
    if not isinstance(values, dict):
        print("ERROR: 'values' field must be an object mapping operator names to [lower, upper] arrays.")
        return False

    for coeff_name in values.keys():
        if coeff_name not in valid_ops:
            print(f"ERROR: operator '{coeff_name}' isn't a valid name in WCxf {eft} {basis} definition.")
            allgood = False

    return allgood


def wcxf_validate_json(json_to_validate):
    """
    Wrapper to run WCxf-related validation on already-parsed json_data.
    Returns True if all checks pass, False otherwise.
    """
    return wcxf_check_operators(json_to_validate)


# This is to add extra high-level validation that cannot easily be put into the schema
# (e.g. cross-checking operator names against WCxf basis definitions).
def validate_content(in_file, verbose=True):
    """
    Load all WCxf basis definitions (once) from the wilson package, then
    validate operator names in the given JSON file.
    """
    import json

    # Lazy-load basis files only once
    if not wcxf_basis_data:
        print("Loading WCxF basis definitions from 'wilson' package...")
        import os
        import glob
        import wilson

        wilson_dir = os.path.dirname(wilson.__file__)
        pattern = os.path.join(wilson_dir, "**", "*.basis.json")
        for f in glob.glob(pattern, recursive=True):
            wcxf_load_basis(f)

    with open(in_file) as f:
        json_to_validate = json.load(f)

    allgood = wcxf_validate_json(json_to_validate)

    if verbose and allgood:
        print("WCxf operator validation passed.")

    return allgood


if __name__ == '__main__':
    import sys

    allgood = True

    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} file1.json [file2.json ...]")
        sys.exit(1)

    for f in sys.argv[1:]:
        print(f"\n=== Validating {f} ===")
        if not validate_json(f):
            allgood = False
        elif not validate_content(f):
            allgood = False

    if not allgood:
        print("\nERROR: some of the files are not valid according to the schema and/or WCxf basis. "
              "Please fix them or contact the authors.")
    else:
        print("\nAll files are valid.")

    sys.exit(0 if allgood else 1)
