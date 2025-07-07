from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Dummy user
users = {"admin": "password"}

# Dummy claims DB
claims = {}

@app.route('/')
def index():
    if 'user' in session:
        return render_template("home.html", user=session['user'])
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        if uname in users and users[uname] == pwd:
            session['user'] = uname
            return redirect('/')
        else:
            return "Invalid credentials!"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

@app.route('/insurance/<type>')
def insurance(type):
    if 'user' not in session:
        return redirect('/login')
    return render_template('insurance.html', insurance_type=type)

@app.route('/claim', methods=['GET', 'POST'])
def claim():
    if 'user' not in session:
        return redirect('/login')
    if request.method == 'POST':
        claim_id = len(claims) + 1
        name = request.form['name']
        insurance_type = request.form['insurance_type']
        amount = request.form['amount']
        claims[claim_id] = {'name': name, 'type': insurance_type, 'amount': amount, 'status': 'Pending'}
        return f"Claim submitted! Your Claim ID is {claim_id}"
    return render_template("claim.html")

@app.route('/status', methods=['GET', 'POST'])
def status():
    if 'user' not in session:
        return redirect('/login')
    if request.method == 'POST':
        claim_id = int(request.form['claim_id'])
        if claim_id in claims:
            return f"Status of Claim {claim_id}: {claims[claim_id]['status']}"
        else:
            return "Invalid Claim ID"
    return render_template("status.html")

@app.route('/premium', methods=['GET', 'POST'])
def premium():
    if 'user' not in session:
        return redirect('/login')
    premium_amount = None
    if request.method == 'POST':
        insurance_type = request.form['insurance_type']
        age = int(request.form['age'])
        base = 1000
        if insurance_type == 'health':
            premium_amount = base + (age * 10)
        elif insurance_type == 'car':
            premium_amount = base + 500
        elif insurance_type == 'bike':
            premium_amount = base + 200
    return render_template('premium.html', premium=premium_amount)

if __name__ == '__main__':
    app.run(debug=True)
