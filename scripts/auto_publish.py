#!/usr/bin/env python3
"""
一键上架工具
结合skill生成 + API自动上架
"""

import os
import sys
import json
import subprocess

# 添加脚本目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wechat_shop_api import WechatShopAPI
from pet_product_generator import generate_pet_product

def auto_publish(product_type: str, pet_kind: str, cost: float, brand: str = ""):
    """
    一键生成并上架商品
    
    Args:
        product_type: 产品类型（如：猫砂盆、猫粮）
        pet_kind: 宠物类型（cat/dog/both）
        cost: 成本价
        brand: 品牌名称（可选）
    """
    print(f"🎯 开始一键上架：{product_type}")
    print("-" * 40)
    
    # 步骤1：生成商品资料
    print("📝 步骤1：生成商品资料...")
    product_data = generate_pet_product(product_type, pet_kind, brand, cost)
    print(f"✅ 标题：{product_data['title']}")
    print(f"✅ 建议售价：¥{product_data['suggested_price']['recommended']}")
    
    # 步骤2：保存到文件（便于查看和备份）
    output_file = f"/tmp/product_{product_type}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(product_data, f, ensure_ascii=False, indent=2)
    print(f"💾 已保存到：{output_file}")
    
    # 步骤3：调用API上架
    print("\\n🚀 步骤2：调用微信小店API上架...")
    try:
        api = WechatShopAPI()
        result = api.add_product(product_data)
        
        if result['success']:
            print(f"✅ 上架成功！商品ID：{result['product_id']}")
            print("\\n💡 提示：")
            print("- 请登录微信小店后台上传商品主图")
            print("- 检查商品信息是否正确")
            print("- 确认无误后手动上架")
        else:
            print(f"❌ 上架失败：{result['message']}")
            print(f"错误码：{result.get('error_code')}")
            
    except Exception as e:
        print(f"❌ API调用失败：{e}")
        print("\\n💡 可能原因：")
        print("1. API权限未开通")
        print("2. appid/secret错误")
        print("3. 网络问题")
        print(f"\\n商品资料已保存，可以手动复制到微信小店后台上传")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='一键上架商品到微信小店')
    parser.add_argument('--type', '-t', required=True, help='产品类型（如：猫砂盆、猫粮）')
    parser.add_argument('--pet', '-p', default='cat', choices=['cat', 'dog', 'both'],
                       help='适用宠物类型')
    parser.add_argument('--cost', '-c', type=float, required=True, help='成本价')
    parser.add_argument('--brand', '-b', default='', help='品牌名称')
    parser.add_argument('--dry-run', action='store_true', 
                       help='仅生成资料，不上架')
    
    args = parser.parse_args()
    
    if args.dry_run:
        # 仅生成资料
        product = generate_pet_product(args.type, args.pet, args.brand, args.cost)
        print(json.dumps(product, ensure_ascii=False, indent=2))
    else:
        # 生成并上架
        auto_publish(args.type, args.pet, args.cost, args.brand)

if __name__ == '__main__':
    main()
