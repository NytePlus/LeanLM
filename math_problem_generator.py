class MathProblemGenerator:
    @staticmethod
    def get_sample_problems():
        """返回一些测试用的数学问题"""
        return [
            "证明：对于任意自然数n，2n是偶数",
            "证明：两个偶数的和是偶数", 
            "证明：如果a和b是整数，那么a² - b² = (a-b)(a+b)",
            "证明：1 + 1 = 2",
            "证明：任意质数大于1",
            "证明：两个奇数的和是偶数",
            "证明：对于所有自然数n，n(n+1)是偶数"
        ]
    
    @staticmethod
    def generate_problem_by_difficulty(difficulty="easy"):
        """根据难度生成问题"""
        problems = {
            "easy": [
                "证明：3是质数",
                "证明：4是偶数",
                "证明：1 + 2 = 3"
            ],
            "medium": [
                "证明：两个有理数的和是有理数",
                "证明：如果x是偶数，那么x²也是偶数",
                "证明：不存在最大的质数"
            ],
            "hard": [
                "证明：√2是无理数",
                "证明：有无限多个质数",
                "证明：费马小定理"
            ]
        }
        
        import random
        return random.choice(problems.get(difficulty, problems["easy"]))