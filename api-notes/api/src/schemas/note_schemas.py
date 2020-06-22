from marshmallow import fields, EXCLUDE
from marshmallow_peewee import ModelSchema

from api.src.models.note import Note
from api.src.common.constants import Constants

class NoteCreateSchema(ModelSchema):

	class Meta:
		model = Note
		unknown = EXCLUDE
		exclude = ('user','created_at')


class NoteListSchema(ModelSchema):

	class Meta:
		model = Note
		unknown = EXCLUDE
		exclude = ('user',)
		datetimeformat = Constants.FORMAT_DATETIME