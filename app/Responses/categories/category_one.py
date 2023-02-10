response = {
    "200": {
        "content": {
            "application/json": {
                "example": {
                    "id": "1",
                    "title": "Music",
                }
            }
        }
    },
    "201": {
        "content": {
            "application/json": {
                "example": {
                    "id": "1",
                    "title": "Music",
                }
            }
        }
    },
    "401": {
        "content": {"application/json": {"example": {"detail": "Not authenticated"}}}
    },
    "404": {
        "content": {
            "application/json": {"example": {"detail": "Category was not found"}}
        }
    },
}
