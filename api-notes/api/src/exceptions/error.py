class BaseError(Exception):
	
	def __init__(self, data, message, previous=None):

		self.data = data
		self.message = message
		self.previous = previous


class InvalidParametersError(BaseError):

	def __init__(self, data, errors, message, previous=None, status=400):

		super().__init__(data, message, previous)
		self.status = status
		self.errors = errors


class UserExistsError(BaseError):

	def __init__(self, data, errors, message, previous=None, status=412):

		super().__init__(data, message, previous)
		self.status = status
		self.errors = errors

class UserNotFoundError(BaseError):

	def __init__(self, data, errors, message, previous=None, status=404):

		super().__init__(data, message, previous)
		self.status = status
		self.errors = errors


class AuthenticationError(BaseError):

	def __init__(self, data, errors, message, previous=None, status=401):

		super().__init__(data, message, previous)
		self.status = status
		self.errors = errors


class InvalidTokenError(BaseError):

	def __init__(self, data, errors, message, previous=None, status=401):

		super().__init__(data, message, previous)
		self.status = status
		self.errors = errors