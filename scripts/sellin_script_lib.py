"""
Sell-in 话术库
"""

SCRIPT_LIBRARY = {
    "opening": {
        "it_director": "{name}，感谢您的时间。飞书在帮制造业客户做AI落地，3个月帮XX企业把订单处理时间从2天降到2小时。今天想了解您的系统现状，看有没有类似机会。",
        "sales_director": "{name}，飞书现在不只是办公工具，我们在帮客户做业务数字化。今天想听听您的业务痛点，看看飞书能不能帮到您。",
        "supply_director": "{name}，我们在帮制造业客户优化供应链效率，有客户用飞书+AI把交付准时率从70%提升到95%。今天想请教您的经验。"
    },
    
    "hooks": {
        "智能订单处理": {
            "it_director": "您刚才提到{context}，我们帮XX客户用飞书+AI自动识别订单，{value}。IT部门还成了业务创新的推动者。",
            "sales_director": "如果订单处理快2倍，客户响应及时，对您的客户满意度和复购率会有多大提升？"
        },
        "视觉质检": {
            "it_director": "质检AI可以24小时不停，准确率比人眼还高。数据还能自动沉淀，以后追溯问题秒级定位。",
            "supply_director": "零缺陷出厂，客户投诉下降80%。您的质量成本能省多少？"
        },
        "智能客服": {
            "sales_director": "AI客服7x24小时在线，响应秒级。客户满意度从80%到95%，转化率能提升多少？",
            "it_director": "知识库自动学习，新人培训周期从1个月缩短到1周。"
        }
    },
    
    "objection_handling": {
        "已经有ERP了": "ERP解决的是流程问题，飞书+AI解决的是效率问题。比如订单处理，ERP需要人工录入，飞书AI可以自动识别录入。不是替换，是增强。",
        "数据安全问题": "支持私有化部署，数据不出厂。已通过等保三级，XX家制造业客户在用。",
        "效果不确定": "可以先选一个客户/一个产线试点，验证效果再推广。我们输出ROI测算，6个月回本。",
        "预算紧张": "SaaS模式按年付费，无需一次性大额投入。效果付费，看到效果再续费。",
        "实施复杂": "飞书专业交付团队，2周上线，不影响现有业务。操作简单，培训1小时上手。"
    },
    
    "closing": {
        "it_director": "我安排技术同事给您做个方案交流，看看具体怎么落地。您看这周还是下周方便？",
        "sales_director": "我们输出一个ROI测算和试点方案，您看看效果预期。明天发给您？",
        "supply_director": "安排您参观一个同行标杆客户，看看实际效果。下周二或周四？"
    }
}

def get_script(script_type, role, context=None):
    """获取话术"""
    if script_type == "opening":
        return SCRIPT_LIBRARY["opening"].get(role, SCRIPT_LIBRARY["opening"]["sales_director"])
    elif script_type == "closing":
        return SCRIPT_LIBRARY["closing"].get(role, SCRIPT_LIBRARY["closing"]["sales_director"])
    elif script_type == "objection":
        return SCRIPT_LIBRARY["objection_handling"].get(context, "这个问题我们有很多成功案例，我发资料给您参考。")
    return ""
