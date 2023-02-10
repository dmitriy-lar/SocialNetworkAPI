response = {
    "201": {
        "content": {
            "application/json": {
                "example": {
                    "title": "Title",
                    "content": "Content",
                    "category_id": 1,
                    "user_id": 1,
                    "time_created": "2023-02-10T12:44:07.464Z",
                    "time_updated": "2023-02-10T12:44:07.464Z",
                }
            }
        }
    },
    "401": {
        "content": {"application/json": {"example": {"detail": "Not authenticated"}}}
    },
    "404": {
        "content": {
            "application/json": {"example": {"detail": "No such category with id 1"}}
        }
    },
}
