from flask import Flask, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cats_notes.db'
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["10 per minute", "1 per second"],
    storage_uri="memory://",
    strategy="fixed-window"
)


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
db.init_app(app)

migrate = Migrate(app, db)
migrate.init_app(app, db)


class Notes(db.Model):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    note: Mapped[str] = mapped_column(Text, nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/notes')
def notes():
    note_list = Notes.query.order_by(Notes.id).limit(6).all()
    return render_template('notes.html', note_list=note_list)


@app.route('/notes/<index>')
def specific_note(index: int):
    note = Notes.query.get(index)
    if note is None:
        return abort(404)
    if note.id == 31:
        return render_template(f'specific_note_{index}.html', note=note)
    if note.id == 419:
        return render_template(f'specific_note_{index}.html', note=note)
    if note.id == 2030:
        return render_template(f'specific_note_{index}.html', note=note)
    if note.id == 1421:
        return render_template(f'specific_note_{index}.html', note=note)
    if note.id == 8859:
        return render_template(f'specific_note_{index}.html', note=note)
    if note.id == 1041:
        return render_template(f'specific_note_{index}.html', note=note)
    if note.id == 2495:
        return render_template(f'specific_note_{index}.html', note=note)
    if note.id == 1350:
        return render_template(f'specific_note_{index}.html', note=note)
    if note.id == 2844:
        return render_template(f'specific_note_{index}.html')
    if note.id == 5194:
        return render_template(f'specific_note_{index}.html')
    return render_template('specific_note.html', note=note)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5690, debug=True)
