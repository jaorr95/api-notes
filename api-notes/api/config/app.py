from bottle import Bottle
from peewee import SqliteDatabase

from api.src.common.utils import Singleton


class App(object, metaclass=Singleton):


	def __init__(self):

		self.app = Bottle()
		self.db = SqliteDatabase('aimo.db')