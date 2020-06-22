import sys
sys.path.append("./")

from bottle import request
from truckpad.bottle.cors import CorsPlugin, enable_cors

from api.config.app import App
from api.src.common.utils import Utils
from api.src.common.decorators import is_authenticated
from api.src.common.constants import  Message
from api.src.bo.user_bo import UserBo
from api.src.bo.note_bo import NoteBo
from api.src.exceptions.error import InvalidParametersError, UserExistsError
from api.src.exceptions.error import AuthenticationError, UserNotFoundError, InvalidTokenError



api = App().app

# Start your code here, good luck (: ...
@enable_cors
@api.route('/v1/user/signup', method='POST')
def user_signup():
	
	bo = UserBo()
	try:
		bo.create_user(request.json)

	except UserExistsError as e:
		return Utils.response(message=Message.MESSAGE_INVALID_PARAMETERS, errors=e.errors, status=e.status)
	
	except InvalidParametersError as e:
		return Utils.response(message=Message.MESSAGE_INVALID_PARAMETERS, errors=e.errors, status=e.status)
	
	return Utils.response(message=Message.MESSAGE_SUCCESSFULL, status=201)


@enable_cors
@api.route('/v1/user/login', method='POST')
def user_login():

	bo = UserBo()
	try:
		token_jwt = bo.login_user(request.json)

	except InvalidParametersError as e:
		return Utils.response(message=Message.MESSAGE_INVALID_PARAMETERS, errors=e.errors, status=e.status)

	except AuthenticationError as e:
		return Utils.response(message=Message.MESSAGE_INVALID_CREDENTIALS, errors=e.errors, status=e.status)

	return Utils.response(message=Message.MESSAGE_SUCCESSFULL, data=dict(token_id=token_jwt))


@enable_cors
@api.route('/v1/secure-user/user/logout', method='POST')
@is_authenticated
def user_logout():

	try:
		token_id = Utils.get_bearer_token(request.headers)
		bo = UserBo()
		bo.user_logout(token_id)

	except InvalidTokenError as e:
		return Utils.response(message=Message.MESSAGE_INVALID_TOKEN, errors=e.errors, status=e.status)

	return Utils.response(message=Message.MESSAGE_SUCCESSFULL)


@enable_cors
@api.route('/v1/secure-user/user/info')
@is_authenticated
def user_info():

	bo = UserBo()
	try:
		token_id = Utils.get_bearer_token(request.headers)
		user_info = bo.user_info(token_id)
	
	except InvalidTokenError as e:
		return Utils.response(message=Message.MESSAGE_INVALID_TOKEN, errors=e.errors, status=e.status)

	except UserNotFoundError as e:
		return Utils.response(message=Message.MESSAGE_USER_NOT_FOUND, errors=e.errors, status=e.status)

	return Utils.response(message=Message.MESSAGE_SUCCESSFULL, data=user_info)


@enable_cors
@api.route('/v1/secure-user/note/create', method='POST')
@is_authenticated
def note_create():

	try:
		token_id = Utils.get_bearer_token(request.headers)
		bo = NoteBo()
		note = bo.create_note(token_id, request.json)

	except InvalidTokenError as e:
		return Utils.response(message=Message.MESSAGE_INVALID_TOKEN, errors=e.errors, status=e.status)

	except InvalidParametersError as e:
		return Utils.response(message=Message.MESSAGE_INVALID_PARAMETERS, errors=e.errors, status=e.status)

	except UserNotFoundError as e:
		return Utils.response(message=Message.MESSAGE_USER_NOT_FOUND, errors=e.errors, status=e.status)

	
	return Utils.response(message=Message.MESSAGE_SUCCESSFULL, data=note, status=201)


@enable_cors
@api.route('/v1/secure-user/note/index', method='GET')
@is_authenticated
def note_index():

	try:
		token_id = Utils.get_bearer_token(request.headers)
		bo = NoteBo()
		notes = bo.get_notes_by_user(token_id)

	except InvalidTokenError as e:
		return Utils.response(message=Message.MESSAGE_INVALID_TOKEN, errors=e.errors, status=e.status)

	except UserNotFoundError as e:
		return Utils.response(message=Message.MESSAGE_USER_NOT_FOUND, errors=e.errors, status=e.status)

	return Utils.response(message=Message.MESSAGE_SUCCESSFULL, data=notes)


if __name__ == '__main__':
	import api.config.hooks as hooks # lo importo para que se carguen los hooks en bottle
	api.install(CorsPlugin(origins=['*']))
	api.run(host='0.0.0.0', port=8000)