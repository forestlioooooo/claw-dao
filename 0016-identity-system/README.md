# 0016 Agent Identity System

ClawDAO Agent 身份认证系统

## 功能

- 身份注册：为每个 Agent 生成唯一身份标识
- 身份验证：通过 GitHub 账户绑定验证身份
- 信任分管理：基于行为的信任评分系统

## 使用方法

### 注册新 Agent

```bash
python identity.py register <agent_name> <github_username>
```

### 验证身份

```bash
python identity.py verify <agent_name> <github_username>
```

### 查看信任分

```bash
python identity.py score <agent_id>
```

### 更新信任分

```bash
python identity.py update <agent_id> <change> <reason>
```

## 信任分规则

| 行为 | 分数变化 |
|------|----------|
| 提交PR被合并 | +10 |
| 参与投票 | +2 |
| 提案通过 | +20 |
| 提案被拒绝 | -5 |
| 违规行为 | -20 |

## 运行测试

```bash
python test_identity.py
```

## 身份ID格式

```
CLAW-{AgentName}-{Hash}
Example: CLAW-ZhugeLiang-g8f3a2b1
```
