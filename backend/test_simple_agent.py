import logging
import sys
import os
from dotenv import load_dotenv
from app.tools import get_account_list, get_access_token, get_daily_report
from app.models.chat_models import setup_llm
from app.core.prompts import SYSTEM_PROMPT
from langchain.schema import SystemMessage, HumanMessage, AIMessage
import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

def test_tools():
    """测试工具函数"""
    logger.info("测试工具函数")
    
    # 测试获取账户列表
    platform = "tencent"
    logger.info(f"获取账户列表，平台: {platform}")
    accounts = get_account_list.invoke(platform)
    logger.info(f"获取到 {len(accounts)} 个账户")
    
    if accounts:
        # 使用第一个账户进行后续测试
        account_id = accounts[0].get('accountId')
        logger.info(f"使用账户ID: {account_id}")
        
        # 测试获取访问令牌
        token = get_access_token.invoke(account_id)
        if token:
            logger.info(f"获取到访问令牌: {token[:5]}...")
            
            # 测试获取日报表
            end_date = datetime.datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d")
            
            logger.info(f"获取日报表，日期范围: {start_date} 至 {end_date}")
            
            # 创建参数字典
            params = {
                "access_token": token,
                "account_id": account_id,
                "start_date": start_date,
                "end_date": end_date
            }
            
            reports = get_daily_report.invoke(params)
            
            logger.info(f"获取到 {len(reports)} 条报表数据")
            return True
        else:
            logger.error("获取访问令牌失败")
            return False
    else:
        logger.error("获取账户列表失败")
        return False

def test_llm_with_tools():
    """测试LLM与工具的集成"""
    logger.info("测试LLM与工具的集成")
    
    # 初始化LLM
    llm = setup_llm()
    
    # 绑定工具
    tools = [get_account_list, get_access_token, get_daily_report]
    llm_with_tools = llm.bind_tools(tools)
    
    # 创建消息
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content="我想了解我的广告账户最近7天的表现如何？")
    ]
    
    # 调用LLM
    logger.info("调用LLM")
    try:
        response = llm_with_tools.invoke(messages)
        logger.info(f"LLM回复: {response.content}")
        return True
    except Exception as e:
        logger.error(f"调用LLM时出错: {str(e)}", exc_info=True)
        return False

if __name__ == "__main__":
    logger.info("开始测试后端功能")
    
    # 测试工具函数
    tools_ok = test_tools()
    logger.info(f"工具函数测试结果: {'成功' if tools_ok else '失败'}")
    
    # 测试LLM与工具的集成
    llm_ok = test_llm_with_tools()
    logger.info(f"LLM与工具集成测试结果: {'成功' if llm_ok else '失败'}")
    
    # 总结测试结果
    if tools_ok and llm_ok:
        logger.info("后端功能测试全部通过")
    else:
        logger.error("后端功能测试存在失败项")
