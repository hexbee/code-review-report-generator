# 代码审查报告生成器

这是一个将JSON格式的代码审查数据转换为HTML报告的工具。

## 功能特点

- 使用Pydantic进行数据验证和类型检查
- 使用Jinja2模板引擎渲染HTML
- 支持自定义HTML模板
- 提供JSON Schema验证
- 自动计算审查清单统计数据
- 支持嵌入CSS样式
- 严格验证35项标准检查清单

## 安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/code-review-report-generator.git
cd code-review-report-generator

# 安装依赖
pip install -r requirements.txt
```

## 使用方法

### 准备输入文件

项目需要一个JSON格式的代码审查报告文件作为输入。您可以：

1. 使用提供的示例文件进行测试：
   ```bash
   cp example_code_review_report.json code_review_report.json
   ```

2. 创建自己的代码审查报告文件，确保它符合项目的数据模型要求。

**注意**：用户创建的`code_review_report.json`文件是输入数据，不应该加入版本控制系统。

### 生成HTML报告

```bash
# 使用基础版本
python json2html.py -j code_review_report.json

# 使用带Pydantic验证的版本
python json2html_pydantic.py -j code_review_report.json

# 指定自定义模板和输出路径
python json2html_pydantic.py -j code_review_report.json -t templates/my_template.html -o output/my_report.html

# 仅验证JSON数据，不生成HTML
python json2html_pydantic.py -j code_review_report.json -v
```

### 使用Pydantic模型验证数据

```python
from code_review_models import validate_json_file

# 验证JSON文件
report = validate_json_file('code_review_report.json')

# 使用验证后的数据
print(f"报告标题: {report.title}")
print(f"检查项: {report.checklist.passed}/{report.checklist.total}")
print(f"发现问题: {len(report.findings)}")
```

### 生成JSON Schema

项目使用Pydantic模型自动生成JSON Schema。可以运行以下命令生成schema文件：

```bash
python generate_schema.py
```

生成的`code_review_schema.json`文件可用于：
- 前端验证
- API文档
- 第三方工具集成

由于该文件是自动生成的，不建议将其加入版本控制系统。

## 数据格式

数据格式基于Pydantic模型定义，可以通过生成JSON Schema查看完整定义。查看`example_code_review_report.json`文件以了解具体示例。

基本结构如下：

```json
{
  "title": "Code Review Report",
  "meta": {
    "commit": "6be21d97aea8ee4eb13249f6c9609a7121ee67fa",
    "author": "Name",
    "email": "name@xxx.com",
    "date": "Wed Apr 2 09:33:19 2025 +0800"
  },
  "commit_message": "...",
  "main_changes": ["...", "..."],
  "checklist": {
    "items": [
      {
        "id": 1,
        "description": "确保没有使用未初始化的指针",
        "passed": true
      },
      ...
    ]
  },
  "findings": [
    {
      "id": "P001",
      "category": "可维护性",
      "severity": "medium",
      "location": "/path/to/file.cpp:123",
      "description": "...",
      "recommendation": "..."
    },
    ...
  ]
}
```

## 自定义模板

可以通过修改 `templates/report_template.html` 来自定义HTML报告的样式和结构。模板使用Jinja2语法。

## 目录结构

```
.
├── json2html.py                   # 基础版本的JSON到HTML转换脚本
├── json2html_pydantic.py          # 使用Pydantic的JSON到HTML转换脚本
├── code_review_models.py          # Pydantic数据模型
├── generate_schema.py             # 生成JSON Schema的脚本
├── example_code_review_report.json # 示例输入数据
├── requirements.txt               # 项目依赖
├── templates/                     # HTML模板目录
│   └── report_template.html       # 默认HTML模板
├── static/                        # 静态资源目录
│   └── styles.css                 # CSS样式
└── output/                        # 输出目录
    └── report.html                # 生成的HTML报告
```

## 检查清单验证

项目确保检查清单必须包含35个标准项目，不能多也不能少。可以使用提供的测试脚本验证这一功能：

```bash
python test_checklist_validation.py
```

检查清单验证包括：
- 确保正好有35个检查项目
- 确保ID从1到35连续且完整
- 确保每个ID对应的描述文本符合标准
- 自动计算通过/失败的项目数量

## 许可证

Apache-2.0 
