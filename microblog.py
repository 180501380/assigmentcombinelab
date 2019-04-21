from app import app, db, cli            #import 左啲簡化command先可以執行
from app.models import User, Post


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}
