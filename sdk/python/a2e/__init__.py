"""
A2E Protocol Python SDK

A Python SDK for the A2E (Agent-to-EveryThing) Protocol.
"""

from .client import A2EClient, AsyncA2EClient
from .models import (
    Service,
    Protocol,
    SearchResult,
    ExecuteResult,
    AuthResult,
)
from .exceptions import A2EError

__version__ = "1.0.0"
__all__ = [
    "A2EClient",
    "AsyncA2EClient",
    "Service",
    "Protocol",
    "SearchResult",
    "ExecuteResult",
    "AuthResult",
    "A2EError",
]
