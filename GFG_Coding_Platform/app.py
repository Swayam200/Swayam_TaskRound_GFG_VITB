from flask import Flask, render_template, request, jsonify
from typing import List, Dict, Any
from dataclasses import dataclass
import time

app = Flask(__name__)

@dataclass
class Problem:
    id: str
    title: str
    description: str
    function_name: str
    test_cases: List[Dict[str, Any]]
    time_limit: float = 1.0

problems = {
    "two-sum": Problem(
        id="two-sum",
        title="Two Sum",
        description="Given an array of integers nums and an integer target, return indices of the two numbers that add up to target.",
        function_name="two_sum",
        test_cases=[
            {"input": ([2, 7, 11, 15], 9), "expected": [0, 1]},
            {"input": ([3, 2, 4], 6), "expected": [1, 2]},
            {"input": ([3, 3], 6), "expected": [0, 1]}
        ]
    ),
    "fibonacci": Problem(
        id="fibonacci",
        title="Fibonacci Number",
        description="Calculate the nth Fibonacci number.",
        function_name="fibonacci",
        test_cases=[
            {"input": (0,), "expected": 0},
            {"input": (1,), "expected": 1},
            {"input": (5,), "expected": 5}
        ]
    )
}

@app.route('/')
def index():
    return render_template('index.html', problems=problems)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    problem_id = data.get('problem_id')
    code = data.get('code')

    if problem_id not in problems:
        return jsonify({"error": "Invalid problem ID"}), 400

    problem = problems[problem_id]
    results = []

    # Evaluate test cases
    for i, test_case in enumerate(problem.test_cases, 1):
        start_time = time.time()
        try:
            # Execute user code
            namespace = {}
            exec(code, namespace)

            if problem.function_name not in namespace:
                raise NameError(f"Function '{problem.function_name}' not found in submission")

            function = namespace[problem.function_name]
            result = function(*test_case["input"])
            execution_time = time.time() - start_time

            if execution_time > problem.time_limit:
                results.append({"test_number": i, "passed": False, "error": "Time Limit Exceeded"})
            elif result == test_case["expected"]:
                results.append({"test_number": i, "passed": True, "execution_time": execution_time})
            else:
                results.append({"test_number": i, "passed": False, "error": f"Expected {test_case['expected']}, got {result}"})
        except Exception as e:
            results.append({"test_number": i, "passed": False, "error": str(e)})

    # Calculate score
    passed_tests = sum(1 for r in results if r["passed"])
    total_tests = len(results)
    score = (passed_tests / total_tests) * 100 if total_tests > 0 else 0

    return jsonify({"results": results, "score": score, "passed_tests": passed_tests, "total_tests": total_tests})

if __name__ == "__main__":
    app.run(debug=True)
