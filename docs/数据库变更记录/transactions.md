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

### 记录 2：字段添加 - user_id

| 项目 | 内容 |
|------|------|
| 修改日期 | 2026-06-29 |
| 修改人 | yueye12 |
| 变更类型 | 字段添加 |
| 变更字段 | user_id |
| 变更原因 | 增加用户认证，流水记录需要关联到用户 |

**SQL 语句：**
```sql
ALTER TABLE transactions_transaction ADD COLUMN user_id INTEGER NOT NULL REFERENCES auth_user(id) DEFAULT 1;
CREATE INDEX transactions_transaction_user_id_idx ON transactions_transaction(user_id);
```

**数据迁移：**
- 创建默认管理员用户 admin（密码 admin123）
- 已有流水记录全部关联到 admin 用户

**回滚 SQL：**
```sql
ALTER TABLE transactions_transaction DROP COLUMN user_id;
```

---

## 汇总

| 序号 | 日期 | 类型 | 表名 | 修改人 |
|------|------|------|-----------|--------|
| 1 | 2026-06-29 | 表创建 | transactions_transaction | yueye12 |
| 2 | 2026-06-29 | 字段添加 | transactions_transaction.user_id | yueye12 |
