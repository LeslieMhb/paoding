# 庖丁 (Paoding)

AI 旅行助手平台MVP 版本。

## 架构

```
paoding-java/     Spring Boot 服务，提供酒店/交通/景点查询 API（mock 数据）
paoding-python/   FastAPI + LangChain + LangGraph，AI Agent 图 + SSE 流式输出
paoding-web/      Vue3 前端，用户登录/聊天/多轮对话/流式展示
```

## 技术栈

| 服务 | 技术 | 版本 |
|------|------|------|
| Java | Spring Boot 3.2 + JDK 21 | 21 |
| Python | FastAPI + LangGraph | 3.11 |
| Frontend | Vue 3 + Vite + TypeScript | Node 22 |

## 快速启动

### Java 服务 (端口 8080)
```bash
cd paoding-java
mvn clean package
java -jar target/paoding-java.jar
```

### Python 服务 (端口 8000)
```bash
cd paoding-python
uv venv --python 3.11
uv pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Vue 前端 (端口 3000)
```bash
cd paoding-web
npm install
npm run dev
```

## 数据流

```
用户(Vue) --SSE--> Python(LangGraph) --HTTP--> Java(Mock API)
```
