recipe_schema = {
    "$jsonSchema": {
            "bsonType": "object",
            "required": ["name", "rating", "prep_time", "cook_time", "ingredients", "method"],
            "properties" : {
                "name": {
                    "bsonType": "string",
                    "description": "must be a string and is required"
                },
                "rating": {
                    "bsonType": "int",
                    "description": "must be an integer and is required"
                },
                "prep_time": {
                    "bsonType": "string",
                    "description": "must be a string and is required"
                },
                "cook_time": {
                    "bsonType": "string",
                    "description": "must be a string and is required"
                },
                "dietry": {
                    "bsonType": "string"
                },
                "ingredients": {
                    "bsonType": "array",
                    "description": "must be an array of ingredients ids and is required"
                },
                "method": {
                    "bsonType": "array",
                    "description": "must be an array of mothods and is required"
                }
            }
    }
}
