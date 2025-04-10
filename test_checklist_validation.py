#!/usr/bin/env python3
"""测试检查清单的验证功能"""

import json
import sys
from code_review_models import ChecklistItem, Checklist, ChecklistItemType

def test_invalid_report():
    """测试各种无效的检查清单配置"""
    
    # 测试1: 缺少项目
    print("\n测试1: 检查清单项目数量不足")
    try:
        # 只有34个项目
        items = [
            ChecklistItem(id=i, 
                          description=getattr(ChecklistItemType, f"ITEM_{i}"), 
                          passed=True)
            for i in range(1, 35)  # 缺少第35项
        ]
        checklist = Checklist(items=items)
        print("❌ 验证失败: 应该检测到项目数量不足")
    except ValueError as e:
        print(f"✅ 成功捕获错误: {e}")
    
    # 测试2: 项目ID不连续
    print("\n测试2: 检查清单项目ID不连续")
    try:
        # 35个项目，但ID为1-34和36
        items = [
            ChecklistItem(id=i, 
                          description=getattr(ChecklistItemType, f"ITEM_{i}"), 
                          passed=True)
            for i in range(1, 35)
        ]
        # 添加ID为36的项目而不是35
        items.append(
            ChecklistItem(id=36, 
                          description=getattr(ChecklistItemType, f"ITEM_1"),  # 随便用一个描述
                          passed=True)
        )
        checklist = Checklist(items=items)
        print("❌ 验证失败: 应该检测到ID不连续")
    except ValueError as e:
        print(f"✅ 成功捕获错误: {e}")
    
    # 测试3: 描述与ID不匹配
    print("\n测试3: 描述与ID不匹配")
    try:
        # ID和描述不匹配
        items = []
        for i in range(1, 36):
            # 故意错配ID和描述
            desc_id = 36 - i  # 反向匹配
            if desc_id <= 35:
                description = getattr(ChecklistItemType, f"ITEM_{desc_id}")
                items.append(
                    ChecklistItem(id=i, description=description, passed=True)
                )
        
        checklist = Checklist(items=items)
        print("❌ 验证失败: 应该检测到描述与ID不匹配")
    except ValueError as e:
        print(f"✅ 成功捕获错误: {e}")
    
    # 测试4: 有效的检查清单
    print("\n测试4: 有效的检查清单")
    try:
        # 正确的35个项目
        items = [
            ChecklistItem(id=i, 
                          description=getattr(ChecklistItemType, f"ITEM_{i}"), 
                          passed=(i % 2 == 0))  # 偶数ID的项目通过
            for i in range(1, 36)
        ]
        checklist = Checklist(items=items)
        print(f"✅ 验证成功: 检查清单有 {checklist.total} 项，通过 {checklist.passed} 项")
    except ValueError as e:
        print(f"❌ 验证失败: {e}")

if __name__ == "__main__":
    test_invalid_report() 