from flask import Flask, render_template

app = Flask(__name__)

# Home page route
@app.route('/')
def home():
    # You can add logic to determine what to show on the home page.
    return render_template('home.html', title='Home')

# Institution page route
@app.route('/institution')
def institution():
    return render_template('institution.html', title='Institution History')

# Structure page route
@app.route('/structure')
def structure():
    # Replace 'structure.html' with the actual name of your template for the structure page.
    return render_template('structure.html', title='Board and Management Structure')

# Administration page route
@app.route('/administration')
def administration():
    # Replace 'administration.html' with the actual name of your template for the administration page.
    return render_template('administration.html', title='Administrative Structure')

# Scholarship page route
@app.route('/scholarship')
def scholarship():
    # Replace 'scholarship.html' with the actual name of your template for the scholarship page.
    return render_template('scholarship.html', title='Scholarship Terms')

# Main function to run the app
if __name__ == '__main__':
    app.run(debug=True)
