import os
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import logging
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

logger = logging.getLogger(__name__)

def setup_llm():
    """
    设置并返回LLM模型
    
    Returns:
        配置好的ChatOpenAI模型实例
    """
    api_key = os.getenv("OPENAI_API_KEY")
    api_base = os.getenv("OPENAI_API_BASE")
    model_name = os.getenv("OPENAI_MODEL_NAME")
    
    if not api_key or not api_base or not model_name:
        logger.error("缺少OpenAI配置环境变量")
        raise ValueError("缺少OpenAI配置环境变量")
    
    logger.info(f"正在初始化LLM模型: {model_name}")
    logger.info(f"API Base: {api_base}")
    
    llm = ChatOpenAI(
        model=model_name,
        api_key=api_key,
        base_url=api_base,
        temperature=0.1,
        streaming=False
    )
    
    return llm
