#!/usr/bin/env python3
import json
from code_review_models import CodeReviewReport
from pydantic.json_schema import model_json_schema

def generate_schema():
    """从Pydantic模型生成JSON Schema并保存到文件"""
    # 获取CodeReviewReport模型的JSON Schema
    schema = model_json_schema(CodeReviewReport)
    
    # 添加$schema字段以符合JSON Schema标准
    schema["$schema"] = "http://json-schema.org/draft-07/schema#"
    
    # 美化输出的JSON格式
    schema_json = json.dumps(schema, indent=2, ensure_ascii=False)
    
    # 保存到文件
    with open("code_review_schema.json", "w", encoding="utf-8") as f:
        f.write(schema_json)
    
    print(f"✅ JSON Schema 已生成到 code_review_schema.json")

if __name__ == "__main__":
    generate_schema()
