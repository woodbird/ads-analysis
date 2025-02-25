import requests
import json
import logging
import time
import random
import string
from typing import Dict, Any, List, Optional
from langchain.tools import tool

logger = logging.getLogger(__name__)

def _log_api_call(func_name: str, request_data: Dict[str, Any], response_data: Dict[str, Any]):
    """记录API调用的请求和响应"""
    logger.info(f"API调用: {func_name}")
    logger.info(f"请求数据: {json.dumps(request_data, ensure_ascii=False)}")
    logger.info(f"响应数据: {json.dumps(response_data, ensure_ascii=False)}")

@tool
def get_account_list(platform: str) -> List[Dict[str, Any]]:
    """
    获取广告平台的账户列表
    
    Args:
        platform: 广告平台标识，tencent就是广点通，ocean就是巨量
        
    Returns:
        账户列表，包含账户ID、名称、状态和余额信息
    """
    url = "https://api.aileyun.net/ads/getAccountList"
    params = {"platform": platform}
    
    try:
        logger.info(f"调用获取账户列表API，参数: {params}")
        response = requests.get(url, params=params)
        response_data = response.json()
        
        _log_api_call("get_account_list", params, response_data)
        
        if response_data.get("code") == 0:
            return response_data.get("data", [])
        elif response_data.get("code") == 200:  # 根据测试结果，API返回code=200也是成功
            return response_data.get("data", [])
        else:
            error_msg = f"获取账户列表失败: {response_data.get('message', '未知错误')}"
            logger.error(error_msg)
            return []
    except Exception as e:
        logger.error(f"调用获取账户列表API时出错: {str(e)}", exc_info=True)
        return []

@tool
def get_access_token(account_id: str) -> str:
    """
    根据账户ID获取广告平台的AccessToken
    
    Args:
        account_id: 广告账户ID
        
    Returns:
        访问令牌字符串
    """
    url = "https://api.aileyun.net/ads/getTokenByAccountId"
    params = {"accountId": account_id}
    
    try:
        logger.info(f"调用获取访问令牌API，参数: {params}")
        response = requests.get(url, params=params)
        response_data = response.json()
        
        _log_api_call("get_access_token", params, response_data)
        
        if response_data.get("code") == 200:
            return response_data.get("data", {}).get("accessToken", "")
        else:
            error_msg = f"获取访问令牌失败: {response_data.get('message', '未知错误')}"
            logger.error(error_msg)
            return ""
    except Exception as e:
        logger.error(f"调用获取访问令牌API时出错: {str(e)}", exc_info=True)
        return ""

@tool
def get_daily_report(
    access_token: str,
    account_id: str,
    start_date: str,
    end_date: str,
    level: str = "REPORT_LEVEL_ADVERTISER",
    fields: Optional[List[str]] = None
) -> List[Dict[str, Any]]:
    """
    查询广告账户的日报表
    
    Args:
        access_token: 访问令牌
        account_id: 广告账户ID
        start_date: 开始日期，格式为YYYY-MM-DD
        end_date: 结束日期，格式为YYYY-MM-DD
        level: 报表维度，可选值为REPORT_LEVEL_ADVERTISER(账户)、REPORT_LEVEL_ADGROUP(广告组)、REPORT_LEVEL_DYNAMIC_CREATIVE(创意)
        fields: 需要返回的字段列表，默认为所有字段
        
    Returns:
        日报表数据列表
    """
    url = "https://api.e.qq.com/v3.0/daily_reports/get"
    
    if fields is None:
        fields = [
            "view_count", "view_user_count", "valid_click_count", 
            "click_user_count", "cpc", "ctr", "cost", 
            "thousand_display_price", "conversions_count", 
            "conversions_rate", "conversions_cost"
        ]
    
    # 生成随机nonce
    nonce = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
    
    # 当前时间戳
    timestamp = int(time.time())
    
    params = {
        "access_token": access_token,
        "timestamp": timestamp,
        "nonce": nonce,
        "account_id": account_id,
        "level": level,
        "date_range": json.dumps({
            "start_date": start_date,
            "end_date": end_date
        }),
        "group_by": json.dumps(["date"]),
        "fields": json.dumps(fields),
        "page": 1,
        "page_size": 100
    }
    
    try:
        # 隐藏敏感信息的日志
        log_params = params.copy()
        log_params["access_token"] = "***" # 隐藏敏感信息
        logger.info(f"调用获取日报表API，参数(脱敏): {log_params}")
        
        response = requests.get(url, params=params)
        response_data = response.json()
        
        # 记录API调用，但移除敏感信息
        _log_api_call("get_daily_report", log_params, response_data)
        
        if response_data.get("code") == 0:
            return response_data.get("data", {}).get("list", [])
        else:
            error_msg = f"获取日报表失败: {response_data.get('message', '未知错误')}"
            logger.error(error_msg)
            return []
    except Exception as e:
        logger.error(f"调用获取日报表API时出错: {str(e)}", exc_info=True)
        return []
