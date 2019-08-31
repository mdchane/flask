import datetime as dt
from marshmallow import Schema, fields, pprint
from random import randrange

#Nesting schema (rlationship bet obj)
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.created_at = dt.datetime.now()
        self.friends = []
        self.employer = None


class Blog:
    def __init__(self, title, author):
        self.title = title
        self.author = author  # A User object

class UserSchema(Schema):
    name = fields.String()
    email = fields.Email()
    created_at = fields.DateTime()


class BlogSchema(Schema):
    title = fields.String()
    author = fields.Nested(UserSchema)  # Nested field

user = User(name="Monty", email="monty@python.org")
blog = Blog(title="Something Completely Different", author=user)
result = BlogSchema().dump(blog)
pprint(result)

# If the field is a collection of nested objects, you must set many=True.
collaborators = fields.Nested(UserSchema, many=True)

print("------------------------------------------\n")
# Specifying Which Fields to Nest
class BlogSchema2(Schema):
    title = fields.String()
    author = fields.Nested(UserSchema, only=["email"])
# Only attribute email will be serializze
schema = BlogSchema2()
result = schema.dump(blog)
pprint(result)

# ALso deeply nested obj with dot
class SiteSchema(Schema):
    blog = fields.Nested(BlogSchema2)

schema = SiteSchema(only=["blog.author.email"])
result = schema.dump(schema)
pprint(result)

print("------------------------------------------\n")
print("replace nested data with a single value with Pluck")
class UserSchema2(Schema):
    name = fields.String()
    email = fields.Email()
    friends = fields.Pluck("self", "name", many=True)


user = User(name="Monty", email="monty@python.org")
#user.friends = ["Mike", "Joe"]
serialized_data = UserSchema2().dump(user)
pprint(serialized_data)
deserialized_data = UserSchema2().load(result)
pprint(deserialized_data)

#You can also exclude fields by passing in an exclude list.

print("------------------------------------------\n")
print("Partial Loading")
class UserSchemaStrict(Schema):
    name = fields.String(required=True)
    email = fields.Email()
    created_at = fields.DateTime(required=True)


class BlogSchemaStrict(Schema):
    title = fields.String(required=True)
    author = fields.Nested(UserSchemaStrict, required=True)


schema = BlogSchemaStrict()
blog = {"title": "Something Completely Different", "author": {}}
result = schema.load(blog, partial=True)
pprint(result)

#Or specifie subset of th fields
author = {"name": "Monty"}
blog = {"title": "Something Completely Different", "author": author}
result = schema.load(blog, partial=("title", "author.created_at"))
pprint(result)

print("------------------------------------------\n")
print("Two-way Nesting")
class Author:
    def __init__(self, name):
        self.name = name
        self.id = randrange(100)

class Book:
    def __init__(self, title, author):
        self.id = randrange(100)
        self.title = title
        self.author = author
class AuthorSchema(Schema):
    # Make sure to use the 'only' or 'exclude' params
    # to avoid infinite recursion
    books = fields.Nested("BookSchema", many=True, exclude=("author",))

    class Meta:
        fields = ("id", "name", "books")


class BookSchema(Schema):
    author = fields.Nested(AuthorSchema, only=("id", "name"))

    class Meta:
        fields = ("id", "title", "author")

author = Author(name="William Faulkner")
book = Book(title="As I Lay Dying", author=author)
book_result = BookSchema().dump(book)
pprint(book_result, indent=2)

author_result = AuthorSchema().dump(author)
pprint(author_result, indent=2)

print("------------------------------------------\n")
print("Nesting A Schema Within Itself")

class UserSchema3(Schema):
    name = fields.String()
    email = fields.Email()
    friends = fields.Nested("self", many=True)
    # Use the 'exclude' argument to avoid infinite recursion
    employer = fields.Nested("self", exclude=("employer",), default=None)


user = User("Steve", "steve@example.com")
user.friends.append(User("Mike", "mike@example.com"))
user.friends.append(User("Joe", "joe@example.com"))
user.employer = User("Dirk", "dirk@example.com")
result = UserSchema3().dump(user)
pprint(result, indent=2)