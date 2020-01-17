import graphene

from apps.participations import schema as participation_schema
from apps.accounts import schema as account_schema


class Query(account_schema.Query,
            participation_schema.Query,
            graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
