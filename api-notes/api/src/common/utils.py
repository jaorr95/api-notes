import bcrypt
import jwt
from bottle import response

from api.src.exceptions.error import InvalidTokenError
from api.src.common.constants import Constants



class Singleton(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):

        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]



class Utils(object):

	@staticmethod
	def response(*, status=200, data=[], message="", errors=[]) -> dict:
		response.status = status
		#data = [data] if data else data
		return dict(code=status, data=data, message=message, errors=errors)

	@staticmethod
	def hash_password(password: str, rounds=12) -> str:

		salt = bcrypt.gensalt(rounds)
		hashpass = bcrypt.hashpw(password.encode(), salt)
		return hashpass.decode()
		
	@staticmethod
	def verify_password(stored_hash_pass: str, password: str) -> bool:

		return bcrypt.checkpw(password.encode(), stored_hash_pass.encode())


	@staticmethod	
	def token_encode(data: dict) -> str:

		jwt_encoded = jwt.encode(data, "secret_key", algorithm="HS256")

		return jwt_encoded.decode()

	@staticmethod
	def token_decode(token_jwt: str) -> str:

		try:

			token_decoded = jwt.decode(token_jwt, "secret_key", algorithms=["HS256"])
			
		except jwt.exceptions.PyJWTError as e:
			raise InvalidTokenError(token_jwt, e.args, "Error ocurrs trying to decode token jwt", e)

		return token_decoded


	@staticmethod
	def get_bearer_token(headers: dict) -> str:

		token = headers.get(Constants.AUTHORIZATION_HEADER)

		if not token or token.split(" ")[0] != "Bearer":
				raise InvalidTokenError(token, "Token must be a bearer token", "Invalid token")
		
		return token.split(" ")[1]