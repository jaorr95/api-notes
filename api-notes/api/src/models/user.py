from datetime import datetime

from peewee import CharField, AutoField, DateTimeField

from api.src.models.base.base_model import BaseModel
from api.src.common.utils import Utils


class User(BaseModel):

	id = AutoField(primary_key=True)
	first_name = CharField(max_length=100, null=False, unique=False)
	last_name = CharField(max_length=100, null=False, unique=False)
	email = CharField(max_length=100, null=False, unique=True)
	_password = CharField(max_length=60, null=False, unique=False, column_name='password')
	created_at = DateTimeField(null=False, default=datetime.now)

	def __str__(self):
		return "User: <id={0}, firstname={1}, lastname={2}, email={3}>".format(
			self.id, self.first_name, self.last_name, self.email)

	def __repr__(self):
		return "User: <id={0}, firstname={1}, lastname={2}, email={3}>".format(
			self.id, self.first_name, self.last_name, self.email)

	@property
	def password(self):
		return self._password

	@password.setter
	def password(self, plain_password):
		self._password =  Utils.hash_password(plain_password)

	