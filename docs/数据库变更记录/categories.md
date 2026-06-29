# 数据库修改记录 - categories

> 修改人标识：`yueye12`（来自 git config user.name）

---

## 修改记录

### 记录 1：表创建（初始建表）

| 项目 | 内容 |
|------|------|
| 修改日期 | 2026-06-29 |
| 修改人 | yueye12 |
| 变更类型 | 表创建 |
| 变更说明 | 创建分类表 |

**SQL 语句：**
```sql
CREATE TABLE transactions_category (
    id              INTEGER      PRIMARY KEY AUTOINCREMENT,
    name            VARCHAR(50)  NOT NULL,
    type            VARCHAR(10)  NOT NULL,
    icon            VARCHAR(10)  NOT NULL DEFAULT '📄',
    sort_order      INTEGER      NOT NULL DEFAULT 0,
    is_deleted      BOOLEAN      NOT NULL DEFAULT 0,
    created_at      DATETIME     NOT NULL,
    updated_at      DATETIME     NOT NULL
);
```

**回滚 SQL：**
```sql
DROP TABLE IF EXISTS transactions_category;
```

---

## 汇总

| 序号 | 日期 | 类型 | 表名 | 修改人 |
|------|------|------|-----------|--------|
| 1 | 2026-06-29 | 表创建 | transactions_category | yueye12 |
