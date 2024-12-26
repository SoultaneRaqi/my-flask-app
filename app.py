# imports
from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime




# my app
app = Flask(__name__)
Scss(app, static_dir='static')


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)



# data class
class MYtASK(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Task(id={self.id}, content={self.Content}, created_at={self.created_at})"
  
with app.app_context():
  db.create_all()

# routes to webpages

#home page
@app.route("/" , methods=["POST" , "GET"])
def index():
  #add tasks
  if request.method == "POST":
    current_task = request.form["content"]
    new_task = MYtASK(content=current_task)
    try:
      db.session.add(new_task)
      db.session.commit()
      return redirect("/")
    except Exception as e:
      print(f"Error: {e}")
      return f"Error: {e}"
  #see all current tasks
  else:
    tasks = MYtASK.query.order_by(MYtASK.created_at).all()
    return render_template("index.html", tasks=tasks)

# delete task
@app.route( "/delete/<int:id>" )
def delete(id: int):
  delete_task = MYtASK.query.get_or_404(id)
  try:
    db.session.delete(delete_task)
    db.session.commit()
    return redirect("/")
  except Exception as e:
    return f"Error: {e}"




# edit task
@app.route( "/edit/<int:id>" , methods=["POST" , "GET"] )
def edit(id: int):
  task = MYtASK.query.get_or_404(id)
  if request.method == "POST":
    task.content = request.form["content"]
    try:
      db.session.commit()
      return redirect("/")
    except Exception as e:
      return f"Error: {e}"
  else:
    return render_template("edit.html", task=task)







if __name__ == "__main__":
  app.run(debug=True)
  



