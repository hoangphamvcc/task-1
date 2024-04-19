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

    def api_price_output(self):
        response = requests.get(self.url, params=self.__api_output, headers=self.headers)
        amount = response.json()['amount']
        return amount * self.times





