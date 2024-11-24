from typing import Mapping, Any

import strawberry
from pymongo.synchronous.collection import Collection
from src.excel.schemas import Sheet, WorkSpace
from src.database import db
from src.excel.room_manager import room_manager

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_workspace(self, name: str) -> WorkSpace:
        connection: Collection[Mapping[str, Any]] = db["workspace"]
        row_count = connection.count_documents({})

        workspace_obj = WorkSpace(id=row_count+1,
                                  name=name,
                                  sheet=[Sheet(id=1, name='default').__dict__])

        connection.insert_one(workspace_obj.__dict__)

        return workspace_obj

    @strawberry.mutation
    async def create_sheet(self, workspace_id: int, name: str) -> Sheet:
        connection: Collection[Mapping[str, Any]] = db["workspace"]
        workspace = connection.find_one({"id": workspace_id})

        room_q = room_manager.get_or_create_room(f"{workspace["name"]}-{workspace_id}")
        sheet = Sheet(id=len(workspace["sheet"]), name=name)

        await room_q.put(sheet)
        return sheet
