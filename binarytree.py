
import math
from flask import Blueprint, render_template, request, session

binary_tree_bp = Blueprint("binary_tree", __name__)

MAX_NODES = 15
MAX_VALUE_LENGTH = 12


def value_key(value):
    value = str(value).strip()

    if value.lstrip("-").isdigit():
        return (0, int(value), "")

    return (1, value.casefold(), "")


class Node:
    def __init__(self, value, left=None, right=None):
        self.value = str(value)
        self.left = left
        self.right = right


class BinaryTree:
    def __init__(self, root_value=None):
        self.root = Node(root_value) if root_value is not None else None

    def insert(self, value):
        self.root = self._insert(self.root, value)

    def _insert(self, root, value):
        if root is None:
            return Node(value)

        if value_key(value) < value_key(root.value):
            root.left = self._insert(root.left, value)
        elif value_key(value) > value_key(root.value):
            root.right = self._insert(root.right, value)

        return root

    def search(self, root, key):
        if root is None:
            return False

        if value_key(root.value) == value_key(key):
            return True

        if value_key(key) < value_key(root.value):
            return self.search(root.left, key)

        return self.search(root.right, key)

    def delete_node(self, root, key):
        if root is None:
            return None

        if value_key(key) < value_key(root.value):
            root.left = self.delete_node(root.left, key)

        elif value_key(key) > value_key(root.value):
            root.right = self.delete_node(root.right, key)

        else:
            if root.left is None:
                return root.right

            if root.right is None:
                return root.left

            successor = root.right

            while successor.left:
                successor = successor.left

            root.value = successor.value
            root.right = self.delete_node(root.right, successor.value)

        return root

    def preorder_values(self, root):
        if root is None:
            return []

        return (
            [root.value]
            + self.preorder_values(root.left)
            + self.preorder_values(root.right)
        )

    def inorder_values(self, root):
        if root is None:
            return []

        return (
            self.inorder_values(root.left)
            + [root.value]
            + self.inorder_values(root.right)
        )

    def postorder_values(self, root):
        if root is None:
            return []

        return (
            self.postorder_values(root.left)
            + self.postorder_values(root.right)
            + [root.value]
        )

    def height(self, root):
        if root is None:
            return 0

        return 1 + max(
            self.height(root.left),
            self.height(root.right)
        )


def build_tree(values):
    tree = BinaryTree()

    for value in values:
        tree.insert(str(value))

    return tree


def create_diagram(tree):
    nodes = []
    edges = []

    count = len(tree.inorder_values(tree.root))

    if count == 0:
        return nodes, edges, 700, 300

    width = max(700, count * 105 + 120)
    height = max(300, tree.height(tree.root) * 115 + 100)

    positions = {}

    def assign_x(node):
        if node is None:
            return

        assign_x(node.left)

        positions[id(node)] = (
            70
            + len(positions)
            * ((width - 140) / max(1, count - 1))
        )

        assign_x(node.right)

    assign_x(tree.root)

    def walk(node, level=0, parent=None):
        if node is None:
            return

        x = positions[id(node)]
        y = 70 + level * 115

        if parent is not None:
            px, py = parent

            dx = x - px
            dy = y - py
            distance = math.hypot(dx, dy)

            if distance > 0:
                ux = dx / distance
                uy = dy / distance

                edges.append({
                    "x1": px + ux * 34,
                    "y1": py + uy * 34,
                    "x2": x - ux * 36,
                    "y2": y - uy * 36
                })

        nodes.append({
            "value": node.value,
            "x": x,
            "y": y,
            "root": level == 0
        })

        walk(node.left, level + 1, (x, y))
        walk(node.right, level + 1, (x, y))

    walk(tree.root)

    return nodes, edges, width, height


@binary_tree_bp.route("/binarytree", methods=["GET", "POST"])
def binarytree_page():
    values = session.get("binary_tree_values_v3", [])
    tree = build_tree(values)

    message = "Your Binary Search Tree is ready."
    message_type = "info"
    highlighted = None

    if request.method == "POST":
        action = request.form.get("action", "")
        raw_value = request.form.get("value", "").strip()

        if action == "clear":
            tree = BinaryTree()
            message = "All nodes have been cleared."
            message_type = "success"

        elif action in ("insert", "search", "delete"):

            if not raw_value:
                message = "Please enter a node value."
                message_type = "error"

            elif len(raw_value) > MAX_VALUE_LENGTH:
                message = "Maximum of 12 characters per node."
                message_type = "error"

            else:
                value = raw_value

                if action == "insert":
                    if tree.search(tree.root, value):
                        message = f"Node {value} already exists."
                        message_type = "error"

                    elif len(tree.inorder_values(tree.root)) >= MAX_NODES:
                        message = "Maximum of 15 nodes allowed."
                        message_type = "error"

                    else:
                        tree.insert(value)
                        highlighted = value
                        message = f"Node {value} inserted successfully."
                        message_type = "success"

                elif action == "search":
                    if tree.search(tree.root, value):
                        highlighted = value
                        message = f"Node {value} was found in the tree."
                        message_type = "success"
                    else:
                        message = f"Node {value} was not found."
                        message_type = "error"

                elif action == "delete":
                    if tree.search(tree.root, value):
                        tree.root = tree.delete_node(tree.root, value)
                        message = f"Node {value} deleted successfully."
                        message_type = "success"
                    else:
                        message = f"Node {value} does not exist."
                        message_type = "error"

        session["binary_tree_values_v3"] = tree.preorder_values(tree.root)

    nodes, edges, width, height = create_diagram(tree)

    preorder_values = tree.preorder_values(tree.root)
    inorder_values = tree.inorder_values(tree.root)
    postorder_values = tree.postorder_values(tree.root)

    preorder = " → ".join(map(str, preorder_values)) if preorder_values else "Empty"
    inorder = " → ".join(map(str, inorder_values)) if inorder_values else "Empty"
    postorder = " → ".join(map(str, postorder_values)) if postorder_values else "Empty"

    return render_template(
        "binarytree.html",
        nodes=nodes,
        edges=edges,
        diagram_width=width,
        diagram_height=height,
        node_count=len(nodes),
        tree_height=tree.height(tree.root),
        root_value=tree.root.value if tree.root else None,
        preorder=preorder,
        inorder=inorder,
        postorder=postorder,
        message=message,
        message_type=message_type,
        highlighted=highlighted
    )
