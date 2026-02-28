"""
A2E Protocol Data Models
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Provider:
    """Service provider information."""
    id: str
    name: str
    certification: str = "none"


@dataclass
class Service:
    """Service information."""
    id: str
    name: str
    type: str
    description: str = ""
    tags: List[str] = field(default_factory=list)
    certification_level: int = 0
    provider: Optional[Provider] = None

    def __post_init__(self):
        if isinstance(self.provider, dict):
            self.provider = Provider(**self.provider)


@dataclass
class SearchResult:
    """Search result containing services."""
    total: int
    list: List[Service] = field(default_factory=list)


@dataclass
class ServiceInfo:
    """Service information in protocol."""
    id: str
    name: str
    type: str
    provider: Optional[Provider] = None

    def __post_init__(self):
        if isinstance(self.provider, dict):
            self.provider = Provider(**self.provider)


@dataclass
class SemanticInfo:
    """Semantic description."""
    description: str = ""
    keywords: List[str] = field(default_factory=list)
    capabilities: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)


@dataclass
class AuthMethod:
    """Authentication method."""
    type: str
    description: str = ""
    endpoint: str = ""


@dataclass
class AuthInfo:
    """Authentication configuration."""
    required: bool = False
    methods: List[AuthMethod] = field(default_factory=list)

    def __post_init__(self):
        self.methods = [
            AuthMethod(**m) if isinstance(m, dict) else m
            for m in self.methods
        ]


@dataclass
class Permission:
    """Permission requirement."""
    name: str
    description: str = ""
    endpoint: str = ""


@dataclass
class PermissionInfo:
    """Permission requirements."""
    required: List[Permission] = field(default_factory=list)
    optional: List[Permission] = field(default_factory=list)

    def __post_init__(self):
        self.required = [
            Permission(**p) if isinstance(p, dict) else p
            for p in self.required
        ]
        self.optional = [
            Permission(**p) if isinstance(p, dict) else p
            for p in self.optional
        ]


@dataclass
class Endpoint:
    """API endpoint definition."""
    name: str
    path: str
    method: str = "POST"
    description: str = ""
    requires_payment: bool = False
    input_schema: Dict[str, Any] = field(default_factory=dict)
    output_schema: Dict[str, Any] = field(default_factory=dict)
    output_description: str = ""


@dataclass
class ErrorCode:
    """Error code definition."""
    code: str
    description: str = ""
    suggestion: str = ""


@dataclass
class ErrorHandling:
    """Error handling configuration."""
    codes: List[ErrorCode] = field(default_factory=list)

    def __post_init__(self):
        self.codes = [
            ErrorCode(**c) if isinstance(c, dict) else c
            for c in self.codes
        ]


@dataclass
class Protocol:
    """A2E Protocol document."""
    version: str = "1.0.0"
    service: Optional[ServiceInfo] = None
    semantic: Optional[SemanticInfo] = None
    authentication: Optional[AuthInfo] = None
    permissions: Optional[PermissionInfo] = None
    endpoints: List[Endpoint] = field(default_factory=list)
    error_handling: Optional[ErrorHandling] = None

    def __post_init__(self):
        if isinstance(self.service, dict):
            self.service = ServiceInfo(**self.service)
        if isinstance(self.semantic, dict):
            self.semantic = SemanticInfo(**self.semantic)
        if isinstance(self.authentication, dict):
            self.authentication = AuthInfo(**self.authentication)
        if isinstance(self.permissions, dict):
            self.permissions = PermissionInfo(**self.permissions)
        self.endpoints = [
            Endpoint(**e) if isinstance(e, dict) else e
            for e in self.endpoints
        ]
        if isinstance(self.error_handling, dict):
            self.error_handling = ErrorHandling(**self.error_handling)


@dataclass
class ExecuteError:
    """Execution error."""
    code: str
    message: str = ""
    suggestion: str = ""


@dataclass
class ExecuteResult:
    """Execution result."""
    execution_id: str = ""
    status: str = ""
    output: Dict[str, Any] = field(default_factory=dict)
    error: Optional[ExecuteError] = None

    def __post_init__(self):
        if isinstance(self.error, dict):
            self.error = ExecuteError(**self.error)


@dataclass
class UserInfo:
    """User information."""
    nickname: str = ""
    avatar: str = ""


@dataclass
class AuthResult:
    """Authentication result."""
    consumer_token: str = ""
    expires_in: int = 0
    user_info: Optional[UserInfo] = None

    def __post_init__(self):
        if isinstance(self.user_info, dict):
            self.user_info = UserInfo(**self.user_info)
