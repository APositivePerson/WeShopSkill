#!/usr/bin/env python3
"""
商品标题优化器
优化标题以提升搜索排名和点击率
"""

import json
import sys
import argparse
import re

def analyze_title(title: str) -> dict:
    """分析标题质量"""
    issues = []
    score = 100
    
    # 长度检查
    if len(title) < 10:
        issues.append("标题过短，建议10-30字")
        score -= 20
    elif len(title) > 30:
        issues.append(f"标题过长({len(title)}字)，建议控制在30字以内")
        score -= 15
    
    # 检查极限词
    forbidden_words = ['最', '第一', '顶级', '唯一', '绝对', '100%', '极品']
    found_forbidden = [w for w in forbidden_words if w in title]
    if found_forbidden:
        issues.append(f"包含极限词: {', '.join(found_forbidden)}")
        score -= 30
    
    # 检查特殊符号
    special_chars = re.findall(r'[★☆※◆◇■□▲△]', title)
    if special_chars:
        issues.append(f"包含特殊符号: {', '.join(set(special_chars))}")
        score -= 10
    
    # 检查重复
    words = list(title)
    for word in set(words):
        if words.count(word) > 3:
            issues.append(f"'{word}'重复过多")
            score -= 5
    
    return {
        "score": max(0, score),
        "issues": issues,
        "length": len(title)
    }

def optimize_title(title: str, keywords: list = None) -> str:
    """优化标题"""
    optimized = title
    
    # 移除极限词
    forbidden_words = ['最', '顶级', '极品', '绝对']
    for word in forbidden_words:
        optimized = optimized.replace(word, '优质')
    
    # 移除特殊符号
    optimized = re.sub(r'[★☆※◆◇■□▲△]', '', optimized)
    
    # 添加关键词（如果提供且标题还有空间）
    if keywords:
        for kw in keywords:
            if kw not in optimized and len(optimized) + len(kw) < 28:
                optimized += kw
    
    # 确保长度合适
    if len(optimized) > 30:
        optimized = optimized[:30]
    
    # 清理多余空格
    optimized = re.sub(r'\s+', '', optimized)
    
    return optimized

def suggest_keywords(category: str, product_type: str) -> list:
    """建议关键词"""
    keyword_map = {
        'clothing': ['新款', '时尚', '百搭', '显瘦', '舒适'],
        'beauty': ['保湿', '美白', '护肤', '正品', '网红'],
        'food': ['新鲜', '美味', '健康', '零食', '特产'],
        'home': ['简约', '实用', '北欧', 'ins风', '创意'],
        'digital': ['原装', '快充', '耐用', '兼容', '便携']
    }
    
    return keyword_map.get(category, ['热销', '推荐', '爆款'])

def main():
    parser = argparse.ArgumentParser(description='优化商品标题')
    parser.add_argument('--title', required=True, help='原始标题')
    parser.add_argument('--category', default='default', help='商品类目')
    parser.add_argument('--optimize', action='store_true', help='执行优化')
    
    args = parser.parse_args()
    
    # 分析标题
    analysis = analyze_title(args.title)
    
    result = {
        "original": args.title,
        "analysis": analysis,
        "suggested_keywords": suggest_keywords(args.category, args.title)
    }
    
    # 如果需要优化
    if args.optimize:
        result["optimized"] = optimize_title(args.title, result["suggested_keywords"])
        result["optimized_analysis"] = analyze_title(result["optimized"])
    
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
