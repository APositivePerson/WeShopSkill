#!/usr/bin/env python3
"""
商品资料格式化导出
将生成的商品信息导出为各种格式
"""

import json
import sys
import argparse
from datetime import datetime

def export_json(data: dict) -> str:
    """导出为JSON格式"""
    return json.dumps(data, ensure_ascii=False, indent=2)

def export_markdown(data: dict) -> str:
    """导出为Markdown格式（便于复制粘贴）"""
    md = f"""# {data.get('title', '商品信息')}

## 商品标题
```
{data.get('title', '')}
```

## 商品描述
{data.get('description', '')}

## 核心卖点
"""
    for i, point in enumerate(data.get('selling_points', []), 1):
        md += f"{i}. {point}\n"
    
    md += f"""
## 关键词
{', '.join(data.get('keywords', []))}

## 价格建议
- 成本价：¥{data.get('suggested_price', {}).get('cost', 0)}
- 建议售价：¥{data.get('suggested_price', {}).get('recommended', 0)}
- 价格区间：¥{data.get('suggested_price', {}).get('min', 0)} - ¥{data.get('suggested_price', {}).get('max', 0)}

## 分类建议
- 一级分类：{data.get('category', {}).get('primary', '')}
- 二级分类：{data.get('category', {}).get('secondary', '')}

## 运费设置
{data.get('shipping_template', '')}

---
生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    return md

def export_csv_line(data: dict) -> str:
    """导出为CSV格式（适合批量导入）"""
    fields = [
        data.get('title', ''),
        data.get('description', '').replace('\n', ' ').replace(',', '，'),
        '|'.join(data.get('selling_points', [])),
        '|'.join(data.get('keywords', [])),
        str(data.get('suggested_price', {}).get('recommended', 0)),
        data.get('category', {}).get('primary', ''),
        data.get('category', {}).get('secondary', '')
    ]
    return ','.join([f'"{f}"' for f in fields])

def export_wechat_template(data: dict) -> str:
    """导出为微信小店批量导入格式"""
    template = f"""
╔════════════════════════════════════════════════════════════╗
║               微信小店商品上架资料                         ║
╠════════════════════════════════════════════════════════════╣
  【商品标题】
  {data.get('title', '')}

  【商品详情】
  {data.get('description', '')}

  【卖点标签】
  {' | '.join(data.get('selling_points', []))}

  【搜索关键词】
  {', '.join(data.get('keywords', []))}

  【价格设置】
  售价：¥{data.get('suggested_price', {}).get('recommended', 0)}
  原价：¥{data.get('suggested_price', {}).get('max', 0)}

  【商品分类】
  {data.get('category', {}).get('primary', '')} > {data.get('category', {}).get('secondary', '')}

  【运费设置】
  {data.get('shipping_template', '')}
╚════════════════════════════════════════════════════════════╝
"""
    return template

def main():
    parser = argparse.ArgumentParser(description='格式化导出商品资料')
    parser.add_argument('--input', '-i', required=True, help='输入JSON文件路径')
    parser.add_argument('--format', '-f', choices=['json', 'markdown', 'csv', 'wechat'], 
                       default='wechat', help='输出格式')
    parser.add_argument('--output', '-o', help='输出文件路径')
    
    args = parser.parse_args()
    
    # 读取输入数据
    with open(args.input, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 根据格式导出
    formatters = {
        'json': export_json,
        'markdown': export_markdown,
        'csv': export_csv_line,
        'wechat': export_wechat_template
    }
    
    output = formatters[args.format](data)
    
    # 输出到文件或stdout
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"已导出到: {args.output}")
    else:
        print(output)

if __name__ == '__main__':
    main()
