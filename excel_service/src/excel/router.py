import strawberry

from fastapi import APIRouter
from strawberry.fastapi import GraphQLRouter
from strawberry.subscriptions import GRAPHQL_TRANSPORT_WS_PROTOCOL, GRAPHQL_WS_PROTOCOL

from src.excel.query import Query
from src.excel.mutations import Mutation
from src.excel.subscription import Subscription

sheet_schema = strawberry.Schema(query=Query, mutation=Mutation, subscription=Subscription)
sheet_app = GraphQLRouter(
    sheet_schema,
    subscription_protocols=[
        GRAPHQL_TRANSPORT_WS_PROTOCOL,
        GRAPHQL_WS_PROTOCOL
    ]
)

excel = APIRouter(prefix="/excel")

excel.include_router(sheet_app, prefix="/sheet")

@excel.get("")
async def hello():
    return {"message": "HI!"}