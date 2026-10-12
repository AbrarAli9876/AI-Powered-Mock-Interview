from __future__ import annotations

from collections import Counter

from app.database import SessionLocal
from app.enums.question_difficulty import QuestionDifficulty
from app.models.question import Question
from app.models.topic import Topic


TOPIC_NAME = "SQL"

# Based on "SQL Interview Questions with Answers (Top Companies).pdf".
# Company tags reflect the PDF's reported/inferred attribution, not official question banks.
QUESTIONS = [
    # EASY — Core Fundamentals (20)
    {
        "difficulty": QuestionDifficulty.EASY,
        "question_text": "What is SQL? What are the types of SQL commands?",
        "expected_answer": "SQL (Structured Query Language) defines, queries, and manages relational data. DDL includes CREATE, ALTER, DROP, TRUNCATE; DML includes INSERT, UPDATE, DELETE, MERGE; DQL includes SELECT; DCL includes GRANT and REVOKE; TCL includes COMMIT, ROLLBACK, SAVEPOINT.",
        "companies": ["Zoho", "Oracle", "Amazon", "Flipkart", "Microsoft"],
    },
    {
        "difficulty": QuestionDifficulty.EASY,
        "question_text": "What is the difference between DBMS and RDBMS?",
        "expected_answer": "A DBMS stores and manages data using different models. An RDBMS uses related tables with rows and columns, keys, constraints, SQL, and transaction support such as ACID. Examples include Oracle, MySQL, PostgreSQL, and SQL Server.",
        "companies": ["Zoho", "Oracle", "Flipkart"],
    },
    {
        "difficulty": QuestionDifficulty.EASY,
        "question_text": "What is the difference between DELETE, TRUNCATE, and DROP?",
        "expected_answer": "DELETE removes selected rows and can use WHERE. TRUNCATE quickly removes all rows and cannot use WHERE; rollback behavior depends on the database. DROP removes the table itself, including its structure and associated indexes and constraints.",
        "companies": ["Zoho", "Oracle", "Amazon", "Flipkart"],
    },
    {
        "difficulty": QuestionDifficulty.EASY,
        "question_text": "What is the difference between WHERE and HAVING?",
        "expected_answer": "WHERE filters individual rows before grouping and cannot normally filter using aggregate results. HAVING filters groups after GROUP BY and can use aggregates. Put non-aggregate filters in WHERE when possible.",
        "companies": ["Zoho", "Amazon", "Goldman Sachs", "Microsoft"],
    },
    {
        "difficulty": QuestionDifficulty.EASY,
        "question_text": "What is the difference between primary, unique, and foreign keys?",
        "expected_answer": "A primary key uniquely identifies each row and cannot be NULL; a table has one primary-key constraint, possibly composite. A UNIQUE constraint prevents duplicate values, with NULL behavior varying by database. A foreign key references a key in another table and enforces referential integrity.",
        "companies": ["Zoho", "Oracle", "Flipkart", "Microsoft"],
    },
    {
        "difficulty": QuestionDifficulty.EASY,
        "question_text": "What are candidate, super, composite, and alternate keys?",
        "expected_answer": "A super key uniquely identifies a row and may contain extra columns. A candidate key is a minimal super key. The chosen candidate key is the primary key; unchosen candidate keys are alternate keys. A composite key contains two or more columns.",
        "companies": ["Zoho", "Oracle", "Flipkart"],
    },
    {
        "difficulty": QuestionDifficulty.EASY,
        "question_text": "What types of relationships can exist between database tables?",
        "expected_answer": "One-to-one relates at most one row on each side. One-to-many relates one row to multiple rows, with the foreign key normally on the many side. Many-to-many is represented using a junction table containing foreign keys to both entities.",
        "companies": ["Zoho", "Oracle", "Flipkart", "Amazon"],
    },
    {
        "difficulty": QuestionDifficulty.EASY,
        "question_text": "Explain the different types of SQL joins.",
        "expected_answer": "INNER JOIN returns matching rows. LEFT JOIN keeps every left row and matching right rows; RIGHT JOIN is the reverse. FULL OUTER JOIN keeps matched and unmatched rows from both sides (not directly supported in MySQL). CROSS JOIN forms a Cartesian product. A self join joins a table to itself.",
        "companies": ["Google", "Microsoft", "Oracle", "Meta", "Zoho", "Flipkart", "Goldman Sachs", "Amazon", "Aginity", "Bodo AI", "Beekeeper Studio", "Holistics Software"],
    },
    {
        "difficulty": QuestionDifficulty.EASY,
        "question_text": "What is the difference between UNION and UNION ALL?",
        "expected_answer": "UNION combines result sets and removes duplicates, which may require extra sorting or hashing. UNION ALL keeps duplicates and is usually faster. Both queries must return the same number of columns with compatible data types.",
        "companies": ["Zoho", "Amazon", "Oracle", "Microsoft"],
    },
    {
        "difficulty": QuestionDifficulty.EASY,
        "question_text": "What are SQL constraints?",
        "expected_answer": "Constraints enforce data integrity. NOT NULL requires a value; UNIQUE prevents duplicates; PRIMARY KEY identifies rows; FOREIGN KEY enforces relationships; CHECK validates a condition; DEFAULT supplies a value when one is not provided.",
        "companies": ["Zoho", "Oracle", "Flipkart"],
    },
    {
        "difficulty": QuestionDifficulty.EASY,
        "question_text": "How does SQL handle NULL, and why should IS NULL be used instead of = NULL?",
        "expected_answer": "NULL represents missing or unknown information. Comparisons such as = NULL or <> NULL evaluate to UNKNOWN, so use IS NULL or IS NOT NULL. COALESCE returns the first non-NULL value; database-specific alternatives include IFNULL, NVL, and ISNULL. Most aggregates ignore NULL values, while COUNT(*) counts rows.",
        "companies": ["Amazon", "Goldman Sachs", "Microsoft", "Zoho"],
    },
    {
        "difficulty": QuestionDifficulty.EASY,
        "question_text": "What is the logical order of execution of a SQL query?",
        "expected_answer": "A simplified logical order is FROM/JOIN, WHERE, GROUP BY, HAVING, SELECT, DISTINCT, ORDER BY, then LIMIT/TOP/FETCH. This explains why a SELECT alias generally cannot be used in WHERE but can often be used in ORDER BY.",
        "companies": ["Amazon", "Microsoft", "Goldman Sachs", "Zoho"],
    },
    {
        "difficulty": QuestionDifficulty.EASY,
        "question_text": "What are aggregate functions? Compare COUNT(*), COUNT(column), and COUNT(DISTINCT column).",
        "expected_answer": "Common aggregate functions are COUNT, SUM, AVG, MIN, and MAX. COUNT(*) counts all rows. COUNT(column) counts rows where that column is not NULL. COUNT(DISTINCT column) counts distinct non-NULL values.",
        "companies": ["Zoho", "Amazon", "Flipkart"],
    },
    {
        "difficulty": QuestionDifficulty.EASY,
        "question_text": "What is the difference between CHAR and VARCHAR?",
        "expected_answer": "CHAR stores fixed-length character values and may pad them with spaces. VARCHAR stores variable-length values and generally uses space according to the actual content plus overhead. CHAR suits fixed-size codes; VARCHAR suits variable-length text. Oracle commonly uses VARCHAR2.",
        "companies": ["Zoho", "Oracle"],
    },
    {
        "difficulty": QuestionDifficulty.EASY,
        "question_text": "What does DISTINCT do, and how is it different from GROUP BY?",
        "expected_answer": "DISTINCT removes duplicate result rows. GROUP BY forms groups and supports aggregate calculations per group. For simple deduplication they may produce similar results, but GROUP BY is used for grouped aggregates.",
        "companies": ["Zoho", "Amazon"],
    },
    {
        "difficulty": QuestionDifficulty.EASY,
        "question_text": "What is a view, and what are its advantages?",
        "expected_answer": "A view is a named query that behaves like a virtual table. It can simplify complex queries, restrict access to rows or columns, and provide a stable interface to underlying data. A normal view stores its definition, while a materialized view stores query results and must be refreshed.",
        "companies": ["Zoho", "Oracle", "Microsoft", "Flipkart"],
    },
    {
        "difficulty": QuestionDifficulty.EASY,
        "question_text": "What is an index, and why is it used?",
        "expected_answer": "An index, often implemented using a B-tree, helps locate rows without scanning an entire table and can speed up filtering, joins, and sorting. Indexes require storage and must be maintained, so they can slow INSERT, UPDATE, and DELETE operations.",
        "companies": ["Zoho", "Oracle", "Microsoft", "Flipkart", "Amazon"],
    },
    {
        "difficulty": QuestionDifficulty.EASY,
        "question_text": "What is normalization? Explain 1NF, 2NF, and 3NF.",
        "expected_answer": "Normalization reduces redundant data and update anomalies. 1NF requires atomic values and no repeating groups. 2NF requires 1NF and no partial dependency of a non-key column on part of a composite candidate key. 3NF requires 2NF and no transitive dependency of non-key columns on a key.",
        "companies": ["Zoho", "Oracle", "Flipkart", "Microsoft"],
    },
    {
        "difficulty": QuestionDifficulty.EASY,
        "question_text": "What is a stored procedure, and how does it differ from a function?",
        "expected_answer": "A stored procedure is a named block of SQL and procedural code stored in the database. A function returns a value and can often be used in a SELECT expression. Procedures can return result sets or output parameters and are invoked using database-specific syntax such as CALL or EXEC. Exact rules vary by database.",
        "companies": ["Zoho", "Oracle", "Microsoft"],
    },
    {
        "difficulty": QuestionDifficulty.EASY,
        "question_text": "What does LIKE do, and how do wildcards affect index usage?",
        "expected_answer": "LIKE matches text patterns: percent (%) matches any sequence of characters and underscore (_) matches one character. A fixed-prefix pattern such as 'abc%' may use a normal index, while a leading wildcard such as '%abc' generally prevents efficient use of a standard B-tree index.",
        "companies": ["Zoho", "Oracle"],
    },

    # MEDIUM — Concepts, Concurrency and Design (20)
    {
        "difficulty": QuestionDifficulty.MEDIUM,
        "question_text": "What are window functions? Explain ROW_NUMBER, RANK, and DENSE_RANK.",
        "expected_answer": "Window functions calculate values across related rows without collapsing them into one row per group. ROW_NUMBER assigns a unique sequence; RANK gives ties equal ranks and leaves gaps; DENSE_RANK gives ties equal ranks without gaps. OVER may contain PARTITION BY, ORDER BY, and a frame. They are useful for top-N-per-group and running totals.",
        "companies": ["Amazon", "Goldman Sachs", "Meta", "Google", "Microsoft", "Holistics Software"],
    },
    {
        "difficulty": QuestionDifficulty.MEDIUM,
        "question_text": "What happens when GROUP BY uses non-key columns, and why must selected columns be grouped or aggregated?",
        "expected_answer": "GROUP BY groups rows by the listed column values, whether or not they are keys. Every selected expression must normally be grouped or aggregated; otherwise the database cannot determine which row's value to display. MySQL's ONLY_FULL_GROUP_BY enforces this, with specific functional-dependency exceptions in some databases.",
        "companies": ["Holistics Software", "Zoho", "Amazon"],
    },
    {
        "difficulty": QuestionDifficulty.MEDIUM,
        "question_text": "What is the difference between IN, EXISTS, and JOIN? What is the NOT IN NULL trap?",
        "expected_answer": "IN checks membership in a list or subquery; EXISTS tests whether a matching row exists; JOIN combines rows and can multiply them when there are multiple matches. If a NOT IN subquery returns NULL, comparisons can become UNKNOWN and unexpectedly return no rows. NOT EXISTS is often safer for anti-matching.",
        "companies": ["Amazon", "Microsoft", "Oracle", "Goldman Sachs"],
    },
    {
        "difficulty": QuestionDifficulty.MEDIUM,
        "question_text": "What is the difference between correlated and non-correlated subqueries?",
        "expected_answer": "A non-correlated subquery can run independently of the outer query. A correlated subquery references columns from the outer query and is logically evaluated in that context for each outer row, though an optimizer may rewrite it as a join. For example, compare an employee's salary with their department's average.",
        "companies": ["Zoho", "Oracle", "Amazon", "Microsoft"],
    },
    {
        "difficulty": QuestionDifficulty.MEDIUM,
        "question_text": "What is a CTE, and how does it differ from a subquery, view, and temporary table?",
        "expected_answer": "A CTE is a named result set scoped to one SQL statement and can improve readability; recursive CTEs can represent hierarchies. A subquery is an inline nested query, a view is a persistent stored query definition, and a temporary table stores session-scoped data and may be indexed. CTE materialization and reevaluation behavior varies by database and version.",
        "companies": ["Microsoft", "Amazon", "Google", "Meta", "Goldman Sachs"],
    },
    {
        "difficulty": QuestionDifficulty.MEDIUM,
        "question_text": "What is the difference between clustered and non-clustered indexes?",
        "expected_answer": "A clustered index determines how table rows are organized at the index's leaf level, so a table generally has at most one. A non-clustered or secondary index is a separate structure pointing to rows or their clustered keys, and a table can have multiple. Implementation and terminology vary by database.",
        "companies": ["Microsoft", "Oracle", "Flipkart", "Goldman Sachs"],
    },
    {
        "difficulty": QuestionDifficulty.MEDIUM,
        "question_text": "What are ACID properties and database transactions?",
        "expected_answer": "A transaction groups operations into one unit, typically completed with COMMIT or undone with ROLLBACK. Atomicity means all-or-nothing; Consistency preserves database rules; Isolation controls interference between concurrent transactions; Durability means committed changes survive failures.",
        "companies": ["Flipkart", "Goldman Sachs", "Amazon", "Microsoft", "Oracle"],
    },
    {
        "difficulty": QuestionDifficulty.MEDIUM,
        "question_text": "Explain transaction isolation levels and the anomalies they prevent.",
        "expected_answer": "Read Uncommitted can allow dirty reads. Read Committed prevents dirty reads but can allow non-repeatable reads. Repeatable Read provides repeatable row reads, while phantom behavior depends on the database and implementation. Serializable provides the strongest standard isolation by making concurrent transactions behave as if serialized. Dirty reads see uncommitted data; non-repeatable reads see changed values; phantom reads see new matching rows.",
        "companies": ["Microsoft", "Goldman Sachs", "Flipkart", "Oracle"],
    },
    {
        "difficulty": QuestionDifficulty.MEDIUM,
        "question_text": "What are database triggers, and what are their advantages and disadvantages?",
        "expected_answer": "A trigger automatically runs in response to events such as INSERT, UPDATE, or DELETE, and some systems support view triggers. Triggers can support auditing and complex rules, but add hidden logic, performance overhead, debugging difficulty, cascading behavior, and testing complexity. Prefer constraints or explicit application logic when appropriate.",
        "companies": ["Zoho", "Oracle", "Microsoft"],
    },
    {
        "difficulty": QuestionDifficulty.MEDIUM,
        "question_text": "What is BCNF, and when would you denormalize a database?",
        "expected_answer": "BCNF is stricter than 3NF: for every non-trivial functional dependency, the determinant must be a superkey. Denormalization deliberately introduces redundancy or precomputed aggregates to improve read-heavy workloads. It costs extra storage and makes writes and consistency harder, so it should be based on measurement.",
        "companies": ["Oracle", "Flipkart", "Zoho", "Microsoft"],
    },
    {
        "difficulty": QuestionDifficulty.MEDIUM,
        "question_text": "Why can large OFFSET pagination be slow, and what is keyset pagination?",
        "expected_answer": "With a large OFFSET, the database may still read and discard many preceding rows. Keyset or seek pagination uses the last seen sort key to retrieve rows after it, often allowing efficient index use. It does not jump to arbitrary page numbers and needs a stable sort with a unique tie-breaker.",
        "companies": ["Flipkart", "Amazon", "Goldman Sachs"],
    },
    {
        "difficulty": QuestionDifficulty.MEDIUM,
        "question_text": "What are Oracle ROWNUM pitfalls, and what is CONNECT BY used for?",
        "expected_answer": "Oracle ROWNUM is assigned before ORDER BY in the same query block, so sorting after filtering ROWNUM can give incorrect top-N results; sort in a subquery or use FETCH FIRST or ROW_NUMBER. ROWNUM = 2 alone returns no rows because the first row fails and the counter does not advance. CONNECT BY with START WITH, PRIOR, and LEVEL supports hierarchical queries; recursive CTEs are a common alternative elsewhere.",
        "companies": ["Oracle"],
    },
    {
        "difficulty": QuestionDifficulty.MEDIUM,
        "question_text": "What is the difference between SQL and NoSQL databases, and when would you choose each?",
        "expected_answer": "Relational SQL databases use tables, relationships, joins, and typically strong schema and ACID transaction support. NoSQL includes key-value, document, wide-column, and graph models, often designed for flexible schemas and particular scaling or access patterns. Choose based on data relationships, integrity, consistency, query needs, and scale; systems may use both.",
        "companies": ["Amazon", "Flipkart", "Google", "Meta", "Microsoft"],
    },
    {
        "difficulty": QuestionDifficulty.MEDIUM,
        "question_text": "What is a database cursor, and why are cursors often discouraged?",
        "expected_answer": "A cursor processes a result set one row at a time in procedural SQL. Explicit cursors are typically declared, opened, fetched, and closed. Row-by-row processing is often slower than set-based operations and may hold resources and locks longer, so use set-based SQL or bulk operations unless row-wise logic is needed.",
        "companies": ["Zoho", "Oracle", "Microsoft"],
    },
    {
        "difficulty": QuestionDifficulty.MEDIUM,
        "question_text": "What is the difference between a surrogate key and a natural key?",
        "expected_answer": "A natural key is a meaningful real-world attribute, such as an email address, that may change. A surrogate key is a generated identifier such as an integer or UUID with no business meaning. Surrogate keys are stable and common in data warehouses; a unique constraint may still be kept on the natural key.",
        "companies": ["Flipkart", "Amazon", "Microsoft", "Holistics Software"],
    },
    {
        "difficulty": QuestionDifficulty.MEDIUM,
        "question_text": "What types of indexes exist, including unique, composite, bitmap, hash, full-text, and partial indexes?",
        "expected_answer": "Unique indexes enforce uniqueness; composite indexes cover multiple columns and depend on column order; bitmap indexes suit low-cardinality, read-mostly data in supported systems; hash indexes suit equality lookups; full-text indexes support text search; partial or filtered indexes include only rows meeting a condition. Availability varies by database.",
        "companies": ["Oracle", "Microsoft", "Goldman Sachs", "Flipkart"],
    },
    {
        "difficulty": QuestionDifficulty.MEDIUM,
        "question_text": "In a LEFT JOIN, what is the difference between putting a condition in ON and in WHERE?",
        "expected_answer": "A right-table condition in ON limits which rows match while preserving all left rows; unmatched right-side columns become NULL. The same condition in WHERE is applied after the join and may remove those NULL-extended rows, effectively turning the outer join into an inner join.",
        "companies": ["Amazon", "Microsoft", "Goldman Sachs", "Zoho"],
    },
    {
        "difficulty": QuestionDifficulty.MEDIUM,
        "question_text": "What kinds of database locks exist, such as shared, exclusive, row, page, and table locks?",
        "expected_answer": "Shared locks permit compatible concurrent readers; exclusive locks protect writes and block conflicting access. Locks can operate at row, page, or table granularity. Fine-grained locks can improve concurrency but consume resources; some systems escalate locks. MVCC systems may allow ordinary reads without read locks.",
        "companies": ["Microsoft", "Goldman Sachs", "Oracle", "Flipkart"],
    },
    {
        "difficulty": QuestionDifficulty.MEDIUM,
        "question_text": "What are foreign-key referential actions such as CASCADE, SET NULL, RESTRICT, and NO ACTION?",
        "expected_answer": "Referential actions define what happens to child rows when a referenced parent key is deleted or updated. CASCADE propagates the change; SET NULL clears the foreign key when allowed; SET DEFAULT uses its default when supported; RESTRICT or NO ACTION blocks the operation while dependent rows exist. CASCADE should be used carefully.",
        "companies": ["Zoho", "Oracle", "Flipkart", "Microsoft"],
    },
    {
        "difficulty": QuestionDifficulty.MEDIUM,
        "question_text": "What is a NATURAL JOIN, and how is it different from a self join?",
        "expected_answer": "A NATURAL JOIN automatically joins columns that have the same names in both tables, which can be fragile if schemas change. A self join joins a table to itself using aliases, for example to relate employees to managers. Explicit ON or USING clauses are generally clearer than NATURAL JOIN.",
        "companies": ["Zoho", "Amazon", "Oracle", "Microsoft"],
    },

    # HARD — Internals, Concurrency, Architecture and Design (20)
    {
        "difficulty": QuestionDifficulty.HARD,
        "question_text": "How do you diagnose and optimize a slow SQL query?",
        "expected_answer": "Measure the query and inspect its actual execution plan, using tools such as EXPLAIN ANALYZE or database-specific plan tools. Look for large scans, inaccurate row estimates, expensive sorts, costly joins, and disk spills. Consider appropriate indexes, sargable predicates, selecting only needed columns, early filtering, updated statistics, and alternative query shapes; verify improvements with timings and plans.",
        "companies": ["Goldman Sachs", "Amazon", "Microsoft", "Oracle", "Flipkart", "Google"],
    },
    {
        "difficulty": QuestionDifficulty.HARD,
        "question_text": "How do B-tree indexes work? Explain composite and covering indexes, and why an index may not be used.",
        "expected_answer": "A B-tree keeps keys sorted in a balanced structure, enabling efficient lookups and range scans. Composite indexes follow a leftmost-prefix principle; column order matters. A covering index contains all columns needed by a query and can avoid table lookups. Indexes may not be used when predicates wrap indexed columns in functions, implicit conversions occur, a pattern has a leading wildcard, many rows are needed, or statistics are stale.",
        "companies": ["Oracle", "Microsoft", "Goldman Sachs", "Flipkart", "Amazon"],
    },
    {
        "difficulty": QuestionDifficulty.HARD,
        "question_text": "What is a sargable predicate, and what makes a predicate non-sargable?",
        "expected_answer": "A sargable predicate can use an index efficiently for a search or seek. Wrapping an indexed column in a function or expression, applying a leading wildcard, or forcing an implicit type conversion can make a condition non-sargable. Prefer comparing the raw indexed column with appropriately calculated constants or ranges.",
        "companies": ["Microsoft", "Goldman Sachs", "Amazon"],
    },
    {
        "difficulty": QuestionDifficulty.HARD,
        "question_text": "Explain nested-loop, hash, and merge join algorithms.",
        "expected_answer": "A nested-loop join checks matches for each row of one input and works well when that input is small and the other has a useful index. A hash join builds a hash table from one input and probes it with the other, often suiting large equality joins. A merge join processes inputs ordered by join keys. The optimizer chooses based on estimates, indexes, memory, and ordering.",
        "companies": ["Oracle", "Microsoft", "Goldman Sachs", "Google"],
    },
    {
        "difficulty": QuestionDifficulty.HARD,
        "question_text": "What is MVCC, and how does it differ from lock-based concurrency control?",
        "expected_answer": "Multi-Version Concurrency Control keeps multiple versions of rows so readers can see a consistent snapshot without necessarily blocking writers. Writers can still conflict with other writers. Implementations differ: PostgreSQL stores old row versions and cleans them with VACUUM, while Oracle and MySQL InnoDB use undo information. Lock-based approaches rely more directly on locks for reads and writes.",
        "companies": ["Goldman Sachs", "Oracle", "Google", "Flipkart"],
    },
    {
        "difficulty": QuestionDifficulty.HARD,
        "question_text": "What causes database deadlocks, and how can they be prevented or handled?",
        "expected_answer": "A deadlock occurs when transactions hold locks that each other needs, forming a cycle. The database normally detects it and aborts a victim transaction. Prevention includes acquiring resources in a consistent order, keeping transactions short, avoiding user interaction inside transactions, and indexing access paths appropriately. Applications should safely retry failed transactions with backoff and inspect database deadlock diagnostics.",
        "companies": ["Goldman Sachs", "Microsoft", "Flipkart", "Amazon", "Oracle"],
    },
    {
        "difficulty": QuestionDifficulty.HARD,
        "question_text": "What are Slowly Changing Dimensions, and how would you model history in an ERD?",
        "expected_answer": "Slowly Changing Dimensions describe how a data warehouse records changes to dimension attributes. Type 1 overwrites values; Type 2 creates a new versioned row with a surrogate key and validity dates or a current flag; Type 3 stores limited prior values in extra columns. Facts reference the dimension version valid at the relevant time, and late-arriving data must be considered.",
        "companies": ["Holistics Software", "Amazon", "Microsoft", "Google"],
    },
    {
        "difficulty": QuestionDifficulty.HARD,
        "question_text": "Compare OLTP and OLAP, and explain star and snowflake schemas.",
        "expected_answer": "OLTP handles many small transactional reads and writes, usually with normalized row-oriented structures. OLAP supports large analytical scans and aggregations, often with denormalized or columnar storage. A star schema has a central fact table connected directly to dimension tables; a snowflake schema further normalizes dimensions, reducing redundancy but requiring more joins.",
        "companies": ["Amazon", "Google", "Microsoft", "Goldman Sachs", "Holistics Software"],
    },
    {
        "difficulty": QuestionDifficulty.HARD,
        "question_text": "Explain window frames and the difference between ROWS and RANGE.",
        "expected_answer": "A window frame defines which rows an aggregate window function considers around the current row. ROWS counts physical rows, whereas RANGE considers ordering-value ranges and peer rows with equal sort values. Default RANGE frames can produce surprising running totals when sort values tie. Specify frames explicitly, and use a calendar table when calculating by calendar days with missing dates.",
        "companies": ["Google", "Meta", "Amazon", "Goldman Sachs"],
    },
    {
        "difficulty": QuestionDifficulty.HARD,
        "question_text": "Explain partitioning, sharding, and replication.",
        "expected_answer": "Partitioning divides a table into pieces within one database, for example by range, list, or hash. Sharding distributes data across database servers using a shard key, improving scale but complicating cross-shard operations and rebalancing. Replication copies data to other servers for read scaling or failover; asynchronous replicas can return stale data.",
        "companies": ["Flipkart", "Amazon", "Goldman Sachs", "Google", "Meta"],
    },
    {
        "difficulty": QuestionDifficulty.HARD,
        "question_text": "How would you design a database schema for an e-commerce system, ride-sharing service, or URL shortener?",
        "expected_answer": "Start with requirements, entities, keys, relationships, constraints, indexes, and growth. For e-commerce, possible entities include users, addresses, products, categories, inventory, orders, order_items, payments, and shipments. Use a junction table for orders and products, preserve the purchase-time price, index foreign keys and common access paths, use DECIMAL for money, and consider scaling, caching, denormalization, and idempotent payments.",
        "companies": ["Amazon", "Flipkart", "Meta", "Goldman Sachs", "Microsoft"],
    },
    {
        "difficulty": QuestionDifficulty.HARD,
        "question_text": "How can you prevent overselling inventory during concurrent requests?",
        "expected_answer": "A separate read-check-write sequence can race. Use an atomic conditional update that decrements stock only when it is positive and check the affected-row count. Alternatives include pessimistic locking with SELECT FOR UPDATE or optimistic locking with a version column and retries. High-contention systems may use reservations, queues, or distributed counters with reconciliation.",
        "companies": ["Flipkart", "Amazon", "Goldman Sachs"],
    },
    {
        "difficulty": QuestionDifficulty.HARD,
        "question_text": "Why might a query optimizer choose a poor execution plan? What are statistics and parameter sniffing?",
        "expected_answer": "The optimizer estimates row counts and costs using statistics such as histograms and distinct counts. Stale statistics, skewed data, correlated columns, and complex expressions can produce poor estimates and bad plans. Parameter sniffing describes plan caching based on initial parameter values that may perform poorly for different values. Updating statistics, improving indexes, carefully using recompilation or hints, and restructuring queries can help.",
        "companies": ["Microsoft", "Oracle", "Goldman Sachs", "Amazon"],
    },
    {
        "difficulty": QuestionDifficulty.HARD,
        "question_text": "How do you prevent SQL injection?",
        "expected_answer": "Do not concatenate untrusted input into SQL. Use parameterized queries or prepared statements and ORM operations that bind parameters. Dynamic identifiers such as table or column names need strict allowlists because they usually cannot be bound as ordinary values. Also use least-privilege database accounts, validate input, and avoid exposing verbose database errors. Stored procedures are not safe if they build unsafe dynamic SQL.",
        "companies": ["Microsoft", "Amazon", "Goldman Sachs", "Oracle"],
    },
    {
        "difficulty": QuestionDifficulty.HARD,
        "question_text": "How can very large data loads or deletes be performed safely and efficiently?",
        "expected_answer": "For loading, use bulk tools or batched inserts, stage and validate data before merging, manage indexes and constraints carefully, and commit in batches. For deletion, use small batches to limit locks, log growth, and replication lag, or use partition operations when appropriate. Run during suitable windows, monitor resources, and maintain a rollback or recovery plan.",
        "companies": ["Amazon", "Flipkart", "Goldman Sachs", "Microsoft"],
    },
    {
        "difficulty": QuestionDifficulty.HARD,
        "question_text": "What is write-ahead logging (WAL), and what is write skew? Which isolation level prevents write skew?",
        "expected_answer": "WAL records changes durably before corresponding data pages are written, allowing recovery after crashes. Write skew occurs when concurrent transactions read overlapping state and then update different rows in ways that together violate a rule. Snapshot isolation alone may permit it; SERIALIZABLE isolation or appropriate explicit locking can prevent it.",
        "companies": ["Goldman Sachs", "Google", "Oracle", "Microsoft"],
    },
    {
        "difficulty": QuestionDifficulty.HARD,
        "question_text": "Explain the CAP theorem and consistency models. Where do distributed SQL databases fit?",
        "expected_answer": "During a network partition, a distributed system must trade off consistency and availability because it cannot guarantee both in every case. PACELC also describes latency-versus-consistency trade-offs when there is no partition. Distributed SQL systems preserve SQL interfaces while coordinating across nodes for strong consistency, typically using consensus protocols, with latency and availability trade-offs.",
        "companies": ["Google", "Amazon", "Meta", "Flipkart"],
    },
    {
        "difficulty": QuestionDifficulty.HARD,
        "question_text": "What is the difference between row-oriented and column-oriented storage, and why are warehouses often columnar?",
        "expected_answer": "Row stores keep a row's columns together and suit transactional access to complete rows. Column stores keep values from the same column together, so analytical queries can read only needed columns, compress similar values efficiently, and process vectors. Columnar storage is excellent for scans and aggregations but can be less suited to single-row updates and point lookups.",
        "companies": ["Google", "Amazon", "Holistics Software", "Microsoft"],
    },
    {
        "difficulty": QuestionDifficulty.HARD,
        "question_text": "What is the role of the query optimizer? Explain cost-based optimization, plan caching, and hints.",
        "expected_answer": "The optimizer turns declarative SQL into an execution plan and compares alternatives such as join orders, join algorithms, and access paths using estimated costs and statistics. Plans may be cached to save compilation time, but reuse can hurt when data or parameters differ. Hints override optimizer choices and should be used cautiously because they may become harmful as data changes.",
        "companies": ["Oracle", "Microsoft", "Goldman Sachs", "Google"],
    },
    {
        "difficulty": QuestionDifficulty.HARD,
        "question_text": "What are index fragmentation and fill factor, and when should an index be rebuilt or reorganized?",
        "expected_answer": "Inserts and deletes can cause page splits and sparse or logically scattered index pages, increasing scan work. Fill factor leaves free space on index pages to reduce page splits, at the cost of a larger index. Reorganizing can address lighter fragmentation incrementally; rebuilding recreates the index and may update statistics but can be more resource-intensive. Measure whether maintenance will help.",
        "companies": ["Microsoft", "Oracle", "Goldman Sachs"],
    },
]


def validate_questions() -> None:
    """Fail early if the bank does not match the PDF's expected structure."""
    expected_counts = {
        QuestionDifficulty.EASY: 20,
        QuestionDifficulty.MEDIUM: 20,
        QuestionDifficulty.HARD: 20,
    }
    actual_counts = Counter(item["difficulty"] for item in QUESTIONS)

    if len(QUESTIONS) != 60:
        raise ValueError(f"Expected 60 SQL questions; found {len(QUESTIONS)}.")

    for difficulty, expected_count in expected_counts.items():
        actual_count = actual_counts.get(difficulty, 0)
        if actual_count != expected_count:
            raise ValueError(
                f"Expected {expected_count} {difficulty.value} questions; "
                f"found {actual_count}."
            )

    for index, item in enumerate(QUESTIONS, start=1):
        for field in ("question_text", "expected_answer"):
            if not isinstance(item.get(field), str) or len(item[field].strip()) < 5:
                raise ValueError(f"Question {index} has an invalid {field}.")
        companies = item.get("companies")
        if not isinstance(companies, list) or not all(
            isinstance(company, str) and company.strip()
            for company in companies
        ):
            raise ValueError(f"Question {index} has invalid company tags.")


def seed_sql_questions() -> None:
    """Insert the 60 SQL theory questions into the existing SQL topic."""
    validate_questions()
    db = SessionLocal()

    try:
        topic = db.query(Topic).filter(Topic.name == TOPIC_NAME).first()

        if topic is None:
            raise RuntimeError(
                "The SQL topic does not exist. Create/activate the SQL topic "
                "in the app first; this seeder will not create a duplicate topic."
            )

        if not topic.is_active:
            raise RuntimeError(
                f"The SQL topic (ID: {topic.id}) is inactive. Activate it first."
            )

        existing_count = (
            db.query(Question)
            .filter(Question.topic_id == topic.id)
            .count()
        )

        if existing_count > 0:
            print(
                f"SQL topic (ID: {topic.id}) already contains "
                f"{existing_count} question(s)."
            )
            print("No questions were inserted to avoid duplicates.")
            print(
                "If this is unexpected, inspect the existing SQL questions "
                "before running any cleanup."
            )
            return

        questions = [
            Question(
                topic_id=topic.id,
                difficulty=item["difficulty"],
                question_text=item["question_text"],
                expected_answer=item["expected_answer"],
                companies=item["companies"],
            )
            for item in QUESTIONS
        ]

        db.add_all(questions)
        db.commit()

        counts = Counter(question.difficulty for question in questions)
        print("=" * 60)
        print("SQL THEORY QUESTION BANK CREATED")
        print("=" * 60)
        print(f"Topic ID        : {topic.id}")
        print(f"Topic           : {topic.name}")
        print(f"Total questions : {len(questions)}")
        print(f"Easy            : {counts[QuestionDifficulty.EASY]}")
        print(f"Medium          : {counts[QuestionDifficulty.MEDIUM]}")
        print(f"Hard            : {counts[QuestionDifficulty.HARD]}")
        print("Company tags    : Stored in the companies JSON column")
        print("=" * 60)

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_sql_questions()
