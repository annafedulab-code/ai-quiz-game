"""퀴즈 1문제를 표현하는 Quiz 클래스"""


class Quiz:
    """문제, 선택지 4개, 정답 번호(1~4)를 가진 퀴즈 1개"""

    def __init__(self, question, choices, answer):
        self.question = question  # 문제 (글자, str)
        self.choices = choices    # 선택지 4개 (목록, list)
        self.answer = answer      # 정답 번호 1~4 (숫자, int)

    def display(self, number):
        """문제 번호, 문제, 선택지를 화면에 보여 준다."""
        print("-" * 40)
        print(f"[문제 {number}]")
        print(self.question)
        print()
        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")
        print()

    def is_correct(self, user_answer):
        """사용자가 고른 번호가 정답이면 True, 아니면 False를 돌려준다."""
        return user_answer == self.answer
