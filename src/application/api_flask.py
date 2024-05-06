from flask import Flask, request, jsonify
from src.domain.task_demo import ApiControl
from src.common.mongo import MongoDB

mongodb = MongoDB().maintain_hours
app = Flask(__name__)
api_list = []


@app.route('/change_api/<string:function>', methods=['GET'])
def change_api(function):
    if function == 'add' or function == 'change':
        plan_names = request.json.get('plan_name')
        for plan_name in plan_names:
            api = ApiControl(plan_name, category_code='dedicated', quantity=1, maintain_hours=1)
            api_list.append(api.api_price_output())
        return jsonify({'amount': api_list}), 200
    elif function == 'delete':
        return jsonify({'payload': {'amount': 0}}), 200


@app.route('/api', methods=['POST'])
def api_control_price():
    plan_name = request.json.get('plan_name')
    category_code = request.json.get('category_code')
    quantity = request.json.get('quantity')
    maintain_hours = mongodb['maintain_hours']
    try:
        maintain_hours = request.json.get('maintain_hours')
    except Exception:
        pass

    api = ApiControl(plan_name, category_code, quantity, maintain_hours)
    return jsonify({'amount': api.api_price_output()}), 200


@app.route('/api/maintain_hour', methods=['GET'])
def get_maintain_hours():
    maintain_hours = mongodb
    plan_name = request.json.get('plan_name')
    default_maintain_hours = next(maintain_hours.find({'plan_name': plan_name}))['deafault_maintain_hours']
    return jsonify({'maintain_hour': default_maintain_hours}), 200


@app.route('/api/maintain_hour', methods=['POST'])
def change_maintain_hours():
    datas = request.json
    return datas[0]['plan_name']


if __name__ == "__main__":
    app.run(port=8887, debug=True)
