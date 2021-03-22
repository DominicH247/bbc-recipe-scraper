cuisine_schema = {
    "$jsonSchema": {
            "bsonType": "object",
            "required": ["name", "recipe_count", "available_count", "recipes"],
            "properties" : {
                "name": {
                    "bsonType": "string",
                    "description": "must be a string and is required"
                },
                "recipe_count": {
                    "bsonType": "int",
                    "description": "must be an integer and is required"
                },
                "available_count": {
                    "bsonType": "int",
                    "description": "must be an integer and is required"
                },
                "recipes": {
                    "bsonType": "array",
                    "description": "must be an array of recipe ids and is required"
                }
            }
    }
}
