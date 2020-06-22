class Message(object):

	MESSAGE_SUCCESSFULL = "Request succesfull"
	MESSAGE_INVALID_PARAMETERS = "Invalid parameters"
	MESSAGE_UNIQUE_PARAMETERS = "Parameter must be unique"
	MESSAGE_INVALID_CREDENTIALS = "Invalid credentials"
	MESSAGE_INVALID_TOKEN = "Invalid token"
	MESSAGE_USER_NOT_FOUND = "User does not exist."


class RegexExpression(object):

	PASSWORD = '^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.[!@#\\$%\\^&\\*\\.]*).{6,20}$'


class Constants(object):

	MIN_LENGTH_NAME = 2
	MAX_LENGTH_NAME = 100

	AUTHORIZATION_HEADER = "Authorization"

	JWT_EXPIRATION_TIME = 1440 #minutes

	FORMAT_DATETIME = '%d-%m-%Y %H:%M:%S'
