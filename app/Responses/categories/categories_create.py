response = {
    "201": {
        "content": {
            "application/json": {
                "example": {
                    "title": "Music",
                }
            }
        }
    },
    "400": {
        "content": {
            "application/json": {"example": {"detail": "Category already exists"}}
        }
    },
    "401": {
        "content": {"application/json": {"example": {"detail": "Not authenticated"}}}
    },
}
