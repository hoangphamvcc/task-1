from flask import Flask, request, jsonify
from src.domain.data_type import JsonDataType, MaintainFeeService, MaintainServiceDatatype, MaintainHourPlanDatatype,\
    MaintainanceFeePlanDatatype, MaintainServiceHourDatatype, MaintainServiceFeeDatatype
from src.domain.task_demo import ApiControl
from src.common.mongo import MongoDB
from src.handler.transfer_maintain_fee import Transfer_maintain_fee
from src.common.redis_check import RedisCache

app = Flask(__name__)


# API 1
@app.route('/api/maintainance-fee/service', methods=['POST'])  # add data to db
def api_maintain_fee_service():
    datas = request.json
    response_data = []
    # confirm data
    for index, data in (enumerate(datas)):  # add data to datas
        mongodb = MongoDB().maintain_service
        try:
            request_data = {'service_name': data['service_name'], 'amount': data['amount']}
            if next(mongodb.find({'service_name': data['service_name']}), None) is None:
                mongodb.insert_one(request_data)

            else:
                mongodb.update_one({'service_name': data['service_name']},
                                   {'$set': {'amount': data['amount']}})
            response_data.append(request_data)
        except:
            return 'api error'
    return jsonify(MaintainServiceFeeDatatype(*response_data).payload), 200


@app.route('/api/maintainance-fee/service', methods=['GET'])  # get data to db
def api_get_maintain_fee_service():
    mongodb = MongoDB().maintain_service
    response_data = []
    datas = request.json
    for payload in datas:
        response_data.append(next(mongodb.find({'service_name': payload['service_name']}), None))
    return jsonify(MaintainServiceDatatype(*response_data).payload), 200


# API 2


@app.route('/api/maintainance-fee/resource', methods=['POST'])  # find data from api
def api_maintain_fee_resource():
    datas = request.json
    response_data = []
    for data in datas:  # add data to datas
        try:
            data_info = ApiControl(data['plan_name'], data['category_code'], data['quantity'], 1).api_info()
            response_data.append(data_info)
        except:
            return 'api error'

    # return payload dataform
    return jsonify(MaintainFeeService(*response_data).payload), 200


@app.route('/api/maintainance-fee/resource', methods=['GET'])  # get data to db, all data
def api_get_maintain_fee_resource():
    mongodb = MongoDB().maintain_plan
    response_data = []
    datas = request.json
    for payload in datas:
        response_data.append(next(mongodb.find({'plan_name': payload['plan_name']}), None))
    return jsonify(MaintainHourPlanDatatype(*response_data).payload), 200


# API 3


@app.route('/api/maintainance-hour/resource', methods=['POST'])  # add data to db
def api_maintain_hour_resource():
    datas = request.json
    response_data = []
    for data in datas:  # add data to datas
        # confirm data
        mongodb = MongoDB().maintain_plan
        request_data = {'plan_name': data['plan_name'], 'maintain_hour': data['maintain_hour']}
        if next(mongodb.find({'plan_name': data['plan_name']}), None) is None:
            mongodb.insert_one(request_data)
        else:
            mongodb.update_one({'plan_name': data['plan_name']}, {'$set': {'maintain_hour': data['maintain_hour']}})
        # mongodb.insert_one(request_data)
        response_data.append(request_data)
    return jsonify(JsonDataType().maintain_hour_resource(*response_data)), 200


# API 4


@app.route('/api/maintainance-hour/service', methods=['POST'])  # add data to db
def api_maintain_hour_service():
    datas = request.json
    response_data = []
    # confirm data
    for index, data in (enumerate(datas)):  # add data to datas
        mongodb = MongoDB().maintain_service
        try:
            request_data = {'service_name': data['service_name'],
                            "maintain_hour": data['maintain_hour']}
            if next(mongodb.find({'service_name': data['service_name']}), None) is None:
                mongodb.insert_one(request_data)

            else:
                mongodb.update_one({'service_name': data['service_name']},
                                   {'$set': {'maintain_hour': data['maintain_hour']}})
            response_data.append(request_data)
        except:
            return 'api error'
    return jsonify(MaintainServiceHourDatatype(*response_data).payload), 200


# API 5


@app.route('/api/maintainance-hour-fee', methods=['GET'])  # get data to db
def api_get_maintain_hour_fee():
    """input {'plan_name'}"""
    mongodb_service = MongoDB().maintain_service
    mongodb_plan = MongoDB().maintain_plan
    datas = request.json
    response_data = []
    for payload in datas:
        # cache check
        redis = RedisCache({'plan_name': payload['plan_name'],
                            'category_code': 'default',
                            'quantity': payload['quantity']})
        if redis.redis_data_check() is True:
            final_data = {"maintain_hour_fee": float(redis.data),
                          "plan_name": payload['plan_name'],
                          "plan_type": 'Hourly',
                          }
            print('cache')
        else:
            # call api
            payload = ApiControl(payload['plan_name'], payload['category_code'], payload['quantity'], 1).api_info()
            tranfer = Transfer_maintain_fee(payload['billing_model'], payload['amount'], payload['plan_name'],
                                            payload['service_name'], mongodb_plan, mongodb_service)
            tranfer.plan_and_service_check()
            final_data = tranfer.payload_data()
            redis.redis_save(float(tranfer.maintainance_fee))
            print('api')
        response_data.append(final_data)
    return jsonify(MaintainanceFeePlanDatatype(*response_data).payload), 200


if __name__ == "__main__":
    app.run(port=8887, debug=True)
