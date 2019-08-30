# DECLARE SHEMAS
import datetime as dt
from marshmallow import Schema, fields, pprint, post_load, ValidationError, validate, validates, INCLUDE

class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.created_at = dt.datetime.now()

    def __repr__(self):
        return "<User(name={self.name!r})>".format(self=self)

# schema for basic user model
class UserSchema(Schema):
    name = fields.Str()
    email = fields.Email()
    created_at = fields.DateTime()

# Serializin object (DUMP)
user = User(name="Monty", email="monty@python.org")
schema = UserSchema()
result = schema.dump(user)
pprint(result)

# serialize to json
json_result = schema.dumps(user)
pprint(json_result)

#Deserializing obj (LOADING)
user_data = {
    "created_at": "2014-08-11T05:26:03.869245",
    "email": "ken@yahoo.com",
    "name": "Ken",
}
schema = UserSchema()
result = schema.load(user_data)
pprint(result)

#Deserialize to obj
class UserSchema2(Schema):
    name = fields.Str()
    email = fields.Email()
    created_at = fields.DateTime()

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)
# deco receives dict of deserialize data 
user_data = {"name": "Ronnie", "email": "ronnie@stones.com"}
schema = UserSchema2()
result = schema.load(user_data)
print(result)

#Set many=True for ++objects

#Validation 
try:
    result = UserSchema().load({"name": "John", "email": "foo"})
except ValidationError as err:
    print(err.messages)
    print(err.valid_data)   

#additionnal validation with validate
class UserSchema3(Schema):
    name = fields.Str(validate=validate.Length(min=1))
    permission = fields.Str(validate=validate.OneOf(["read", "write", "admin"]))
    age = fields.Int(validate=validate.Range(min=18, max=40))


in_data = {"name": "", "permission": "invalid", "age": 71}
try:
    UserSchema3().load(in_data)
except ValidationError as err:
    pprint(err.messages)

#or create validation fct
def validate_quantity(n):
    if n < 0:
        raise ValidationError("Quantity must be greater than 0.")
    if n > 30:
        raise ValidationError("Quantity must not be greater than 30.")

#or as methods
class ItemSchema(Schema):
    quantity = fields.Integer()

    @validates("quantity")
    def validate_quantity(self, value):
        if value < 0:
            raise ValidationError("Quantity must be greater than 0.")
        if value > 30:
            raise ValidationError("Quantity must not be greater than 30.")

#Make fields required
class UserSchema4(Schema):
    name = fields.String(required=True)
    age = fields.Integer(required=True, error_messages={"required": "Age is required."})
    city = fields.String(
        required=True,
        error_messages={"required": {"message": "City required", "code": 400}},
    )
    email = fields.Email()

try:
    result = UserSchema().load({"email": "foo@bar.com"})
except ValidationError as err:
    pprint(err.messages)

#to skip required validation -> partial
class UserSchema5(Schema):
    name = fields.String(required=True)
    age = fields.Integer(required=True)

result = UserSchema5().load({"age": 42}, partial=("name",))
print(result)
#or set partial=True
result = UserSchema5().load({"age": 42}, partial=True)
print(result)

#missing specifies the default deserialization value for a field. 
#default specifies the default serialization value.
class UserSchema6(Schema):
    #id = fields.UUID(missing=uuid.uuid1)
    birthdate = fields.DateTime(default=dt.datetime(2017, 9, 29))

#Handle Unknown fields
class UserSchema7(Schema):
    class Meta:
        unknown = INCLUDE

#just validate without deserialization use Shema.validate
errors = UserSchema().validate({"name": "Ronnie", "email": "invalid-email"})
print(errors)

#“Read-only” and “Write-only” Fields
class UserSchema8(Schema):
    name = fields.Str()
    # password is "write-only"
    password = fields.Str(load_only=True)
    # created_at is "read-only"
    created_at = fields.DateTime(dump_only=True)

#Specifing Key with data_key
class UserSchema9(Schema):
    name = fields.String()
    email = fields.Email(data_key="emailAddress")


s = UserSchema9()

data = {"name": "Mike", "email": "foo@bar.com"}
result = s.dump(data)
print(result)

data = {"name": "Mike", "emailAddress": "foo@bar.com"}
result = s.load(data)
print(result)