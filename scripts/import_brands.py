"""
品牌数据导入脚本 - 简化版
从Excel文件导入品牌列表到数据库
"""
import pandas as pd
import sys
import os
import re

# 添加后端目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

def clean_brand_name(brand_name):
    """清理品牌名称，去掉店铺后缀"""
    if pd.isna(brand_name):
        return None
    
    name = str(brand_name).strip()
    
    # 去掉常见的店铺后缀
    suffixes = [
        '官方旗舰店', '旗舰店', '官方海外旗舰店', '海外旗舰店',
        '官方', '海外', '旗舰店'
    ]
    
    for suffix in suffixes:
        name = name.replace(suffix, '')
    
    return name.strip()

def import_brands_from_excel(excel_path):
    """从Excel文件导入品牌数据"""
    
    print(f"正在读取Excel文件: {excel_path}")
    df = pd.read_excel(excel_path)
    
    print(f"读取到 {len(df)} 行数据")
    print(f"列名: {df.columns.tolist()}")
    
    # 提取品牌名称并去重
    brand_names = []
    for index, row in df.iterrows():
        brand_name = clean_brand_name(row.get('店铺名称', ''))
        if brand_name and brand_name not in brand_names:
            brand_names.append(brand_name)
            print(f"提取品牌: {brand_name}")
    
    print(f"\n共提取 {len(brand_names)} 个唯一品牌")
    
    # 保存到JSON文件（供后端导入）
    import json
    output_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'brands.json')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    brands_data = []
    for name in brand_names:
        brands_data.append({
            "name": name,
            "search_keywords": name,
            "category": "",
            "is_active": True
        })
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(brands_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n品牌数据已保存到: {output_path}")
    
    return brand_names

if __name__ == '__main__':
    excel_path = '/Users/zhangweng/.qwenpaw/workspaces/default/media/5a879a5fadc44f21bb111cc2590382e4_TOP20合作客户.xlsx'
    
    if os.path.exists(excel_path):
        brands = import_brands_from_excel(excel_path)
        print(f"\n成功提取 {len(brands)} 个品牌")
    else:
        print(f"Excel文件不存在: {excel_path}")
