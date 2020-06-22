from marshmallow.exceptions import ValidationError

from api.src.common.utils import Utils
from api.src.bo.session_bo import SessionBo
from api.src.bo.user_bo import UserBo
from api.src.models.note import Note
from api.src.schemas.note_schemas import NoteCreateSchema, NoteListSchema
from api.src.exceptions.error import InvalidParametersError

"""
La clase NoteBo se encarga de ejecutar la logica de negocio relacionada con las notas
"""
class NoteBo(object):

	def create_note(self, token_id: str, data: dict) -> dict:

		try:
			note = NoteCreateSchema().load(data)
			user = UserBo().get_user_by_token_id(token_id)
			note.user = user

			note.save()
		except ValidationError as e:
			raise InvalidParametersError(e.data, e.messages, 
				"Error occurred when trying to create new note", e)

		note_dump = NoteListSchema().dump(note)

		return dict(notes=[note_dump])

		


	def get_notes_by_user(self, token_id: str) -> dict:

		user = UserBo().get_user_by_token_id(token_id)
		notes = Note.select().where(Note.user == user).execute()
		notes_dump = NoteListSchema(many=True).dump(notes)
		return dict(notes=notes_dump)



