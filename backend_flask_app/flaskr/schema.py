# import graphene
# from bson.objectid import ObjectId
# from . import mongo 

# # Example user data (this would be from your database in a real app)
# # users = {
# #     '1': {'id': '1', 'username': 'admin', 'role': 'admin'},
# #     '2': {'id': '2', 'username': 'user1', 'role': 'user'},
# # }

# # Define the UserType for GraphQL
# class UserType(graphene.ObjectType):
#     id = graphene.String()
#     username = graphene.String()
#     role = graphene.String()

# # Define the Query class
# class Query(graphene.ObjectType):
#     # Example query to get a user by ID
#     users = graphene.List(UserType)
#     user = graphene.Field(UserType, username=graphene.String())

#     # Query to retrieve all users
#     def resolve_users(self, info):
#         users_collection = mongo.db.users.find()
#         return [UserType(id=str(user['_id']), username=user['username'], role=user['role']) for user in users_collection]

#      # Query to retrieve a single user by username
#     def resolve_user(self, info, username):
#         user = mongo.db.users.find_one({"username": username})
#         if user:
#             return UserType(id=str(user['_id']), username=user['username'], role=user['role'])
#         return None
    
# class CreateUser(graphene.Mutation):
#     class Arguments:
#         username = graphene.String()
#         role = graphene.String()

#     user = graphene.Field(lambda: UserType)

#     def mutate(self, info, username, role):
#          # Insert a new user into MongoDB
#         new_user = {"username": username, "role": role}
#         mongo.db.users.insert_one(new_user)
#         return CreateUser(user=UserType(username=username, role=role))

# # add the mutation to the schema  
# class Mutation(graphene.ObjectType):
#     create_user = CreateUser.Field()

# # Define the schema with the query
# schema = graphene.Schema(query=Query, mutation=Mutation)
