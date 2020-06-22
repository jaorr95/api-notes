from datetime import datetime

from peewee import CharField, AutoField, TextField, ForeignKeyField, DateTimeField

from api.src.models.base.base_model import BaseModel
from api.src.models.user import User

class Note(BaseModel):

	id = AutoField(primary_key=True)
	title = CharField(max_length=100, null=False, unique=False)
	content = TextField(null=False)
	user = ForeignKeyField(User, backref='notes', null=False)
	created_at = DateTimeField(null=False, default=datetime.now)

	def __str__(self):
		return "Note: <id={0}, title={1}, description={2}, user={3}>".format(
			self.id, self.title, self.description, self.user.id)

	def __repr__(self):
		return "Note: <id={0}, title={1}, description={2}, user={3}>".format(
			self.id, self.title, self.description, self.user.id)