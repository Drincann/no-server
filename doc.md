### 使用百度地图 api

前端引入百度地图的开放 api，使用百度地图的 JavaScript 开源库 BMapLib。

### 在 Node.js 下

后端应用基于高效率高并发的 JavaScript 环境 Node.js 开发，Node.js 是基于 Chrome V8 引擎的跨平台的 JavaScript runtime，底层提供了强大高效的异步非阻塞 I/O 接口的 C 实现。

事件驱动、非阻塞 I/O、强大的 V8 引擎。

### 后端应用基于 Koa

基于 Koa 框架，Koa 是继 express 后最受欢迎的 Node.js Web 框架，更小、更紧凑、更开放、更干净。

### 接口设计基于 GraphQL

使用 GraphQL 设计 http 接口。

**GQL（Graph Query Language）**是一种查询语言。用来设计出较 Restful api 更易于扩展和升级的接口，可以理解为 Restful api 的替代品。

通过 GraphQL 內建的静态类型检查和 Schema 定义，减少 JavaScript 作为弱类型语言在类型检查方面的弱势，同时易于接口升级、演化，减少接口冗余。

前端可以使用语义化且更自然的方式请求数据。

接口请求示例：

请求

```gql
query {
    NOLevel(
        minlat: 36.563808,
        maxlat: 36.664154,
        minlon: 114.402726,
        maxlon: 114.579512,
        year: 2019, month: 1
    ): {
        code,
        imgBase64,
        message
    }
}
```

响应示例

```json
{
    "data": {
        "NOLevel": {
            "code": 0,
            "imgBase64": {... base64 data }
        }
    }
}
```

### 核心基于 Python

接口的核心功能基于 Python 实现，Web 后端应用通过 exca 模块调用 Python 脚本，经过一系列对卫星数据的检索、处理操作绘制成图，并通过标准 IO 流与 Node.js 通信。

Python 脚本的核心逻辑将通过 getopt 封装为命令行工具，通过 matplotlib.pyplot 绘制出图后，在内存中原地 encode 为 base64 编码，并序列化为 json 写入标准输出流。

Web 后端应用将通过协定的输出格式进行 json 的反序列化，以实现进程间通信。

接口协定：

```ts
interface PyData {
    code: number;
    imgBase64?: string;
    message?: string;
}
```

