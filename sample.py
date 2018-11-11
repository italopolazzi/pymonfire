# -*- coding: utf-8 -*-
from datetime import datetime, timezone


def document_to_update():
    return {
        "_id": "iXLhIvLyWaWM8FN4rJxQk3pdv9D2",
        "updatedAt": datetime.now(timezone.utc),
        "tweets": {
            "my": {
                "aleatorio1": "Hoje comi hambúrguer!",
                "aleatorio2": "Joguei muito @itpzzi"
            },
            "linked": [
                "aleatorio3",
                "aleatorio4"
            ]
        }
    }

