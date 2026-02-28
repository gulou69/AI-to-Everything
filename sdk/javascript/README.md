# A2E JavaScript/TypeScript SDK

A2E协议的官方JavaScript/TypeScript SDK。

## 安装

```bash
npm install a2e-protocol
# 或
yarn add a2e-protocol
# 或
pnpm add a2e-protocol
```

## 快速开始

```typescript
import { A2EClient } from 'a2e-protocol';

// 创建客户端
const client = new A2EClient({
  baseURL: 'https://api.a2e-platform.com',
  appId: 'your_app_id',
  appSecret: 'your_app_secret',
});

// 搜索服务
const services = await client.searchServices({
  keyword: '奶茶',
  page: 1,
  size: 10,
});

console.log(`找到 ${services.list.length} 个服务`);

// 获取服务协议
const protocol = await client.getProtocol(services.list[0].id);
console.log(`服务: ${protocol.service.name}`);
console.log(`描述: ${protocol.semantic.description}`);

// 执行服务
const result = await client.execute({
  serviceId: services.list[0].id,
  endpoint: 'get_menu',
  consumerToken: 'user_token_xxx',
  input: {},
});

console.log('执行结果:', result.output);
```

## API文档

### Client

```typescript
import { A2EClient } from 'a2e-protocol';

const client = new A2EClient({
  baseURL: 'https://api.a2e-platform.com',  // API地址
  appId: 'your_app_id',                      // AppID（可选）
  appSecret: 'your_app_secret',              // AppSecret（可选）
  timeout: 30000,                            // 超时时间（毫秒）
});
```

### 搜索服务

```typescript
const result = await client.searchServices({
  keyword: '奶茶',
  type: 'food_delivery',  // 可选
  location: {             // 可选
    latitude: 31.2304,
    longitude: 121.4737,
  },
  page: 1,
  size: 10,
});
```

### 获取服务协议

```typescript
const protocol = await client.getProtocol(serviceId);
```

### 执行服务

```typescript
const result = await client.execute({
  serviceId: 'service_001',
  endpoint: 'get_menu',
  consumerToken: 'token_xxx',
  input: {},
});
```

### 获取用户Token

```typescript
const auth = await client.getConsumerToken({
  authType: 'wechat',
  authCode: 'wechat_auth_code',
});

console.log(auth.consumerToken);
```

## TypeScript 类型

SDK 完全使用 TypeScript 编写，提供完整的类型定义：

```typescript
import type {
  Service,
  Protocol,
  SearchResult,
  ExecuteResult,
  AuthResult,
  A2EError,
} from 'a2e-protocol';
```

## 错误处理

```typescript
import { A2EError } from 'a2e-protocol';

try {
  const result = await client.execute({...});
} catch (error) {
  if (error instanceof A2EError) {
    console.log(`API错误: ${error.code} - ${error.message}`);
  }
}
```

## 浏览器使用

SDK 同时支持 Node.js 和浏览器环境：

```html
<script type="module">
  import { A2EClient } from 'https://unpkg.com/a2e-protocol@latest/dist/index.mjs';
  
  const client = new A2EClient({
    baseURL: 'https://api.a2e-platform.com',
  });
  
  // ...
</script>
```

## License

Apache License 2.0
