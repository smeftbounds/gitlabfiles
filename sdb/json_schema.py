global_schema = {
    "type": "object",
    "properties": {
        "$schema": { "type": "string" },
        "eft":   { "type": "string" },
        "basis": { "type": "string" },
        "scale": { "type": "number" },
        "metadata": {
            "type": "object",
            "properties": {
                "lumi":                { "type": "number" },
                "cme":                 { "type": "number" },
                "perturbative_order":  { "type": "string" },
                "comment":             { "type": "string" },
                "submitter": {
                    "type": "object",
                    "properties": {
                        "name":  { "type": "string" },
                        "email": { "type": "string" },  
                    },
                    "required": [ "name", "email" ],
                },
                "doi":      { "type": "string" },
                "authors": {
                    "type": "array",
                    "items": { "type": "string" },
                },
                "fit_type": { "type": "string" },
                "eft_order": {
                    "type": "object",
                    "properties": {
                        "truncation_level": { "type": "string","enum": ["amplitude", "observable", "mixed"]},
                        "truncation_order": { "type": "string" },
                    },
                    "required": [ "truncation_level", "truncation_order" ],
                },
                "bounds_cl": {
                    "type": "array",
                    "items": { "type": "number" },
                    "minItems": 1,
                },
                "data_type": { "type": "string" },
                "title":         { "type": "string" },
                "arxiv":         { "type": "string" },
                "report_number": { "type": "string" },
                "date":          { "type": "string" },  
                "inputs":        { "type": "string" },
            },
            "required": [
                "submitter",
                "doi",
                "authors",
                "fit_type",
                "eft_order",
                "bounds_cl",
                "data_type",
            ],
        },
        "values": {
            "type": "object",
            "additionalProperties": {
                "type": "array",
                "items": { "type": "number" },
                "minItems": 2,
                "maxItems": 4,
            },
        },
    },
    "required": [ "eft", "basis", "scale", "metadata", "values" ],
}
