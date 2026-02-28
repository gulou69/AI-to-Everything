// Package a2e provides a Go SDK for the A2E (Agent-to-EveryThing) Protocol.
package a2e

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"time"
)

// Client is the A2E API client.
type Client struct {
	baseURL    string
	httpClient *http.Client
	appID      string
	appSecret  string
}

// ClientOption is a function that configures the client.
type ClientOption func(*Client)

// NewClient creates a new A2E client.
func NewClient(opts ...ClientOption) *Client {
	c := &Client{
		baseURL: "https://api.a2e-platform.com",
		httpClient: &http.Client{
			Timeout: 30 * time.Second,
		},
	}

	for _, opt := range opts {
		opt(c)
	}

	return c
}

// WithBaseURL sets the API base URL.
func WithBaseURL(url string) ClientOption {
	return func(c *Client) {
		c.baseURL = url
	}
}

// WithTimeout sets the HTTP timeout.
func WithTimeout(seconds int) ClientOption {
	return func(c *Client) {
		c.httpClient.Timeout = time.Duration(seconds) * time.Second
	}
}

// WithAppID sets the App ID for authentication.
func WithAppID(appID string) ClientOption {
	return func(c *Client) {
		c.appID = appID
	}
}

// WithAppSecret sets the App Secret for authentication.
func WithAppSecret(secret string) ClientOption {
	return func(c *Client) {
		c.appSecret = secret
	}
}

// Location represents a geographic location.
type Location struct {
	Latitude  float64 `json:"latitude"`
	Longitude float64 `json:"longitude"`
}

// SearchRequest is the request for searching services.
type SearchRequest struct {
	Keyword  string    `json:"keyword"`
	Type     string    `json:"type,omitempty"`
	Location *Location `json:"location,omitempty"`
	Page     int       `json:"page"`
	Size     int       `json:"size"`
}

// Service represents a service in the search results.
type Service struct {
	ID                 string   `json:"id"`
	Name               string   `json:"name"`
	Type               string   `json:"type"`
	Description        string   `json:"description"`
	Tags               []string `json:"tags"`
	CertificationLevel int      `json:"certification_level"`
	Provider           Provider `json:"provider"`
}

// Provider represents a service provider.
type Provider struct {
	ID            string `json:"id"`
	Name          string `json:"name"`
	Certification string `json:"certification"`
}

// SearchResult is the response for searching services.
type SearchResult struct {
	Total int       `json:"total"`
	List  []Service `json:"list"`
}

// SearchServices searches for services by keyword.
func (c *Client) SearchServices(ctx context.Context, req *SearchRequest) (*SearchResult, error) {
	var result SearchResult
	err := c.post(ctx, "/api/v1/open/services/search", req, &result)
	return &result, err
}

// Protocol represents the A2E protocol document.
type Protocol struct {
	Version        string         `json:"version"`
	Service        ServiceInfo    `json:"service"`
	Semantic       SemanticInfo   `json:"semantic"`
	Authentication AuthInfo       `json:"authentication"`
	Permissions    PermissionInfo `json:"permissions"`
	Endpoints      []Endpoint     `json:"endpoints"`
	ErrorHandling  ErrorHandling  `json:"error_handling"`
}

// ServiceInfo represents service information.
type ServiceInfo struct {
	ID       string   `json:"id"`
	Name     string   `json:"name"`
	Type     string   `json:"type"`
	Provider Provider `json:"provider"`
}

// SemanticInfo represents semantic description.
type SemanticInfo struct {
	Description  string   `json:"description"`
	Keywords     []string `json:"keywords"`
	Capabilities []string `json:"capabilities"`
	Constraints  []string `json:"constraints"`
}

// AuthInfo represents authentication configuration.
type AuthInfo struct {
	Required bool         `json:"required"`
	Methods  []AuthMethod `json:"methods"`
}

// AuthMethod represents an authentication method.
type AuthMethod struct {
	Type        string `json:"type"`
	Description string `json:"description"`
	Endpoint    string `json:"endpoint"`
}

// PermissionInfo represents permission requirements.
type PermissionInfo struct {
	Required []Permission `json:"required"`
	Optional []Permission `json:"optional"`
}

// Permission represents a single permission.
type Permission struct {
	Name        string `json:"name"`
	Description string `json:"description"`
	Endpoint    string `json:"endpoint"`
}

// Endpoint represents an API endpoint.
type Endpoint struct {
	Name              string                 `json:"name"`
	Path              string                 `json:"path"`
	Method            string                 `json:"method"`
	Description       string                 `json:"description"`
	RequiresPayment   bool                   `json:"requires_payment"`
	InputSchema       map[string]interface{} `json:"input_schema"`
	OutputSchema      map[string]interface{} `json:"output_schema"`
	OutputDescription string                 `json:"output_description"`
}

// ErrorHandling represents error handling configuration.
type ErrorHandling struct {
	Codes []ErrorCode `json:"codes"`
}

// ErrorCode represents an error code definition.
type ErrorCode struct {
	Code        string `json:"code"`
	Description string `json:"description"`
	Suggestion  string `json:"suggestion"`
}

// GetProtocol retrieves the A2E protocol document for a service.
func (c *Client) GetProtocol(ctx context.Context, serviceID string) (*Protocol, error) {
	var result Protocol
	err := c.get(ctx, fmt.Sprintf("/api/v1/open/services/%s/protocol", serviceID), &result)
	return &result, err
}

// ExecuteRequest is the request for executing a service endpoint.
type ExecuteRequest struct {
	ServiceID     string                 `json:"service_id"`
	Endpoint      string                 `json:"endpoint"`
	ConsumerToken string                 `json:"consumer_token"`
	Input         map[string]interface{} `json:"input"`
}

// ExecuteResult is the response for executing a service endpoint.
type ExecuteResult struct {
	ExecutionID string                 `json:"execution_id"`
	Status      string                 `json:"status"`
	Output      map[string]interface{} `json:"output"`
	Error       *ExecuteError          `json:"error,omitempty"`
}

// ExecuteError represents an execution error.
type ExecuteError struct {
	Code       string `json:"code"`
	Message    string `json:"message"`
	Suggestion string `json:"suggestion"`
}

// Execute executes a service endpoint.
func (c *Client) Execute(ctx context.Context, req *ExecuteRequest) (*ExecuteResult, error) {
	var result ExecuteResult
	path := fmt.Sprintf("/api/v1/open/services/%s/execute/%s", req.ServiceID, req.Endpoint)
	err := c.post(ctx, path, map[string]interface{}{
		"consumer_token": req.ConsumerToken,
		"input":          req.Input,
	}, &result)
	return &result, err
}

// AuthRequest is the request for getting a consumer token.
type AuthRequest struct {
	Type string `json:"auth_type"`
	Code string `json:"auth_code"`
}

// AuthResult is the response for getting a consumer token.
type AuthResult struct {
	ConsumerToken string   `json:"consumer_token"`
	ExpiresIn     int      `json:"expires_in"`
	UserInfo      UserInfo `json:"user_info"`
}

// UserInfo represents basic user information.
type UserInfo struct {
	Nickname string `json:"nickname"`
	Avatar   string `json:"avatar"`
}

// GetConsumerToken gets a consumer token for authentication.
func (c *Client) GetConsumerToken(ctx context.Context, req *AuthRequest) (*AuthResult, error) {
	var result AuthResult
	err := c.post(ctx, "/api/v1/open/platform/get_user_token", req, &result)
	return &result, err
}

// APIError represents an API error.
type APIError struct {
	Code    string `json:"code"`
	Message string `json:"message"`
}

func (e *APIError) Error() string {
	return fmt.Sprintf("API Error: %s - %s", e.Code, e.Message)
}

// apiResponse is the standard API response wrapper.
type apiResponse struct {
	Code    int             `json:"code"`
	Message string          `json:"message"`
	Data    json.RawMessage `json:"data"`
}

func (c *Client) get(ctx context.Context, path string, result interface{}) error {
	req, err := http.NewRequestWithContext(ctx, "GET", c.baseURL+path, nil)
	if err != nil {
		return err
	}

	return c.doRequest(req, result)
}

func (c *Client) post(ctx context.Context, path string, body interface{}, result interface{}) error {
	jsonBody, err := json.Marshal(body)
	if err != nil {
		return err
	}

	req, err := http.NewRequestWithContext(ctx, "POST", c.baseURL+path, bytes.NewReader(jsonBody))
	if err != nil {
		return err
	}

	req.Header.Set("Content-Type", "application/json")

	return c.doRequest(req, result)
}

func (c *Client) doRequest(req *http.Request, result interface{}) error {
	if c.appID != "" && c.appSecret != "" {
		// Add authentication headers
		req.Header.Set("X-App-ID", c.appID)
		// In production, you would sign the request using appSecret
	}

	resp, err := c.httpClient.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	respBody, err := io.ReadAll(resp.Body)
	if err != nil {
		return err
	}

	var apiResp apiResponse
	if err := json.Unmarshal(respBody, &apiResp); err != nil {
		return err
	}

	if apiResp.Code != 0 {
		return &APIError{
			Code:    fmt.Sprintf("%d", apiResp.Code),
			Message: apiResp.Message,
		}
	}

	if result != nil && len(apiResp.Data) > 0 {
		return json.Unmarshal(apiResp.Data, result)
	}

	return nil
}
