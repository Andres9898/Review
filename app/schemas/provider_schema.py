from marshmallow import Schema, fields, validate, validates, ValidationError
from datetime import datetime

class ProviderSchema(Schema):
    id = fields.Int(dump_only=True)
    business_name = fields.Str(required=True, validate=validate.Length(min=2, max=150))
    legal_name = fields.Str()
    rfc = fields.Str(required=True, validate=validate.Regexp(r'^[A-ZÑ&]{3,4}\d{6}[A-Z0-9]{0,3}$'))
    email = fields.Email(required=True)
    phone = fields.Str(validate=validate.Regexp(r'^\+?[1-9]\d{1,14}$'))
    address = fields.Str()
    city = fields.Str()
    state = fields.Str()
    postal_code = fields.Str(validate=validate.Regexp(r'^\d{5}$'))
    country = fields.Str(default='Mexico')
    status = fields.Str(validate=validate.OneOf(['pending', 'approved', 'suspended']))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    @validates('postal_code')
    def validate_postal_code(self, value):
        if value and (not value.isdigit() or len(value) != 5):
            raise ValidationError("Postal code must be 5 digits")