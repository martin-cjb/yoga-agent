# 🧘 瑜伽馆智能客服机器人

基于 Java + LangChain4j 的AI智能体，用于瑜伽馆客服场景。

## 快速开始

### 1. 准备API Key

推荐使用**硅基流动**（国内可用，价格便宜）:
- 访问 https://cloud.siliconflow.cn 注册
- 获取API Key

### 2. 配置

编辑 `start.sh`，修改:
```bash
export SILICON_API_KEY="你的API Key"
```

### 3. 启动

```bash
chmod +x start.sh
./start.sh
```

### 4. 测试

```bash
# 询问价格
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"你们的课程怎么收费？"}'

# 询问地址
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"你们在哪里？"}'

# 预约课程
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"我想预约明天下午的瑜伽课"}'
```

## 配置知识库

编辑 `src/main/resources/application.yml` 中的 `yoga.knowledge` 部分，自定义：
- 营业时间
- 地址电话
- 课程价格

## 下一步

- [ ] 接入微信公众号/企业微信
- [ ] 对接约课系统
- [ ] 添加会员管理功能
- [ ] 部署到云服务器

## 技术栈

- Java 17
- Spring Boot 3.2
- LangChain4j 0.35.0
- Docker