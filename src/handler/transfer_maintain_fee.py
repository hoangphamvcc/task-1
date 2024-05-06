class Transfer_maintain_fee:
    """status fee is 0,1,2 for FR, PAYG, or else"""

    def __init__(self, billing_model, amount, plan_name, service_name, mongodb_plan, mongodb_service):
        self.billing_model = billing_model
        self.amount = amount
        self.plan_name = plan_name
        self.service_name = service_name
        self.mongodb_plan = mongodb_plan
        self.mongodb_service = mongodb_service
        self.fee_status = 0
        self.payload = {}
        self.plan_and_service = 0  # 0-1: none plan, 0-2: none service
        self.maintain_hour_service = 0
        self.maintain_hour_plan = 0
        self.maintainance_fee = 0

    def plan_and_service_check(self):
        if next(self.mongodb_plan.find({'plan_name': self.plan_name}), None) is None:
            if next(self.mongodb_service.find({'service_name': self.service_name}), None) is None:
                self.plan_and_service = 0
            else:
                self.plan_and_service = 1
                self.maintain_hour_service = next(self.mongodb_service.find({'service_name': self.service_name}))['maintain_hour']

        else:
            self.plan_and_service = 2
            self.maintain_hour_plan = next(self.mongodb_plan.find({'plan_name': self.plan_name}))['maintain_hour']

    def payload_data(self):
        if self.billing_model == 'FR':
            self.payload = {'plan_name': self.plan_name, 'plan_type': 'Hourly', 'maintain_hour_fee': self.amount / 720}
            self.maintainance_fee = self.amount/720
        elif self.billing_model == 'PAYG':
            if self.plan_and_service == 0:  # khong co plan va service
                self.payload = {'plan_name': self.plan_name, 'plan_type': 'Hourly', 'maintain_hour_fee': 0}
            else:
                hour_fee = self.amount
                if self.plan_and_service == 1:  # khong plan, co service
                    self.maintainance_fee = hour_fee * self.maintain_hour_service
                    self.payload = {'plan_name': self.plan_name, 'plan_type': 'Hourly',
                                    'maintain_hour_fee': self.maintainance_fee}
                elif self.plan_and_service == 2:  # co plan
                    self.maintainance_fee = hour_fee * self.maintain_hour_plan
                    self.payload = {'plan_name': self.plan_name, 'plan_type': 'Hourly',
                                    'maintain_hour_fee': self.maintainance_fee}

        else:
            if self.plan_and_service == 0:  # khong co plan va service
                self.payload = {'plan_name': self.plan_name, 'plan_type': 'Monthly', 'maintain_hour_fee': 0}
            else:
                hour_fee = self.amount / 720
                if self.plan_and_service == 1:  # khong plan, co service
                    self.maintainance_fee = hour_fee * self.maintain_hour_service
                    self.payload = {'plan_name': self.plan_name, 'plan_type': 'Hourly',
                                    'maintain_hour_fee': self.maintainance_fee}
                elif self.plan_and_service == 2:  # co plan
                    self.maintainance_fee = hour_fee * self.maintain_hour_plan
                    self.payload = {'plan_name': self.plan_name, 'plan_type': 'Hourly',
                                    'maintain_hour_fee': self.maintainance_fee}
        return self.payload
