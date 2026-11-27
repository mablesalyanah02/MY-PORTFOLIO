from flask import Blueprint, render_template, request, session
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
    finished = set()

    def record(message, active=None):
        steps.append({
            "array": a.copy(),
            "message": message,
            "active": active or [],
            "sorted": sorted(finished),
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

                    record(
                        "Swapped adjacent elements.",
                        [j, j + 1]
                    )

            finished.add(len(a) - i - 1)

            record("Element reached its sorted position.")

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

                    record(
                        f"New minimum found: {a[minimum]}.",
                        [minimum]
                    )

            if minimum != i:
                a[i], a[minimum] = a[minimum], a[i]
                writes += 2

                record(
                    "Moved minimum to sorted position.",
                    [i, minimum]
                )

            finished.add(i)

            record(f"Index {i} is now sorted.")

    elif algorithm == "insertion":
        for i in range(1, len(a)):
            key = a[i]
            j = i - 1

            record(f"Selected key: {key}.", [i])

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

                record(
                    "Shifting element to the right.",
                    [j, j + 1]
                )

                j -= 1

            a[j + 1] = key
            writes += 1

            record(
                f"Inserted {key} at index {j + 1}.",
                [j + 1]
            )

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

                record(
                    f"Comparing {L[i]} and {R[j]}.",
                    [k]
                )

                if L[i] <= R[j]:
                    a[k] = L[i]
                    i += 1
                else:
                    a[k] = R[j]
                    j += 1

                writes += 1

                record(
                    "Writing merged element.",
                    [k]
                )

                k += 1

            while i < len(L):
                a[k] = L[i]
                i += 1
                writes += 1

                record(
                    "Copying remaining left element.",
                    [k]
                )

                k += 1

            while j < len(R):
                a[k] = R[j]
                j += 1
                writes += 1

                record(
                    "Copying remaining right element.",
                    [k]
                )

                k += 1

            record(
                f"Merged range {left} to {right - 1}.",
                list(range(left, right))
            )

        merge_sort(0, len(a))

    elif algorithm == "quick":

        def quick_sort(low, high):
            nonlocal comparisons, writes

            if low > high:
                return

            if low == high:
                finished.add(low)
                record(f"Index {low} is sorted.")
                return

            pivot = a[high]
            i = low - 1

            record(
                f"Pivot selected: {pivot}.",
                [high]
            )

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

                        record(
                            "Swapping partition elements.",
                            [i, j]
                        )

            p = i + 1

            if p != high:
                a[p], a[high] = a[high], a[p]
                writes += 2

            finished.add(p)

            record(
                f"Pivot placed at index {p}.",
                [p]
            )

            quick_sort(low, p - 1)
            quick_sort(p + 1, high)

        quick_sort(0, len(a) - 1)

    finished.update(range(len(a)))

    record("Sorting completed! The array is now fully sorted.")

    return steps


@sorting_bp.route("/sorting", methods=["GET", "POST"])
def sorting_page():
    numbers = session.get(
        "sorting_array",
        DEFAULT_ARRAY.copy()
    )

    algorithm = session.get(
        "sorting_algorithm",
        "bubble"
    )

    error = ""
    autoplay = False

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

            except ValueError:
                error = (
                    "Enter 1 to 30 valid integers "
                    "separated by commas."
                )

        elif action == "random":
            numbers = [
                random.randint(1, 99)
                for _ in range(10)
            ]

            session["sorting_array"] = numbers

        elif action == "clear":
            numbers = []

            session["sorting_array"] = []

        elif action == "run":
            algorithm = request.form.get(
                "algorithm",
                "bubble"
            )

            if algorithm not in ALGORITHMS:
                algorithm = "bubble"

            session["sorting_algorithm"] = algorithm

            if numbers:
                autoplay = True
            else:
                error = "Please set an array first."

    steps = []

    if autoplay:
        steps = generate_steps(numbers, algorithm)

    max_value = max(
        (abs(n) for n in numbers),
        default=1
    )

    max_value = max(max_value, 1)

    return render_template(
        "sorting.html",
        numbers=numbers,
        original_array=numbers,
        algorithms=ALGORITHMS,
        algorithm=algorithm,
        steps=steps,
        max_value=max_value,
        autoplay=autoplay,
        error=error
    )
