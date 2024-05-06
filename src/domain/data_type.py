import dataclasses
from bson import ObjectId


@dataclasses.dataclass
class JsonDataType:
    _items = []
    _meta: dict = None

    # response data add
    def maintain_fee_service(self, *args: dict) -> dict:
        """input is data like
        data = [{'amount': '1','service_name': 'test'}]"""
        self._meta = {'total': len(args)}

        for item in args:
            self._items.append({'amount': item['amount'], 'service_name': item['service_name'],
                                'maintain_hour': item['maintain_hour']})
        return {'items': self._items, 'meta': self._meta}

    def maintain_fee_resource(self, *args: dict) -> dict:
        """input is data like
        data = { "amount": 1386000.0,
                "category_code": "default",
                "is_trial": false,
                "plan_name": "k8s:standard-1",
                "quantity": 1.0,
                "service_name": "kubernetes_engine"
        }"""
        self._meta = {'total': len(args)}

        for item in args:
            self._items.append({'amount': item['amount'],
                                'category_code': item['category_code'],
                                'is_trial': item['is_trial'],
                                'plan_name': item['plan_name'],
                                'quantity': item['quantity'],
                                'service_name': item['service_name'],
                                })
        return {'items': self._items, 'meta': self._meta}

    def maintain_hour_resource(self, *args: dict) -> dict:
        """input is data like
        data = {"plan_name": "k8s:standard-1",
                "maintain_hour": 72,}"""
        self._meta = {'total': len(args)}

        for item in args:
            self._items.append({'plan_name': item['plan_name'],
                                'maintain_hour': item['maintain_hour'], })
        return {'items': self._items, 'meta': self._meta}

    def maintain_hour_service(self, *args: dict) -> dict:
        """input is data like
        data = {"service_name": "cloud_server",
                "maintain_hour": 72,}"""
        self._meta = {'total': len(args)}

        for item in args:
            self._items.append({'service_name': item['service_name'],
                                'maintain_hours': item['maintain_hours'],
                                'amount': item['amount']})
        return {'items': self._items, 'meta': self._meta}

    def clear(self):
        self._items = []
        self._meta = None


class MaintainFeeService:
    def __init__(self, *args: dict):
        """input is data like
        data = [{'amount': '1','service_name': 'test'}]"""
        self._meta = {'total': len(args)}
        self._items = [{'amount': item['amount'],
                        'category_code': item['category_code'],
                        'is_trial': item['is_trial'],
                        'plan_name': item['plan_name'],
                        'quantity': item['quantity'],
                        'service_name': item['service_name'],
                        }
                       for item in args]
        self.payload = {'items': self._items, 'meta': self._meta}


class MaintainServiceDatatype:
    def __init__(self, *args: dict):
        self._meta = {'total': len(args)}
        self._items = [{'service_name': item['service_name'],
                        'amount': item['amount'],
                        'maintain_hour': item['maintain_hour'],
                        }
                       for item in args]
        self.payload = {'items': self._items, 'meta': self._meta}
        self.maintain_hour = [{'maintain_hour': item['maintain_hour'],
                               'service_name': item['service_name']}
                              for item in args]


class MaintainHourPlanDatatype:
    def __init__(self, *args: dict):
        self._meta = {'total': len(args)}
        self._items = [{'plan_name': item['plan_name'],
                        'maintain_hour': item['maintain_hour'],
                        }
                       for item in args]
        self.payload = {'items': self._items, 'meta': self._meta}
        self.maintain_hour = [{'maintain_hour': item['maintain_hour'],
                               'plan_name': item['plan_name']}
                              for item in args]


class MaintainanceFeePlanDatatype:
    def __init__(self, *args: dict):
        self._meta = {'total': len(args)}
        self._items = [{'plan_name': item['plan_name'],
                        'plan_type': item['plan_type'],
                        'maintain_hour_fee': item['maintain_hour_fee'],
                        }
                       for item in args]
        self.payload = {'items': self._items, 'meta': self._meta}
