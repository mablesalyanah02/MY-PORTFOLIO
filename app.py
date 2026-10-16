from flask import Flask, render_template, request
from linklist import linked_bp
from stack import stack_bp
from area import area_bp
from pushpoppeek import pushpoppeek_bp

app = Flask(__name__)
app.secret_key = 'lab4-secret-key'

app.register_blueprint(linked_bp)
app.register_blueprint(stack_bp)
app.register_blueprint(area_bp)
app.register_blueprint(pushpoppeek_bp)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/works')
def works():
    return render_template('works.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/touppercase', methods=['GET', 'POST'])
def touppercase():
    result = ""
    if request.method == 'POST':
        input_text = request.form.get('input_text', '')
        result = input_text.upper()
    return render_template('touppercase.html', result=result)

if __name__ == '__main__':
    app.run(debug=True,)