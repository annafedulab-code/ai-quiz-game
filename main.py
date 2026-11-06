"""AI 활용 상식 퀴즈 게임 - 실행 파일"""

from quiz_game import QuizGame


def main():
    """게임을 만들고 실행한다. Ctrl+C를 눌러도 저장 후 안전하게 종료한다."""
    game = QuizGame()
    try:
        game.run()
    except (KeyboardInterrupt, EOFError):
        print("\n\n⚠️ 입력이 중단되었습니다. 데이터를 저장하고 안전하게 종료합니다.")
        game.save_state()  # [추가] 가능한 범위에서 저장


if __name__ == "__main__":
    main()
