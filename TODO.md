# FinSight 后端开发 - TODO 列表

## 阶段 0: 环境与基础设置 (Environment & Foundation)

* [x] 1. (结构) 创建 `finsight-backend` 根目录及 `/app`, `/collection` 两个子目录。
* [x] 2. (结构) 创建所有子目录和空的 `__init__.py` 文件，保持Python模块化。
* [ ] 3. (环境) 创建并激活Python虚拟环境 (`venv`)。
* [x] 4. (依赖) 填写 `requirements.txt` (fastapi, uvicorn, crewai, python-dotenv, psycopg2-binary, tushare, qdrant-client, PyMuPDF, sentence-transformers, tqdm)。
* [ ] 5. (环境) 运行 `pip install -r requirements.txt`。
* [ ] 6. (配置) 填写 `.env` 文件，包含所有4个服务的密钥/连接串 (Tushare, Supabase, Qdrant, GLM)。
* [x] 7. (配置) 填写 `config.py`，定义 `LOOKBACK_DAYS`, `DB_BATCH_SIZE`, `EMBEDDING_MODEL` 等常量。
* [ ] 8. **[关键]** 运行 `python migration_comprehensive_setup.py`，在Supabase上创建所有数据库表、索引和备注。

---

## 阶段 1: 离线数据管道 (`/collection`)

**目标：** 构建健壮、高效、可重复运行的数据采集脚本。

* [ ] 1. **(Supabase)** `db_handler.py`:
    * [ ] 1.1. 实现 `__init__` (连接池) 和 `__exit__` (关闭连接)。
    * [ ] 1.2. 实现 `upsert_data()`: **通用的UPSERT函数** (`ON CONFLICT DO UPDATE`)，用于写入三张财务报表和`financial_indicators`。(优化点)
    * [ ] 1.3. 实现 `batch_insert_chunks()`: 批量插入 `chunks` 表。(批量优化)
    * [ ] 1.4. 实现 `upsert_document_status()`: 用于 `documents` 表的状态流转 (`PENDING` -> `PROCESSING` -> `COMPLETED`/`FAILED`)。
    * [ ] 1.5. 实现 `filter_existing_reports()`: (检查 `documents` 表 `status='COMPLETED'`)，用于增量更新时去重。

* [ ] 2. **(Tushare)** `tushare_handler.py`:
    * [ ] 2.1. 实现 `__init__` (初始化 Tushare Pro API)。
    * [ ] 2.2. 实现 `get_stock_basic()`: 获取公司主数据。
    * [ ] 2.3. 实现 `get_notices(start_date, end_date)`: **批量**获取所有公告。(批量优化)
    * [ ] 2.4. **[遗漏点补充]** 实现 `get_income(ts_code, ...)`。
    * [ ] 2.5. **[遗漏点补充]** 实现 `get_balance_sheet(ts_code, ...)`。
    * [ ] 2.6. **[遗漏点补充]** 实现 `get_cash_flow(ts_code, ...)`。
    * [ ] 2.7. **[遗漏点补充]** 实现 `get_fina_indicator(ts_code, ...)`。

* [ ] 3. **(Qdrant)** `vector_handler.py`:
    * [ ] 3.1. 实现 `__init__` (连接Qdrant, 加载`EMBEDDING_MODEL`模型)。
    * [ ] 3.2. 实现 `_ensure_collection_exists()` (检查并创建集合)。
    * [ ] 3.3. 实现 `batch_upsert_vectors()`: **批量**嵌入文本并上传。(批量优化)

* [ ] 4. **(PDF)** `pdf_processor.py`:
    * [ ] 4.1. **[难点细化]** 实现 `discover_pdf_url(ts_code, ann_date, title)`: 核心爬虫逻辑，模拟请求巨潮资讯网，找到真实的PDF下载链接。
    * [ ] 4.2. 实现 `download_pdf(url)`: (使用 `requests`, 处理超时)。
    * [ ] 4.3. 实现 `parse_pdf(pdf_content)`: (使用 PyMuPDF)。
    * [ ] 4.4. 实现 `chunk_text(text)`: (使用 `RecursiveCharacterTextSplitter` 等)。

* [ ] 5. **(核心逻辑)** `pipeline_logic.py`:
    * [ ] 5.1. 实现 `process_single_report(report_notice)` 函数，该函数**必须**：
        * [ ] 包含一个完整的 `try...except` 块。
        * [ ] `try` 块中按顺序调用：`db.upsert_document_status(PENDING)` -> **(定量)** `tushare.get_...` (x4) -> `db.upsert_data` (x4) -> **(定性)** `pdf.discover_url` -> `pdf.download` -> `pdf.parse` -> `pdf.chunk` -> `db.batch_insert_chunks` & `vector.batch_upsert_vectors` (RAG) -> `db.upsert_document_status(COMPLETED)`。
        * [ ] `except` 块中调用 `db.upsert_document_status(FAILED)` 并记录详细错误。

* [ ] 6. **(主入口)** `collection/main.py`:
    * [ ] 6.1. 实现 `argparse` 来解析 `--mode` (`full` / `incremental`)。
    * [ ] 6.2. 编写主函数：初始化所有 Handlers -> `tushare.get_notices` (批量) -> `db.filter_existing_reports` (去重) -> `tqdm` 循环遍历任务 -> 调用 `pipeline_logic.process_single_report()`。

* [ ] 7. **[验证]** 运行 `python collection/main.py --mode=incremental`，检查Supabase和Qdrant中的数据是否完整、正确，`documents`表状态是否为`COMPLETED`。

---

## 阶段 2: 在线AI分析服务 (`/app`)

**目标：** 构建高精度、确定性的CrewAI装配线，并通过FastAPI暴露。

* [ ] 1. **(工具)** `tools/` 目录 (Agent 2 的“武器库”):
    * [ ] 1.1. `db_tools.py`: 实现 `@tool def tool_get_trend_data(...)` (查询`financial_indicators`等表)。
    * [ ] 1.2. `db_tools.py`: **[遗漏点补充]** 实现 `@tool def tool_get_comparison_data(...)` (循环查询多公司数据)。
    * [ ] 1.3. `rag_tools.py`: 实现 `@tool def tool_get_rag_context(...)` (查询Qdrant获取原文片段)。
    * [ ] 1.4. `realtime_tools.py`: 实现 `@tool def tool_get_realtime_quote(...)` (调用Tushare `daily` 和 `daily_basic`)。
    * [ ] 1.5. **[关键]** 确保所有 `@tool` 函数都有**清晰的 `docstring`** 和 **Pydantic `args_schema`**，以便CrewAI能正确解析和调用。

* [ ] 2. **(Prompts)** `prompts.py`:
    * [ ] 2.1. 复制/粘贴我们最终确定的**意图分析Prompt** (`INTENT_ANALYSIS_PROMPT`)。
    * [ ] 2.2. 复制/粘贴我们最终确定的**综合分析Prompt** (`MAIN_FRAMEWORK_PROMPT` 和 `TASK_BLOCKS`)。

* [ ] 3. **(CrewAI)** `agents.py`:
    * [ ] 3.1. 定义 `Agent 1: RequestAnalystAgent` (引用`INTENT_ANALYSIS_PROMPT`, 使用GLM快速模型, `temperature=0.0`)。
    * [ ] 3.2. 定义 `Agent 2: DataRetrievalAgent` (绑定 `tools/` 中的所有 `@tool` 函数, 使用GLM快速模型)。
    * [ ] 3.3. 定义 `Agent 3: FinancialSynthesisAgent` (引用`MAIN_FRAMEWORK_PROMPT`和`TASK_BLOCKS`, 使用GLM强大模型)。

* [ ] 4. **(CrewAI)** `tasks.py`:
    * [ ] 4.1. 定义 `Task 1: analyze_intent` (分配给Agent 1, `expected_output` 是“执行蓝图”JSON)。
    * [ ] 4.2. 定义 `Task 2: retrieve_data` (分配给Agent 2, `context=[task_1]`)。
    * [ ] 4.3. 定义 `Task 3: synthesize_report` (分配给Agent 3, `context=[task_2]`)。

* [ ] 5. **(CrewAI)** `crew.py`:
    * [ ] 5.1. 导入Agents和Tasks。
    * [ ] 5.2. 组装并创建 `Crew(agents=..., tasks=..., process=Process.sequential)`。

* [ ] 6. **(FastAPI)** `schemas.py`:
    * [ ] 6.1. 定义Pydantic模型 `AnalyzeRequest` (包含 `user_query: str`)。

* [ ] 7. **(FastAPI)** `app/main.py`:
    * [ ] 7.1. 导入 `crew.py` 中的 `financial_crew`。
    * [ ] 7.2. 创建FastAPI实例 `app`。
    * [ ] 7.3. **[遗漏点补充]** 实现**结构化日志记录** (例如使用 `loguru`)。
    * [ ] 7.4. **[安全优化]** 实现内部密钥 `X-Internal-Auth-Key` 的依赖注入验证函数。
    * [ ] 7.5. 定义 `/analyze` (POST) 路由 (依赖内部密钥验证)。
    * [ ] 7.6. 在路由中：接收`AnalyzeRequest` -> 调用 `financial_crew.kickoff(inputs={'user_query': ...})` -> 记录日志 -> 返回最终报告。

* [ ] 8. **[验证]** 运行 `uvicorn app.main:app --reload`，并使用Postman或curl（携带 `X-Internal-Auth-Key` 头）向 `http://127.0.0.1:8000/analyze` 发送请求，验证端到端流程是否跑通。

---

## 阶段 3: 部署与集成 (Deployment & Integration)

* [ ] 1. 编写 `Dockerfile` 用于 `finsight-backend`。
* [ ] 2. 编写 `docker-compose.yml` (如果本地需要)。
* [ ] 3. 将 `finsight-backend` 部署到云服务器（如ECS/EC2）或容器服务（如K8s/Cloud Run）。
* [ ] 4. 在 `finsight-app` (Next.js) 的 `.env` 文件中配置 `AGENT_SERVICE_URL` 和 `INTERNAL_S2S_KEY`。
* [ ] 5. 编写 `finsight-app/app/api/analyze/route.ts` 的BFF转发逻辑（**必须**包含 `INTERNAL_S2S_KEY`）。
* [ ] 6. **[全流程验证]** 从 `finsight-app` 的UI发起请求，确保全链路（`UI -> BFF -> CrewAI -> DBs -> LLM -> UI`）通畅。
* [ ] 7. 为 `collection/main.py` 设置 `cron` 定时任务 (例如 `0 2 * * *` / 每天凌晨2点执行增量更新)。