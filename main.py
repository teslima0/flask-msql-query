from flask import Flask, jsonify,request
import mysql.connector

app = Flask(__name__)

# Set up database connection
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="mydatabase"
)

# Create cursor object
mycursor = mydb.cursor()
mycursor.execute("""CREATE TABLE IF NOT EXISTS  register (
  id INT NOT NULL AUTO_INCREMENT,
  username VARCHAR(50) NOT NULL,
  password VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
)""")

# Define endpoint to retrieve a single user by ID
@app.route('/userss/<int:user_id>', methods=['GET'])
def read_user(user_id):
    # Execute SQL query to retrieve user with matching ID
    sql = "SELECT * FROM users WHERE id = %s"
    val = (user_id,)
    mycursor.execute(sql, val)
    row = mycursor.fetchone()

    # Check if user was found
    if not row:
        return jsonify({'error': 'User not found'}), 404

    # Convert SQL result to dictionary
    user = {'id': row[0], 'username': row[1], 'email': row[2]}

    # Return user data as JSON response
    return jsonify(user)

# Define endpoint to retrieve all users from database
@app.route('/usersC', methods=['GET'])
def read_users():
    # Execute SQL query to retrieve all users
    mycursor.execute("SELECT * FROM users")
    rows = mycursor.fetchall()

    # Convert SQL results to list of dictionaries
    users = []
    for row in rows:
        user = {'id': row[0], 'username': row[1], 'email': row[2]}
        users.append(user)

    # Return list of users as JSON response
    return jsonify(users)

# Define endpoint to delete a user by ID
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    # Execute SQL query to delete user with matching ID
    sql = "DELETE FROM register WHERE id = %s "
    val = (id,)
    mycursor.execute(sql, val)
    mydb.commit()

    # Return success message
    message = {'status': 'success', 'message': 'User deleted from database'}
    return jsonify(message)
# Define endpoint to update a user by ID
@app.route('/useUpdate/<int:user_id>', methods=['PATCH'])
def updateUser(user_id):
    # Get user data from request
    update_data = request.json

    # Validate request data
    if 'username' not in update_data and 'email' not in update_data:
        return jsonify({'error': 'Invalid request data'}), 400
    if 'username' in update_data and 'email' in update_data:
        return jsonify({'error': 'Can only update either username or email, not both'}), 400

    # Execute SQL query to update user data
    if 'username' in update_data:
        sql = "UPDATE users SET username = %s WHERE id = %s"
        val = (update_data['username'], user_id)
    else:
        sql = "UPDATE users SET email = %s WHERE id = %s"
        val = (update_data['email'], user_id)
    mycursor.execute(sql, val)
    mydb.commit()

    # Return success message
    message = {'status': 'success', 'message': 'User updated in database'}
    return jsonify(message)

# Create
@app.route('/users', methods=['POST'])
def create_user():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    
    mycursor.execute('INSERT INTO register (username, email, password) VALUES (%s, %s, %s)', (username, email, password))
    mydb.commit()
    #
    # mycursor.close()
    return jsonify({'status': 'success', 'message': 'User created'})

@app.route('/use/<int:id>', methods=['PATCH'])
def user_update(id):
    #get user data from request
    user_data = request.json
    #validate request data
    if 'username' not in user_data and 'email' not in user_data:
        return jsonify({'error':'Invalid request data'}), 400
    # execute sql query to update user data
    sql="UPDATE register SET "
    val=[]
    if 'username' in user_data:
        sql += "username = %s, "
        val.append(user_data['username'])
    if 'email' in user_data:
        sql += "email = %s, "
        val.append(user_data['email'])
    sql= sql[:-2] + " WHERE id = %s"
    val.append(id)
    mycursor.execute(sql,val)
    mydb.commit()
    #return success message
    message={'status':'success','message':'user updated in database'}
    return jsonify(message)


@app.route('/users', methods=['GET'])
def get_all_users():
    mycursor.execute('select * from register')
   
    results = mycursor.fetchall()
    # Convert results to a list of dictionaries
    data = []
    for row in results:
        d = {}
        d['id'] = row[0]
        d['username'] = row[1]
        d['email'] = row[3]
        
        data.append(d)
    return jsonify(data)

#get user details
@app.route('/use/<int:id>', methods=['GET'])
def get_one_user(id):
    mycursor.execute('select * from register where id= %s',(id,) )
    data=mycursor.fetchone()
    if data:
        user = { 'username': data[1], 'email': data[3],'id': data[0]}
        return jsonify(user)
    else:
        return jsonify({'message': 'User not found'})
    
# Define endpoint to add user data to database
@app.route('/reg', methods=['POST'])
def register():
    # Get user data from request
   
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    

    # Execute SQL query to insert user data
    sql = "INSERT INTO register (username, email, password) VALUES ( %s, %s, %s)"
    val = ( username, email,password )
    mycursor.execute(sql, val)
    mydb.commit()

    # Return success message
    message = {'status': 'success', 'message': 'User added to database'}
    return jsonify(message)
# Define route to retrieve data from database
@app.route('/get_data')
def get_data():
    # Execute SQL query
    mycursor.execute("SELECT * FROM register")

    # Fetch all results
    results = mycursor.fetchall()

    # Convert results to a list of dictionaries
    data = []
    for row in results:
        d = {}
        d['id'] = row[0]
        d['username'] = row[1]
        d['email'] = row[3]
        data.append(d)

    # Return JSON response
    return jsonify(data)



@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    # Retrieve user from database
   
    mycursor.execute("SELECT * FROM register WHERE id = %s", (id,))
   
    data = mycursor.fetchone()
    #mycursor.close()
    
    # Return user details as JSON response
    if data:
        user = { 'username': data[1], 'email': data[3],'id': data[0]}
        return jsonify(user)
    else:
        return jsonify({'message': 'User not found'})

# Update user endpoint
@app.route('/users/<int:id>', methods=['PATCH'])
def update_user(id):
    
    username = request.json.get['username']
    email = request.json['email']
    #password = request.json['password']
     # Retrieve user from database

    # Validate request data
    #if not email:
        #return jsonify({'message': 'Email is required'}), 400
    #if not username:
        #return jsonify({'message': 'username is required'}), 400
    
    mycursor.execute("SELECT * FROM register WHERE id = %s", (id,))
   
    data = mycursor.fetchone()
    if data:
        mycursor.execute("UPDATE register SET username=%s, email=%s  WHERE id=%s",(username, email, id) )
        mydb.commit()
    
        return jsonify({'message': 'User updated successfully'})
    else:
        return jsonify({'message': 'User not found'})

if __name__ == '__main__':
    app.run(debug=True)