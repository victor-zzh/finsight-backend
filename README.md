finsight-backend/
├── .env                # (!!!) 存储所有密钥: Tushare, Supabase, Qdrant, GLM
├── .gitignore          # 忽略 venv, __pycache__, .env, *.pdf
├── config.py           # 存储可配置参数 (LOOKBACK_DAYS, DB_BATCH_SIZE, EMBEDDING_MODEL)
├── migration_comprehensive_setup.py  # [已完成] 数据库迁移脚本
├── requirements.txt    # 所有Python依赖 (fastapi, uvicorn, crewai, tushare, psycopg2-binary, ...)
│
├── app/                # [在线分析服务 - FastAPI & CrewAI]
│   ├── __init__.py
│   ├── main.py         # FastAPI 服务器主入口 (定义 /analyze 路由)
│   ├── agents.py       # 定义 Agent 1(解析), Agent 2(检索), Agent 3(分析)
│   ├── tasks.py        # 定义 Task 1, 2, 3 (与Agent一一对应)
│   ├── crew.py         # 组装 Agents 和 Tasks, 定义并创建 Sequential Crew
│   ├── prompts.py      # [关键] 存储 Agent 1(意图分析) 和 Agent 3(综合分析) 的Prompt模板
│   ├── schemas.py      # Pydantic模型 (用于 /analyze 的请求和响应体校验)
│   └── tools/
│       ├── __init__.py
│       ├── db_tools.py       # (Supabase/PG) 趋势/对比查询工具
│       ├── rag_tools.py      # (Qdrant) 定性问答工具
│       └── realtime_tools.py # (Tushare) 实时行情工具
│
└── collection/         # [离线数据管道]
    ├── __init__.py
    ├── main.py         # 采集脚本主入口 (argparse for --mode)
    ├── pipeline_logic.py # 完整的工作流逻辑 (try/except, 循环, 状态管理)
    ├── db_handler.py     # 封装 Supabase/PG 交互 (UPSERT, filter, batch_insert)
    ├── tushare_handler.py# 封装 Tushare API (batch notice, financials)
    ├── pdf_processor.py  # 下载/解析/切分 PDF (包含爬虫逻辑)
    └── vector_handler.py   # 封装 Qdrant 交互 (batch upsert, 嵌入模型)