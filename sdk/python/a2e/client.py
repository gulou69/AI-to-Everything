"""
A2E Protocol Client
"""

from typing import Any, Dict, List, Optional, Tuple
import httpx

from .models import (
    Service,
    Protocol,
    SearchResult,
    ExecuteResult,
    AuthResult,
)
from .exceptions import A2EError


class A2EClient:
    """Synchronous A2E API client."""

    def __init__(
        self,
        base_url: str = "https://api.a2e-platform.com",
        app_id: Optional[str] = None,
        app_secret: Optional[str] = None,
        timeout: int = 30,
    ):
        self.base_url = base_url.rstrip("/")
        self.app_id = app_id
        self.app_secret = app_secret
        self.timeout = timeout
        self._client = httpx.Client(timeout=timeout)

    def _get_headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.app_id:
            headers["X-App-ID"] = self.app_id
        return headers

    def _handle_response(self, response: httpx.Response) -> Dict[str, Any]:
        response.raise_for_status()
        data = response.json()
        
        if data.get("code", 0) != 0:
            raise A2EError(
                code=str(data.get("code")),
                message=data.get("message", "Unknown error")
            )
        
        return data.get("data", {})

    def search_services(
        self,
        keyword: str,
        service_type: Optional[str] = None,
        location: Optional[Tuple[float, float]] = None,
        page: int = 1,
        size: int = 10,
    ) -> SearchResult:
        """Search for services by keyword."""
        payload = {
            "keyword": keyword,
            "page": page,
            "size": size,
        }
        
        if service_type:
            payload["type"] = service_type
        
        if location:
            payload["location"] = {
                "latitude": location[0],
                "longitude": location[1],
            }

        response = self._client.post(
            f"{self.base_url}/api/v1/open/services/search",
            json=payload,
            headers=self._get_headers(),
        )
        
        data = self._handle_response(response)
        return SearchResult(
            total=data.get("total", 0),
            list=[Service(**s) for s in data.get("list", [])]
        )

    def get_protocol(self, service_id: str) -> Protocol:
        """Get the A2E protocol document for a service."""
        response = self._client.get(
            f"{self.base_url}/api/v1/open/services/{service_id}/protocol",
            headers=self._get_headers(),
        )
        
        data = self._handle_response(response)
        return Protocol(**data)

    def execute(
        self,
        service_id: str,
        endpoint: str,
        consumer_token: str,
        input_data: Dict[str, Any],
    ) -> ExecuteResult:
        """Execute a service endpoint."""
        payload = {
            "consumer_token": consumer_token,
            "input": input_data,
        }

        response = self._client.post(
            f"{self.base_url}/api/v1/open/services/{service_id}/execute/{endpoint}",
            json=payload,
            headers=self._get_headers(),
        )
        
        data = self._handle_response(response)
        return ExecuteResult(**data)

    def get_consumer_token(
        self,
        auth_type: str,
        auth_code: str,
    ) -> AuthResult:
        """Get a consumer token for authentication."""
        payload = {
            "auth_type": auth_type,
            "auth_code": auth_code,
        }

        response = self._client.post(
            f"{self.base_url}/api/v1/open/platform/get_user_token",
            json=payload,
            headers=self._get_headers(),
        )
        
        data = self._handle_response(response)
        return AuthResult(**data)

    def close(self):
        """Close the HTTP client."""
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class AsyncA2EClient:
    """Asynchronous A2E API client."""

    def __init__(
        self,
        base_url: str = "https://api.a2e-platform.com",
        app_id: Optional[str] = None,
        app_secret: Optional[str] = None,
        timeout: int = 30,
    ):
        self.base_url = base_url.rstrip("/")
        self.app_id = app_id
        self.app_secret = app_secret
        self.timeout = timeout
        self._client = httpx.AsyncClient(timeout=timeout)

    def _get_headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.app_id:
            headers["X-App-ID"] = self.app_id
        return headers

    def _handle_response(self, response: httpx.Response) -> Dict[str, Any]:
        response.raise_for_status()
        data = response.json()
        
        if data.get("code", 0) != 0:
            raise A2EError(
                code=str(data.get("code")),
                message=data.get("message", "Unknown error")
            )
        
        return data.get("data", {})

    async def search_services(
        self,
        keyword: str,
        service_type: Optional[str] = None,
        location: Optional[Tuple[float, float]] = None,
        page: int = 1,
        size: int = 10,
    ) -> SearchResult:
        """Search for services by keyword."""
        payload = {
            "keyword": keyword,
            "page": page,
            "size": size,
        }
        
        if service_type:
            payload["type"] = service_type
        
        if location:
            payload["location"] = {
                "latitude": location[0],
                "longitude": location[1],
            }

        response = await self._client.post(
            f"{self.base_url}/api/v1/open/services/search",
            json=payload,
            headers=self._get_headers(),
        )
        
        data = self._handle_response(response)
        return SearchResult(
            total=data.get("total", 0),
            list=[Service(**s) for s in data.get("list", [])]
        )

    async def get_protocol(self, service_id: str) -> Protocol:
        """Get the A2E protocol document for a service."""
        response = await self._client.get(
            f"{self.base_url}/api/v1/open/services/{service_id}/protocol",
            headers=self._get_headers(),
        )
        
        data = self._handle_response(response)
        return Protocol(**data)

    async def execute(
        self,
        service_id: str,
        endpoint: str,
        consumer_token: str,
        input_data: Dict[str, Any],
    ) -> ExecuteResult:
        """Execute a service endpoint."""
        payload = {
            "consumer_token": consumer_token,
            "input": input_data,
        }

        response = await self._client.post(
            f"{self.base_url}/api/v1/open/services/{service_id}/execute/{endpoint}",
            json=payload,
            headers=self._get_headers(),
        )
        
        data = self._handle_response(response)
        return ExecuteResult(**data)

    async def get_consumer_token(
        self,
        auth_type: str,
        auth_code: str,
    ) -> AuthResult:
        """Get a consumer token for authentication."""
        payload = {
            "auth_type": auth_type,
            "auth_code": auth_code,
        }

        response = await self._client.post(
            f"{self.base_url}/api/v1/open/platform/get_user_token",
            json=payload,
            headers=self._get_headers(),
        )
        
        data = self._handle_response(response)
        return AuthResult(**data)

    async def close(self):
        """Close the HTTP client."""
        await self._client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
