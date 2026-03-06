#!/usr/bin/env python3
"""
ICIS CLI - 智能客户访谈系统命令行工具
"""

import argparse
import os
import sys
import yaml
import json
from datetime import datetime

# 获取 ICIS 根目录
ICIS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_template(industry):
    """加载行业模板"""
    template_path = os.path.join(ICIS_DIR, 'templates', 'manufacturing', f'{industry}.yaml')
    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    return None

def load_cases():
    """加载案例库"""
    cases_path = os.path.join(ICIS_DIR, 'knowledge_base', 'cases.json')
    if os.path.exists(cases_path):
        with open(cases_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'cases': []}

def load_scripts():
    """加载话术库"""
    scripts_path = os.path.join(ICIS_DIR, 'scripts', 'sellin_script_lib.py')
    if os.path.exists(scripts_path):
        # 动态导入话术库
        import importlib.util
        spec = importlib.util.spec_from_file_location("sellin_script_lib", scripts_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.SCRIPT_LIBRARY
    return {}

def cmd_plan(args):
    """生成访谈计划"""
    template = load_template(args.industry)
    if not template:
        print(f"错误：找不到行业模板 '{args.industry}'")
        print(f"可用模板：appliances, electronics, machinery")
        return
    
    print(f"\n{'='*60}")
    print(f"📋 访谈计划 - {args.company}")
    print(f"{'='*60}")
    print(f"\n行业：{template['industry']}")
    print(f"规模：{args.scale or '未指定'}")
    print(f"\n{'─'*60}")
    
    # 输出访谈对象
    print("\n🎯 推荐访谈对象（按优先级排序）：\n")
    for i, target in enumerate(template['interview_targets'], 1):
        print(f"  {i}. {target['role']}（优先级{target['priority']}，{target['duration']}分钟）")
        print(f"     目标：了解{'、'.join(target['key_questions'][:1])}...")
    
    # 输出预期痛点
    print(f"\n{'─'*60}")
    print("\n⚠️  预期痛点（基于行业模板）：\n")
    for pain in template['core_pain_points'][:3]:
        severity = "🔴" if pain['severity'] == '高' else "🟡"
        print(f"  {severity} {pain['name']} - {pain['description'][:30]}...")
    
    # 输出AI机会点
    print(f"\n{'─'*60}")
    print("\n💡 推荐 AI 解决方案：\n")
    for opp in template['ai_opportunities'][:3]:
        print(f"  • {opp['name']}")
        print(f"    价值：{opp['value_proposition']}")
    
    print(f"\n{'='*60}\n")
    
    # 保存到文件
    if args.output:
        output_dir = args.output
        os.makedirs(output_dir, exist_ok=True)
        
        plan_content = generate_plan_markdown(args.company, template, args.scale)
        plan_file = os.path.join(output_dir, f"{args.company}-访谈计划.md")
        with open(plan_file, 'w', encoding='utf-8') as f:
            f.write(plan_content)
        print(f"✓ 访谈计划已保存：{plan_file}")

def cmd_analyze(args):
    """分析访谈记录"""
    if not os.path.exists(args.input):
        print(f"错误：找不到输入文件 '{args.input}'")
        return
    
    with open(args.input, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"\n{'='*60}")
    print(f"🔍 访谈记录分析")
    print(f"{'='*60}\n")
    
    # 简单分析（实际应使用NLP）
    print("📊 分析结果：\n")
    
    # 提取关键词
    keywords = []
    if '订单' in content or '录入' in content:
        keywords.append(('订单处理效率', '高', '智能订单处理'))
    if '质量' in content or '追溯' in content:
        keywords.append(('质量管理追溯', '高', '视觉质检'))
    if '客户' in content or '响应' in content:
        keywords.append(('客户需求响应', '中', '智能客服'))
    
    if keywords:
        print("识别到的痛点：\n")
        for pain, severity, solution in keywords:
            print(f"  • {pain}（严重度：{severity}）")
            print(f"    → 推荐方案：{solution}")
    else:
        print("  未能自动识别痛点，请手动分析")
    
    print(f"\n{'='*60}\n")
    
    # 保存到文件
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(f"# 访谈记录分析\n\n## 原始记录\n\n{content}\n\n## 分析结果\n\n")
            for pain, severity, solution in keywords:
                f.write(f"- {pain}（{severity}）→ {solution}\n")
        print(f"✓ 分析报告已保存：{args.output}")

def cmd_script(args):
    """查询话术"""
    scripts = load_scripts()
    
    if not scripts:
        print("错误：无法加载话术库")
        return
    
    print(f"\n{'='*60}")
    print(f"💬 销售话术")
    print(f"{'='*60}\n")
    
    if args.type == 'opening':
        print("🎬 开场白：\n")
        for role, script in scripts.get('opening', {}).items():
            print(f"  【{role}】")
            print(f"  {script}\n")
    
    elif args.type == 'objection':
        print("🛡️ 异议处理：\n")
        if args.context:
            response = scripts.get('objection_handling', {}).get(args.context, "暂无标准话术")
            print(f"  异议：{args.context}")
            print(f"  回应：{response}\n")
        else:
            for objection, response in scripts.get('objection_handling', {}).items():
                print(f"  【{objection}】")
                print(f"  {response}\n")
    
    elif args.type == 'closing':
        print("🏁 Closing 话术：\n")
        for role, script in scripts.get('closing', {}).items():
            print(f"  【{role}】")
            print(f"  {script}\n")
    
    print(f"{'='*60}\n")

def cmd_case(args):
    """查询案例"""
    cases_data = load_cases()
    cases = cases_data.get('cases', [])
    
    print(f"\n{'='*60}")
    print(f"📚 成功案例")
    print(f"{'='*60}\n")
    
    filtered = cases
    if args.industry:
        filtered = [c for c in filtered if args.industry in c.get('tags', [])]
    if args.pain:
        filtered = [c for c in filtered if args.pain in c.get('pain', '')]
    
    if not filtered:
        print("未找到匹配的案例\n")
        return
    
    for case in filtered:
        print(f"  【{case['company']}】")
        print(f"  行业：{case['industry']} | 规模：{case['scale']}")
        print(f"  痛点：{case['pain']}")
        print(f"  方案：{case['solution']}")
        print(f"  效果：{case['result']}")
        print(f"  联系人：{case['contact']}")
        print(f"  Sell-in路径：{case['sell_in_path']}")
        print()
    
    print(f"{'='*60}\n")

def generate_plan_markdown(company, template, scale):
    """生成访谈计划 Markdown"""
    md = f"""# {company} - 访谈计划

## 客户信息
- **行业**：{template['industry']}
- **规模**：{scale or '未指定'}
- **业务模式**：{'、'.join(template['company_profile']['business_model'])}

## 访谈安排

"""
    for target in template['interview_targets']:
        md += f"""### {target['role']}（优先级{target['priority']}，{target['duration']}分钟）

**目标**：了解{target['key_questions'][0][:20]}...

**核心问题**：
"""
        for q in target['key_questions']:
            md += f"- {q}\n"
        md += "\n"
    
    md += """## 配套材料
- [ ] 行业案例集
- [ ] 解决方案PPT
- [ ] POC方案模板
- [ ] 竞品对比表

## 注意事项
- 开场先建立信任，不要急于推销
- 多问开放式问题，让客户多说
- 记录关键数字和具体案例
- 结束时明确下一步

---
生成时间：""" + datetime.now().strftime('%Y-%m-%d %H:%M')
    
    return md

def main():
    parser = argparse.ArgumentParser(
        description='ICIS - 智能客户访谈系统',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  icis plan --company "XX公司" --industry appliances
  icis analyze --input interview.txt --output report.md
  icis script --type objection --context "已经有ERP了"
  icis case --industry appliances --pain "订单处理"
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # plan 命令
    plan_parser = subparsers.add_parser('plan', help='生成访谈计划')
    plan_parser.add_argument('--company', '-c', required=True, help='公司名称')
    plan_parser.add_argument('--industry', '-i', required=True, help='行业（appliances/electronics/machinery）')
    plan_parser.add_argument('--scale', '-s', help='公司规模（如：10亿/2000人）')
    plan_parser.add_argument('--output', '-o', help='输出目录')
    
    # analyze 命令
    analyze_parser = subparsers.add_parser('analyze', help='分析访谈记录')
    analyze_parser.add_argument('--input', '-i', required=True, help='访谈记录文件')
    analyze_parser.add_argument('--output', '-o', help='分析报告输出文件')
    
    # script 命令
    script_parser = subparsers.add_parser('script', help='查询销售话术')
    script_parser.add_argument('--type', '-t', required=True, choices=['opening', 'objection', 'closing'], help='话术类型')
    script_parser.add_argument('--context', '-c', help='具体场景（如：已经有ERP了）')
    
    # case 命令
    case_parser = subparsers.add_parser('case', help='查询成功案例')
    case_parser.add_argument('--industry', '-i', help='行业筛选')
    case_parser.add_argument('--pain', '-p', help='痛点筛选')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # 执行对应命令
    commands = {
        'plan': cmd_plan,
        'analyze': cmd_analyze,
        'script': cmd_script,
        'case': cmd_case,
    }
    
    commands[args.command](args)

if __name__ == '__main__':
    main()
