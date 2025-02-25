import logging
import sys
import os
from dotenv import load_dotenv
from app.tools import get_account_list, get_access_token, get_daily_report
from app.graphs.chat_graph import process_chat
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

def test_get_account_list():
    """测试获取账户列表功能"""
    logger.info("测试获取账户列表功能")
    platform = "tencent"  # 广点通平台
    accounts = get_account_list.invoke(platform)
    logger.info(f"获取到 {len(accounts)} 个账户")
    for account in accounts[:5]:  # 只显示前5个账户
        logger.info(f"账户ID: {account.get('accountId')}, 名称: {account.get('accountName')}")
    return accounts

def test_get_access_token(account_id):
    """测试获取访问令牌功能"""
    logger.info(f"测试获取访问令牌功能，账户ID: {account_id}")
    token = get_access_token.invoke(account_id)
    if token:
        logger.info(f"获取到访问令牌: {token[:5]}...")  # 只显示令牌的前5个字符
    else:
        logger.error("未能获取访问令牌")
    return token

def test_get_daily_report(access_token, account_id):
    """测试获取日报表功能"""
    logger.info(f"测试获取日报表功能，账户ID: {account_id}")
    
    # 获取最近7天的数据
    end_date = datetime.datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d")
    
    logger.info(f"查询日期范围: {start_date} 至 {end_date}")
    
    # 将参数打包成字典
    params = {
        "access_token": access_token,
        "account_id": account_id,
        "start_date": start_date,
        "end_date": end_date
    }
    
    reports = get_daily_report.invoke(params)
    
    logger.info(f"获取到 {len(reports)} 条报表数据")
    for report in reports:
        logger.info(f"日期: {report.get('date')}, 花费: {report.get('cost', 0)/100}元, 点击次数: {report.get('valid_click_count', 0)}")
    
    return reports

def test_chat_process():
    """测试聊天处理功能"""
    logger.info("测试聊天处理功能")
    
    # 测试简单问题
    test_message = "我想了解我的广告账户最近7天的表现如何？"
    logger.info(f"测试消息: {test_message}")
    
    response = process_chat(test_message)
    logger.info(f"AI回复: {response}")
    
    return response

if __name__ == "__main__":
    try:
        # 测试获取账户列表
        accounts = test_get_account_list()
        
        if accounts:
            # 使用第一个账户进行后续测试
            account_id = accounts[0].get('accountId')
            
            # 测试获取访问令牌
            token = test_get_access_token(account_id)
            
            if token:
                # 测试获取日报表
                reports = test_get_daily_report(token, account_id)
            else:
                logger.error("无法获取访问令牌，跳过日报表测试")
        else:
            logger.error("无法获取账户列表，跳过后续测试")
        
        # 测试聊天处理
        test_chat_process()
        
    except Exception as e:
        logger.error(f"测试过程中出错: {str(e)}", exc_info=True)
