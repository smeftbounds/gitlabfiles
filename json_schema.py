
# Author: K. Potamianos <karolos.potamianos@cern.ch>

global_schema = {
        "type": "object",
        "properties": {
            # Information about the submitter of the entry First Last <First.Last@Domain.Ext>
            "submitter": { "type": "string" },
            # Information about the publication
            "title": { "type": "string" },
            "arxiv": { "type": "string" },
            "reportNumber": { "type": "string" },
            "date": { "type": "string" },                               # Todo: use proper date field
            "doi": { "type": "string" },
            "description": { "type": "string" },
            "comments": { "type": "string" },
            # Information about the results contained in the paper (could be multiple)
            "results": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "lumi": { "type": "number" },
                        "cme": { "type": "number" },
                        "wcxf_eft": { "type": "string" },
                        "wcxf_basis": { "type": "string" },
                        "p_order": { "type": "string" },
                        "eft_order": { "type": "string" },
                        "lambda_norm": { "type": "number" },
                        "fit_type": { "type": "string" },
                        "ewk_inputs": { "type": "string" },
                        "bounds_cl": { "type": "string" },
                        "coeffs": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "coeff": { "type": "string" },
                                    "bound": { "type": "string" },
                                    },
                                "required": [ "coeff", "bound" ],
                                },
                            },
                        },
                    "required": [ "lumi", "cme", "wcxf_eft", "wcxf_basis", "p_order", "eft_order", "lambda_norm", "fit_type", "ewk_inputs", "bounds_cl", "bounds_coeffs" ],
                    },
                },
            },
        "required": [ "submitter", "title", "arxiv", "reportNumber", "date", "doi", "description", "comments", "results" ],
        }
