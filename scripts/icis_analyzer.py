#!/usr/bin/env python3
"""
AI Sell-in 分析工具
将访谈录音转化为可执行的销售策略
"""

import os
import sys
import json
import re
from datetime import datetime
from pathlib import Path

class AISellInAnalyzer:
    def __init__(self):
        self.workspace = os.path.expanduser("~/.openclaw/workspace")
        self.output_dir = f"{self.workspace}/10-Work/90-Outputs/ai-sellin-reports"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 制造业AI场景库
        self.ai_scenarios = {
            "订单处理": {
                "pain": "手工录入订单，处理时间长，容易出错",
                "solution": "AI智能识别订单+自动录入",
                "feishu_product": "飞书多维表格+AI插件",
                "value": "处理时间从2天降到2小时，准确率99%+",
                "hook": "让IT部门从支持角色变成业务创新推动者"
            },
            "质量管理": {
                "pain": "质检依赖人工，追溯困难，不良品流出",
                "solution": "视觉AI质检+全流程数据溯源",
                "feishu_product": "飞书+第三方AI质检系统集成",
                "value": "质检效率提升5倍，追溯时间从小时到秒",
                "hook": "零缺陷出厂，客户投诉下降80%"
            },
            "客户响应": {
                "pain": "客户咨询响应慢，信息查询困难",
                "solution": "AI智能客服+知识库自动问答",
                "feishu_product": "飞书智能客服+知识库",
                "value": "响应时间从小时到秒，7x24小时服务",
                "hook": "客户满意度从80%提升到95%"
            },
            "需求预测": {
                "pain": "库存积压或缺货，预测不准确",
                "solution": "AI需求预测+智能补货",
                "feishu_product": "飞书多维表格+AI预测模型",
                "value": "库存周转提升30%，缺货率下降50%",
                "hook": "释放现金流，减少资金占用"
            },
            "设备维护": {
                "pain": "设备突发故障，停机损失大",
                "solution": "设备预测性维护+故障预警",
                "feishu_product": "飞书+IoT+AI预测",
                "value": "非计划停机减少70%，维护成本降低40%",
                "hook": "从救火变成预防，设备OEE提升"
            }
        }
        
        # 决策角色策略库
        self.role_strategies = {
            "IT总监": {
                "type": "技术把关者",
                "concerns": ["系统稳定", "数据安全", "技术可控", "供应商实力"],
                "hooks": ["技术领先性", "架构先进性", "安全合规", "可扩展性"],
                "objections": {
                    "数据安全": "支持私有化部署，已通过等保三级，数据不出厂",
                    "系统稳定": "SLA 99.9%，7x24小时运维支持，故障分钟级响应",
                    "技术可控": "开放API，支持二次开发，技术文档完整",
                    "供应商实力": "字节跳动旗下，服务10万+企业，制造业标杆客户XX家"
                },
                "next_step": "技术方案交流+POC环境搭建"
            },
            "销售/市场总监": {
                "type": "业务决策者",
                "concerns": ["业绩增长", "客户满意", "市场份额", "竞争压力"],
                "hooks": ["客户满意度提升", "响应速度", "转化率增长", "同行成功案例"],
                "objections": {
                    "效果不确定": "可以先选一个客户/一个产品线试点，验证效果再推广",
                    "投入产出比": "我们输出ROI测算，6个月回本，年化收益XX%",
                    "实施复杂": "飞书专业交付团队，2周上线，不影响现有业务"
                },
                "next_step": "POC试点+ROI测算"
            },
            "供应链/制造总监": {
                "type": "运营效率决策者",
                "concerns": ["生产效率", "质量控制", "成本控制", "交付准时"],
                "hooks": ["效率提升", "质量零缺陷", "成本降低", "交付准时率"],
                "objections": {
                    "影响生产": "可以先在非关键产线试点，验证稳定后再推广",
                    "员工抵触": "操作简单，培训1小时上手，减轻员工重复劳动",
                    "投资回报": "单产线3个月回本，全厂年化节省XX万"
                },
                "next_step": "产线试点+效果对比"
            },
            "财务总监": {
                "type": "成本把关者",
                "concerns": ["成本控制", "投资回报", "预算合规", "风险管控"],
                "hooks": ["成本降低", "效率提升", "现金流优化", "合规透明"],
                "objections": {
                    "预算紧张": "SaaS模式按年付费，无需一次性大额投入",
                    "效果难量化": "提供详细ROI测算，关键指标可量化追踪",
                    "隐性成本": "全包价格，无隐藏费用，免费升级"
                },
                "next_step": "ROI测算+预算方案"
            }
        }

    def analyze_transcript(self, transcript_text, interviewee_info):
        """
        分析访谈文本，输出Sell-in策略
        """
        # 1. 提取痛点
        pains = self._extract_pains(transcript_text)
        
        # 2. 匹配AI机会点
        opportunities = self._match_opportunities(pains)
        
        # 3. 生成角色策略
        role = interviewee_info.get("role", "")
        role_strategy = self._generate_role_strategy(role, opportunities)
        
        # 4. 生成话术
        scripts = self._generate_scripts(role, opportunities, role_strategy)
        
        # 5. 生成行动计划
        action_plan = self._generate_action_plan(interviewee_info)
        
        # 6. 组装报告
        report = self._assemble_report(
            interviewee_info,
            pains,
            opportunities,
            role_strategy,
            scripts,
            action_plan
        )
        
        return report

    def _extract_pains(self, text):
        """提取痛点关键词"""
        pain_keywords = {
            "效率": ["慢", "耗时", "手工", "重复", "加班", "来不及"],
            "质量": ["错误", "不良", "返工", "投诉", "退货", "索赔"],
            "成本": ["贵", "浪费", "高", "亏损", "预算", "省钱"],
            "协同": ["沟通", "协调", "信息", "断层", "孤岛", "不同步"],
            "数据": ["统计", "报表", "分析", "看不到", "不清楚", "滞后"]
        }
        
        pains = []
        for category, keywords in pain_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    # 提取上下文
                    pattern = f".{keyword}."
                    matches = re.findall(pattern, text)
                    if matches:
                        pains.append({
                            "category": category,
                            "keyword": keyword,
                            "context": matches[0] if matches else "",
                            "severity": self._assess_severity(text, keyword)
                        })
        
        return pains

    def _assess_severity(self, text, keyword):
        """评估痛点严重程度"""
        severe_indicators = ["最头疼", "最大问题", "严重影响", "每天", "总是", "经常"]
        urgent_indicators = ["急需", "马上", "立刻", "不能再等", "必须解决"]
        
        severity = "中"
        for indicator in severe_indicators:
            if indicator in text and keyword in text[max(0, text.find(indicator)-50):text.find(indicator)+50]:
                severity = "高"
                break
        
        return severity

    def _match_opportunities(self, pains):
        """匹配AI机会点"""
        opportunities = []
        
        # 如果没有提取到痛点，返回默认机会点
        if not pains:
            return [{
                "pain": {"context": "业务流程效率待提升", "category": "效率", "severity": "中"},
                "scenario": "订单处理",
                "details": self.ai_scenarios["订单处理"]
            }]
        
        for pain in pains:
            matched = False
            for scenario_name, scenario in self.ai_scenarios.items():
                # 更宽松的匹配逻辑
                pain_text = pain.get("context", "").lower()
                scenario_pain = scenario["pain"].lower()
                
                # 检查关键词匹配
                keywords = ["订单", "录入", "手工", "客户", "响应", "质量", "质检", "库存", "设备", "维护"]
                for keyword in keywords:
                    if keyword in pain_text and keyword in scenario_pain:
                        opportunities.append({
                            "pain": pain,
                            "scenario": scenario_name,
                            "details": scenario
                        })
                        matched = True
                        break
                
                if matched:
                    break
            
            # 如果没有匹配到，默认给订单处理
            if not matched and pain.get("category") == "效率":
                opportunities.append({
                    "pain": pain,
                    "scenario": "订单处理",
                    "details": self.ai_scenarios["订单处理"]
                })
        
        # 去重并排序
        seen = set()
        unique_opps = []
        for opp in opportunities:
            if opp["scenario"] not in seen:
                seen.add(opp["scenario"])
                unique_opps.append(opp)
        
        return unique_opps[:3]  # 返回Top 3

    def _generate_role_strategy(self, role, opportunities):
        """生成角色策略"""
        # 匹配角色
        matched_role = None
        for role_key in self.role_strategies.keys():
            if role_key in role:
                matched_role = role_key
                break
        
        if not matched_role:
            matched_role = "销售/市场总监"  # 默认
        
        strategy = self.role_strategies[matched_role].copy()
        strategy["matched_role"] = matched_role
        strategy["top_opportunities"] = [opp["scenario"] for opp in opportunities]
        
        return strategy

    def _generate_scripts(self, role, opportunities, role_strategy):
        """生成销售话术"""
        scripts = {
            "opening": [],
            "hook": [],
            "objection_handling": {},
            "closing": []
        }
        
        # 开场话术
        scripts["opening"].append(f"【开场】{role}，感谢您的时间。今天聊下来，我觉得您在{opportunities[0]['scenario'] if opportunities else '业务效率'}方面，飞书可能有帮到您的地方。")
        
        # 钩子话术
        for opp in opportunities[:2]:
            scripts["hook"].append(f"【钩子-{opp['scenario']}】您刚才提到{opp['pain']['context']}，我们帮XX客户用{opp['details']['feishu_product']}，{opp['details']['value']}。{opp['details']['hook']}")
        
        # 抗拒处理
        for concern, response in role_strategy.get("objections", {}).items():
            scripts["objection_handling"][concern] = response
        
        # 收尾话术
        scripts["closing"].append(f"【下一步】{role_strategy['next_step']}，您看这周方便吗？")
        
        return scripts

    def _generate_action_plan(self, interviewee_info):
        """生成行动计划"""
        return {
            "immediate": {
                "time": "24小时内",
                "actions": [
                    "发送《AI Sell-in分析报告》",
                    "整理相关案例资料",
                    "准备POC方案框架"
                ],
                "owner": "道哥"
            },
            "short_term": {
                "time": "1周内",
                "actions": [
                    "预约下次交流/POC启动",
                    "协调技术资源",
                    "准备演示环境"
                ],
                "owner": "道哥+解决方案"
            },
            "medium_term": {
                "time": "1个月内",
                "actions": [
                    "POC试点执行",
                    "效果数据收集",
                    "内部汇报材料"
                ],
                "owner": "客户成功+交付团队"
            }
        }

    def _assemble_report(self, interviewee_info, pains, opportunities, role_strategy, scripts, action_plan):
        """组装最终报告"""
        report = f"""
═══════════════════════════════════════════════════════════
【AI Sell-in 分析报告】
═══════════════════════════════════════════════════════════

【访谈信息】
客户：{interviewee_info.get('company', '待填写')}
访谈对象：{interviewee_info.get('name', '待填写')} ({interviewee_info.get('role', '待填写')})
访谈日期：{datetime.now().strftime('%Y-%m-%d')}
分析时间：{datetime.now().strftime('%H:%M')}

【核心痛点】（Top {len(pains)}）
"""
        
        for i, pain in enumerate(pains[:5], 1):
            report += f"{i}. 【{pain['category']}】{pain['context']} (严重度：{pain['severity']})\n"
        
        report += f"""
【AI机会点】（Top {len(opportunities)}）
"""
        
        for i, opp in enumerate(opportunities, 1):
            report += f"""
┌─────────────────────────────────────────────────────────┐
│ 机会点{i}：{opp['scenario']}                              │
├─────────────────────────────────────────────────────────┤
│ 痛点：{opp['pain']['context'][:40]}...                   │
│ 方案：{opp['details']['solution']}                       │
│ 产品：{opp['details']['feishu_product']}                 │
│ 价值：{opp['details']['value']}                          │
│ 钩子：{opp['details']['hook']}                           │
└─────────────────────────────────────────────────────────┘
"""
        
        report += f"""
【决策角色分析】
角色类型：{role_strategy['type']}
核心关切：{', '.join(role_strategy['concerns'])}
最佳钩子：{', '.join(role_strategy['hooks'])}
下一步：{role_strategy['next_step']}

【销售话术】
"""
        
        for script_type, script_list in scripts.items():
            if isinstance(script_list, list):
                for script in script_list:
                    report += f"{script}\n"
            elif isinstance(script_list, dict):
                for concern, response in script_list.items():
                    report += f"【抗拒处理-{concern}】{response}\n"
        
        report += f"""
【行动计划】
□ 即时行动（{action_plan['immediate']['time']}）
"""
        for action in action_plan['immediate']['actions']:
            report += f"  - {action}（{action_plan['immediate']['owner']}）\n"
        
        report += f"""
□ 短期行动（{action_plan['short_term']['time']}）
"""
        for action in action_plan['short_term']['actions']:
            report += f"  - {action}（{action_plan['short_term']['owner']}）\n"
        
        report += f"""
□ 中期行动（{action_plan['medium_term']['time']}）
"""
        for action in action_plan['medium_term']['actions']:
            report += f"  - {action}（{action_plan['medium_term']['owner']}）\n"
        
        report += """
═══════════════════════════════════════════════════════════
【使用建议】
1. 本报告基于访谈文本自动生成，关键信息请与录音核对
2. 话术请根据实际情况调整，避免生硬套用
3. 下一步动作请在24小时内启动，保持热度
═══════════════════════════════════════════════════════════
"""
        
        return report

    def save_report(self, report, company_name):
        """保存报告到文件"""
        filename = f"{self.output_dir}/{company_name}_{datetime.now().strftime('%Y%m%d_%H%M')}_sellin_report.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        return filename


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法: python ai_sellin_analyzer.py <访谈文本文件> [访谈对象信息JSON]")
        print("示例: python ai_sellin_analyzer.py interview.txt '{\"name\":\"张三\",\"role\":\"IT总监\",\"company\":\"XX公司\"}'")
        sys.exit(1)
    
    transcript_file = sys.argv[1]
    interviewee_info = {}
    
    if len(sys.argv) >= 3:
        try:
            interviewee_info = json.loads(sys.argv[2])
        except:
            print("警告：访谈对象信息JSON格式错误，使用默认值")
    
    # 读取访谈文本
    with open(transcript_file, 'r', encoding='utf-8') as f:
        transcript_text = f.read()
    
    # 分析
    analyzer = AISellInAnalyzer()
    report = analyzer.analyze_transcript(transcript_text, interviewee_info)
    
    # 保存
    company = interviewee_info.get('company', 'unknown')
    filename = analyzer.save_report(report, company)
    
    # 输出
    print(report)
    print(f"\n报告已保存至: {filename}")


if __name__ == "__main__":
    main()

# 新增：模板加载功能
def load_industry_template(industry):
    """加载行业模板"""
    import yaml
    template_path = f"{os.path.expanduser('~/.openclaw/workspace/icis-mvp/templates/manufacturing')}/{industry}.yaml"
    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    return None

def generate_interview_plan(company_info):
    """生成访谈计划"""
    industry = company_info.get('industry', 'appliances')
    template = load_industry_template(industry)
    
    if not template:
        return None
    
    plan = {
        "industry": template["industry"],
        "targets": template["interview_targets"],
        "total_duration": sum([t["duration"] for t in template["interview_targets"]]),
        "key_questions": {t["role"]: t["key_questions"] for t in template["interview_targets"]},
        "ai_opportunities": template["ai_opportunities"]
    }
    
    return plan
