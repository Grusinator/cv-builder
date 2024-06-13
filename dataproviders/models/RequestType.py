from enum import Enum


class RequestType(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    UPDATE = "UPDATE"

    @classmethod
    def build_choices(cls) -> list:
        return [(element.value, element.value) for element in cls]
