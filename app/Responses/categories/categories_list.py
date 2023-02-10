response = {
    "200": {
        "content": {
            "application/json": {
                "example": [
                    {
                        "id": "1",
                        "title": "Category 1",
                    },
                    {
                        "id": "2",
                        "title": "Category 2    ",
                    },
                ]
            }
        }
    },
    "401": {
        "content": {"application/json": {"example": {"detail": "Not authenticated"}}}
    },
}
