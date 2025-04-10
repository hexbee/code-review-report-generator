#!/usr/bin/env python3
import json
import os
import click
import traceback
from jinja2 import Environment, FileSystemLoader
from code_review_models import CodeReviewReport, validate_json_file


def convert_json_to_html(json_file, template_file, output_file):
    """
    将JSON文件转换为HTML报告，使用Pydantic验证数据并使用Jinja2模板引擎
    
    Args:
        json_file (str): JSON文件路径
        template_file (str): HTML模板文件路径
        output_file (str): 输出HTML文件路径
    """
    try:
        # 加载并验证JSON数据
        click.echo(f"正在加载并验证JSON数据: {json_file}")
        report = validate_json_file(json_file)
        click.echo(f"成功加载JSON数据: {json_file}")
        
        # 设置Jinja2环境
        template_dir = os.path.dirname(template_file)
        if not template_dir:
            template_dir = '.'
        template_name = os.path.basename(template_file)
        click.echo(f"模板目录: {template_dir}, 模板名称: {template_name}")
        
        env = Environment(loader=FileSystemLoader(template_dir))
        
        # 添加自定义过滤器，计算通过的检查项数量
        def count_passed(items):
            if items is None:
                return 0
            return sum(1 for item in items if item.get('passed', False))
        
        env.filters['count_passed'] = count_passed
        
        try:
            # 加载模板
            template = env.get_template(template_name)
            click.echo(f"成功加载模板: {template_file}")
            
            # 检查数据结构
            click.echo(f"数据结构: 标题='{report.title}', 检查清单项数量={len(report.checklist.items)}")
            
            # 直接渲染HTML
            # 将Pydantic模型转换为dict
            data_dict = report.model_dump()
            html = template.render(data=data_dict)
            click.echo("成功渲染HTML")
            
            # 如果需要嵌入CSS
            css_file = 'static/styles.css'
            if os.path.exists(css_file):
                with open(css_file, 'r', encoding='utf-8') as f:
                    css_content = f.read()
                    click.echo(f"已加载CSS样式: {css_file}")
                # 将CSS嵌入到HTML中
                html = html.replace('<link rel="stylesheet" href="../static/styles.css">', 
                                   f'<style>\n{css_content}\n</style>')
            
            # 确保输出目录存在
            output_dir = os.path.dirname(output_file)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
            
            # 保存文件
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html)
                
            click.echo(f"成功生成HTML报告: {output_file}")
        except Exception as template_error:
            click.echo(f"模板处理错误: {str(template_error)}")
            traceback.print_exc()
            raise
        
    except Exception as e:
        click.echo(f"错误: {str(e)}", err=True)
        traceback.print_exc()
        raise click.Abort()


@click.command()
@click.option('--json-file', '-j', required=True, help='输入JSON文件路径')
@click.option('--template', '-t', default='templates/report_template.html', help='HTML模板文件路径')
@click.option('--output', '-o', default='output/report.html', help='输出HTML文件路径')
@click.option('--validate-only', '-v', is_flag=True, help='仅验证JSON数据，不生成HTML')
def main(json_file, template, output, validate_only):
    """将代码审查JSON报告转换为HTML格式，使用Pydantic验证数据"""
    if validate_only:
        try:
            report = validate_json_file(json_file)
            click.echo(f"✅ 验证成功! 报告标题: {report.title}")
            click.echo(f"   检查项: {report.checklist.passed}/{report.checklist.total}")
            click.echo(f"   发现问题: {len(report.findings)}")
        except Exception as e:
            click.echo(f"❌ 验证失败: {e}")
            raise click.Abort()
    else:
        convert_json_to_html(json_file, template, output)


if __name__ == '__main__':
    main() 