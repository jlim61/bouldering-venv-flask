from marshmallow import Schema, fields


# ==================================Moonboard Boulders Schemas==================================

class MoonBoardBoulderSchema(Schema):
    boulder_name = fields.Str(required=True)
    grade = fields.Str(required=True)
    setter_id = fields.Int(dump_only=True)
    starting_hold = fields.List(fields.Str, required=True)
    usable_holds = fields.List(fields.Str, required=True)
    finish_hold = fields.List(fields.Str, required=True)
    moonboard_configuration = fields.Str()

class UpdateMoonBoardBoulderSchema(Schema):
    boulder_name = fields.Str()
    grade = fields.Str()
    setter_id = fields.Int(dump_only=True)
    starting_hold = fields.List(fields.Str)
    usable_holds = fields.List(fields.Str)
    finish_hold = fields.List(fields.Str)
    moonboard_configuration = fields.Str()

# ==================================Gym Boulders Schemas==================================

class GymBoulderSchema(Schema):
    location = fields.Str(required=True)
    grade = fields.Str(required=True)
    setter_id = fields.Int(required=True)

class UpdateGymBoulderSchema(Schema):
    location = fields.Str()
    grade = fields.Str()
    setter_id = fields.Int(dump_only=True)

# ==================================Projected Boulders Schemas==================================

class ProjectedBoulderSchema(Schema):
    boulder_id = fields.Int()
    completed = fields.Bool()
    attempts = fields.Int()
    boulder_info = fields.Nested(MoonBoardBoulderSchema, dump_only=True)


# ==================================All Boulders Schemas==================================

class AllBoulderSchema(Schema):
    moonboard_boulders = fields.List(fields.Nested(MoonBoardBoulderSchema), dump_only=True)
    gym_boulders = fields.List(fields.Nested(GymBoulderSchema), dump_only=True)

# ==================================User/Setter Schemas==================================

class UserSetterSchema(Schema):
    id = fields.Str(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True, load_only = True)
    first_name = fields.Str()
    last_name = fields.Str()
    setter = fields.Bool()


class UserSchemaNested(UserSetterSchema):
    moonboard_boulders = fields.List(fields.Nested(MoonBoardBoulderSchema), dump_only=True)
    gym_boulders = fields.List(fields.Nested(GymBoulderSchema), dump_only=True)
    followed = fields.List(fields.Nested(UserSetterSchema), dump_only=True)
    moonboard_info = fields.List(fields.Nested(ProjectedBoulderSchema), dump_only=True)

class UpdateUserSetterSchema(Schema):
  username = fields.Str()
  email = fields.Str()
  password = fields.Str(required = True, load_only = True)
  new_password = fields.Str()
  first_name = fields.Str()
  last_name = fields.Str()
  setter = fields.Bool()

class MoonboardBoulderNestedSchema(MoonBoardBoulderSchema):
    setters = fields.Nested(UserSetterSchema, dump_only=True)

# ==================================Other Schemas==================================

class AuthUserSchema(Schema):
   username = fields.Str()
   password = fields.Str(required=True, load_only = True)