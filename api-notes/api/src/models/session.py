from datetime import datetime

from peewee import CharField, AutoField, ForeignKeyField, DateTimeField

from api.src.models.base.base_model import BaseModel
from api.src.models.user import User


class Session(BaseModel):

	id = AutoField(primary_key=True)
	token = CharField(max_length=60)
	user = ForeignKeyField(User, backref='sessions', null=False)
	created_at = DateTimeField(null=False, default=datetime.now)

	def __str__(self):
		return "Session: <id={0}, token={1}, user={2}>".format(
			self.id, self.token, self.user.id)

	def __repr__(self):
		return "Session: <id={0}, token={1}, user={2}>".format(
			self.id, self.token, self.user.id)

	