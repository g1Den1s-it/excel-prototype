import strawberry



@strawberry.type
class Sheet:
    id: str
    name: str


@strawberry.type
class User:
    id: int


@strawberry.type
class WorkSpace:
    id: str
    name: str
    sheet: list[Sheet]
    owner_id: int
    user_list: list[User]
