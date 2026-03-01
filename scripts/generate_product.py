#!/usr/bin/env python3
"""
微信小店商品信息生成器
根据商品基本信息生成完整的上架资料
"""

import json
import sys
import argparse
from typing import Dict, List, Optional

def generate_title(product_name: str, category: str, attributes: List[str]) -> str:
    """生成商品标题"""
    # 标题结构：核心词 + 属性词 + 场景词
    title_parts = [product_name]
    
    # 添加关键属性
    for attr in attributes[:3]:  # 最多3个属性
        if len(''.join(title_parts)) + len(attr) < 26:
            title_parts.append(attr)
    
    title = ''.join(title_parts)
    
    # 确保长度在合理范围
    if len(title) > 30:
        title = title[:30]
    elif len(title) < 10:
        title += f"{category}推荐"
    
    return title

def generate_description(product_name: str, attributes: Dict, specs: Dict) -> str:
    """生成商品描述"""
    sections = []
    
    # 开篇吸引
    sections.append(f"✨ {product_name}，品质之选")
    sections.append("")
    
    # 产品参数
    sections.append("📋 产品参数")
    for key, value in specs.items():
        sections.append(f"• {key}：{value}")
    sections.append("")
    
    # 产品特色
    sections.append("🌟 产品特色")
    sections.append(f"精选优质材料，精工细作，给您舒适的{product_name}体验。")
    sections.append("")
    
    # 使用场景
    sections.append("🎯 适用场景")
    sections.append("适合日常穿着/使用，百搭时尚，轻松驾驭各种场合。")
    sections.append("")
    
    # 售后保障
    sections.append("🛡️ 售后保障")
    sections.append("• 正品保证，假一赔十")
    sections.append("• 7天无理由退换")
    sections.append("• 质量问题包退包换")
    
    return '\n'.join(sections)

def generate_selling_points(product_name: str, attributes: List[str]) -> List[str]:
    """生成卖点"""
    points = []
    
    # 基础卖点模板
    templates = [
        "精选优质材质，舒适亲肤",
        "精工细作，品质保证", 
        "经典百搭，永不过时",
        "性价比高，物超所值",
        "多尺码可选，适合各种身材"
    ]
    
    # 根据属性生成卖点
    for i, attr in enumerate(attributes[:3]):
        if i < len(templates):
            points.append(f"{attr} - {templates[i]}")
    
    # 确保有3-5个卖点
    while len(points) < 3:
        points.append(templates[len(points)])
    
    return points[:5]

def suggest_price(cost_price: float, category: str) -> Dict:
    """建议售价"""
    # 不同类目利润率
    margin_rates = {
        'clothing': 0.5,      # 服装 50%
        'beauty': 0.6,        # 美妆 60%
        'food': 0.25,         # 食品 25%
        'digital': 0.35,      # 数码 35%
        'home': 0.4,          # 家居 40%
        'pet': 0.45,          # 宠物用品 45%
        'pet_food': 0.35,     # 宠物食品 35%
        'pet_health': 0.6,    # 宠物医疗 60%
        'default': 0.4        # 默认 40%
    }
    
    margin = margin_rates.get(category, margin_rates['default'])
    
    base_price = cost_price * (1 + margin)
    
    # 应用心理定价
    recommended = round(base_price * 0.95)  # 略低于计算价
    
    # 调整到常见的尾数
    if recommended < 50:
        recommended = (recommended // 10) * 10 + 9  # 19, 29, 39...
    else:
        recommended = (recommended // 50) * 50 + 49  # 49, 99, 149...
    
    return {
        "min": round(base_price * 0.8),
        "max": round(base_price * 1.2),
        "recommended": recommended,
        "cost": cost_price
    }

def suggest_category(product_name: str, description: str = "") -> Dict:
    """建议分类"""
    # 简单的关键词匹配
    keywords = {
        '女装': ['女', '裙', '连衣裙', '女装'],
        '男装': ['男', '男装', '男士'],
        'T恤': ['T恤', 't恤', '短袖'],
        '鞋': ['鞋', '靴', '拖鞋'],
        '包': ['包', '袋', '箱'],
        '美妆': ['化妆品', '护肤', '口红', '面膜'],
        '食品': ['食品', '零食', '水果', '茶'],
        '家居': ['家居', '收纳', '床品', '装饰'],
        '数码': ['手机', '耳机', '数据线', '充电宝'],
        '母婴': ['婴儿', '宝宝', '童装', '玩具'],
        '宠物用品': ['猫', '狗', '宠物', '猫粮', '狗粮', '猫砂', '猫砂盆', '牵引绳', '宠物玩具', '宠物窝'],
        '宠物食品': ['猫粮', '狗粮', '罐头', '零食', '营养膏'],
        '宠物医疗保健': ['驱虫', '疫苗', '维生素', '补钙']
    }
    
    text = product_name + description
    
    for category, words in keywords.items():
        for word in words:
            if word in text:
                return {
                    "primary": category,
                    "secondary": "其他",
                    "confidence": "medium"
                }
    
    return {
        "primary": "未分类",
        "secondary": "其他",
        "confidence": "low"
    }

def generate_keywords(product_name: str, category: str) -> List[str]:
    """生成搜索关键词"""
    words = product_name.replace('，', ' ').replace(',', ' ').split()
    keywords = []
    
    for word in words:
        if len(word) >= 2:
            keywords.append(word)
    
    keywords.append(category)
    keywords.append(f"优质{product_name}")
    
    return list(set(keywords))[:10]

def main():
    parser = argparse.ArgumentParser(description='生成微信小店商品信息')
    parser.add_argument('--name', required=True, help='商品名称')
    parser.add_argument('--category', default='default', help='商品类目')
    parser.add_argument('--cost', type=float, required=True, help='成本价')
    parser.add_argument('--attrs', nargs='+', default=[], help='商品属性')
    parser.add_argument('--specs', type=json.loads, default='{}', help='规格参数(JSON)')
    
    args = parser.parse_args()
    
    # 生成完整商品信息
    result = {
        "title": generate_title(args.name, args.category, args.attrs),
        "description": generate_description(args.name, {}, args.specs),
        "selling_points": generate_selling_points(args.name, args.attrs),
        "keywords": generate_keywords(args.name, args.category),
        "suggested_price": suggest_price(args.cost, args.category),
        "category": suggest_category(args.name),
        "shipping_template": "建议设置满69元包邮"
    }
    
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
