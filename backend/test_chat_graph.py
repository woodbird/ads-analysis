import logging
import sys
from app.graphs.chat_graph import process_chat

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # 测试消息
    test_message = "我想了解我的广告账户最近7天的表现如何？我使用的是腾讯广告平台。"
    
    # 处理消息
    logger.info(f"测试消息: {test_message}")
    response = process_chat(test_message)
    
    # 输出结果
    logger.info(f"AI回复: {response}")
