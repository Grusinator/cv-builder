from enum import Enum
class ApiTypes(Enum):
    OAUTH_REST = "OauthRest"
    OAUTH_GRAPHQL = "OauthGraphql"
    TOKEN_REST = "TokenRest"

    @classmethod
    def build_choices(cls) -> list:
        return [(element.value, element.value) for element in cls]
