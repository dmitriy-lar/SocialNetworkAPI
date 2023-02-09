response = {
    '201': {
        "content": {
            "application/json": {
                "example": {
                    "user": {"id": 1, "email": "user@example.com"},
                    "message": "Successfully registered",
                }
            }
        }
    },
    '400': {
        "content": {
            "application/json": {
                "example": {"detail": "User with this email already exists"}
            }
        }
    },
}
