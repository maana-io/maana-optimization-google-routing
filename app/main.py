from __future__ import print_function
from ariadne import ObjectType, QueryType, MutationType, gql, make_executable_schema
from ariadne.asgi import GraphQL
from asgi_lifespan import Lifespan, LifespanMiddleware
from graphqlclient import GraphQLClient

# HTTP request library for access token call
import requests
import numpy as np
# .env
from dotenv import load_dotenv
import os

from app.my_types.type_def_strings_2 import optimizer_types
from app.resolvers.resolvers import resolve_pickups_and_deliveries_mapper, \
    resolve_routing_solver_mapper, \
    resolve_routing_solver_with_br_mapper, \
    resolve_routing_solver_with_br_max_profit_mapper


# Load environment variables
load_dotenv()

type_defs = gql(optimizer_types)

query = QueryType()

# resolve_pickups_and_deliveries_mapper(query)
resolve_routing_solver_mapper(query)
resolve_routing_solver_with_br_mapper(query)
resolve_routing_solver_with_br_max_profit_mapper(query)

# Create executable GraphQL schema
schema = make_executable_schema(type_defs, [query])

# --- ASGI app

# Create an ASGI app using the schema, running in debug mode
# Set context with authenticated graphql client.
app = GraphQL(
    schema, debug=True)

# context_value={'client': getClient()})

# 'Lifespan' is a standalone ASGI app.
# It implements the lifespan protocol,
# and allows registering lifespan event handlers.
lifespan = Lifespan()


@lifespan.on_event("startup")
async def startup():
    print("Starting up...")
    print("... done!")


@lifespan.on_event("shutdown")
async def shutdown():
    print("Shutting down...")
    print("... done!")

# 'LifespanMiddleware' returns an ASGI app.
# It forwards lifespan requests to 'lifespan',
# and anything else goes to 'app'.
app = LifespanMiddleware(app, lifespan=lifespan)
