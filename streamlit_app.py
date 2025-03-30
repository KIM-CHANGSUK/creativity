import random
import time
from typing import Dict, List

class CreativeWritingAssessment:
    def __init__(self):
        self.questions = [
            {
                "question": "의자가 꼭 앉는 용도로만 사용되어야 할까요? 의자를 전혀 다른 용도로 사용할 수 있는 방법을 최대한 많이 적어보세요.",
                "max_points": 10
            },
            {
                "question": "달걀, 구름, 시계 이 세 단어를 모두 포함한 짧은 이야기를 만들어 보세요.",
                "max_points": 10
            },
            {
                "question": "시간이 거꾸로 흐른다면 우리 생활은 어떻게 달라질까요? 가정에 기반한 아이디어를 자유롭게 제시해보세요.",
                "max_points": 10
            },
            {
                "question": "하루 동안 모든 전자기기가 사라진다면, 당신은 어떤 방법으로 하루를 보낼 건가요?",
                "max_points": 10
            },
            {
                "question": "환경 문제(예: 플라스틱 쓰레기)를 해결할 수 있는 기발한 방법을 생각해보세요. 현실적 적용이 가능할수록 좋아요.",
                "max_points": 10
            },
            {
                "question": "당신이 새로운 나라를 만든다면, 어떤 규칙 3가지를 만들고 왜 그렇게 정했는지 설명해보세요.",
                "max_points": 10
            },
            {
                "question": "자주 사용하는 물건 하나(예: 칫솔, 이어폰 등)의 디자인을 새롭게 바꾼다면 어떻게 바꾸고 싶은가요?",
                "max_points": 10
            },
            {
                "question": "친구와 크게 다퉜을 때, 기존과 다른 방식으로 화해할 수 있는 창의적인 방법을 제시해보세요.",
                "max_points": 10
            },
            {
                "question": "하늘을 나는 가방이 현실에 존재한다면, 어디에 사용하면 좋을까요? 3가지 이상 활용처를 제안해보세요.",
                "max_points": 10
            },
            {
                "question": "자신이 살아온 이야기를 '식물'에 비유해 보세요. 어떤 식물에 가장 비슷하다고 생각하나요? 이유는?",
                "max_points": 10
            }
        ]
        self.answers = []
        self.scores = []

    def start_assessment(self):
        print("\n=== 창의적 글쓰기 평가 시스템 ===\n")
        print("각 질문에 대해 충분히 생각하고 답변해주세요.")
        print("답변을 입력한 후 Enter를 두 번 눌러주세요.\n")
        
        for i, q in enumerate(self.questions, 1):
            print(f"\n[문제 {i}/10]")
            print(q["question"])
            print("\n답변을 입력하세요:")
            
            answer_lines = []
            while True:
                line = input()
                if line == "":
                    break
                answer_lines.append(line)
            
            answer = "\n".join(answer_lines)
            self.answers.append(answer)
            print("\n" + "="*50 + "\n")

    def evaluate_answers(self):
        print("\n=== AI 평가 결과 ===\n")
        total_score = 0
        
        for i, (q, a) in enumerate(zip(self.questions, self.answers), 1):
            # AI 평가 로직 (실제로는 더 복잡한 평가 시스템이 필요)
            score = random.randint(5, q["max_points"])
            self.scores.append(score)
            total_score += score
            
            print(f"[문제 {i}] 점수: {score}/{q['max_points']}")
            print(f"AI 피드백: {self._generate_feedback(score)}")
            print("-" * 50)
        
        print(f"\n총점: {total_score}/100")
        print(f"평균 점수: {total_score/10:.1f}/10")

    def _generate_feedback(self, score: int) -> str:
        if score >= 9:
            return "매우 창의적이고 상세한 답변입니다. 독창적인 아이디어가 잘 표현되었습니다."
        elif score >= 7:
            return "좋은 답변입니다. 몇 가지 더 구체적인 예시를 추가하면 더 좋을 것 같습니다."
        elif score >= 5:
            return "기본적인 답변은 잘 작성되었습니다. 더 창의적인 아이디어를 추가해보세요."
        else:
            return "답변을 더 구체적이고 창의적으로 발전시켜보세요."

def main():
    assessment = CreativeWritingAssessment()
    assessment.start_assessment()
    
    print("\n모든 문제가 완료되었습니다. AI 평가를 시작하시겠습니까? (y/n)")
    if input().lower() == 'y':
        assessment.evaluate_answers()
    else:
        print("평가가 취소되었습니다.")

if __name__ == "__main__":
    main()
