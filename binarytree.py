from flask import Blueprint, render_template, request, session, redirect, url_for

binary_tree_bp = Blueprint("binary_tree", __name__)


class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
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

        if value < root.value:
            root.left = self._insert(root.left, value)
        elif value > root.value:
            root.right = self._insert(root.right, value)

        return root

    def search(self, root, key):
        if root is None:
            return False

        if root.value == key:
            return True

        if key < root.value:
            return self.search(root.left, key)

        return self.search(root.right, key)

    def post_traversal(self, start, traversal):
        if start:
            traversal = self.post_traversal(start.left, traversal)
            traversal = self.post_traversal(start.right, traversal)
            traversal += str(start.value) + " "
        return traversal

    def postorder_traversal(self, start, traversal):
        return self.post_traversal(start, traversal)

    def delete_node(self, root, key):
        if root is None:
            return None

        if key < root.value:
            root.left = self.delete_node(root.left, key)

        elif key > root.value:
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

    def inorder_values(self, root):
        if root is None:
            return []

        return (
            self.inorder_values(root.left)
            + [root.value]
            + self.inorder_values(root.right)
        )

    def preorder_values(self, root):
        if root is None:
            return []

        return (
            [root.value]
            + self.preorder_values(root.left)
            + self.preorder_values(root.right)
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
        tree.insert(value)

    return tree


def create_diagram(tree):
    nodes = []
    edges = []
    count = len(tree.inorder_values(tree.root))

    if count == 0:
        return nodes, edges, 700, 300

    width = max(700, count * 85 + 100)
    height = max(300, tree.height(tree.root) * 105 + 80)

    positions = {}

    def assign_x(node):
        if node is None:
            return

        assign_x(node.left)

        positions[id(node)] = 60 + len(positions) * (
            (width - 120) / max(1, count - 1)
        )

        assign_x(node.right)

    assign_x(tree.root)

    def walk(node, level=0, parent=None):
        if node is None:
            return

        x = positions[id(node)]
        y = 65 + level * 105

        if parent is not None:
            edges.append({
                "x1": parent[0],
                "y1": parent[1],
                "x2": x,
                "y2": y
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
    values = session.get("binary_tree_values", [])
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
            try:
                value = int(raw_value)

                if action == "insert":
                    if tree.search(tree.root, value):
                        message = f"Node {value} already exists."
                        message_type = "error"
                    elif len(tree.inorder_values(tree.root)) >= 15:
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

            except ValueError:
                message = "Please enter a valid integer."
                message_type = "error"

        session["binary_tree_values"] = tree.preorder_values(tree.root)

    nodes, edges, width, height = create_diagram(tree)

    postorder = tree.post_traversal(tree.root, "").strip()
    inorder = tree.inorder_traversal(tree.root, "").strip() if hasattr(
        tree, "inorder_traversal"
    ) else " → ".join(map(str, tree.inorder_values(tree.root)))

    return render_template(
        "binarytree.html",
        nodes=nodes,
        edges=edges,
        diagram_width=width,
        diagram_height=height,
        node_count=len(nodes),
        tree_height=tree.height(tree.root),
        root_value=tree.root.value if tree.root else None,
        postorder=" → ".join(postorder.split()) if postorder else "Empty",
        inorder=inorder,
        message=message,
        message_type=message_type,
        highlighted=highlighted
    )
