"""게임 전체를 관리하는 QuizGame 클래스"""

import json  # [추가] JSON 파일 읽기/쓰기
from pathlib import Path  # [추가] 파일 경로 다루기

from default_quizzes import get_default_quizzes
from quiz import Quiz

# [추가] 데이터 파일 위치: 프로젝트 폴더(이 파일과 같은 폴더)의 state.json
STATE_FILE = Path(__file__).parent / "state.json"


class QuizGame:
    """퀴즈 목록과 최고 점수를 가지고, 메뉴·풀기·추가·목록·점수 기능을 담당한다."""

    MENU_COUNT = 5  # 메뉴 개수

    def __init__(self):
        self.quizzes = []        # 퀴즈 목록 (Quiz 객체들)
        self.best_score = None   # 최고 점수 (기록이 없으면 None)
        self.load_state()        # [추가] 시작할 때 파일에서 불러오기

    # ---------- 파일 저장/불러오기 ----------

    def load_state(self):
        """[추가] state.json에서 퀴즈와 최고 점수를 불러온다."""
        if not STATE_FILE.exists():
            print("📂 저장된 데이터가 없어 기본 퀴즈로 시작합니다.")
            self.quizzes = get_default_quizzes()
            self.best_score = None
            return

        try:
            with open(STATE_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
            quizzes = [Quiz.from_dict(item) for item in data["quizzes"]]
            best_score = data.get("best_score")
            if best_score is not None and not isinstance(best_score, int):
                raise ValueError("최고 점수 형식이 올바르지 않습니다.")
        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError):
            print("⚠️ 데이터 파일이 손상되어 기본 퀴즈 데이터로 복구합니다.")
            self.quizzes = get_default_quizzes()
            self.best_score = None
            self.save_state()
            return

        self.quizzes = quizzes
        self.best_score = best_score
        best_text = "기록 없음" if best_score is None else f"{best_score}점"
        print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(quizzes)}개, 최고점수 {best_text})")

    def save_state(self):
        """[추가] 퀴즈와 최고 점수를 state.json에 UTF-8로 저장한다."""
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
        }
        try:
            with open(STATE_FILE, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except OSError:
            print("⚠️ 데이터를 파일에 저장하지 못했습니다.")

    # ---------- 입력 처리 ----------

    def get_number(self, prompt, min_value, max_value):
        """숫자를 입력받아 min_value~max_value 범위의 정수를 돌려준다."""
        while True:
            text = input(prompt).strip()  # 앞뒤 공백 제거
            if text == "":
                print("⚠️ 입력이 비어 있습니다. 숫자를 입력하세요.")
                continue
            try:
                number = int(text)  # 글자를 숫자로 바꾸기
            except ValueError:
                print(f"⚠️ 잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
                continue
            if number < min_value or number > max_value:
                print(f"⚠️ 잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
                continue
            return number

    def get_text(self, prompt):
        """빈 칸이 아닌 글자를 입력받아 돌려준다."""
        while True:
            text = input(prompt).strip()
            if text == "":
                print("⚠️ 입력이 비어 있습니다. 내용을 입력하세요.")
                continue
            return text

    # ---------- 화면 ----------

    def show_menu(self):
        """메뉴 화면을 출력한다."""
        print()
        print("=" * 40)
        print("      🎯 AI 활용 상식 퀴즈 게임 🎯")
        print("=" * 40)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("=" * 40)

    # ---------- 게임 기능 ----------

    def play_quiz(self):
        """퀴즈를 차례로 출제하고, 끝나면 최고 점수와 비교한다."""
        if not self.quizzes:
            print("📭 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return

        print(f"\n📝 퀴즈를 시작합니다! (총 {len(self.quizzes)}문제)")
        correct = 0  # 맞힌 개수
        for number, quiz in enumerate(self.quizzes, start=1):
            quiz.display(number)
            user_answer = self.get_number("정답 입력: ", 1, 4)
            if quiz.is_correct(user_answer):
                print("✅ 정답입니다!")
                correct += 1
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.")

        score = round(correct / len(self.quizzes) * 100)
        print("=" * 40)
        print(f"🏆 결과: {len(self.quizzes)}문제 중 {correct}문제 정답! ({score}점)")
        print("=" * 40)
        self.update_best_score(score)

    def add_quiz(self):
        """문제, 선택지 4개, 정답 번호를 입력받아 새 퀴즈를 등록한다."""
        print("\n📌 새로운 퀴즈를 추가합니다.\n")
        question = self.get_text("문제를 입력하세요: ")
        choices = []
        for index in range(1, 5):
            choices.append(self.get_text(f"선택지 {index}: "))
        answer = self.get_number("정답 번호 (1-4): ", 1, 4)
        self.quizzes.append(Quiz(question, choices, answer))
        self.save_state()  # [추가] 추가한 퀴즈를 파일에 저장
        print("\n✅ 퀴즈가 추가되었습니다!")

    def show_quiz_list(self):
        """등록된 퀴즈의 문제 목록을 보여 준다."""
        if not self.quizzes:
            print("📭 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return

        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)\n")
        print("-" * 40)
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"[{number}] {quiz.question}")
        print("-" * 40)

    def update_best_score(self, score):
        """이번 점수가 최고 점수보다 높으면 최고 점수를 바꾼다."""
        if self.best_score is None or score > self.best_score:
            self.best_score = score
            self.save_state()  # [추가] 최고 점수를 파일에 저장
            print("🎉 새로운 최고 점수입니다!")
        else:
            print(f"현재 최고 점수는 {self.best_score}점입니다.")

    def show_best_score(self):
        """최고 점수를 보여 준다. 아직 기록이 없으면 안내한다."""
        if self.best_score is None:
            print("📭 아직 퀴즈를 푼 기록이 없습니다. 먼저 퀴즈를 풀어 보세요.")
        else:
            print(f"\n🏆 최고 점수: {self.best_score}점")

    # ---------- 실행 ----------

    def run(self):
        """메뉴를 반복해서 보여 주고, 선택에 따라 기능을 실행한다."""
        while True:
            self.show_menu()
            choice = self.get_number("선택: ", 1, self.MENU_COUNT)
            if choice == 1:
                self.play_quiz()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.show_quiz_list()
            elif choice == 4:
                self.show_best_score()
            else:
                self.save_state()  # [추가] 종료 전에 저장
                print("👋 게임을 종료합니다. 안녕히 가세요!")
                break
