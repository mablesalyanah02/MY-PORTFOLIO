from flask import Blueprint, render_template, request, session
from stack import Stack, to_list

pushpoppeek_bp = Blueprint('pushpoppeek', __name__)


@pushpoppeek_bp.route('/stack', methods=['GET', 'POST'])
def stack_page():
    if 'stack_items' not in session:
        session['stack_items'] = []

    stack = Stack()

    for item in reversed(session['stack_items']):
        stack.push(item)

    message = ''

    if request.method == 'POST':
        action = request.form.get('action')
        value = request.form.get('value', '').strip()

        if action == 'push':
            if value:
                stack.push(value)
                message = f'Pushed: {value}'
            else:
                message = 'Please enter a value.'

        elif action == 'pop':
            removed = stack.pop()

            if removed is not None:
                message = f'Popped: {removed}'
            else:
                message = 'Stack is empty.'

        elif action == 'peek':
            top_value = stack.peek()

            if top_value is not None:
                message = f'Top item: {top_value}'
            else:
                message = 'Stack is empty.'

        session['stack_items'] = to_list(stack)

    return render_template(
        'infixpostfix.html',
        infix='',
        postfix_result=None,
        items=to_list(stack),
        message=message
    )
