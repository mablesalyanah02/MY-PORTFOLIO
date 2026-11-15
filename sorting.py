
from flask import Blueprint, render_template, request, session, redirect, url_for
import random

sorting_bp = Blueprint("sorting", __name__)

DEFAULT_ARRAY = [42, 17, 8, 91, 23, 5, 64, 12]

ALGORITHMS = {
    "bubble": "Bubble Sort",
    "selection": "Selection Sort",
    "insertion": "Insertion Sort",
    "merge": "Merge Sort",
    "quick": "Quick Sort"
}


def generate_steps(numbers, algorithm):
    a = numbers.copy()
    steps = []
    comparisons = 0
    writes = 0

    def record(message, active=None, sorted_indices=None):
        steps.append({
            "array": a.copy(),
            "message": message,
            "active": active or [],
            "sorted": sorted_indices or [],
            "comparisons": comparisons,
            "writes": writes
        })

    record("Initial array loaded.")

    if algorithm == "bubble":
        for i in range(len(a)):
            swapped = False

            for j in range(len(a) - i - 1):
                comparisons += 1
                record(
                    f"Comparing {a[j]} and {a[j + 1]}.",
                    [j, j + 1]
                )

                if a[j] > a[j + 1]:
                    a[j], a[j + 1] = a[j + 1], a[j]
                    writes += 2
                    swapped = True
                    record("Swapped adjacent elements.", [j, j + 1])

            if not swapped:
                break

    elif algorithm == "selection":
        for i in range(len(a)):
            minimum = i

            for j in range(i + 1, len(a)):
                comparisons += 1
                record(
                    f"Comparing {a[j]} with {a[minimum]}.",
                    [minimum, j]
                )

                if a[j] < a[minimum]:
                    minimum = j

            if minimum != i:
                a[i], a[minimum] = a[minimum], a[i]
                writes += 2
                record("Moved minimum to sorted position.", [i, minimum])

    elif algorithm == "insertion":
        for i in range(1, len(a)):
            key = a[i]
            j = i - 1

            while j >= 0:
                comparisons += 1
                record(
                    f"Comparing {a[j]} with key {key}.",
                    [j, j + 1]
                )

                if a[j] <= key:
                    break

                a[j + 1] = a[j]
                writes += 1
                record("Shifting element to the right.", [j, j + 1])
                j -= 1

            a[j + 1] = key
            writes += 1
            record(f"Inserted {key} at index {j + 1}.", [j + 1])

    elif algorithm == "merge":

        def merge_sort(left, right):
            nonlocal comparisons, writes

            if right - left <= 1:
                return

            mid = (left + right) // 2

            record(
                f"Dividing range {left} to {right - 1}.",
                list(range(left, right))
            )

            merge_sort(left, mid)
            merge_sort(mid, right)

            L = a[left:mid]
            R = a[mid:right]

            i = j = 0
            k = left

            while i < len(L) and j < len(R):
                comparisons += 1
                record(f"Comparing {L[i]} and {R[j]}.", [k])

                if L[i] <= R[j]:
                    a[k] = L[i]
                    i += 1
                else:
                    a[k] = R[j]
                    j += 1

                writes += 1
                record("Writing merged element.", [k])
                k += 1

            while i < len(L):
                a[k] = L[i]
                i += 1
                writes += 1
                record("Copying remaining left element.", [k])
                k += 1

            while j < len(R):
                a[k] = R[j]
                j += 1
                writes += 1
                record("Copying remaining right element.", [k])
                k += 1

        merge_sort(0, len(a))

    elif algorithm == "quick":

        def quick_sort(low, high):
            nonlocal comparisons, writes

            if low >= high:
                return

            pivot = a[high]
            i = low - 1

            record(f"Pivot selected: {pivot}.", [high])

            for j in range(low, high):
                comparisons += 1
                record(
                    f"Comparing {a[j]} with pivot {pivot}.",
                    [j, high]
                )

                if a[j] <= pivot:
                    i += 1

                    if i != j:
                        a[i], a[j] = a[j], a[i]
                        writes += 2
                        record("Swapping partition elements.", [i, j])

            p = i + 1

            if p != high:
                a[p], a[high] = a[high], a[p]
                writes += 2

            record(f"Pivot placed at index {p}.", [p])

            quick_sort(low, p - 1)
            quick_sort(p + 1, high)

        quick_sort(0, len(a) - 1)

    record("Sorting completed!", sorted_indices=list(range(len(a))))
    return steps


@sorting_bp.route("/sorting", methods=["GET", "POST"])
def sorting_page():
    numbers = session.get("sorting_array", DEFAULT_ARRAY.copy())
    steps = []
    current = 0
    algorithm = session.get("sorting_algorithm", "bubble")
    error = ""
    message = "Array initialized. Select an algorithm to begin."

    if request.method == "POST":
        action = request.form.get("action", "")
        raw = request.form.get("array_input", "")

        if action == "set":
            try:
                parts = [p.strip() for p in raw.split(",")]

                if not raw.strip() or any(not p for p in parts):
                    raise ValueError

                new_numbers = [int(p) for p in parts]

                if len(new_numbers) > 30 or any(
                    abs(n) > 99999 for n in new_numbers
                ):
                    raise ValueError

                numbers = new_numbers
                session["sorting_array"] = numbers
                session["sorting_step"] = 0
                session["sorting_started"] = False

            except ValueError:
                error = "Enter 1 to 30 valid integers separated by commas."

        elif action == "random":
            numbers = [random.randint(1, 99) for _ in range(10)]
            session["sorting_array"] = numbers
            session["sorting_step"] = 0
            session["sorting_started"] = False

        elif action == "clear":
            numbers = []
            session["sorting_array"] = []
            session["sorting_step"] = 0
            session["sorting_started"] = False

        elif action == "run":
            algorithm = request.form.get("algorithm", "bubble")

            if algorithm not in ALGORITHMS:
                algorithm = "bubble"

            session["sorting_algorithm"] = algorithm
            session["sorting_step"] = 0
            session["sorting_started"] = bool(numbers)

            if not numbers:
                error = "Please set an array first."

        elif action == "next":
            session["sorting_step"] = session.get("sorting_step", 0) + 1

        elif action == "previous":
            session["sorting_step"] = max(
                0, session.get("sorting_step", 0) - 1
            )

        elif action == "reset":
            session["sorting_step"] = 0

    started = session.get("sorting_started", False)

    if started and numbers:
        steps = generate_steps(numbers, algorithm)

        current = min(
            session.get("sorting_step", 0),
            len(steps) - 1
        )

        session["sorting_step"] = current
        step = steps[current]

    else:
        step = {
            "array": numbers,
            "message": "Array initialized. Select an algorithm to begin.",
            "active": [],
            "sorted": [],
            "comparisons": 0,
            "writes": 0
        }

    if error:
        message = error
    else:
        message = step["message"]

    status = "IDLE"

    if started and steps:
        status = "DONE" if current == len(steps) - 1 else "RUNNING"

    return render_template(
        "sorting.html",
        numbers=step["array"],
        original_array=numbers,
        steps=steps,
        current=current,
        step=step,
        message=message,
        error=error,
        status=status,
        algorithm=algorithm,
        algorithms=ALGORITHMS
    )
