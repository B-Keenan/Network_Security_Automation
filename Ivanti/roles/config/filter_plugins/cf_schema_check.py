from jsonschema import validate


class FilterModule(object):
    def filters(self):
        return {
            'cf_schema_check_run_operational_command': self.schema_check_run_operational_command
        }

    def schema_check_run_operational_command(self, additional_arguments_task):

        # Define the schema
        schema = {
            "type": "object",
            "properties": {
                "command": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "cmd": {"type": "string", "pattern": "^show"},
                            "table_body": {"type": "string"},
                            "table_header": {"type": "array", "items": {"type": "string"}}
                        },
                        "required": ["cmd"],
                        "additionalProperties": False
                    }
                }
            },
            "required": ["command"],
            "additionalProperties": False
        }

        # Validate the dictionary against the schema
        try:
            validate(instance=additional_arguments_task, schema=schema)
            return {
                "failure": False,
                "result": additional_arguments_task
            }
        except Exception as e:
            return {
                "failure": True,
                "result": f"Validation failed: {e}"
            }
