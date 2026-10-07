from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = 'lab4-secret-key'

@app.route('/')
def home():
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

@app.route('/area', methods=['GET', 'POST'])
def area():
    if 'circle_result' not in session:
        session['circle_result'] = None
    if 'triangle_result' not in session:
        session['triangle_result'] = None
    if 'radius_val' not in session:
        session['radius_val'] = ''
    if 'base_val' not in session:
        session['base_val'] = ''
    if 'height_val' not in session:
        session['height_val'] = ''

    if request.method == 'POST':
        if 'clear_all' in request.form:
            session['circle_result'] = None
            session['triangle_result'] = None
            session['radius_val'] = ''
            session['base_val'] = ''
            session['height_val'] = ''

        elif 'calc_circle' in request.form:
            r = float(request.form.get('radius', 0))
            session['radius_val'] = r
            session['circle_result'] = 3.1415926535 * r * r
            session['base_val'] = request.form.get('base', session['base_val'])
            session['height_val'] = request.form.get('height', session['height_val'])

        elif 'calc_triangle' in request.form:
            b = float(request.form.get('base', 0))
            h = float(request.form.get('height', 0))
            session['base_val'] = b
            session['height_val'] = h
            session['triangle_result'] = 0.5 * b * h
            session['radius_val'] = request.form.get('radius', session['radius_val'])

    return render_template(
        'area.html',
        circle_result=session['circle_result'],
        triangle_result=session['triangle_result'],
        radius=session['radius_val'],
        base=session['base_val'],
        height=session['height_val']
    )

@app.route('/linklist', methods=['GET', 'POST'])
def linklist():
    if 'mylist' not in session:
        session['mylist'] = []

    if request.method == 'POST':
        action = request.form.get('action')
        val = request.form.get('value', '').strip()
        mylist = session['mylist']

        if action == 'add' and val:
            mylist.append(val)
        elif action == 'delete' and val in mylist:
            mylist.remove(val)
        elif action == 'clear':
            mylist = []

        session['mylist'] = mylist

    return render_template('linklist.html', items=session['mylist'])

if __name__ == '__main__':
    app.run(debug=True)