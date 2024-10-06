from datetime import datetime, timezone

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Date, Time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///task.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Task(db.Model):
    sno = Column(db.Integer, primary_key=True)
    title = Column(db.String(200), nullable=False)
    desc = Column(db.String(500), nullable=False)
    date_created = Column(Date, default=lambda: datetime.now(timezone.utc).date())
    time_created = Column(Time, default=lambda: datetime.now(timezone.utc).time())

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


@app.route('/', methods=['GET', 'POST'])
def create():
    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["desc"]
        if not title and not desc:
            all_task = Task.query.all()
            return render_template("error.html", all_task=all_task)
        task = Task(title=title, desc=desc)
        db.session.add(task)
        db.session.commit()

    all_task = Task.query.all()

    return render_template("index.html", all_task=all_task)


@app.route('/show/')
def show():
    all_task = Task.query.all()

    return render_template("show.html", all_task=all_task)


@app.route('/delete/<int:sno>')
def delete(sno):
    task = Task.query.filter_by(sno=sno).first()
    db.session.delete(task)
    db.session.commit()
    print("task deleted")

    return redirect("/")


@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["desc"]
        if not title and not desc:
            all_task = Task.query.all()
            return render_template("error.html", all_task=all_task)
        task = Task.query.filter_by(sno=sno).first()
        task.title = title
        task.desc = desc
        db.session.add(task)
        db.session.commit()

        return redirect("/")

    task = Task.query.filter_by(sno=sno).first()
    return render_template("update.html", task=task)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
