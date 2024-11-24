from collections.abc import Mapping
from typing import Any

import strawberry
from pymongo.synchronous.collection import Collection
from src.excel.schemas import Sheet, WorkSpace, User
from src.database import db


@strawberry.type
class Query:
    @strawberry.field
    def work_space(self) -> list[WorkSpace]:
        connection: Collection[Mapping[str, Any]] = db["workspace"]
        workspace = connection.find()

        list_workspace = [
            WorkSpace(
                id=work["_id"],
                name=work["name"],
                user_list = [User(id=id) for id in work['user_list']],
                sheet=[Sheet(**sheet) for sheet in work["sheet"]],
            )
            for work in workspace
        ]
        return list_workspace

    @strawberry.field
    def work_space(self, id: int) -> WorkSpace:
        connection: Collection[Mapping[str, Any]] = db["workspace"]
        workspace = connection.find_one({"id": id})

        return WorkSpace(
            id=workspace['id'],
            name=workspace['name'],
            sheet=workspace['sheet'],
            owner_id=1,
            user_list=[]
        )
