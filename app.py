from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = 'lab4-secret-key'

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        curr = self.head
        while curr.next:
            curr = curr.next
        curr.next = new_node

    def prepend(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert_at_index(self, index, data):
        if index == 0:
            self.prepend(data)
            return True
        curr = self.head
        count = 0
        while curr and count < index - 1:
            curr = curr.next
            count += 1
        if not curr:
            return False
        new_node = Node(data)
        new_node.next = curr.next
        curr.next = new_node
        return True

    def search_value(self, target):
        curr = self.head
        pos = 0
        while curr:
            if curr.data == target:
                return pos
            curr = curr.next
            pos += 1
        return -1

    def delete_value(self, target):
        curr = self.head
        if curr and curr.data == target:
            self.head = curr.next
            return True
        prev = None
        while curr and curr.data != target:
            prev = curr
            curr = curr.next
        if not curr:
            return False
        prev.next = curr.next
        return True

    def pop_head(self):
        if not self.head:
            return False
        self.head = self.head.next
        return True

    def pop_tail(self):
        if not self.head:
            return False
        if not self.head.next:
            self.head = None
            return True
        curr = self.head
        while curr.next.next:
            curr = curr.next
        curr.next = None
        return True

    def clear(self):
        self.head = None

    def get_all(self):
        items = []
        curr = self.head
        while curr:
            items.append(curr.data)
            curr = curr.next
        return items
# =======================================


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
    if 'linked_data' not in session:
        session['linked_data'] = []

    status_msg = ""
    items = session['linked_data']

    if request.method == 'POST':
        action = request.form.get('action')
        node_val = request.form.get('node_val', '').strip()
        index_str = request.form.get('index_val', '').strip()

        ll = LinkedList()
        for d in items:
            ll.append(d)

        if action == 'append':
            if node_val:
                ll.append(node_val)
                status_msg = f"Added '{node_val}' to the end."
            else:
                status_msg = "Please enter a node value."

        elif action == 'prepend':
            if node_val:
                ll.prepend(node_val)
                status_msg = f"Added '{node_val}' to the start."
            else:
                status_msg = "Please enter a node value."

        elif action == 'insert_at_index':
            if not node_val or not index_str:
                status_msg = "Enter both value and index."
            else:
                try:
                    idx = int(index_str)
                    if ll.insert_at_index(idx, node_val):
                        status_msg = f"Inserted '{node_val}' at index {idx}."
                    else:
                        status_msg = f"Index {idx} is out of range."
                except ValueError:
                    status_msg = "Index must be a number."

        elif action == 'search':
            if node_val:
                pos = ll.search_value(node_val)
                if pos != -1:
                    status_msg = f"Found '{node_val}' at index {pos}."
                else:
                    status_msg = f" '{node_val}' not found in list."
            else:
                status_msg = "Enter value to search."

        elif action == 'delete_value':
            if node_val:
                if ll.delete_value(node_val):
                    status_msg = f"Deleted '{node_val}'."
                else:
                    status_msg = f" '{node_val}' not found."
            else:
                status_msg = "Enter value to delete."

        elif action == 'pop_head':
            if ll.pop_head():
                status_msg = "Deleted first node (Pop Head)."
            else:
                status_msg = "List is empty."

        elif action == 'pop_tail':
            if ll.pop_tail():
                status_msg = "Deleted last node (Pop Tail)."
            else:
                status_msg = "List is empty."

        elif action == 'clear':
            ll.clear()
            status_msg = "Cleared the entire linked list."

        session['linked_data'] = ll.get_all()
        items = session['linked_data']

    total_nodes = len(items)
    return render_template('linklist.html', items=items, status_msg=status_msg, total_nodes=total_nodes)


if __name__ == '__main__':
    app.run(debug=True)