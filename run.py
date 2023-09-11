"""Flask CLI/точка входа в приложение.""" 
import os

from jwt_authentication import create_app, db

app = create_app(os.getenv("FLASK_ENV", "development"))


@app.shell_context_processor
def shell():
    return {"db" : db}
