
"""
MockMentor Question Bank
"""

QUESTIONS = {
    # --- SQL ---
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

    # --- Data Pipelines ---
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

    # --- Data Modeling ---
    "model_001": {
        "id": "model_001",
        "topic": "modeling",
        "difficulty": "medium",
        "text": "Compare Star Schema vs Snowflake Schema. in 2024 with modern columnar warehouses (Snowflake, BigQuery, Redshift), which one is preferred and why?",
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

    # --- System Design ---
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
    
    # --- Debugging ---
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
    }
}
