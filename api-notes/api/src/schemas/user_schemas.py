import re

from marshmallow import fields, EXCLUDE, Schema, validates, ValidationError
from marshmallow_peewee import ModelSchema

from api.src.models.user import User
from api.src.common.constants import RegexExpression, Constants


class UserCreateSchema(ModelSchema):

	class Meta:

		model = User
		unknown = EXCLUDE
		exclude = ('_password', 'created_at')

	first_name = fields.String(required=True)
	last_name = fields.String(required=True)
	email = fields.Email(required=True)
	password = fields.String(required=True)

	
	@validates('first_name')
	def validate_first_name(self, value):
		self.validate_name_length(value)
	
	@validates('last_name')
	def validate_last_name(self, value):
		self.validate_name_length(value)


	@validates('password')
	def validate_password(self, value):

		if not re.match(RegexExpression.PASSWORD, value):
			raise ValidationError(
				'Password must have at least: one number, one lowecase, one uppercase and length between 6 and 20')


	def validate_name_length(self, value):

		if (len(value) < 2  or len(value) > 100):
			raise ValidationError('Length mut be between 2 and 100')


class UserListSchema(ModelSchema):

	class Meta:

		model = User
		unknown = EXCLUDE
		exclude = ('_password',)
		datetimeformat = Constants.FORMAT_DATETIME


class UserLoginSchema(Schema):

	class Meta:
		
		unknown = EXCLUDE

	email = fields.Email(required=True)
	password = fields.String(required=True)