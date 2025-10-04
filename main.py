import os
from deepseek_client import SJTUDeepSeekClient
from lean_manager import LeanManager
from math_problem_generator import MathProblemGenerator

def main():
    # 配置 - 请替换为您的DeepSeek API密钥
    DEEPSEEK_API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjJkNjUxODc2LTI5YWEtNGQ2Ni04N2ZkLWEzODdmOWYzMGM3YiIsImV4cCI6MTc1OTYxMDE5MH0.WUM5GPYaFAPWqOsfgVW89i4qlhT9sRUwRe5KG9NQflw'

    if DEEPSEEK_API_KEY == "your_deepseek_api_key_here":
        print("请先在代码中设置您的DeepSeek API密钥")
        return
    
    # 初始化客户端
    deepseek = SJTUDeepSeekClient(DEEPSEEK_API_KEY)
    lean_manager = LeanManager()
    
    try:
        # 获取数学问题
        problem_generator = MathProblemGenerator()
        problems = problem_generator.get_sample_problems()
        
        print("=== 数学定理自动证明系统 ===\n")
        
        for i, problem in enumerate(problems[:3], 1):  # 测试前3个问题
            print(f"\n{'='*50}")
            print(f"问题 {i}: {problem}")
            print(f"{'='*50}")
            
            # 步骤1: 调用DeepSeek生成解答
            print("\n1. 正在调用DeepSeek API生成证明...")
            response = deepseek.generate_math_solution(problem)
            print("生成完成！")
            
            # 显示生成的解答
            print("\n2. DeepSeek生成的解答：")
            print(response)
            
            # 步骤2: 提取Lean代码
            print("\n3. 提取Lean证明代码...")
            lean_code = deepseek.extract_lean_code(response)
            
            if lean_code:
                print("Lean代码提取成功！")
                print(f"\n提取的Lean代码：\n{lean_code}")
                
                # 步骤3: 验证Lean证明
                print("\n4. 正在使用Lean验证证明...")
                verification_result = lean_manager.verify_proof(lean_code)
                
                if verification_result["success"]:
                    print("✅ 证明验证成功！")
                    print(f"输出: {verification_result['message']}")
                else:
                    print("❌ 证明验证失败")
                    print(f"错误: {verification_result.get('error', '未知错误')}")
                    print(f"详细信息: {verification_result.get('message', '')}")
            else:
                print("❌ 未能从响应中提取Lean代码")
            
            print(f"\n{'='*50}")
            input("按Enter继续下一个问题...")
    
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"程序运行出错: {e}")
    finally:
        # 清理资源
        lean_manager.cleanup()

if __name__ == "__main__":
    main()