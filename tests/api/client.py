import allure
import requests
from tests.utils.logger import setup_logger

logger = setup_logger(__name__)

class ApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def _post(self, path: str, data: dict = None, headers: dict = None):
        url = f"{self.base_url}{path}"
        headers = headers or {"Content-Type": "application/x-www-form-urlencoded"}
        with allure.step(f"POST {url}"):
            logger.info(f"POST {url} | data={data}")
            resp = requests.post(url, data=data or {}, headers=headers)
            self._attach_response("POST", url, resp, data)
            return resp

    def _get(self, path: str, params: dict = None):
        url = f"{self.base_url}{path}"
        with allure.step(f"GET {url}"):
            logger.info(f"GET {url} | params={params}")
            resp = requests.get(url, params=params or {})
            self._attach_response("GET", url, resp, params)
            return resp

    @staticmethod
    def _attach_response(method: str, url: str, response, payload):
        try:
            allure.attach(
                f"{method} {url}\nPayload: {payload}\nStatus: {response.status_code}\nBody: {response.text}",
                name="api_call",
                attachment_type=allure.attachment_type.TEXT
            )
        except Exception:
            pass

    # Public methods
    def verify_login(self, email: str, password: str):
        return self._post("/api/verifyLogin", data={"email": email, "password": password})

    def search_product(self, query: str):
        return self._post("/api/searchProduct", data={"search_product": query})

    def search_product_get(self):
        return self._get("/api/searchProduct")
