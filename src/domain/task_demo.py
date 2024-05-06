import dataclasses
import requests


@dataclasses.dataclass
class ApiControl:
    url = 'https://staging-billing2.bizflycloud.vn/api/v4.1/pricing'
    headers = {'Content-Type': 'application/json'}

    def __init__(self, plan_name, category_code, quantity, maintain_hours):
        self.plan_name = plan_name
        self.category_code = category_code
        self.quantity = quantity

        self.__api_output = {
            "plan_name": f"{plan_name}",
            "category_code": f"{category_code}",
            "quantity": quantity,
        }
        self.times = maintain_hours

    def api_price_output(self) -> float:
        response = requests.get(self.url, params=self.__api_output, headers=self.headers)
        amount = response.json()['amount']
        return amount * self.times

    def api_info(self):
        response = requests.get(self.url, params=self.__api_output, headers=self.headers)
        data = response.json()
        return {'amount': data['amount'],
                'category_code': data['category_code'],
                'is_trial': data['is_trial'],
                'plan_name': data['plan_name'],
                'quantity': data['quantity'],
                'service_name': data['service_name'],
                'billing_model': data['billing_model'],}
