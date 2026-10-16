from flask import Blueprint, render_template, request, session
area_bp = Blueprint('area', __name__)


@area_bp.route('/area', methods=['GET', 'POST'])
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
            session['base_val'] = request.form.get(
                'base', session['base_val']
            )
            session['height_val'] = request.form.get(
                'height', session['height_val']
            )

        elif 'calc_triangle' in request.form:
            b = float(request.form.get('base', 0))
            h = float(request.form.get('height', 0))
            session['base_val'] = b
            session['height_val'] = h
            session['triangle_result'] = 0.5 * b * h
            session['radius_val'] = request.form.get(
                'radius', session['radius_val']
            )

    return render_template(
        'area.html',
        circle_result=session['circle_result'],
        triangle_result=session['triangle_result'],
        radius=session['radius_val'],
        base=session['base_val'],
        height=session['height_val']
    )
