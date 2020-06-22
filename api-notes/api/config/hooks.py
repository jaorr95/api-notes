from api.config.app import App
from api.src.models.user import User
from api.src.models.note import Note
from api.src.models.session import Session

app = App()

@app.app.hook('before_request')
def init_db():
	app.db.connect()
	app.db.create_tables([User, Note, Session])


@app.app.hook('after_request')
def close_db():
	app.db.close()