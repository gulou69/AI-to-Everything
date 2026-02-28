/**
 * A2E Protocol TypeScript SDK
 * 
 * @packageDocumentation
 */

// Types
export interface Location {
  latitude: number;
  longitude: number;
}

export interface Provider {
  id: string;
  name: string;
  certification: string;
}

export interface Service {
  id: string;
  name: string;
  type: string;
  description: string;
  tags: string[];
  certificationLevel: number;
  provider: Provider;
}

export interface SearchRequest {
  keyword: string;
  type?: string;
  location?: Location;
  page?: number;
  size?: number;
}

export interface SearchResult {
  total: number;
  list: Service[];
}

export interface ServiceInfo {
  id: string;
  name: string;
  type: string;
  provider: Provider;
}

export interface SemanticInfo {
  description: string;
  keywords: string[];
  capabilities: string[];
  constraints: string[];
}

export interface AuthMethod {
  type: string;
  description: string;
  endpoint: string;
}

export interface AuthInfo {
  required: boolean;
  methods: AuthMethod[];
}

export interface Permission {
  name: string;
  description: string;
  endpoint: string;
}

export interface PermissionInfo {
  required: Permission[];
  optional: Permission[];
}

export interface Endpoint {
  name: string;
  path: string;
  method: string;
  description: string;
  requiresPayment: boolean;
  inputSchema: Record<string, unknown>;
  outputSchema: Record<string, unknown>;
  outputDescription: string;
}

export interface ErrorCode {
  code: string;
  description: string;
  suggestion: string;
}

export interface ErrorHandling {
  codes: ErrorCode[];
}

export interface Protocol {
  version: string;
  service: ServiceInfo;
  semantic: SemanticInfo;
  authentication: AuthInfo;
  permissions: PermissionInfo;
  endpoints: Endpoint[];
  errorHandling: ErrorHandling;
}

export interface ExecuteRequest {
  serviceId: string;
  endpoint: string;
  consumerToken: string;
  input: Record<string, unknown>;
}

export interface ExecuteError {
  code: string;
  message: string;
  suggestion: string;
}

export interface ExecuteResult {
  executionId: string;
  status: string;
  output: Record<string, unknown>;
  error?: ExecuteError;
}

export interface AuthRequest {
  authType: string;
  authCode: string;
}

export interface UserInfo {
  nickname: string;
  avatar: string;
}

export interface AuthResult {
  consumerToken: string;
  expiresIn: number;
  userInfo: UserInfo;
}

export interface ClientOptions {
  baseURL?: string;
  appId?: string;
  appSecret?: string;
  timeout?: number;
}

// Error class
export class A2EError extends Error {
  code: string;
  
  constructor(code: string, message: string) {
    super(message);
    this.code = code;
    this.name = 'A2EError';
  }
}

// API Response wrapper
interface APIResponse<T> {
  code: number;
  message: string;
  data: T;
}

// Client
export class A2EClient {
  private baseURL: string;
  private appId?: string;
  private appSecret?: string;
  private timeout: number;

  constructor(options: ClientOptions = {}) {
    this.baseURL = (options.baseURL || 'https://api.a2e-platform.com').replace(/\/$/, '');
    this.appId = options.appId;
    this.appSecret = options.appSecret;
    this.timeout = options.timeout || 30000;
  }

  private getHeaders(): Record<string, string> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };
    
    if (this.appId) {
      headers['X-App-ID'] = this.appId;
    }
    
    return headers;
  }

  private async request<T>(
    method: string,
    path: string,
    body?: unknown
  ): Promise<T> {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);

    try {
      const response = await fetch(`${this.baseURL}${path}`, {
        method,
        headers: this.getHeaders(),
        body: body ? JSON.stringify(body) : undefined,
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      const data: APIResponse<T> = await response.json();

      if (data.code !== 0) {
        throw new A2EError(String(data.code), data.message);
      }

      return data.data;
    } catch (error) {
      clearTimeout(timeoutId);
      
      if (error instanceof A2EError) {
        throw error;
      }
      
      throw new A2EError('NETWORK_ERROR', String(error));
    }
  }

  /**
   * Search for services by keyword
   */
  async searchServices(request: SearchRequest): Promise<SearchResult> {
    return this.request<SearchResult>('POST', '/api/v1/open/services/search', {
      keyword: request.keyword,
      type: request.type,
      location: request.location,
      page: request.page || 1,
      size: request.size || 10,
    });
  }

  /**
   * Get the A2E protocol document for a service
   */
  async getProtocol(serviceId: string): Promise<Protocol> {
    return this.request<Protocol>('GET', `/api/v1/open/services/${serviceId}/protocol`);
  }

  /**
   * Execute a service endpoint
   */
  async execute(request: ExecuteRequest): Promise<ExecuteResult> {
    return this.request<ExecuteResult>(
      'POST',
      `/api/v1/open/services/${request.serviceId}/execute/${request.endpoint}`,
      {
        consumer_token: request.consumerToken,
        input: request.input,
      }
    );
  }

  /**
   * Get a consumer token for authentication
   */
  async getConsumerToken(request: AuthRequest): Promise<AuthResult> {
    return this.request<AuthResult>('POST', '/api/v1/open/platform/get_user_token', {
      auth_type: request.authType,
      auth_code: request.authCode,
    });
  }
}

// Default export
export default A2EClient;
