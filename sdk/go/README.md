# A2E Go SDK

A2E协议的官方Go语言SDK。

## 安装

```bash
go get github.com/gulou69/AI-to-Everything/sdk/go
```

## 快速开始

```go
package main

import (
    "context"
    "fmt"
    "log"

    a2e "github.com/gulou69/AI-to-Everything/sdk/go"
)

func main() {
    // 创建客户端
    client := a2e.NewClient(
        a2e.WithBaseURL("https://api.a2e-platform.com"),
        a2e.WithTimeout(30),
    )

    ctx := context.Background()

    // 搜索服务
    services, err := client.SearchServices(ctx, &a2e.SearchRequest{
        Keyword: "奶茶",
        Page:    1,
        Size:    10,
    })
    if err != nil {
        log.Fatal(err)
    }

    fmt.Printf("找到 %d 个服务\n", len(services.List))

    // 获取服务协议
    protocol, err := client.GetProtocol(ctx, services.List[0].ID)
    if err != nil {
        log.Fatal(err)
    }

    fmt.Printf("服务: %s\n", protocol.Service.Name)
    fmt.Printf("描述: %s\n", protocol.Semantic.Description)

    // 执行服务
    result, err := client.Execute(ctx, &a2e.ExecuteRequest{
        ServiceID:     services.List[0].ID,
        Endpoint:      "get_menu",
        ConsumerToken: "user_token_xxx",
        Input:         map[string]interface{}{},
    })
    if err != nil {
        log.Fatal(err)
    }

    fmt.Printf("执行结果: %v\n", result.Output)
}
```

## API文档

### Client

```go
// 创建客户端
client := a2e.NewClient(options...)

// 可用选项
a2e.WithBaseURL(url string)      // 设置API地址
a2e.WithTimeout(seconds int)     // 设置超时时间
a2e.WithAppID(appID string)      // 设置AppID
a2e.WithAppSecret(secret string) // 设置AppSecret
```

### 搜索服务

```go
result, err := client.SearchServices(ctx, &a2e.SearchRequest{
    Keyword:  "奶茶",           // 搜索关键词
    Type:     "food_delivery", // 服务类型（可选）
    Location: &a2e.Location{   // 位置（可选）
        Latitude:  31.2304,
        Longitude: 121.4737,
    },
    Page: 1,
    Size: 10,
})
```

### 获取服务协议

```go
protocol, err := client.GetProtocol(ctx, serviceID)
```

### 执行服务

```go
result, err := client.Execute(ctx, &a2e.ExecuteRequest{
    ServiceID:     "service_001",
    Endpoint:      "get_menu",
    ConsumerToken: "token_xxx",
    Input:         map[string]interface{}{},
})
```

### 获取用户Token

```go
token, err := client.GetConsumerToken(ctx, &a2e.AuthRequest{
    Type: "wechat",
    Code: "wechat_auth_code",
})
```

## 错误处理

```go
result, err := client.Execute(ctx, req)
if err != nil {
    if apiErr, ok := err.(*a2e.APIError); ok {
        fmt.Printf("API错误: %s - %s\n", apiErr.Code, apiErr.Message)
    }
}
```

## 完整示例

参见 [examples/](../../examples/) 目录。

## License

Apache License 2.0
