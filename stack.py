from flask import Blueprint, render_template, request
stack_bp = Blueprint('stack', __name__)


@stack_bp.route('/infixpostfix', methods=['GET', 'POST'])
def infixpostfix():
    infix = ''
    postfix_result = None

    if request.method == 'POST':
        if 'clear_infix' in request.form:
            infix = ''
            postfix_result = None
        else:
            infix = request.form.get('infix_expr', '').strip()
            if infix:
                postfix_result = infix_to_postfix(infix)

    return render_template(
        'infixpostfix.html',
        infix=infix,
        postfix_result=postfix_result
    )


def infix_to_postfix(expr):
    precedence = {'^': 3, '*': 2, '/': 2, '+': 1, '-': 1}
    stack = []
    output = []

    expr = expr.replace(" ", "")

    for token in expr:
        if token.isalnum():
            output.append(token)

        elif token == '(':
            stack.append(token)

        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())

            if not stack:
                return "Error - Mismatched Parenthesis"

            stack.pop()

        else:
            if token not in precedence:
                return f"Error - Unknown Character '{token}'"

            while (
                stack
                and stack[-1] != '('
                and precedence[stack[-1]] >= precedence[token]
            ):
                output.append(stack.pop())

            stack.append(token)

    while stack:
        item = stack.pop()

        if item == '(':
            return "Error: Mismatched Parenthesis"

        output.append(item)

    return ''.join(output)


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class Stack:
    def __init__(self):
        self.top = None

    def push(self, data):
        new_node = Node(data)
        new_node.next = self.top
        self.top = new_node

    def pop(self):
        if self.top is None:
            return None

        data = self.top.data
        self.top = self.top.next
        return data

    def peek(self):
        if self.top is None:
            return None

        return self.top.data


def to_list(stack):
    items = []
    node = stack.top

    while node:
        items.append(node.data)
        node = node.next

    return items

