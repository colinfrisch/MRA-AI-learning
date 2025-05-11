# tools.py


def get_tool_definitions():
    return [
        {
            "type": "function",
            "function": {
                "name": "get_training_list",
                "description": (
                    "Obtenir la liste des programmes d'apprentissage disponibles"
                ),
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_all_training_summary_for_field",
                "description": (
                    "Obtenir la liste des programmes d'apprentissage disponibles "
                    "pour un domaine donné"
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "field": {
                            "type": "string",
                            "description": (
                                "le domaine pour lequel on veut obtenir les "
                                "programmes d'apprentissage"
                            ),
                        }
                    },
                    "required": ["field"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "create_training",
                "description": (
                    "Créer un nouveau programme d'apprentissage à partir de la "
                    "description fournie"
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "subject": {
                            "type": "string",
                            "description": (
                                "Sujet du programme d'apprentissage"
                            ),
                        },
                        "field": {
                            "type": "string",
                            "description": (
                                "Domaine du programme d'apprentissage"
                            ),
                        },
                    },
                    "required": ["subject", "field"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "subscribe_user_to_training",
                "description": (
                    "Souscrire un utilisateur à un programme d'apprentissage"
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": (
                                "Le prenom de l'utilisateur"
                            ),
                        },
                        "phone": {
                            "type": "string",
                            "description": (
                                "Le numéro de téléphone de l'utilisateur"
                            ),
                        },
                        "program_id": {
                            "type": "string",
                            "description": (
                                "L'identifiant du programme d'apprentissage"
                            ),
                        },
                    },
                    "required": ["name", "phone", "program_id"],
                },
            },
        },
    ]
