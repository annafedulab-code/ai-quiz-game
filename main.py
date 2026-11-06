"""AI 활용 상식 퀴즈 게임 - 실행 파일"""

from default_quizzes import get_default_quizzes  # 기본 퀴즈 가져오기
from quiz import Quiz  # 새 퀴즈를 만들 때 사용

MENU_COUNT = 5  # 메뉴 개수


def show_menu():
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


def get_number(prompt, min_value, max_value):
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


def get_text(prompt):
    """빈 칸이 아닌 글자를 입력받아 돌려준다."""
    while True:
        text = input(prompt).strip()
        if text == "":
            print("⚠️ 입력이 비어 있습니다. 내용을 입력하세요.")
            continue
        return text


def play_quiz(quizzes):
    """퀴즈를 차례로 출제하고, 맞힌 개수를 돌려준다."""
    if not quizzes:
        print("📭 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
        return 0

    print(f"\n📝 퀴즈를 시작합니다! (총 {len(quizzes)}문제)")
    correct = 0  # 맞힌 개수
    for number, quiz in enumerate(quizzes, start=1):
        quiz.display(number)
        user_answer = get_number("정답 입력: ", 1, 4)
        if quiz.is_correct(user_answer):
            print("✅ 정답입니다!")
            correct += 1
        else:
            print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.")

    score = round(correct / len(quizzes) * 100)
    print("=" * 40)
    print(f"🏆 결과: {len(quizzes)}문제 중 {correct}문제 정답! ({score}점)")
    print("=" * 40)
    return correct


def add_quiz(quizzes):
    """문제, 선택지 4개, 정답 번호를 입력받아 새 퀴즈를 등록한다."""
    print("\n📌 새로운 퀴즈를 추가합니다.\n")
    question = get_text("문제를 입력하세요: ")
    choices = []
    for index in range(1, 5):
        choices.append(get_text(f"선택지 {index}: "))
    answer = get_number("정답 번호 (1-4): ", 1, 4)
    quizzes.append(Quiz(question, choices, answer))
    print("\n✅ 퀴즈가 추가되었습니다!")


def show_quiz_list(quizzes):
    """[추가] 등록된 퀴즈의 문제 목록을 보여 준다."""
    if not quizzes:
        print("📭 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
        return

    print(f"\n📋 등록된 퀴즈 목록 (총 {len(quizzes)}개)\n")
    print("-" * 40)
    for number, quiz in enumerate(quizzes, start=1):
        print(f"[{number}] {quiz.question}")
    print("-" * 40)


def main():
    """메뉴를 반복해서 보여 주고, 선택에 따라 동작한다."""
    quizzes = get_default_quizzes()  # 퀴즈 목록 준비
    while True:
        show_menu()
        choice = get_number("선택: ", 1, MENU_COUNT)
        if choice == 1:
            play_quiz(quizzes)
        elif choice == 2:
            add_quiz(quizzes)
        elif choice == 3:
            show_quiz_list(quizzes)  # [변경] 퀴즈 목록
        elif choice == 4:
            print("🏆 점수 확인 기능은 준비 중입니다.")
        else:
            print("👋 게임을 종료합니다. 안녕히 가세요!")
            break


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\n⚠️ 입력이 중단되어 프로그램을 안전하게 종료합니다.")
