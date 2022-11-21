# [logining]

# API_ID and API_HASH get from https://my.telegram.org/auth and there is a "API development tools"
API_ID = 12345678 # Your api id
API_HASH = "YOUR API HASH" # Your api hash

# [command settings]
START_ARGS = {
    "recording": {
        "usage": ["recording", "r"]
    },
    "dice": {
        "usage": ["dice"]
    },
}
GET_ARGS = {
    "info": {
        "usage": ["info", "i"]
    },
    "chat": {
        "usage": ["chat", "c"]
    },
    "pow": {
        "usage": ["pow"]
    },
    "database": {
        "usage": ["database", "data", "d"]
    },
    "sqrt": {
        "usage": ["sqrt"]
    },
    "sin": {
        "usage": ["sin"]
    },
    "cos": {
        "usage": ["cos"]
    },
    "tg": {
        "usage": ["tg"]
    }
}
STOP_ARGS = {
    "recording": {
        "usage": ["recording", "r"]
    }
}

ALL_COMMANDS = {
    "start": {
        "description": "Starts some events in this chat",
        "args": {
            "recording": "Starts recording of chat. Have one optional argument. It is a id of chat for recording.",
            "dice": "send a working dice"
        }
    },
    "get": {
        "description": "Get some information",
        "args": {
            "info chat": "Get information about chat",
            "pow": "Get a power of number. Have two argument. First argument is necessary. It is a base number. Second argument is optional. It is a index of power",
            "database": "Get a database of bot",
            "sqrt": "Get a sqrt of number. Have two argument. First argument is necessary. It is a base number. Second argument is optional. It is a index of sqrt",
            "sin": "Get a sine of number.",
            "cos": "Get a cosine of number.",
            "tg": "Get a tangent of number."
        }
    },
    "stop": {
        "description": "Stop some events in this chat",
        "args": {
            "recording": "Stop recording of chat."
        }
    }
}

# [debbuger]
PRINT_RETRANSLATED_MESSAGES = True