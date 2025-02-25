import logging
from typing import Dict, Any, List, Annotated, TypedDict, Sequence, Union, Tuple
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain_core.messages import ToolMessage
import json
import datetime
import uuid

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain.schema.runnable import RunnableConfig

from app.models.chat_models import setup_llm
from app.core.prompts import SYSTEM_PROMPT
from app.tools import get_account_list, get_access_token, get_daily_report

logger = logging.getLogger(__name__)

# 定义状态类型
class AgentState(TypedDict):
    messages: List[Union[SystemMessage, HumanMessage, AIMessage, ToolMessage]]

# 初始化LLM
llm = setup_llm()

# 工具列表
available_tools = [get_account_list, get_access_token, get_daily_report]

def agent_node(state: AgentState) -> AgentState:
    """LLM代理节点"""
    messages = state["messages"]
    logger.info(f"代理节点接收到消息: {messages[-1].content if messages else 'None'}")
    
    # 绑定工具
    llm_with_tools = llm.bind_tools(available_tools)
    
    # 调用LLM
    response = llm_with_tools.invoke(messages)
    logger.info(f"LLM回复: {response.content}")
    
    # 更新消息
    messages.append(response)
    return {"messages": messages}

def tool_node(state: AgentState) -> AgentState:
    """工具执行节点"""
    messages = state["messages"]
    last_message = messages[-1]
    
    # 检查是否有工具调用
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        logger.info(f"检测到工具调用: {last_message.tool_calls}")
        
        # 执行工具调用
        for tool_call in last_message.tool_calls:
            # 使用字典访问方式
            tool_name = tool_call['name']
            tool_args = tool_call['args']  # 已经是字典，不需要json.loads
            tool_id = tool_call['id']
            
            logger.info(f"执行工具: {tool_name}，参数: {tool_args}")
            
            # 根据工具名称选择工具
            if tool_name == "get_account_list":
                tool = get_account_list
                result = tool.invoke(tool_args.get("platform", "tencent"))
            elif tool_name == "get_access_token":
                tool = get_access_token
                # 修正参数名称
                account_id = tool_args.get("account_id", "")
                if not account_id:
                    account_id = tool_args.get("accountId", "")
                result = tool.invoke(account_id)
            elif tool_name == "get_daily_report":
                tool = get_daily_report
                # 确保所有必要参数都存在
                params = {
                    "access_token": tool_args.get("access_token", ""),
                    "account_id": tool_args.get("account_id", ""),
                    "start_date": tool_args.get("start_date", ""),
                    "end_date": tool_args.get("end_date", "")
                }
                result = tool.invoke(params)
            else:
                result = f"未知工具: {tool_name}"
                
            logger.info(f"工具执行结果: {result}")
            
            # 添加工具执行结果 - 使用ToolMessage而不是AIMessage
            messages.append(
                ToolMessage(
                    content=json.dumps(result, ensure_ascii=False),
                    tool_call_id=tool_id
                )
            )
    
    return {"messages": messages}

def should_continue(state: AgentState) -> str:
    """决定是否继续执行工具或结束"""
    messages = state["messages"]
    last_message = messages[-1]
    
    # 如果最后一条消息是AI消息，则检查是否有工具调用
    if isinstance(last_message, AIMessage):
        logger.info(f"AI消息: {last_message.content}")
        
        # 检查是否有工具调用
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            logger.info(f"检测到工具调用: {last_message.tool_calls}")
            return "continue"
        
        # 如果没有工具调用，则结束
        logger.info("AI没有请求工具调用，结束对话")
        return "end"
    
    # 默认结束
    return "end"

def process_chat(user_message: str) -> str:
    """
    处理用户聊天消息
    
    Args:
        user_message: 用户输入的消息
        
    Returns:
        AI助手的回复
    """
    try:
        # 创建工作流图
        workflow = StateGraph(AgentState)
        
        # 添加节点
        workflow.add_node("agent", agent_node)
        workflow.add_node("tool_executor", tool_node)
        
        # 添加边
        workflow.add_conditional_edges(
            "agent",
            should_continue,
            {
                "continue": "tool_executor",
                "end": END
            }
        )
        workflow.add_edge("tool_executor", "agent")
        
        # 设置入口节点
        workflow.set_entry_point("agent")
        
        # 编译工作流
        graph = workflow.compile()
        
        # 创建初始状态
        initial_state = {
            "messages": [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=user_message)
            ]
        }
        
        # 执行工作流
        logger.info(f"开始处理用户消息: {user_message}")
        
        # 配置运行时
        config = RunnableConfig(
            configurable={"thread_id": str(uuid.uuid4())},
        )
        
        # 获取最终状态
        final_state = graph.invoke(initial_state, config)
        
        # 提取AI回复
        messages = final_state["messages"]
        ai_messages = [m for m in messages if isinstance(m, AIMessage)]
        
        if ai_messages:
            # 获取最后一条非工具调用的AI消息
            for msg in reversed(ai_messages):
                if not (hasattr(msg, "tool_calls") and msg.tool_calls):
                    return msg.content
            
            # 如果所有消息都是工具调用结果，则返回最后一条
            return ai_messages[-1].content
        else:
            logger.error("未找到AI回复")
            return "抱歉，我无法处理您的请求。请稍后再试。"
    
    except Exception as e:
        logger.error(f"处理聊天时出错: {str(e)}", exc_info=True)
        return f"处理请求时出错: {str(e)}"
