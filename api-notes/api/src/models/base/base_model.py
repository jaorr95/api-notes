from peewee import Model

from api.config.app import App

class BaseModel(Model):

	class Meta:
		database = App().db