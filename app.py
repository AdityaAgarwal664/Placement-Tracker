from flask import Flask,render_template,request,redirect
#pip install flask-sqlalchemy, by python you use database
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///mytodo.db" 
app.config['SQLALCHEMY_DATABASE_MODIFICATIONS']=False
db=SQLAlchemy(app)


class Todo(db.Model):
    sno= db.Column(db.Integer,primary_key=True)
    title= db.Column(db.String(2000),nullable=False)
    desc= db.Column(db.String(500),nullable=False)
    date_created=db.Column(db.DateTime)

    def __repr__(self)->str:
        return f"{self.sno} - {self.title}"


@app.route('/',methods=["GET","POST"])
def hello_world():
    if request.method=='POST':
        title=request.form["title"]
        desc=request.form["desc"]
        todo=Todo(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()
    return redirect("/show")

@app.route("/<proname>")
def products(proname):
    return f"This won't work to write {proname} in url, sorry baby."

@app.route("/show")
def show():
    allTodo=Todo.query.all()
    #print(allTodo)
    return render_template("index.html",allTodo=allTodo)

@app.route("/delete/<int:sno>")
def delete(sno):
    allTodo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(allTodo)
    db.session.commit()
    return redirect("/show")


    
if __name__=="__main__":
    app.run(debug=True,port=8000)