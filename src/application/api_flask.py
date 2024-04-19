from flask import Flask, request, jsonify
from src.domain import ApiControl
from src.common.mongo import MongoDB

mongodb = MongoDB().maintain_hours
app = Flask(__name__)


@app.route('/change_api/<string:function>', methods=['POST'])
def change_api(function):
    if function == 'add' or function == 'change':
        plan_name = request.json.get('plan_name')
        api = ApiControl(plan_name, category_code='dedicated', quantity=1, maintain_hours=1)
        return jsonify({'amount': api.api_price_output()}), 200
    elif function == 'delete':
        return jsonify({'amount': 0}), 200


@app.route('/api', methods=['POST'])
def api_control_price():
    plan_name = request.json.get('plan_name')
    category_code = request.json.get('category_code')
    quantity = request.json.get('quantity')
    maintain_hours = mongodb['maintain_hours']
    try:
        maintain_hours = request.json.get('maintain_hours')
        api = ApiControl(plan_name, category_code, quantity, maintain_hours)
        return jsonify({'amount': api.api_price_output()}), 200
    except Exception as e:
        return jsonify(str(e)), 400


@app.route('/api/maintain_hour', methods=['GET'])
def get_maintain_hours():
    maintain_hours = mongodb['maintain_hours']
    return jsonify({'maintain_hours': maintain_hours}), 200

if __name__ == "__main__":
    app.run(port=8887, debug=True)
