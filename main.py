"""AI 활용 상식 퀴즈 게임 - 실행 파일"""

from quiz_game import QuizGame


def main():
    """게임을 만들고 실행한다. Ctrl+C를 눌러도 안전하게 종료한다."""
    game = QuizGame()
    try:
        game.run()
    except (KeyboardInterrupt, EOFError):
        print("\n\n⚠️ 입력이 중단되어 프로그램을 안전하게 종료합니다.")


if __name__ == "__main__":
    main()
