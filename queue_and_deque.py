from flask import Blueprint, render_template, request, session

queue_and_deque_bp = Blueprint("queue_and_deque_bp", __name__)

@queue_and_deque_bp.route("/queueanddeque", methods=["GET", "POST"])
def queue_de_que_page():
    queue_values = session.get("queue_values", [])
    deque_values = session.get("deque_values", [])
    message = ""
    message_type = "success"

    if request.method == "POST":
        action = request.form.get("action", "")
        value = request.form.get("value", "").strip()

        queue = create_queue(queue_values)
        deque = create_deque(deque_values)

        if action == "enqueue":
            if value:
                queue.enqueue(value)
                message = f"Successfully enqueued: {value}"
            else:
                message = "Please enter a value."
                message_type = "error"

        elif action == "dequeue":
            removed = queue.dequeue()
            if removed is None:
                message = "Queue is empty."
                message_type = "error"
            else:
                message = f"Successfully dequeued: {removed}"

        elif action == "clear_queue":
            queue = LinkedQueue()
            message = "Queue cleared successfully."

        elif action == "add_front":
            if value:
                deque.add_front(value)
                message = f"Added to front: {value}"
            else:
                message = "Please enter a front value."
                message_type = "error"

        elif action == "add_rear":
            if value:
                deque.add_rear(value)
                message = f"Added to rear: {value}"
            else:
                message = "Please enter a rear value."
                message_type = "error"

        elif action == "remove_front":
            removed = deque.remove_front()
            if removed is None:
                message = "Deque is empty."
                message_type = "error"
            else:
                message = f"Removed from front: {removed}"

        elif action == "remove_rear":
            removed = deque.remove_rear()
            if removed is None:
                message = "Deque is empty."
                message_type = "error"
            else:
                message = f"Removed from rear: {removed}"

        elif action == "clear_deque":
            deque = LinkedDeque()
            message = "Deque cleared successfully."

        queue_values = queue.display()
        deque_values = deque.display()
        session["queue_values"] = queue_values
        session["deque_values"] = deque_values
        session.modified = True

    return render_template(
        "queue_de_que.html",
        queue_values=queue_values,
        deque_values=deque_values,
        message=message,
        message_type=message_type
    )

class QueueNode:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedQueue:
    def __init__(self):
        self.front = None
        self.rear = None
        self.size = 0

    def enqueue(self, data):
        new_node = QueueNode(data)
        if self.rear is None:
            self.front = new_node
            self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
        self.size += 1

    def dequeue(self):
        if self.front is None:
            return None
        removed = self.front.data
        self.front = self.front.next
        self.size -= 1
        if self.front is None:
            self.rear = None
        return removed

    def display(self):
        values = []
        current = self.front
        while current is not None:
            values.append(current.data)
            current = current.next
        return values

class DequeNode:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class LinkedDeque:
    def __init__(self):
        self.front = None
        self.rear = None
        self.size = 0

    def add_front(self, data):
        new_node = DequeNode(data)
        if self.front is None:
            self.front = self.rear = new_node
        else:
            new_node.next = self.front
            self.front.prev = new_node
            self.front = new_node
        self.size += 1

    def add_rear(self, data):
        new_node = DequeNode(data)
        if self.rear is None:
            self.front = self.rear = new_node
        else:
            new_node.prev = self.rear
            self.rear.next = new_node
            self.rear = new_node
        self.size += 1

    def remove_front(self):
        if self.front is None:
            return None
        removed = self.front.data
        self.front = self.front.next
        self.size -= 1
        if self.front is None:
            self.rear = None
        else:
            self.front.prev = None
        return removed

    def remove_rear(self):
        if self.rear is None:
            return None
        removed = self.rear.data
        self.rear = self.rear.prev
        self.size -= 1
        if self.rear is None:
            self.front = None
        else:
            self.rear.next = None
        return removed

    def display(self):
        values = []
        current = self.front
        while current is not None:
            values.append(current.data)
            current = current.next
        return values

def create_queue(values):
    queue = LinkedQueue()
    for value in values:
        queue.enqueue(value)
    return queue

def create_deque(values):
    deque = LinkedDeque()
    for value in values:
        deque.add_rear(value)
    return deque