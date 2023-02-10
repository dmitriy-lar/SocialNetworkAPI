response = {
    "200": {
        "content": {
            "application/json": {
                "example": {
                    "id": '1',
                    "title": 'Music',
                }
            }
        }
    },
    "400": {
        "content": {
            "application/json": {
                "example": {"detail": "Not authenticated"}
            }
        }
    },
}
