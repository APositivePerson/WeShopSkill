#!/usr/bin/env python3
"""
宠物用品专用生成器
针对宠物用品店的特殊需求优化
"""

import json
import sys
import argparse

def generate_pet_product(product_type: str, pet_kind: str, brand: str = "", cost: float = 0):
    """生成宠物用品商品信息"""
    
    # 宠物类型映射
    pet_names = {
        'cat': '猫咪',
        'dog': '狗狗',
        'both': '猫狗通用',
        'bird': '鸟类',
        'fish': '水族',
        'rabbit': '兔子',
        'hamster': '仓鼠'
    }
    
    pet_name = pet_names.get(pet_kind, '宠物')
    
    # 产品类型模板
    templates = {
        '猫砂盆': {
            'title_suffix': '大号封闭式防外溅除臭',
            'selling_points': [
                '超大空间，肥猫也能转身',
                '半封闭设计，防外溅防带砂',
                '活性炭除臭，有效隔绝异味',
                '易拆卸清洗，懒人福音',
                '环保材质，安全无异味'
            ],
            'keywords': ['猫砂盆', '封闭式', '大号', '防外溅', '除臭'],
            'margin': 0.45
        },
        '猫粮': {
            'title_suffix': '天然无谷全价猫粮营养增肥',
            'selling_points': [
                '天然无谷配方，降低过敏风险',
                '高蛋白含量，满足猫咪营养需求',
                '添加益生菌，呵护肠胃健康',
                '适口性佳，挑嘴猫也爱吃',
                '全价营养，幼猫成猫都适用'
            ],
            'keywords': ['猫粮', '天然粮', '无谷', '全价', '营养'],
            'margin': 0.35
        },
        '狗粮': {
            'title_suffix': '天然狗粮中大型犬通用型',
            'selling_points': [
                '优质肉类蛋白来源，强健体魄',
                '添加葡萄糖胺，保护关节',
                '均衡脂肪酸，毛发更亮丽',
                '天然抗氧化成分，增强免疫力',
                '适口性测试，90%以上狗狗爱吃'
            ],
            'keywords': ['狗粮', '天然', '中大型犬', '通用', '营养'],
            'margin': 0.35
        },
        '牵引绳': {
            'title_suffix': '遛狗绳背心式胸背带防挣脱',
            'selling_points': [
                '背心式设计，分散压力不伤颈',
                '透气网布，夏天不闷热',
                '反光条设计，夜间出行更安全',
                '防爆冲设计，轻松控制大型犬',
                '快速穿脱，3秒搞定'
            ],
            'keywords': ['牵引绳', '胸背带', '遛狗绳', '防挣脱', '背心式'],
            'margin': 0.5
        },
        '猫抓板': {
            'title_suffix': '耐磨瓦楞纸猫爪板磨爪器',
            'selling_points': [
                '高密度瓦楞纸，耐磨耐抓',
                '双面可用，延长使用寿命',
                '剑麻材质，天然不掉屑',
                '造型可爱，还能当猫窝',
                '保护家具，让猫咪尽情磨爪'
            ],
            'keywords': ['猫抓板', '磨爪', '瓦楞纸', '剑麻', '猫玩具'],
            'margin': 0.55
        },
        '宠物窝': {
            'title_suffix': '四季通用可拆洗保暖猫窝狗窝',
            'selling_points': [
                '加厚填充，保暖又柔软',
                '可拆洗设计，清洁更方便',
                '防滑底部，不易移位',
                '四季通用，冬暖夏凉',
                '多尺码可选，适合各种体型'
            ],
            'keywords': ['宠物窝', '猫窝', '狗窝', '保暖', '可拆洗'],
            'margin': 0.5
        },
        '逗猫棒': {
            'title_suffix': '长杆羽毛逗猫棒耐咬猫玩具',
            'selling_points': [
                '长杆设计，主人不累手',
                '天然羽毛，激发捕猎本能',
                '弹性钢丝，摆动更灵活',
                '耐咬材质，不易损坏',
                '互动神器，增进人宠感情'
            ],
            'keywords': ['逗猫棒', '猫玩具', '羽毛', '互动', '耐咬'],
            'margin': 0.6
        },
        '驱虫药': {
            'title_suffix': '体内外驱虫滴剂除跳蚤蜱虫',
            'selling_points': [
                '体内外同驱，一次搞定',
                '进口原液，品质有保障',
                '温和配方，不刺激皮肤',
                '持续防护30天，省心省力',
                '正品保证，防伪可查'
            ],
            'keywords': ['驱虫药', '体内外驱虫', '跳蚤', '蜱虫', '宠物保健'],
            'margin': 0.55,
            'note': '⚠️ 销售驱虫药需要相关资质'
        }
    }
    
    # 获取模板或使用默认
    template = templates.get(product_type, {
        'title_suffix': '宠物用品高品质',
        'selling_points': [
            '精选优质材料，安全无毒',
            '针对宠物习性设计，实用性强',
            '易于清洁打理，方便使用',
            '经久耐用，性价比高',
            '好评如潮，万千铲屎官推荐'
        ],
        'keywords': ['宠物用品', pet_name, product_type],
        'margin': 0.45
    })
    
    # 生成标题
    brand_prefix = f"【{brand}】" if brand else ""
    title = f"{brand_prefix}{pet_name}{product_type}{template['title_suffix']}"
    
    # 确保标题长度
    if len(title) > 30:
        title = title[:30]
    
    # 计算价格
    margin = template.get('margin', 0.45)
    if cost > 0:
        base_price = cost * (1 + margin)
        recommended = round(base_price * 0.95)
        # 心理定价
        if recommended < 50:
            recommended = (recommended // 10) * 10 - 1
        else:
            recommended = (recommended // 50) * 50 - 1
    else:
        recommended = 0
    
    # 生成长描述
    description = f"""✨ {pet_name}专用{product_type}，品质之选

🐾 产品特色
{chr(10).join(['• ' + sp for sp in template['selling_points'][:3]])}

📋 产品参数
• 适用对象：{pet_name}
• 材质：优质环保材料
• 包装：独立包装

🎯 适用场景
适合日常家用，给{pet_name}更好的生活体验。

🛡️ 售后保障
• 正品保证，假一赔十
• 7天无理由退换
• 质量问题包退包换
• 专业客服在线解答

💡 使用建议
根据{pet_name}的体型和习惯选择合适规格，如有疑问请联系客服。"""
    
    result = {
        "title": title,
        "description": description,
        "selling_points": template['selling_points'],
        "keywords": template['keywords'] + [pet_name, '宠物'],
        "suggested_price": {
            "cost": cost,
            "recommended": recommended,
            "min": round(cost * (1 + margin * 0.8)) if cost > 0 else 0,
            "max": round(cost * (1 + margin * 1.2)) if cost > 0 else 0
        },
        "category": {
            "primary": "宠物用品",
            "secondary": product_type,
            "pet_type": pet_kind
        },
        "shipping_template": "建议设置满69元包邮（宠物用品重量较大）"
    }
    
    if 'note' in template:
        result['note'] = template['note']
    
    return result

def main():
    parser = argparse.ArgumentParser(description='生成宠物用品商品信息')
    parser.add_argument('--type', '-t', required=True, help='产品类型（如：猫砂盆、猫粮、牵引绳）')
    parser.add_argument('--pet', '-p', default='cat', choices=['cat', 'dog', 'both', 'bird', 'fish', 'rabbit', 'hamster'],
                       help='适用宠物类型')
    parser.add_argument('--brand', '-b', default='', help='品牌名称')
    parser.add_argument('--cost', '-c', type=float, default=0, help='成本价')
    
    args = parser.parse_args()
    
    result = generate_pet_product(args.type, args.pet, args.brand, args.cost)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
