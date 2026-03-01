# 微信小店API接入指南

## 概述

微信小店提供API接口，可以实现：
- 商品批量上架/下架
- 库存同步
- 订单管理
- 数据统计

⚠️ **注意**：目前微信小店API主要面向企业/个体户开放，需要申请权限。

## 接入条件

### 资质要求
1. 已完成微信小店开店认证
2. 企业/个体户资质（个人店部分API受限）
3. 通过微信支付的商户认证

### 申请流程
1. 登录 [微信开放平台](https://open.weixin.qq.com/)
2. 进入「微信小店」→「开发者设置」
3. 申请API权限（需提交使用场景说明）
4. 审核通过后获取 `appid` 和 `appsecret`

## API接口说明

### 接口地址
```
https://api.weixin.qq.com/shop/
```

### 认证方式
使用 AccessToken 进行接口认证：
```python
# 获取AccessToken
import requests

def get_access_token(appid, appsecret):
    url = f"https://api.weixin.qq.com/cgi-bin/token"
    params = {
        "grant_type": "client_credential",
        "appid": appid,
        "secret": appsecret
    }
    resp = requests.get(url, params=params)
    return resp.json().get("access_token")
```

### 核心接口

#### 1. 添加商品
```
POST /product/add
```
请求示例：
```json
{
  "title": "猫砂盆大号封闭式",
  "desc": "防外溅设计，活性炭除臭...",
  "cats": ["宠物用品", "猫砂盆"],
  "price": 8900,
  "stock_num": 100,
  "head_imgs": ["https://example.com/img1.jpg"],
  "detail": "<img src='...'>"
}
```

#### 2. 修改商品
```
POST /product/update
```

#### 3. 获取商品列表
```
GET /product/list?access_token=xxx&page=1&page_size=20
```

#### 4. 上架/下架商品
```
POST /product/listing
POST /product/delisting
```

## 宠物用品店接入示例

### 场景：批量上架猫砂盆

```python
import requests
import json

class WechatShopAPI:
    def __init__(self, appid, appsecret):
        self.appid = appid
        self.appsecret = appsecret
        self.access_token = self._get_access_token()
        self.base_url = "https://api.weixin.qq.com/shop"
    
    def _get_access_token(self):
        url = "https://api.weixin.qq.com/cgi-bin/token"
        params = {
            "grant_type": "client_credential",
            "appid": self.appid,
            "secret": self.appsecret
        }
        resp = requests.get(url, params=params)
        return resp.json()["access_token"]
    
    def add_product(self, product_data):
        """添加商品"""
        url = f"{self.base_url}/product/add"
        params = {"access_token": self.access_token}
        
        # 构建商品数据结构
        payload = {
            "title": product_data["title"],
            "desc": product_data["description"],
            "cats": [product_data["category"]["primary"]],
            "price": int(product_data["suggested_price"]["recommended"] * 100),  # 转为分
            "stock_num": 100,
            "head_imgs": ["https://your-cdn.com/default.jpg"],  # 主图URL
            "detail": product_data["description"].replace("\n", "<br>"),
            "express_info": {
                "template_id": "0"  # 使用默认运费模板
            }
        }
        
        resp = requests.post(url, params=params, json=payload)
        return resp.json()

# 使用示例
api = WechatShopAPI("your_appid", "your_appsecret")

# 使用AI生成的商品数据
product = {
    "title": "猫砂盆大号封闭式防外溅除臭",
    "description": "✨ 大号封闭式猫砂盆，给猫咪私密空间...",
    "category": {"primary": "宠物用品"},
    "suggested_price": {"recommended": 89}
}

result = api.add_product(product)
print(f"商品上架结果: {result}")
```

## 无API权限的替代方案

如果暂时没有API权限，可以使用以下方式：

### 方案1：半自动导入
1. 使用本skill生成完整商品资料
2. 导出为CSV/Excel格式
3. 使用微信小店的「批量导入」功能上传

### 方案2：RPA自动化
使用浏览器自动化工具（如Selenium、Playwright）模拟人工操作：
```python
from playwright.sync_api import sync_playwright

# 自动登录并上架商品
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://channels.weixin.qq.com/shop")
    # ... 自动化操作
```

⚠️ **风险提示**：RPA方式可能违反平台服务条款，谨慎使用。

## 配置存储

建议将API配置存储在环境变量或配置文件中：

```bash
# .env 文件
WECHAT_SHOP_APPID=wx1234567890
WECHAT_SHOP_SECRET=your_secret_here
WECHAT_SHOP_TOKEN=your_token
```

## 常见问题

### Q: 个人店可以申请API吗？
A: 目前主要开放给企业/个体户，个人店部分接口受限。

### Q: API调用频率限制？
A: 一般接口 2000次/分钟，商品接口 100次/分钟。

### Q: 如何测试API？
A: 微信提供沙箱环境，可在开发者后台申请。

### Q: 商品图片怎么处理？
A: 需要先将图片上传到微信服务器获取media_id，或使用自己的CDN链接。

## 相关资源

- [微信小店开发文档](https://developers.weixin.qq.com/doc/store/)
- [微信开放社区](https://developers.weixin.qq.com/)
- [API调试工具](https://mp.weixin.qq.com/debug/)
