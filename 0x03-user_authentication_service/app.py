from flask import Flask, request, jsonify, abort
from auth import Auth

app = Flask(__name__)
AUTH = Auth()

# POST /sessions route to handle login
@app.route('/sessions', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            AUTH.valid_login(email, password)
            session_id = AUTH.create_session(email)
            response = jsonify({"email": email, "message": "logged in"})
            response.set_cookie('session_id', session_id)
            return response, 200
        except ValueError:
            abort(401)

# DELETE /sessions route to handle logout
@app.route('/sessions', methods=['DELETE'])
def logout():
    if request.method == 'DELETE':
        session_id = request.cookies.get('session_id')
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user.id)
            return redirect('/')
        else:
            abort(403)

# GET /profile route to fetch user profile
@app.route('/profile', methods=['GET'])
def profile():
    if request.method == 'GET':
        session_id = request.cookies.get('session_id')
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            return jsonify({"email": user.email}), 200
        else:
            abort(403)

# GET / route to return a welcome message
@app.route('/')
def welcome():
    return jsonify({"message": "Bienvenue"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

@app.route('/reset_password', methods=['POST'])
def reset_password():
    email = request.form.get('email')

    try:
        reset_token = auth.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError:
        return "Email not registered", 403
    
@app.route('/reset_password', methods=['PUT'])
def update_password():
    try:
        email = request.form.get('email')
        reset_token = request.form.get('reset_token')
        new_password = request.form.get('new_password')

        AUTH.update_password(reset_token, new_password)

        return jsonify({
            "email": email,
            "message": "Password updated"
        }), 200
    except ValueError:
        abort(403)