import asyncio


class RoomManager:
    def __init__(self):
        self.room: dict[str, asyncio.Queue] = {}

    def get_or_create_room(self, name: str) -> asyncio.Queue:
        if name not in self.room:
            self.room[name] = asyncio.Queue()

        return self.room[name]

room_manager = RoomManager()