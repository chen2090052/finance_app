# 数据库修改记录 - transactions

> 修改人标识：`yueye12`（来自 git config user.name）

---

## 修改记录

### 记录 1：表创建（初始建表）

| 项目 | 内容 |
|------|------|
| 修改日期 | 2026-06-29 |
| 修改人 | yueye12 |
| 变更类型 | 表创建 |
| 变更说明 | 创建流水表 |

**SQL 语句：**
```sql
CREATE TABLE transactions_transaction (
    id              INTEGER          PRIMARY KEY AUTOINCREMENT,
    amount          DECIMAL(12,2)    NOT NULL,
    type            VARCHAR(10)      NOT NULL,
    category_id     INTEGER          NOT NULL REFERENCES transactions_category(id),
    note            VARCHAR(200)     NOT NULL DEFAULT '',
    date            DATE             NOT NULL,
    is_deleted      BOOLEAN          NOT NULL DEFAULT 0,
    created_at      DATETIME         NOT NULL,
    updated_at      DATETIME         NOT NULL
);

CREATE INDEX transactions_transaction_type_idx ON transactions_transaction(type);
CREATE INDEX transactions_transaction_category_id_idx ON transactions_transaction(category_id);
CREATE INDEX transactions_transaction_date_idx ON transactions_transaction(date);
```

**回滚 SQL：**
```sql
DROP TABLE IF EXISTS transactions_transaction;
```

---

## 汇总

| 序号 | 日期 | 类型 | 表名 | 修改人 |
|------|------|------|-----------|--------|
| 1 | 2026-06-29 | 表创建 | transactions_transaction | yueye12 |
