from functools import wraps

from bottle import request

from api.src.common.utils import Utils
from api.src.bo.session_bo import SessionBo
from api.src.exceptions.error import InvalidTokenError
from api.src.common.constants import Message

def is_authenticated(f):
	"""
	El decorador is_authenticated valida si existe el token jwt en el header
	de la peticion, de existir y ser valido la peticion continua de la forma 
	esperada, caso contrario responde la peticion con un error de invalid token
	"""

	@wraps(f)
	def wrapper(*args, **kwars):

		try:
			token = Utils.get_bearer_token(request.headers)

			token_decode = Utils.token_decode(token)
			token_session = token_decode["token"]
			exists = SessionBo().session_exists(token_session)

			if not exists:
				raise InvalidTokenError(token, "User does not have an active session", "Invalid token")


		except InvalidTokenError as e:
			return Utils.response(message=Message.MESSAGE_INVALID_TOKEN, errors=e.errors, status=e.status)

		return f(*args, **kwars)

	return wrapper