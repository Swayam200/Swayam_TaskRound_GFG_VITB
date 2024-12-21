// Problem Data
const problems = {
    "two-sum": {
        title: "Two Sum",
        description: "Given an array of integers nums and a target value, return indices of the two numbers that add up to the target.",
        testCases: [
            { input: [[2, 7, 11, 15], 9], expected: [0, 1] },
            { input: [[3, 2, 4], 6], expected: [1, 2] },
            { input: [[3, 3], 6], expected: [0, 1] }
        ]
    },
    "fibonacci": {
        title: "Fibonacci",
        description: "Calculate the nth Fibonacci number.",
        testCases: [
            { input: [0], expected: 0 },
            { input: [1], expected: 1 },
            { input: [5], expected: 5 }
        ]
    }
};

// Evaluate Test Cases
function evaluate(problemId, userCode) {
    const problem = problems[problemId];
    const results = [];

    problem.testCases.forEach((test, index) => {
        try {
            const userFunction = new Function("input", userCode);
            const result = userFunction(test.input);

            if (JSON.stringify(result) === JSON.stringify(test.expected)) {
                results.push(`Test ${index + 1}: ✓ Passed`);
            } else {
                results.push(`Test ${index + 1}: ✗ Failed (Expected ${JSON.stringify(test.expected)}, got ${JSON.stringify(result)})`);
            }
        } catch (error) {
            results.push(`Test ${index + 1}: ✗ Failed (Error: ${error.message})`);
        }
    });

    return results;
}

// Event Listener
document.getElementById("submit").addEventListener("click", () => {
    const problemId = document.getElementById("problem").value;
    const userCode = document.getElementById("code").value;
    const resultsDiv = document.getElementById("results");

    const results = evaluate(problemId, userCode);
    resultsDiv.innerHTML = `<h2>Results</h2>`;
    results.forEach(result => {
        resultsDiv.innerHTML += `<p>${result}</p>`;
    });
});
