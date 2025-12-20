
"""
MockMentor Question Bank
Comprehensive Data Engineering Interview Questions
"""

QUESTIONS = {
    # ============================================================================
    # SQL (8 questions)
    # ============================================================================
    "sql_001": {
        "id": "sql_001",
        "topic": "sql",
        "difficulty": "medium",
        "text": "Write a SQL query using a window function to find the top 3 highest-paid employees in each department. Explain your choice of RANK vs DENSE_RANK vs ROW_NUMBER.",
        "hints": [
            "Think about how to group rows by department.",
            "Consider what happens if two employees have the exact same salary.",
            "You'll need a subquery or CTE to filter for rank <= 3."
        ],
        "ideal_points": [
            "Uses PARTITION BY department_id",
            "Uses ORDER BY salary DESC",
            "Explains that DENSE_RANK handles ties without skipping numbers, unlike RANK",
            "Correctly filters outside the window function"
        ]
    },
    "sql_002": {
        "id": "sql_002",
        "topic": "sql",
        "difficulty": "hard",
        "text": "How would you optimize a query that performs a join between a very large fact table (billions of rows) and a large dimension table (millions of rows) where the join is causing a skew?",
        "hints": [
            "What is data skew in the context of distributed joins?",
            "Can you break the heavy keys apart?",
            "Look up 'salting' or 'broadcast join' limitations."
        ],
        "ideal_points": [
            "Identify the skewed key problem (all data for one key going to one reducer)",
            "Suggest Salted Join (adding random prefix to keys)",
            "Mention Broadcast Join if the dimension fits in memory (but millions might be too big)",
            "Filter early before joining"
        ]
    },
    "sql_003": {
        "id": "sql_003",
        "topic": "sql",
        "difficulty": "easy",
        "text": "Explain the difference between UNION and UNION ALL. When would you use one over the other?",
        "hints": [
            "One removes duplicates, the other doesn't.",
            "Think about performance implications."
        ],
        "ideal_points": [
            "UNION removes duplicates, UNION ALL appends all rows",
            "UNION ALL is faster because it doesn't need to sort/distinct",
            "Use UNION ALL by default unless unique rows are strictly required"
        ]
    },
    "sql_004": {
        "id": "sql_004",
        "topic": "sql",
        "difficulty": "medium",
        "text": "Explain the difference between WHERE and HAVING clauses. Write a query to find departments with more than 5 employees whose average salary exceeds $100,000.",
        "hints": [
            "WHERE filters rows before grouping.",
            "HAVING filters groups after aggregation.",
            "You need GROUP BY to use HAVING."
        ],
        "ideal_points": [
            "WHERE filters individual rows before GROUP BY",
            "HAVING filters aggregated results after GROUP BY",
            "Correct query uses GROUP BY department, HAVING COUNT(*) > 5 AND AVG(salary) > 100000",
            "Cannot use aliases in HAVING in some databases"
        ]
    },
    "sql_005": {
        "id": "sql_005",
        "topic": "sql",
        "difficulty": "hard",
        "text": "Write a SQL query to find gaps in a sequence of order IDs. Orders table has order_id (integer) column. Return the start and end of each gap.",
        "hints": [
            "Use LEAD or LAG window functions.",
            "Compare each row with the next row.",
            "A gap exists when next_id - current_id > 1."
        ],
        "ideal_points": [
            "Uses LEAD(order_id) OVER (ORDER BY order_id) to get next value",
            "Filters where next_order_id - order_id > 1",
            "Returns gap_start as order_id + 1 and gap_end as next_order_id - 1",
            "Handles edge cases like the last row"
        ]
    },
    "sql_006": {
        "id": "sql_006",
        "topic": "sql",
        "difficulty": "medium",
        "text": "What is a correlated subquery? How does it differ from a regular subquery? Provide an example and discuss performance implications.",
        "hints": [
            "A correlated subquery references the outer query.",
            "It executes once per row of the outer query.",
            "Think about when you might rewrite it as a JOIN."
        ],
        "ideal_points": [
            "Correlated subquery references columns from the outer query",
            "Executes once per row (can be O(n*m) complexity)",
            "Regular subquery executes independently once",
            "Often can be rewritten as JOIN for better performance"
        ]
    },
    "sql_007": {
        "id": "sql_007",
        "topic": "sql",
        "difficulty": "easy",
        "text": "What are the different types of JOINs in SQL? Explain INNER, LEFT, RIGHT, and FULL OUTER joins with examples.",
        "hints": [
            "Think about what happens with non-matching rows.",
            "LEFT keeps all rows from the left table.",
            "FULL OUTER keeps everything from both."
        ],
        "ideal_points": [
            "INNER JOIN returns only matching rows from both tables",
            "LEFT JOIN returns all left table rows + matching right rows (NULL if no match)",
            "RIGHT JOIN returns all right table rows + matching left rows",
            "FULL OUTER JOIN returns all rows from both tables with NULLs where no match"
        ]
    },
    "sql_008": {
        "id": "sql_008",
        "topic": "sql",
        "difficulty": "hard",
        "text": "Explain query execution plans. How do you read an EXPLAIN output and identify performance bottlenecks?",
        "hints": [
            "Look for sequential scans vs index scans.",
            "Watch for high row estimates vs actual rows.",
            "Identify expensive operations like sorts and hash joins."
        ],
        "ideal_points": [
            "EXPLAIN shows the optimizer's chosen execution plan",
            "Key metrics: cost, rows, width, actual time (with ANALYZE)",
            "Sequential Scan on large tables indicates missing index",
            "Sort operations can be expensive - check for ORDER BY optimization",
            "Nested Loop joins on large tables suggest missing indexes"
        ]
    },

    # ============================================================================
    # DATA PIPELINES (8 questions)
    # ============================================================================
    "pipe_001": {
        "id": "pipe_001",
        "topic": "pipelines",
        "difficulty": "medium",
        "text": "How do you ensure idempotency in a data pipeline that writes to a data lake? What happens if the job fails halfway?",
        "hints": [
            "Idempotency means running the same job twice produces the same result.",
            "Think about overwrite modes vs append modes.",
            "Consider atomic commits or staging directories."
        ],
        "ideal_points": [
            "Write to a temporary/staging location first",
            "Atomic swap or overwrite of the target partition",
            "Avoid simple 'append' without cleanup",
            "Use unique run IDs to track processed data"
        ]
    },
    "pipe_002": {
        "id": "pipe_002",
        "topic": "pipelines",
        "difficulty": "hard",
        "text": "Design a pipeline to process real-time clickstream data with late-arriving events. How do you handle events that arrive 1 hour late vs 1 day late?",
        "hints": [
            "Look into Watermarks.",
            "What is the trade-off between latency and completeness?",
            "How does windowing help?"
        ],
        "ideal_points": [
            "Use Event Time processing (not Processing Time)",
            "Define a Watermark for acceptable lateness",
            "Send very late data to a 'dead letter' or side output for batch reprocessing",
            "Update previous results if allowed (re-statement)"
        ]
    },
    "pipe_003": {
        "id": "pipe_003",
        "topic": "pipelines",
        "difficulty": "easy",
        "text": "Explain the difference between batch processing and stream processing. When would you choose one over the other?",
        "hints": [
            "Think about latency requirements.",
            "Consider data volume and processing patterns.",
            "What about cost implications?"
        ],
        "ideal_points": [
            "Batch: processes bounded datasets, higher latency, simpler error handling",
            "Stream: processes unbounded data continuously, low latency, complex state management",
            "Batch for reporting, ML training, data warehousing",
            "Stream for real-time alerts, live dashboards, fraud detection"
        ]
    },
    "pipe_004": {
        "id": "pipe_004",
        "topic": "pipelines",
        "difficulty": "medium",
        "text": "What is backpressure in streaming systems? How do Kafka, Flink, and Spark Streaming handle it differently?",
        "hints": [
            "Backpressure occurs when downstream can't keep up with upstream.",
            "Think about buffering strategies.",
            "What happens when buffers fill up?"
        ],
        "ideal_points": [
            "Backpressure: when consumers can't keep up with producers",
            "Kafka: uses consumer lag, consumers pull at their own pace",
            "Flink: propagates backpressure upstream, slows down sources",
            "Spark: micro-batch model, adjusts batch intervals or fails"
        ]
    },
    "pipe_005": {
        "id": "pipe_005",
        "topic": "pipelines",
        "difficulty": "hard",
        "text": "Explain exactly-once semantics in distributed systems. How do Kafka transactions achieve this?",
        "hints": [
            "Think about the producer, broker, and consumer sides.",
            "What is idempotent production?",
            "How do transaction coordinators work?"
        ],
        "ideal_points": [
            "Exactly-once: each message processed exactly one time",
            "Idempotent producer: uses sequence numbers to deduplicate",
            "Transactional producer: atomic writes across partitions",
            "Consumer: read_committed isolation level",
            "End-to-end requires coordination between source, processor, and sink"
        ]
    },
    "pipe_006": {
        "id": "pipe_006",
        "topic": "pipelines",
        "difficulty": "medium",
        "text": "What is data lineage and why is it important? How would you implement lineage tracking in a modern data stack?",
        "hints": [
            "Lineage tracks where data comes from and where it goes.",
            "Think about auditing and debugging use cases.",
            "Consider tools like OpenLineage, DataHub, or Marquez."
        ],
        "ideal_points": [
            "Lineage: tracking data origin, transformations, and destinations",
            "Important for debugging, compliance (GDPR), impact analysis",
            "Implement via OpenLineage standard for interoperability",
            "Tools: DataHub, Marquez, Atlan, or custom metadata store"
        ]
    },
    "pipe_007": {
        "id": "pipe_007",
        "topic": "pipelines",
        "difficulty": "easy",
        "text": "What is a DAG in the context of data pipelines? How do tools like Airflow use DAGs?",
        "hints": [
            "DAG stands for Directed Acyclic Graph.",
            "Think about task dependencies.",
            "Why must it be acyclic?"
        ],
        "ideal_points": [
            "DAG: Directed Acyclic Graph - nodes are tasks, edges are dependencies",
            "Directed: clear parent-child relationships",
            "Acyclic: no circular dependencies (would cause infinite loops)",
            "Airflow uses DAGs to schedule and orchestrate task execution order"
        ]
    },
    "pipe_008": {
        "id": "pipe_008",
        "topic": "pipelines",
        "difficulty": "hard",
        "text": "Compare Change Data Capture (CDC) approaches: log-based vs query-based vs trigger-based. What are the trade-offs?",
        "hints": [
            "Think about performance impact on source systems.",
            "Consider data consistency guarantees.",
            "What about schema changes?"
        ],
        "ideal_points": [
            "Log-based: reads database transaction logs (Debezium), minimal impact, captures all changes",
            "Query-based: polls tables with timestamps, simpler but misses deletes",
            "Trigger-based: database triggers write to change tables, high overhead",
            "Log-based is preferred for production due to low latency and complete capture"
        ]
    },

    # ============================================================================
    # DATA MODELING (8 questions)
    # ============================================================================
    "model_001": {
        "id": "model_001",
        "topic": "modeling",
        "difficulty": "medium",
        "text": "Compare Star Schema vs Snowflake Schema. In 2024 with modern columnar warehouses (Snowflake, BigQuery, Redshift), which one is preferred and why?",
        "hints": [
            "Star schema is de-normalized. Snowflake is normalized.",
            "Storage is cheap now. Compute (joins) is expensive."
        ],
        "ideal_points": [
            "Star schema is generally preferred today",
            "Reduces number of joins needed for analytics queries",
            "Modern storage compression handles the redundancy of Star schema well",
            "Snowflake schema is harder for business users to query"
        ]
    },
    "model_002": {
        "id": "model_002",
        "topic": "modeling",
        "difficulty": "hard",
        "text": "Explain Slowly Changing Dimensions (SCD) Type 2. How do you implement it efficiently?",
        "hints": [
            "Type 2 keeps history.",
            "You need start_date, end_date, and current_flag columns."
        ],
        "ideal_points": [
            "New record inserts for changes, updates previous record's end_date",
            "Columns: Surrogate Key, Business Key, Attributes, Start Date, End Date, Is Active",
            "Efficiency: Use MERGE statement or Hash Diff to detect changes before inserting"
        ]
    },
    "model_003": {
        "id": "model_003",
        "topic": "modeling",
        "difficulty": "easy",
        "text": "What is the difference between a fact table and a dimension table? Give examples of each.",
        "hints": [
            "Facts contain measurements/metrics.",
            "Dimensions provide context (who, what, where, when).",
            "Think about an e-commerce scenario."
        ],
        "ideal_points": [
            "Fact tables: contain quantitative metrics (sales amount, quantity, clicks)",
            "Dimension tables: contain descriptive attributes (customer name, product category, date)",
            "Facts are typically narrow and very tall (many rows)",
            "Dimensions are typically wide and shorter (fewer rows)"
        ]
    },
    "model_004": {
        "id": "model_004",
        "topic": "modeling",
        "difficulty": "medium",
        "text": "What is a degenerate dimension? When would you use one instead of creating a separate dimension table?",
        "hints": [
            "Think about transaction or order numbers.",
            "Would a separate dimension table add value?",
            "Consider the granularity of the fact table."
        ],
        "ideal_points": [
            "Degenerate dimension: dimension key stored in fact table without a dimension table",
            "Common examples: order number, invoice number, transaction ID",
            "Used when dimension would only have one attribute (the key itself)",
            "Keeps the model simpler without losing analytical value"
        ]
    },
    "model_005": {
        "id": "model_005",
        "topic": "modeling",
        "difficulty": "hard",
        "text": "Explain the concept of grain in dimensional modeling. What happens if you mix grains incorrectly?",
        "hints": [
            "Grain defines what a single row represents.",
            "Think about aggregation levels.",
            "What happens when you join tables with different grains?"
        ],
        "ideal_points": [
            "Grain: the level of detail of each row in a fact table",
            "Examples: one row per order line, per day, per customer-product",
            "Mixing grains causes fan-out (duplicate counting) or fan-in (data loss)",
            "Always define grain before adding dimensions or facts"
        ]
    },
    "model_006": {
        "id": "model_006",
        "topic": "modeling",
        "difficulty": "medium",
        "text": "What is a bridge table and when do you need one? Provide an example.",
        "hints": [
            "Think about many-to-many relationships.",
            "How do you connect a fact to multiple dimension values?",
            "Consider a scenario where one order has multiple promotions."
        ],
        "ideal_points": [
            "Bridge table: resolves many-to-many relationships in dimensional models",
            "Contains foreign keys to both sides plus optional weighting factor",
            "Example: student-course enrollment, order-promotion associations",
            "Alternative to multi-valued dimensions which are harder to query"
        ]
    },
    "model_007": {
        "id": "model_007",
        "topic": "modeling",
        "difficulty": "easy",
        "text": "What is data normalization? Explain 1NF, 2NF, and 3NF with examples.",
        "hints": [
            "Normalization reduces data redundancy.",
            "Each normal form builds on the previous.",
            "Think about functional dependencies."
        ],
        "ideal_points": [
            "1NF: atomic values, no repeating groups (one value per cell)",
            "2NF: 1NF + no partial dependencies (all non-key attributes depend on full primary key)",
            "3NF: 2NF + no transitive dependencies (non-key attributes don't depend on other non-key attributes)",
            "Trade-off: normalization reduces redundancy but increases joins"
        ]
    },
    "model_008": {
        "id": "model_008",
        "topic": "modeling",
        "difficulty": "hard",
        "text": "Explain the Data Vault 2.0 modeling approach. When would you choose it over traditional Kimball dimensional modeling?",
        "hints": [
            "Think about Hubs, Links, and Satellites.",
            "Consider auditability and parallel loading.",
            "When is schema flexibility important?"
        ],
        "ideal_points": [
            "Hubs: unique business keys, Links: relationships, Satellites: descriptive attributes with history",
            "Parallel loadable due to insert-only pattern",
            "Better for highly volatile source systems with frequent schema changes",
            "Choose Kimball for simpler, more query-friendly analytics layers"
        ]
    },

    # ============================================================================
    # SYSTEM DESIGN (6 questions)
    # ============================================================================
    "sys_001": {
        "id": "sys_001",
        "topic": "system_design",
        "difficulty": "hard",
        "text": "Design a data platform for a ride-sharing app. You need to support: 1. Real-time pricing (surge) 2. Daily financial reporting. 3. Machine Learning feature store.",
        "hints": [
            "This likely requires a Lambda or Kappa architecture.",
            "Real-time needs streaming (Kafka/Flink).",
            "Reporting needs batch (Data Warehouse)."
        ],
        "ideal_points": [
            "Ingestion: Kafka for high throughput events",
            "Speed Layer: Flink/Spark Streaming for real-time pricing calculation",
            "Batch Layer: S3 Data Lake -> Snowflake/BigQuery for daily reporting",
            "Feature Store: Redis for low-latency serving, offline store for training"
        ]
    },
    "sys_002": {
        "id": "sys_002",
        "topic": "system_design",
        "difficulty": "hard",
        "text": "Design a real-time fraud detection system for a payment processor handling 10,000 transactions per second.",
        "hints": [
            "Think about latency requirements (milliseconds).",
            "How do you handle ML model inference at scale?",
            "Consider both rule-based and ML-based detection."
        ],
        "ideal_points": [
            "Ingest via Kafka with low-latency consumers",
            "Rule engine (Flink CEP) for known fraud patterns",
            "ML model served via low-latency inference (TensorFlow Serving, Triton)",
            "Feature store for real-time features (last N transactions)",
            "Async feedback loop for model retraining"
        ]
    },
    "sys_003": {
        "id": "sys_003",
        "topic": "system_design",
        "difficulty": "medium",
        "text": "Design a data lake architecture for a company migrating from an on-premise data warehouse. What are the key components?",
        "hints": [
            "Think about storage, compute, governance.",
            "Consider the medallion architecture (bronze/silver/gold).",
            "How do you handle schema evolution?"
        ],
        "ideal_points": [
            "Storage: S3/GCS/ADLS with partitioning strategy",
            "Format: Parquet or Delta Lake/Iceberg for ACID transactions",
            "Medallion: raw (bronze) -> cleaned (silver) -> aggregated (gold)",
            "Catalog: Glue/Hive Metastore for schema management",
            "Governance: column-level security, data classification"
        ]
    },
    "sys_004": {
        "id": "sys_004",
        "topic": "system_design",
        "difficulty": "medium",
        "text": "Explain the trade-offs between using a data warehouse (Snowflake/BigQuery) vs a data lakehouse (Databricks/Delta Lake).",
        "hints": [
            "Think about structured vs unstructured data.",
            "Consider cost models and use cases.",
            "What about machine learning workloads?"
        ],
        "ideal_points": [
            "Warehouse: optimized for SQL, governed, higher cost per TB, BI-friendly",
            "Lakehouse: flexible formats, ML-native, cheaper storage, more complexity",
            "Warehouse for pure analytics and reporting",
            "Lakehouse when you need ML + analytics + raw data in one place"
        ]
    },
    "sys_005": {
        "id": "sys_005",
        "topic": "system_design",
        "difficulty": "hard",
        "text": "How would you design a system to handle schema evolution in a data lake without breaking downstream consumers?",
        "hints": [
            "Think about backward and forward compatibility.",
            "Consider schema registries.",
            "What role do table formats like Iceberg play?"
        ],
        "ideal_points": [
            "Schema Registry (Confluent) for Avro/Protobuf versioning",
            "Additive changes only (new columns with defaults) for backward compatibility",
            "Delta Lake/Iceberg handle schema evolution natively",
            "Contract testing between producers and consumers",
            "Separate raw layer from transformed layer to isolate changes"
        ]
    },
    "sys_006": {
        "id": "sys_006",
        "topic": "system_design",
        "difficulty": "medium",
        "text": "Design a metric/analytics platform that serves dashboards with sub-second query latency over billions of rows.",
        "hints": [
            "Pre-aggregation vs real-time aggregation.",
            "Think about OLAP cubes.",
            "Consider tools like Druid, ClickHouse, or Pinot."
        ],
        "ideal_points": [
            "Pre-aggregate common dimensions during ingestion",
            "Use columnar OLAP database (Druid, ClickHouse, Pinot)",
            "Partition by time, cluster by high-cardinality dimensions",
            "Caching layer (Redis) for most common queries",
            "Materialized views for complex aggregations"
        ]
    },

    # ============================================================================
    # DEBUGGING & TROUBLESHOOTING (6 questions)
    # ============================================================================
    "debug_001": {
        "id": "debug_001",
        "topic": "debugging",
        "difficulty": "medium",
        "text": "Your Spark job is failing with an OutOfMemoryError (OOM) on the driver. What are the likely causes and how do you fix it?",
        "hints": [
            "Driver vs Executor memory.",
            "Are you bringing too much data back to the driver?",
            "Check for collect() calls."
        ],
        "ideal_points": [
            "Caused by `collect()` bringing dataset to driver",
            "Caused by `broadcast()` of a too-large table",
            "Fix: Remove `collect()`, increase `spark.driver.memory`, or disable broadcast join"
        ]
    },
    "debug_002": {
        "id": "debug_002",
        "topic": "debugging",
        "difficulty": "hard",
        "text": "Your Spark job is running very slowly with most tasks completing quickly but a few tasks taking 10x longer. What's happening and how do you fix it?",
        "hints": [
            "This is a data skew problem.",
            "Check the Spark UI for task distribution.",
            "Think about null values or popular keys."
        ],
        "ideal_points": [
            "Data skew: some partitions have much more data than others",
            "Common causes: null values, hot keys (popular customer IDs)",
            "Fixes: salting keys, separate handling for skewed keys",
            "Use Spark 3.0+ Adaptive Query Execution (AQE) for automatic skew handling"
        ]
    },
    "debug_003": {
        "id": "debug_003",
        "topic": "debugging",
        "difficulty": "medium",
        "text": "Your Airflow DAG is stuck and tasks are not being scheduled. How do you troubleshoot this?",
        "hints": [
            "Check the scheduler logs.",
            "Are there any upstream dependencies blocking?",
            "Look at pool and slot availability."
        ],
        "ideal_points": [
            "Check scheduler health and logs",
            "Verify upstream tasks are successful (dependencies)",
            "Check if pool/slot limits are reached",
            "Look for parsing errors in the DAG file",
            "Verify start_date and schedule_interval configuration"
        ]
    },
    "debug_004": {
        "id": "debug_004",
        "topic": "debugging",
        "difficulty": "easy",
        "text": "Your data pipeline is producing fewer rows than expected. How do you systematically debug this?",
        "hints": [
            "Think about a data quality checklist.",
            "Check each transformation step.",
            "Are there filters or joins dropping data?"
        ],
        "ideal_points": [
            "Add row counts at each transformation step",
            "Check JOIN conditions - are they too restrictive?",
            "Look for WHERE clauses filtering unexpectedly",
            "Check for NULL handling dropping rows",
            "Compare source count vs destination count"
        ]
    },
    "debug_005": {
        "id": "debug_005",
        "topic": "debugging",
        "difficulty": "hard",
        "text": "Explain how you would debug a Kafka consumer that is experiencing high consumer lag.",
        "hints": [
            "Consumer lag means messages are piling up.",
            "Think about consumer throughput vs producer rate.",
            "Check partition assignment and consumer group health."
        ],
        "ideal_points": [
            "Check consumer processing time per message",
            "Verify partition count matches consumer count",
            "Look for slow downstream dependencies (database, API)",
            "Check for consumer rebalancing issues",
            "Consider scaling consumers or increasing partitions"
        ]
    },
    "debug_006": {
        "id": "debug_006",
        "topic": "debugging",
        "difficulty": "medium",
        "text": "Your BigQuery query is scanning too much data and costs are high. How do you optimize it?",
        "hints": [
            "BigQuery charges by data scanned.",
            "Think about partitioning and clustering.",
            "Check the query execution plan."
        ],
        "ideal_points": [
            "Use partitioned tables and filter on partition column",
            "Use clustering for frequently filtered columns",
            "Select only needed columns (avoid SELECT *)",
            "Check INFORMATION_SCHEMA for table metadata before querying",
            "Use LIMIT for exploratory queries"
        ]
    },

    # ============================================================================
    # CLOUD & INFRASTRUCTURE (6 questions) - NEW TOPIC
    # ============================================================================
    "cloud_001": {
        "id": "cloud_001",
        "topic": "cloud",
        "difficulty": "medium",
        "text": "Compare the data lake storage services across AWS, GCP, and Azure. What are the key differences?",
        "hints": [
            "Think about S3, GCS, and ADLS.",
            "Consider pricing models, consistency guarantees.",
            "What about integration with compute services?"
        ],
        "ideal_points": [
            "AWS S3: most mature, strong consistency (since 2020), extensive ecosystem",
            "GCS: strong consistency, simpler pricing, native BigQuery integration",
            "ADLS Gen2: hierarchical namespace, tight Azure Synapse integration",
            "All support similar features but differ in ecosystem and pricing"
        ]
    },
    "cloud_002": {
        "id": "cloud_002",
        "topic": "cloud",
        "difficulty": "hard",
        "text": "Explain the concept of infrastructure as code (IaC). How would you use Terraform to provision a data pipeline infrastructure?",
        "hints": [
            "IaC means defining infrastructure in code files.",
            "Think about modules, state management.",
            "What are the benefits for data teams?"
        ],
        "ideal_points": [
            "IaC: version-controlled, reproducible infrastructure definitions",
            "Terraform: declarative, provider-agnostic, state management",
            "Modules for reusable components (S3 bucket, Glue job)",
            "Benefits: reproducibility, documentation, review process, disaster recovery"
        ]
    },
    "cloud_003": {
        "id": "cloud_003",
        "topic": "cloud",
        "difficulty": "easy",
        "text": "What is the difference between vertical scaling and horizontal scaling? When would you use each for data workloads?",
        "hints": [
            "Vertical: bigger machine. Horizontal: more machines.",
            "Think about limits and failure modes.",
            "Consider different types of data workloads."
        ],
        "ideal_points": [
            "Vertical: increase CPU/RAM of single machine (scale up)",
            "Horizontal: add more machines (scale out)",
            "Vertical: simpler, limited by hardware maximums",
            "Horizontal: for distributed workloads (Spark, Kafka), more resilient"
        ]
    },
    "cloud_004": {
        "id": "cloud_004",
        "topic": "cloud",
        "difficulty": "medium",
        "text": "What is Kubernetes and why might a data engineering team use it? What are the challenges?",
        "hints": [
            "K8s orchestrates containers.",
            "Think about scaling and resource management.",
            "Consider the learning curve."
        ],
        "ideal_points": [
            "Container orchestration for deploying and scaling applications",
            "Benefits: resource efficiency, autoscaling, isolation",
            "Data uses: Spark on K8s, Airflow, Flink, ML serving",
            "Challenges: complexity, networking, stateful workloads"
        ]
    },
    "cloud_005": {
        "id": "cloud_005",
        "topic": "cloud",
        "difficulty": "hard",
        "text": "Design a disaster recovery strategy for a critical data pipeline. What is your RTO and RPO?",
        "hints": [
            "RTO: how fast to recover. RPO: how much data loss acceptable.",
            "Think about multi-region replication.",
            "Consider cost vs recovery guarantees."
        ],
        "ideal_points": [
            "RTO (Recovery Time Objective): time to restore service",
            "RPO (Recovery Point Objective): acceptable data loss window",
            "Multi-region replication for storage (S3 cross-region)",
            "Standby compute infrastructure or infrastructure as code for quick rebuild",
            "Regular backup testing and runbooks"
        ]
    },
    "cloud_006": {
        "id": "cloud_006",
        "topic": "cloud",
        "difficulty": "medium",
        "text": "Explain the cost optimization strategies for cloud data platforms. How do you reduce spending without sacrificing performance?",
        "hints": [
            "Think about compute vs storage costs.",
            "Consider reserved capacity vs on-demand.",
            "What about data lifecycle policies?"
        ],
        "ideal_points": [
            "Right-size compute resources based on actual usage",
            "Use spot/preemptible instances for fault-tolerant batch jobs",
            "Reserved instances for steady-state workloads",
            "Data lifecycle: transition to cheaper storage tiers (S3 Glacier)",
            "Partition pruning and query optimization to reduce scanned data"
        ]
    },

    # ============================================================================
    # PYTHON & CODING (6 questions) - NEW TOPIC
    # ============================================================================
    "python_001": {
        "id": "python_001",
        "topic": "python",
        "difficulty": "medium",
        "text": "Explain Python generators. How would you use one to process a 100GB CSV file that doesn't fit in memory?",
        "hints": [
            "Generators use yield instead of return.",
            "Think about lazy evaluation.",
            "How do you chain generators?"
        ],
        "ideal_points": [
            "Generators produce values lazily (one at a time)",
            "Use with open() and iterate line by line",
            "Yield processed rows without loading entire file",
            "Chain with other generators for transformation pipelines"
        ]
    },
    "python_002": {
        "id": "python_002",
        "topic": "python",
        "difficulty": "easy",
        "text": "What is the difference between a list and a tuple in Python? When would you use each?",
        "hints": [
            "One is mutable, one is immutable.",
            "Think about hashability.",
            "Consider performance and intent."
        ],
        "ideal_points": [
            "List: mutable, can add/remove elements",
            "Tuple: immutable, hashable, can be dictionary keys",
            "Tuple for fixed collections (coordinates, DB rows)",
            "List for collections that change (appending results)"
        ]
    },
    "python_003": {
        "id": "python_003",
        "topic": "python",
        "difficulty": "hard",
        "text": "Explain Python's Global Interpreter Lock (GIL). How does it affect data processing and what are the workarounds?",
        "hints": [
            "GIL prevents true multi-threading for CPU work.",
            "Think about I/O-bound vs CPU-bound tasks.",
            "Consider multiprocessing, async, or external libraries."
        ],
        "ideal_points": [
            "GIL: only one thread executes Python bytecode at a time",
            "Limits CPU-bound parallelism with threads",
            "I/O-bound work (network, disk) releases GIL and benefits from threading",
            "Workarounds: multiprocessing, NumPy (releases GIL), async for I/O"
        ]
    },
    "python_004": {
        "id": "python_004",
        "topic": "python",
        "difficulty": "medium",
        "text": "How do you handle errors gracefully in a data pipeline written in Python? Show patterns for retry and logging.",
        "hints": [
            "Think about try/except structure.",
            "Consider exponential backoff.",
            "What information should you log?"
        ],
        "ideal_points": [
            "Use specific exception types, not bare except",
            "Implement retry with exponential backoff (tenacity library)",
            "Log: timestamp, error type, context (row ID, file name)",
            "Dead letter queue pattern: capture failed records for later review"
        ]
    },
    "python_005": {
        "id": "python_005",
        "topic": "python",
        "difficulty": "easy",
        "text": "What are decorators in Python? Give an example of a useful decorator for data engineering.",
        "hints": [
            "Decorators wrap functions to add behavior.",
            "Think about logging, timing, retry.",
            "Use @ syntax to apply."
        ],
        "ideal_points": [
            "Decorators are functions that modify other functions",
            "Common uses: @retry, @log_execution_time, @validate_input",
            "Example: timing decorator to measure function execution time",
            "Keep decorators focused on single responsibility"
        ]
    },
    "python_006": {
        "id": "python_006",
        "topic": "python",
        "difficulty": "hard",
        "text": "Compare Pandas vs PySpark vs Polars for data processing. When would you choose each?",
        "hints": [
            "Think about data size and distribution.",
            "Consider API familiarity and ecosystem.",
            "What about memory efficiency?"
        ],
        "ideal_points": [
            "Pandas: single machine, up to ~10GB, rich ecosystem, familiar",
            "PySpark: distributed, TB+ scale, lazy evaluation, cluster required",
            "Polars: single machine like Pandas but much faster, Rust-based",
            "Choose based on data size, infrastructure, and team familiarity"
        ]
    },

    # ============================================================================
    # DATA QUALITY (6 questions) - NEW TOPIC
    # ============================================================================
    "quality_001": {
        "id": "quality_001",
        "topic": "data_quality",
        "difficulty": "medium",
        "text": "What are the dimensions of data quality? How would you measure each one?",
        "hints": [
            "Think beyond just 'correct' data.",
            "Consider completeness, timeliness, consistency.",
            "How do you quantify each dimension?"
        ],
        "ideal_points": [
            "Completeness: % of non-null required fields",
            "Accuracy: correctness verified against source of truth",
            "Consistency: same data matches across systems",
            "Timeliness: data freshness meets SLA",
            "Uniqueness: no unexpected duplicates"
        ]
    },
    "quality_002": {
        "id": "quality_002",
        "topic": "data_quality",
        "difficulty": "hard",
        "text": "Design a data quality monitoring system. What checks would you implement and how would you alert on failures?",
        "hints": [
            "Think about Great Expectations or dbt tests.",
            "Consider different check levels: row, column, table.",
            "How do you avoid alert fatigue?"
        ],
        "ideal_points": [
            "Schema validation: column types, required fields",
            "Row-level: null checks, regex patterns, value ranges",
            "Aggregate: row count changes, unique count, distribution shifts",
            "Tools: Great Expectations, dbt tests, Monte Carlo",
            "Alert on anomalies vs thresholds, aggregate failures, escalation paths"
        ]
    },
    "quality_003": {
        "id": "quality_003",
        "topic": "data_quality",
        "difficulty": "easy",
        "text": "What is a data contract? Why are they important in a decentralized data organization?",
        "hints": [
            "Think about producer-consumer relationships.",
            "Consider schema, SLAs, ownership.",
            "How do you enforce contracts?"
        ],
        "ideal_points": [
            "Data contract: formal agreement between producer and consumer",
            "Defines: schema, SLAs (freshness, availability), ownership",
            "Important for decentralized orgs to prevent breaking changes",
            "Enforce via CI/CD checks, schema registries, automated testing"
        ]
    },
    "quality_004": {
        "id": "quality_004",
        "topic": "data_quality",
        "difficulty": "medium",
        "text": "How do you detect and handle duplicate records in a data pipeline?",
        "hints": [
            "Duplicates can come from retries or source issues.",
            "Think about deduplication keys.",
            "When do you dedupe: ETL or query time?"
        ],
        "ideal_points": [
            "Define natural key or composite key for deduplication",
            "Detect: GROUP BY key HAVING COUNT(*) > 1",
            "Handle: keep first/last by timestamp, or aggregate",
            "Dedupe in ETL preferred over query time for consistency",
            "Use QUALIFY or window functions for efficient deduplication"
        ]
    },
    "quality_005": {
        "id": "quality_005",
        "topic": "data_quality",
        "difficulty": "hard",
        "text": "Explain anomaly detection for data quality. How would you detect unexpected changes in data distributions?",
        "hints": [
            "Think about statistical methods.",
            "Consider historical baselines.",
            "What about seasonality?"
        ],
        "ideal_points": [
            "Track metrics over time: row counts, null rates, value distributions",
            "Statistical: z-score for detecting outliers from historical mean",
            "Handle seasonality: compare to same day last week, not yesterday",
            "ML-based: train models on normal patterns, alert on anomalies"
        ]
    },
    "quality_006": {
        "id": "quality_006",
        "topic": "data_quality",
        "difficulty": "medium",
        "text": "What is data observability? How does it differ from traditional monitoring?",
        "hints": [
            "Observability is about understanding internal state from external outputs.",
            "Think about the five pillars: freshness, volume, schema, distribution, lineage.",
            "Consider proactive vs reactive."
        ],
        "ideal_points": [
            "Observability: holistic view of data health across pipelines",
            "Five pillars: freshness, volume, schema, distribution, lineage",
            "Traditional monitoring: predefined metrics, reactive",
            "Observability: detects unknown-unknowns, proactive anomaly detection",
            "Tools: Monte Carlo, Bigeye, Datadog for data"
        ]
    },
}

# Topic metadata for UI display
TOPICS = {
    "sql": {
        "name": "SQL",
        "description": "Window functions, query optimization, joins, and advanced SQL concepts",
        "question_count": 8
    },
    "pipelines": {
        "name": "Data Pipelines",
        "description": "ETL design, streaming, batch processing, orchestration",
        "question_count": 8
    },
    "modeling": {
        "name": "Data Modeling",
        "description": "Star schema, dimensional modeling, SCDs, normalization",
        "question_count": 8
    },
    "system_design": {
        "name": "System Design",
        "description": "Data platform architecture, scalability, distributed systems",
        "question_count": 6
    },
    "debugging": {
        "name": "Debugging",
        "description": "Spark troubleshooting, performance issues, pipeline debugging",
        "question_count": 6
    },
    "cloud": {
        "name": "Cloud & Infrastructure",
        "description": "AWS/GCP/Azure, IaC, Kubernetes, cost optimization",
        "question_count": 6
    },
    "python": {
        "name": "Python & Coding",
        "description": "Python concepts, data processing libraries, best practices",
        "question_count": 6
    },
    "data_quality": {
        "name": "Data Quality",
        "description": "Data validation, observability, contracts, anomaly detection",
        "question_count": 6
    }
}


def get_questions_by_topic(topic: str) -> list:
    """Get all questions for a specific topic."""
    return [q for q in QUESTIONS.values() if q["topic"] == topic]


def get_question_by_id(question_id: str) -> dict:
    """Get a specific question by ID."""
    return QUESTIONS.get(question_id)


def get_all_topics() -> list:
    """Get list of all available topics."""
    return list(TOPICS.keys())
