import requests


class DashboardApiPayCourse:
    def __init__(self):
        self.api_key = 'sk_test_51PaMycRoAnBDq3fbeeWvGLGFUfDkJ3c5LiF4u0Z8D0UoWuTy5XmGovYBdB81wMNlkJPyPewj5jL8LQ8K2EE7JH8h00WHECF0P4'
        self.headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

    def create_product(self, name, description):
        url = "https://api.stripe.com/v1/products"

        data = {
            "name": name,
            "active": True,
            "description": description,
        }

        response = requests.post(url, headers=self.headers, data=data)

        return response.json()

    def create_price(self, currency, unit_amount, product_data):
        url = "https://api.stripe.com/v1/prices"

        data = {
            "currency": currency,
            "unit_amount": unit_amount,
            "product_data[name]": product_data['name'],
        }

        response = requests.post(url, headers=self.headers, data=data)

        return response.json()

    def create_session(self, success_url, cancel_url, price_id, payment_method_types):
        url = "https://api.stripe.com/v1/checkout/sessions"

        data = {
            "payment_method_types[]": payment_method_types,
            "line_items[0][price]": price_id,
            "line_items[0][quantity]": 1,
            "mode": "payment",
            "success_url": success_url,
            "cancel_url": cancel_url,
        }

        response = requests.post(url, headers=self.headers, data=data)

        return response.json()
