#!/usr/bin/env python3
"""
微信小店API客户端
支持自动上架商品
"""

import os
import json
import requests
from typing import Dict, Optional

# 尝试加载环境变量（如果python-dotenv已安装）
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # 手动读取.env文件
    def load_dotenv():
        env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key] = value
    load_dotenv()

class WechatShopAPI:
    """微信小店API客户端"""
    
    def __init__(self, appid: str = None, secret: str = None):
        """
        初始化API客户端
        
        优先使用传入的参数，否则从环境变量读取
        """
        self.appid = appid or os.getenv('WECHAT_SHOP_APPID')
        self.secret = secret or os.getenv('WECHAT_SHOP_SECRET')
        
        if not self.appid or not self.secret:
            raise ValueError("缺少appid或secret，请检查.env文件或传入参数")
        
        self.access_token = self._get_access_token()
        self.base_url = "https://api.weixin.qq.com/shop"
    
    def _get_access_token(self) -> str:
        """获取AccessToken"""
        url = "https://api.weixin.qq.com/cgi-bin/token"
        params = {
            "grant_type": "client_credential",
            "appid": self.appid,
            "secret": self.secret
        }
        
        try:
            resp = requests.get(url, params=params, timeout=10)
            data = resp.json()
            
            if 'access_token' in data:
                return data['access_token']
            else:
                raise Exception(f"获取token失败: {data}")
        except Exception as e:
            raise Exception(f"请求token失败: {e}")
    
    def add_product(self, product_data: Dict) -> Dict:
        """
        添加商品到微信小店
        
        Args:
            product_data: 商品数据字典，格式如下：
            {
                "title": "商品标题",
                "description": "商品描述",
                "selling_points": ["卖点1", "卖点2"],
                "suggested_price": {"recommended": 169},
                "category": {"primary": "宠物用品"},
                "keywords": ["关键词1", "关键词2"]
            }
        
        Returns:
            API响应结果
        """
        url = f"{self.base_url}/product/add"
        params = {"access_token": self.access_token}
        
        # 构建微信小店API所需的商品数据结构
        price = int(product_data.get('suggested_price', {}).get('recommended', 0) * 100)  # 转为分
        
        # 构建详情（卖点+描述）
        selling_points = product_data.get('selling_points', [])
        description = product_data.get('description', '')
        
        detail_html = ""
        if selling_points:
            detail_html += "<h3>🌟 核心卖点</h3><ul>"
            for point in selling_points:
                detail_html += f"<li>{point}</li>"
            detail_html += "</ul>"
        
        detail_html += f"<h3>📋 商品详情</h3><p>{description.replace(chr(10), '<br>')}</p>"
        
        # 构建分类（微信小店需要数字类目ID，这里简化处理）
        category = product_data.get('category', {}).get('primary', '宠物用品')
        
        payload = {
            "title": product_data.get('title', '')[:30],  # 标题最多30字
            "desc": selling_points[0] if selling_points else product_data.get('title', ''),
            "cats": [category],  # 类目数组
            "price": price,
            "stock_num": int(os.getenv('WECHAT_SHOP_DEFAULT_STOCK', 100)),
            "head_imgs": ["https://mmbiz.qpic.cn/sz_mmbiz_jpg/xxxxx/xxxx.jpg"],  # 需要替换为真实图片URL
            "detail": detail_html,
            "express_info": {
                "template_id": os.getenv('WECHAT_SHOP_SHIPPING_TEMPLATE_ID', '0')
            }
        }
        
        try:
            resp = requests.post(url, params=params, json=payload, timeout=30)
            result = resp.json()
            
            if result.get('errcode') == 0:
                return {
                    "success": True,
                    "product_id": result.get('data', {}).get('product_id'),
                    "message": "商品上架成功"
                }
            else:
                return {
                    "success": False,
                    "error_code": result.get('errcode'),
                    "message": result.get('errmsg', '未知错误')
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"请求失败: {e}"
            }
    
    def list_products(self, page: int = 1, page_size: int = 20) -> Dict:
        """获取商品列表"""
        url = f"{self.base_url}/product/list"
        params = {
            "access_token": self.access_token,
            "page": page,
            "page_size": page_size
        }
        
        try:
            resp = requests.get(url, params=params, timeout=10)
            return resp.json()
        except Exception as e:
            return {"error": str(e)}


def main():
    """示例：自动上架商品"""
    import sys
    
    # 示例商品数据（实际使用时可以从skill生成）
    product = {
        "title": "智能自动喂食器猫狗定时定量投食器远程控制",
        "description": "✨ 智能自动喂食器，让毛孩子按时吃饭\\n\\n定时定量喂食，科学喂养更健康...",
        "selling_points": [
            "定时定量喂食，科学控制宠物体重",
            "APP远程操控，随时随地查看喂食记录",
            "4L大容量储粮，单猫可吃15天",
            "双重防卡粮设计，出粮顺畅不堵塞",
            "双重供电保障，断电也不怕饿到毛孩子"
        ],
        "suggested_price": {"recommended": 169},
        "category": {"primary": "宠物用品"},
        "keywords": ["自动喂食器", "智能喂食器", "定时喂食"]
    }
    
    # 初始化API客户端（自动读取.env中的配置）
    try:
        api = WechatShopAPI()
        print("✅ API客户端初始化成功")
        
        # 上架商品
        print("🚀 正在上架商品...")
        result = api.add_product(product)
        
        if result['success']:
            print(f"✅ {result['message']}")
            print(f"📦 商品ID: {result['product_id']}")
        else:
            print(f"❌ 上架失败: {result['message']}")
            print(f"错误码: {result.get('error_code')}")
            
    except Exception as e:
        print(f"❌ 错误: {e}")
        print("\\n💡 请检查：")
        print("1. .env文件是否存在且包含正确的appid和secret")
        print("2. 网络连接是否正常")
        print("3. API权限是否已开通")


if __name__ == '__main__':
    main()
