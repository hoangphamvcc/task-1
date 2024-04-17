from flask import Flask, request, jsonify
from src.domain import ApiControl
from src.common.mongo import MongoDB

mongodb = MongoDB()
app = Flask(__name__)


@app.route('/api', methods=['POST'])
def api_control_price():
    plan_name = request.json.get('plan_name')
    category_code = request.json.get('category_code')
    quantity = request.json.get('quantity')
    maintain_hours = MongoDB().maintain_hours['maintain_hours']
    try:
        maintain_hours = request.json.get('maintain_hours')
        api = ApiControl(plan_name, category_code, quantity, maintain_hours)
        return jsonify(api.api_price_output()), 200
    except Exception as e:
        return jsonify(str(e)), 400


if __name__ == "__main__":
    app.run(port=8887, debug=True)
