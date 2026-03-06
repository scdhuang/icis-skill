# ICIS MVP 使用手册

## 快速开始（5分钟上手）

### Step 1: 准备客户信息
填写客户基本信息：
```yaml
公司名称: XX科技有限公司
行业: 家电/电子/机械
规模: 10亿营收/2000人
业务模式: 80%代工+20%自有品牌
```

### Step 2: 生成访谈计划
```bash
python3 ~/.openclaw/workspace/icis-mvp/scripts/icis_analyzer.py \
  --mode plan \
  --company "XX科技有限公司" \
  --industry appliances \
  --output plan.md
```

### Step 3: 执行访谈
使用生成的访谈计划，按顺序访谈关键人。

### Step 4: 分析访谈记录
```bash
python3 ~/.openclaw/workspace/icis-mvp/scripts/icis_analyzer.py \
  --mode analyze \
  --input interview.txt \
  --output report.md
```

## 输出说明

### 访谈计划包含：
- 推荐访谈对象（3-4人）
- 每人核心问题（3-5个）
- 预估访谈时长
- 配套材料清单

### 分析报告包含：
- 核心痛点（Top 5）
- AI机会点（Top 3）
- 销售话术
- 行动计划

## 常见问题

**Q: 客户行业不在模板里怎么办？**
A: 选择最接近的行业，或联系道哥添加新模板。

**Q: 访谈时间不够怎么办？**
A: 优先访谈IT总监，其他可以电话补充。

**Q: 分析结果不准确怎么办？**
A: 检查访谈记录是否完整，关键信息是否提取正确。

## 支持

有问题联系：道哥 / 道道虾 🦞
