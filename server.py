
from flask import Flask, render_template, request, redirect
from mysqlconnection import connectToMySQL    # import the function that will return an instance of a connection
app = Flask(__name__)
@app.route("/")
def index():
    mysql = connectToMySQL('Users_rest_api')	        # call the function, passing in the name of our db
    users = mysql.query_db('SELECT * FROM Users;')  # call the query_db function, pass in the query as a string
    return render_template("index.html", users = users)

@app.route("/create_user", methods=['POST'])
def add_friend_to_db():
    print(request.form)
    mysql = connectToMySQL('Users_rest_api')
    query = "INSERT into Users (first_name, last_name, email, created_at, updated_at) VALUES (%(fn)s, %(ln)s, %(em)s, NOW(), NOW());"
    data = {
        "fn": request.form["first_name"],
        "ln": request.form["last_name"],
        "em": request.form["email"]
    }
    new_friend_id = mysql.query_db(query, data)
    return redirect("/")

@app.route("/users/<user_id>")
def show_specific_user(user_id):
    mysql = connectToMySQL('Users_rest_api')
    users = mysql.query_db(f"SELECT first_name, last_name, email, created_at FROM Users WHERE Users.id = {user_id};")
  

    return render_template('show_user.html', users = users)


@app.route("/users/<user_id>/edit")
def show_update_specific_user(user_id):
    mysql = connectToMySQL('Users_rest_api')
    users = mysql.query_db(
        f"SELECT * FROM Users WHERE Users.id = {user_id};")
    print(users)

    return render_template('update_user.html', users = users)

@app.route("/update_user", methods=["POST"])
def update_specific_user():
    mysql = connectToMySQL('Users_rest_api')
    query = "UPDATE Users SET first_name = %(fn)s, last_name = %(ln)s, email = %(em)s, updated_at = NOW() WHERE Users.id = %(id)s;"
    data = {
      'fn': request.form["first_name"],
      'ln': request.form["last_name"],
      'em': request.form["email"],
      'id': request.form["id"]
    }
    print(data)
    update_friend_id = mysql.query_db(query, data)
    return redirect("/")

@app.route("/users/<user_id>/destroy")
def delete_specific_record(user_id):
    mysql = connectToMySQL('Users_rest_api')
    query = "DELETE FROM Users WHERE Users.id = %(id)s"
    data = { 'id': user_id }
    delete_user_id = mysql.query_db(query, data)
    return redirect("/")
    


@app.route("/users/new")
def display_add_user_page():
    print('Got here!')

    return render_template("create_user.html")


   

if __name__ == "__main__":
    app.run(debug=True)
