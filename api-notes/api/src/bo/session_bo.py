import hashlib
from datetime import datetime, timedelta

import bcrypt

from api.src.models.user import User
from api.src.models.session import Session
from api.src.common.utils import Utils
from api.src.common.constants import Constants

"""
La clase SessionBo se encarga de ejecutar la logica de negocio relacionada con las sesiones
"""
class SessionBo(object):


	def generate_session(self, user: User) -> dict:
		
		tokens = self.generate_tokens(dict(id=user.id, email=user.email))
		self.save_session(user, tokens['token_session'])

		return tokens


	def generate_tokens(self, data: dict) -> dict:
		
		data["exp"] = datetime.utcnow() + timedelta(minutes=Constants.JWT_EXPIRATION_TIME)
		data["iat"] = datetime.utcnow()
		data["token"] = self.generate_session_token()
		token_jwt = Utils.token_encode(data)

		return dict(token_id=token_jwt, token_session=data['token'])

	
	def generate_session_token(self) -> str:

		return hashlib.sha256(bcrypt.gensalt()).hexdigest()

	
	def save_session(self, user: User, token_session: str) -> None:

		Session.create(user=user, token=token_session)


	
	def get_session_by_token(self, token_session: str) -> Session:
		
		return Session.get_or_none(Session.token == token_session)


	def delete_session_by_token(self, token_session: str) -> None:
		
		return Session.delete().where(Session.token == token_session).execute()

	
	def session_exists(self, token_session: str) -> bool:

		session = self.get_session_by_token(token_session)
		if session:
			return True

		return False


