response = {
    "401": {
        "content": {"application/json": {"example": {"detail": "Not authenticated"}}}
    },
    "404": {
        "content": {
            "application/json": {"example": {"detail": "Category was not found"}}
        }
    },
}
