import strawberry

from src.excel.schemas import Sheet
from src.excel.room_manager import room_manager


@strawberry.type
class Subscription:
    @strawberry.subscription
    async def work_space_room(self, room_name: str) -> Sheet:
        room_q = room_manager.get_or_create_room(room_name)
        while True:
            sheet = room_q.get()
            yield sheet
