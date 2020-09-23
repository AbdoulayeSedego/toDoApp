from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////toDoApp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
class toDoApp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    complete = db.Column(db.Boolean)

@app.route('/')
def index():
    incomplete = toDoApp.query.filter_by(complete=False).all()
    complete = toDoApp.query.filter_by(complete=True).all()
    return render_template('index.html', incomplete=incomplete, complete=complete)

@app.route('/add', methods=['POST'])
def add():
    dbApp = toDoApp(text=request.form['todoitem'], complete=False)
    db.session.add(dbApp)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/complete/<id>')
def complete(id):
    dbApp = toDoApp.query.filter_by(id=int(id)).first()
    dbApp.complete = True
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/uncheck/<id>')
def uncheck(id):
    dbApp = toDoApp.query.filter_by(id=int(id)).first()
    dbApp.complete = False
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<id>')
def delete(id):
    dbApp = toDoApp.query.filter_by(id=int(id)).first()
    db.session.delete(dbApp)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
