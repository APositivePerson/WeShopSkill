---
name: wechat-shop-assistant
description: 微信小店AI上架助手 - 帮助商家快速生成和优化商品信息，包括标题、描述、卖点、价格建议和分类推荐。使用Canvas展示交互式上架界面，支持一键生成完整商品资料。适用于微信小店的商品上架、信息优化、批量处理等场景。
---

# 微信小店AI上架助手

帮助商家快速完成微信小店商品上架的AI助手。

## 核心功能

### 1. 商品信息生成
- **标题生成**：根据商品名称、品类生成吸引人的标题（30字以内）
- **描述撰写**：生成详细的商品描述，包含规格、材质、使用方法等
- **卖点提取**：自动提取3-5个核心卖点
- **关键词推荐**：推荐搜索关键词提高曝光

### 2. 智能建议
- **价格建议**：基于商品类型给出定价区间建议
- **分类推荐**：推荐最合适的商品分类
- **运费模板**：建议合适的运费设置

### 3. 交互界面
- 使用Canvas展示商品上架工作台
- 支持表单填写和实时预览
- 一键导出完整商品资料

## 使用流程

### 方式一：AI对话调用（推荐）

直接在聊天中描述商品，AI会自动调用本skill生成上架资料：

**示例对话：**
```
你：帮我上架一款宠物用品，是猫砂盆，大号封闭式，成本45元
AI：✨ 已为您生成猫砂盆的完整上架资料...

你：优化一下这个标题：最好用的猫砂盆超大号
AI：⚠️ 检测到标题包含极限词"最好"，已优化为：优质猫砂盆超大号防外溅...

你：导出刚才生成的商品资料为微信格式
AI：📋 已为您导出微信小店格式的商品资料...
```

### 方式二：Canvas交互模式

启动可视化上架工作台：

```python
# 读取并展示Canvas界面
canvas.navigate(file="/home/wangziyi/.openclaw/workspace/skills/wechat-shop-assistant/assets/shop-workshop.html")
```

## 生成规范

### 商品标题规范
- 长度：10-30个字符
- 结构：【核心词】+【属性词】+【场景词】
- 示例：「纯棉白色T恤女夏季宽松显瘦基础款百搭短袖上衣」

### 商品描述结构
1. 开篇吸引（1-2句）
2. 产品参数（材质、尺寸、重量等）
3. 使用场景
4. 售后保障

### 卖点提炼原则
- 具体可量化（如"95%含棉量"而非"高品质"）
- 差异化优势
- 用户痛点解决
- 场景化描述

## 参考资料

- **微信小店规范**：见 [references/wechat-shop-rules.md](references/wechat-shop-rules.md)
- **商品分类表**：见 [references/category-table.md](references/category-table.md)
- **定价策略**：见 [references/pricing-guide.md](references/pricing-guide.md)
- **API接入指南**：见 [references/api-integration.md](references/api-integration.md) - 如何连接微信小店API

## 脚本工具

- `scripts/generate_product.py` - 商品信息生成器
- `scripts/optimize_title.py` - 标题优化器
- `scripts/format_export.py` - 资料格式化导出
- `scripts/pet_product_generator.py` - 🐾 宠物用品专用生成器
- `scripts/wechat_shop_api.py` - 微信小店API客户端
- `scripts/auto_publish.py` - 一键生成+上架工具

## 🔌 API接入配置

### 1. 配置API凭证

编辑 `.env` 文件，填入你的微信小店API凭证：

```bash
# 复制示例配置文件
cp .env.example .env

# 编辑.env文件
nano .env
```

文件内容：
```
WECHAT_SHOP_APPID=yout_shop_appID
WECHAT_SHOP_SECRET=yout_shop_secret
WECHAT_SHOP_SHIPPING_TEMPLATE_ID=0
WECHAT_SHOP_DEFAULT_STOCK=100
```

⚠️ **安全提醒**：`.env`文件已加入.gitignore，不会被提交到git

### 2. 安装依赖（可选）

```bash
pip3 install python-dotenv requests
```

如果不安装，脚本会自动读取.env文件（内置兼容代码）

### 3. 使用API上架

#### 方式A：一键上架（推荐）

```bash
# 生成资料 + 自动调用API上架
python3 scripts/auto_publish.py --type 猫砂盆 --pet cat --cost 45

# 仅生成资料，不上架
python3 scripts/auto_publish.py --type 猫粮 --pet cat --cost 30 --dry-run
```

#### 方式B：Python代码调用

```python
from scripts.wechat_shop_api import WechatShopAPI
from scripts.pet_product_generator import generate_pet_product

# 生成商品资料
product = generate_pet_product("猫砂盆", "cat", cost=45)

# 初始化API（自动读取.env配置）
api = WechatShopAPI()

# 上架商品
result = api.add_product(product)
if result['success']:
    print(f"上架成功！商品ID：{result['product_id']}")
else:
    print(f"上架失败：{result['message']}")
```

#### 方式C：AI对话直接上架

```
你：用API上架一个猫砂盆，成本45元
AI：【自动调用auto_publish.py】
    ✅ 商品资料已生成
    🚀 正在调用微信小店API...
    ✅ 上架成功！商品ID: 123456
```

## 宠物用品店专用 🐾

本skill针对宠物用品店有特殊优化：

### 支持的宠物类型
- 猫咪用品 (cat)
- 狗狗用品 (dog)
- 猫狗通用 (both)
- 鸟类/水族/小宠 (bird, fish, rabbit, hamster)

### 宠物产品模板
- 猫砂盆、猫粮、猫抓板、逗猫棒
- 狗粮、牵引绳、宠物窝
- 驱虫药（含资质提醒）

### 使用示例
```bash
# 生成猫砂盆资料
python3 scripts/pet_product_generator.py --type 猫砂盆 --pet cat --cost 45

# 生成狗粮资料
python3 scripts/pet_product_generator.py --type 狗粮 --pet dog --brand 皇家 --cost 80
```

### AI对话示例
```
你：我要上架一款猫砂盆，成本45元
AI：✨ 为您生成猫咪用品上架资料...

你：帮我写个狗粮的商品信息，要适合中大型犬
AI：🐕 已生成狗粮商品资料，包含6个卖点和定价建议...

你：这个标题合规吗：最好的猫砂盆
AI：⚠️ 检测到极限词，建议改为：优质猫砂盆大号封闭式...
```

## 输出示例

标准输出格式为JSON，包含：

```json
{
  "title": "商品标题",
  "description": "商品描述",
  "selling_points": ["卖点1", "卖点2", "卖点3"],
  "keywords": ["关键词1", "关键词2"],
  "suggested_price": {"min": 49, "max": 79, "recommended": 59},
  "category": {"primary": "一级分类", "secondary": "二级分类"},
  "shipping_template": "建议模板"
}
```
