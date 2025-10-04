import subprocess
import tempfile
import os
from pathlib import Path

class LeanManager:
    def __init__(self, lean_path="lean"):
        self.lean_path = lean_path
        self.temp_dir = tempfile.mkdtemp()
    
    def create_lean_file(self, lean_code, filename="proof.lean"):
        """创建Lean证明文件"""
        filepath = Path(self.temp_dir) / filename
        
        # 使用Lean 4的基础库，避免Mathlib依赖
        full_code = lean_code
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(full_code)
        
        return filepath
    
    def verify_proof(self, lean_code):
        """验证Lean证明"""
        try:
            # 创建临时文件
            lean_file = self.create_lean_file(lean_code)
            
            # 运行Lean验证
            result = subprocess.run(
                [self.lean_path, str(lean_file)],
                capture_output=True,
                text=True,
                timeout=300
            )
            
            # 清理临时文件
            lean_file.unlink()
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "message": "证明验证成功！",
                    "output": result.stdout
                }
            else:
                return {
                    "success": False,
                    "message": "证明验证失败",
                    "error": result.stderr + '\n' + result.stdout,
                    "output": result.stdout
                }
                
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "message": "验证超时",
                "error": "Lean验证过程超过30秒"
            }
        except Exception as e:
            return {
                "success": False,
                "message": "验证过程出错",
                "error": str(e)
            }
    
    def cleanup(self):
        """清理临时目录"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)