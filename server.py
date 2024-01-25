from flask import Flask, request, jsonify
import logging
from flask_cors import CORS, cross_origin
import itertools

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/*": {"origins": "*"}})


logging.basicConfig(level=logging.DEBUG)

def find_subsets(numbers, target):
    results = []

    # Function to check if current combination sums up to target
    def check_subset(subset):
        if round(sum(subset), 2) == target:
            results.append(subset)
            return True
        return False

    # Iterate over all combinations of the numbers list
    for r in range(1, len(numbers) + 1):
        for subset in itertools.combinations(numbers, r):
            if check_subset(subset):
                # Stop searching after finding a sufficient number of subsets to avoid long processing
                if len(results) >= 10:
                    return results

    return results

def find_approximate_subsets(numbers, target):
    numbers.sort(reverse=True)
    current_sum = 0
    subset = []

    for num in numbers:
        if current_sum + num <= target:
            current_sum += num
            subset.append(num)

    return [subset] if subset else []

# cross_origin(origins=["*"])
@app.route('/api/calculate', methods=['POST'])
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def calculate_subsets():
    data = request.get_json()
    logging.debug("Received data: %s", data)
    try:
        include_decimals = data['includeDecimals']
        numbers = [num for num in data.get('numbers', []) if num is not None]
        target = data.get('target')

        if numbers is None or target is None:
            raise ValueError("Missing numbers or target in the request")

        # Convert numbers to float and handle decimals
        numbers = [float(num) for num in numbers]
        target = float(target)

        if not include_decimals:
            numbers = [round(num) for num in numbers]
            target = round(target)

        subsets = find_subsets(numbers, target)

        # If no subsets found and approximation is requested
        if not subsets and data.get('approxMode', False):
            subsets = find_approximate_subsets(numbers, target)

        return jsonify(subsets)
    except Exception as e:
        logging.error("Error in calculation: %s", str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/api', methods=['GET'])
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def checkServer():
    return jsonify({
        "message": "working fine"
    })

if __name__ == '__main__':
    app.run(port=3002, host="18.191.23.206")
