"""AI 활용 상식 퀴즈 게임 - 실행 파일"""

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


def main():
    """메뉴를 반복해서 보여 주고, 선택에 따라 동작한다."""
    while True:
        show_menu()
        choice = get_number("선택: ", 1, MENU_COUNT)
        if choice == 1:
            print("📝 퀴즈 풀기 기능은 준비 중입니다.")
        elif choice == 2:
            print("📌 퀴즈 추가 기능은 준비 중입니다.")
        elif choice == 3:
            print("📋 퀴즈 목록 기능은 준비 중입니다.")
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

