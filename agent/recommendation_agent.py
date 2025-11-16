# recommendation_agent.py
from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage
from tools import predict_fuel_tool
from prompts import SYSTEM_PROMPT
import json
import re

# AGENT CREATION WITH MEMORY
def create_recommendation_agent():
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.1,
        max_tokens=2000,
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ])

    chain = prompt | llm | StrOutputParser()
    
    return chain

# PARSE PREDICTION REQUEST
def parse_prediction_request(text: str) -> Dict[str, float] | None:
    """Extract prediction parameters from LLM response."""
    if "PREDICT:" not in text:
        return None
    
    try:
        # Extract the PREDICT line
        predict_line = [line for line in text.split('\n') if 'PREDICT:' in line][0]
        
        # Extract parameters using regex
        params = {}
        params['speed'] = float(re.search(r'speed=([\d.]+)', predict_line).group(1))
        params['acceleration'] = float(re.search(r'acceleration=([\d.]+)', predict_line).group(1))
        params['engine_rpm'] = float(re.search(r'engine_rpm=([\d.]+)', predict_line).group(1))
        params['vehicle_weight'] = float(re.search(r'vehicle_weight=([\d.]+)', predict_line).group(1))
        params['temp'] = float(re.search(r'temp=([\d.]+)', predict_line).group(1))
        
        return params
    except Exception as e:
        print(f"[DEBUG] Failed to parse prediction request: {e}")
        return None

# RUN AGENT WITH CONVERSATION MEMORY
def run_agent(user_message: str):
    agent = create_recommendation_agent()
    chat_history = []
    
    # First interaction - ask LLM to process input
    print("\n[Agent] Processing your request...")
    response = agent.invoke({
        "input": user_message,
        "chat_history": chat_history
    })
    print(f"\n[Agent Response]\n{response}")
    
    # Add to chat history
    chat_history.append(HumanMessage(content=user_message))
    chat_history.append(AIMessage(content=response))
    
    # Check if LLM is ready to make a prediction
    params = parse_prediction_request(response)
    
    if params:
        print(f"\n[Agent] Calling fuel prediction tool with: {params}")
        prediction_result = predict_fuel_tool(**params)
        
        if prediction_result.get('fuel_consumption') is None:
            error_msg = prediction_result.get('error', 'Unknown error')
            print(f"[ERROR] Prediction failed: {error_msg}")
            return f"Sorry, I couldn't make a prediction due to an error: {error_msg}"
        
        fuel_consumption = prediction_result['fuel_consumption']
        print(f"[Agent] Predicted fuel consumption: {fuel_consumption:.2f} L/100km")
        
        # Second interaction - give LLM the prediction result WITH CONTEXT
        followup_message = f"""
        The fuel prediction model returned: {fuel_consumption:.2f} L/100km

        Based on the driving conditions you provided:
        - Speed: {params['speed']} km/h
        - Acceleration: {params['acceleration']} m/s²
        - Engine RPM: {params['engine_rpm']}
        - Vehicle Weight: {params['vehicle_weight']} kg
        - Temperature: {params['temp']}°C

        Please provide:
        1. Analysis: Is {fuel_consumption:.2f} L/100km efficient, moderate, or high for these conditions?
        2. Top 3 specific recommendations to improve fuel efficiency
        3. Estimated savings if recommendations are followed
        """
        print("\n[Agent] Analyzing prediction results...")
        final_response = agent.invoke({
            "input": followup_message,
            "chat_history": chat_history
        })
        
        return final_response
    else:
        # LLM needs more information or answered a general question
        return response
