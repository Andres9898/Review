from marshmallow import Schema, fields, validate, validates, ValidationError
from datetime import datetime

class UserSchema(Schema):
    id = fields.Str(dump_only=True)
    email = fields.Email(required=True)
    password = fields.Str(load_only=True, required=True, validate=validate.Length(min=8))
    confirm_password = fields.Str(load_only=True, required=True)
    role = fields.Str(validate=validate.OneOf(['admin', 'provider', 'warehouse', 'logistics']))
    created_at = fields.DateTime(dump_only=True)
    last_login = fields.DateTime(dump_only=True)
    is_active = fields.Boolean()
    
    @validates('password')
    def validate_password(self, value):
        if not any(char.isdigit() for char in value):
            raise ValidationError('Password must contain at least one number')
        if not any(char.isupper() for char in value):
            raise ValidationError('Password must contain at least one uppercase letter')
        if not any(char.islower() for char in value):
            raise ValidationError('Password must contain at least one lowercase letter')
        if not any(char in '!@#$%^&*()-_=+[]{}|;:,.<>?/~`' for char in value):
            raise ValidationError('Password must contain at least one special character')
            
    @validates('confirm_password')
    def validate_confirm_password(self, value, **kwargs):
        if 'password' in self.context and value != self.context['password']:
            raise ValidationError('Passwords do not match')