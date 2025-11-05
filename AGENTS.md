## 2. BFF后端规范 (Backend/BFF - `finsight-app/api`)

### 2.1 核心理念：“安全网关与转发器” (The Secure Gateway & Forwarder)

BFF（Next.js API路由）是系统的“**贴身保镖**”。它不执行AI逻辑，但它**保护**AI逻辑。它负责处理所有面向公网的Web安全事务，并安全地将请求转发给内部的Python AI服务。

### 2.2 必须遵守的标准 (Standards)

1.  **【安全】 绝对的密钥隔离:**
    * **所有**密钥（`AGENT_SERVICE_URL`, `INTERNAL_S2S_KEY`等）**必须**通过环境变量从部署平台（如Vercel）注入。
    * **严禁**将这些密钥以任何形式暴露给前端。

2.  **【安全】 认证与授权 (未来):**
    * 此BFF是执行用户认证（如NextAuth.js, Clerk）的理想场所。
    * 在调用内部Python AI服务之前，**必须**先验证用户的登录状态和权限。

3.  **【职责】 纯粹的请求转发:**
    * BFF的核心职责是验证请求，然后将其**原封不动地转发**给`AGENT_SERVICE_URL`（即Python/CrewAI后端）。
    * 它**不应**参与任何Prompt组装或AI逻辑。

4.  **【健壮性】 超时与错误处理:**
    * 对内部Python服务的`fetch`调用**必须**设置一个合理的超时时间（例如30秒），以防止Serverless函数超时。
    * **必须**能优雅地处理Python服务返回的HTTP错误（如 `500`, `503`），并将其转换为对前端友好的错误JSON。

5.  **【安全】 内部服务认证 (推荐):**
    * BFF在调用Python后端时，**应**在请求头中加入一个内部共享的密钥（`X-Internal-Auth-Key`），Python后端**必须**验证此密钥。这确保了只有您的BFF可以调用您昂贵的AI服务。

---

## 3. AI后端规范 (AI Backend - `finsight-backend`)

这是系统的“**智能大脑**”，分为 `/collection` (离线) 和 `/app` (在线) 两部分。

### 3.1 规范 (A): 离线数据采集 (`/collection`)

#### 核心理念：“知识库的建造者” (The Knowledge Base Creator)

此智能体的标准是关于**数据质量、完整性和RAG就绪性**。

1.  **【数据】 RAG-Ready (孪生标准):**
    * 这是RAG系统的核心。在向Supabase `chunks` 表插入文本块时，其生成的 `id` (UUID) **必须**被用作Qdrant中对应向量的 `id`。

2.  **【数据】 强制元数据 (Metadata Mandate):**
    * 每一个上传到Qdrant的向量**必须**携带一个结构化的元数据`payload`（例如 `{"ts_code": "600519", "year": 2024, "period": "FY", "doc_id": "..."}`）。
    * 缺少元数据的向量是“死”数据，无法被`Agent 2`（检索智能体）精确过滤。

3.  **【数据】 UPSERT 逻辑:**
    * 所有从Tushare获取的结构化财务数据（三张报表、指标表）**必须**使用`UPSERT` (`ON CONFLICT...`) 逻辑写入数据库，以确保数据能被“更正公告”所更新。

4.  **【性能】 批量化标准:**
    * 所有对外部API（`notice`）的调用**必须**是批量的（按日期范围，而非按公司循环）。
    * 所有对数据库的写入（`chunks`表, 向量库）**必须**是批量化的（按`DB_BATCH_SIZE`配置）。

5.  **【健壮性】 状态追踪与错误隔离:**
    * **必须**通过`documents.status`字段追踪每个文档的处理生命周期。
    * `try...except`块**必须**能隔离单个财报的处理失败，防止其TTC (Time To Crash) 导致整个脚本中断。

### 3.2 规范 (B): 在线AI分析 (`/app` - CrewAI)

#### 核心理念：“高精度的智能体装配线” (The High-Precision Agent Assembly Line)

此智能体的标准是关于**流程控制、成本管理和结果可靠性**。

1.  **【架构】 确定性流程 (The Assembly Line Standard):**
    * **严禁**构建“完全自主思考”的Agent。
    * MVP的AI流程**必须**遵循我们设计的**确定性、顺序化**的“装配线”：`Task 1 (Intent)` -> `Task 2 (Retrieve)` -> `Task 3 (Synthesize)`。
    * `Agent 2`（检索）**必须**通过调用预定义的Python工具 (`@tool`) 来获取数据，**严禁**给它“自主思考”如何查询数据的能力。

2.  **【Prompt】 集中管理标准:**
    * **严禁**在`agents.py`或`tasks.py`中硬编码Prompt。
    * 所有Prompt**必须**从中心的`prompts.py`文件中加载。
    * `Agent 1`**必须**使用“意图分析Prompt”，`Agent 3`**必须**使用“综合分析Prompt”。

3.  **【LLM】 成本与性能隔离:**
    * `Agent 1`（意图分析）**必须**使用轻量级、低成本的快速LLM。
    * `Agent 3`（综合分析）**必须**使用强大的、高质量的LLM。
    * 这种隔离确保了在保持高质量输出的同时，最大限度地控制成本。

4.  **【可靠性】 遵守核心原则 (Agent 3):**
    * `Agent 3`（综合分析）的Prompt**必须**包含**“绝对事实性”、“可追溯性”、“客观中立”**和**“结构化JSON输出”**的核心原则约束。
    * 它的任务是“基于材料的总结”，**严禁**它访问外部知识或进行任何猜测。