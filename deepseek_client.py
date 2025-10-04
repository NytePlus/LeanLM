import requests
import json
import time

class SJTUDeepSeekClient:
    def __init__(self, api_key, base_url="https://chat.sjtu.edu.cn/api"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
    
    def generate_math_solution(self, problem):
        """调用DeepSeek API生成数学解答和Lean证明"""
        
        prompt = f"""
请解决以下数学问题，并提供两种形式的解答：

数学问题：{problem}

要求：
1. 使用Lean 4标准库，不要使用Mathlib
2. 只使用基础的定理和定义
3. 证明应该简单直接
4. 在Lean代码前加上标记：```lean
5. 在Lean代码后加上标记：```

请确保Lean证明是正确的且能够通过Lean 4编译器验证。
"""
        
        payload = {
            "model": "deepseek-v3",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.3,
            "max_tokens": 4000
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            
            result = response.json()
            return result['choices'][0]['message']['content']
            
        except Exception as e:
            return f"API调用错误: {str(e)}"
    
    def extract_lean_code(self, response_text):
        """从响应中提取Lean代码"""
        if '```lean' in response_text and '```' in response_text:
            start = response_text.find('```lean') + 7
            end = response_text.find('```', start)
            return response_text[start:end].strip()
        return None