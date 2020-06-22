from marshmallow.exceptions import ValidationError

from api.src.models.user import User
from api.src.bo.session_bo import SessionBo
from api.src.schemas.user_schemas import UserCreateSchema, UserLoginSchema, UserListSchema
from api.src.common.utils import Utils
from api.src.exceptions.error import InvalidParametersError, UserExistsError, AuthenticationError, UserNotFoundError


"""
La clase UserBo se encarga de ejecutar la logica de negocio relacionada con los usuarios
"""
class UserBo(object):

	def create_user(self, data: dict) -> None:
		schema = UserCreateSchema()
		
		try:
			user = schema.load(data)

			if self.email_exists(user.email):
				raise UserExistsError(
					user.email, dict(email="{0} is not unique".format(user.email)), 
					"Error occurred when trying to create new user")
			user.save()

		except ValidationError as e:
			raise InvalidParametersError(e.data, e.messages, 
				"Error occurred when trying to create new user", e)
	
	def email_exists(self, email: str) -> bool:

		user = User.get_or_none(User.email == email)
		if user:
			return True

		return False

		

	def login_user(self, credentials: dict) -> str:
		
		try:
			UserLoginSchema().load(credentials)
			user = User.get(User.email == credentials['email'])
			
			if not Utils.verify_password(user.password, credentials['password']):
				raise AuthenticationError(credentials, "Invalid password or email",
					"Error occurred when trying to login user")

			tokens = SessionBo().generate_session(user)

		except ValidationError as e:
			raise InvalidParametersError(e.data, e.messages, 
				"Error occurred when trying to loggin user", e)

		except User.DoesNotExist as e:
			raise AuthenticationError(credentials, "Invalid password or email",
					"Error occurred when trying to login user", e)

		return tokens["token_id"]


	def user_logout(self, token_id: str) -> None:

		token_session = Utils.token_decode(token_id)['token']
		SessionBo().delete_session_by_token(token_session)


	def get_user_by_token_id(self, token_id: str) -> User:

		try:
			token_decode = Utils.token_decode(token_id)
			user = User.get_by_id(token_decode['id'])
		except User.DoesNotExist as e:
			raise UserNotFoundError(
					token_decode, "User not found", 
					"Error occurred when trying to get user by token id")
		return user


	def user_info(self, token_id: str) -> dict:

		user = self.get_user_by_token_id(token_id)
		info = UserListSchema().dump(user)
		return dict(user=info)
			
		











		