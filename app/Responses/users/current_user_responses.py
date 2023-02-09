response = {
    "200": {
        "content": {
            "application/json": {
                "example": {
                    "user": "user@example.com",
                }
            }
        }
    },
    "400": {
        "content": {"application/json": {"example": {"detail": "Not authenticated"}}}
    },
}
