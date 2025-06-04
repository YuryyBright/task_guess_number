import pytest
import unittest.mock as mock
import random
import io
import sys
from main import (
    display_welcome,
    get_player_guess,
    give_hint,
    play_game,
    ask_play_again,
    main
)


class TestDisplayWelcome:
    """Тести для функції display_welcome"""

    def test_display_welcome_output(self, capsys):
        """Тест виводу привітального повідомлення"""
        display_welcome()
        captured = capsys.readouterr()

        assert "Вітаємо у грі 'Вгадай число'!" in captured.out
        assert "Правила:" in captured.out
        assert "Комп'ютер загадав число від 1 до 100" in captured.out
        assert "У вас є 7 спроб" in captured.out
        assert "Удачі!" in captured.out


class TestGetPlayerGuess:
    """Тести для функції get_player_guess"""

    @mock.patch('builtins.input', return_value='50')
    def test_valid_guess(self, mock_input):
        """Тест валідного введення числа"""
        result = get_player_guess(1, 7)
        assert result == 50

    @mock.patch('builtins.input', side_effect=['abc', '50'])
    def test_invalid_then_valid_guess(self, mock_input, capsys):
        """Тест неправильного введення, потім правильного"""
        result = get_player_guess(1, 7)
        captured = capsys.readouterr()

        assert result == 50
        assert "Введіть ціле число!" in captured.out

    @mock.patch('builtins.input', side_effect=['0', '101', '50'])
    def test_out_of_range_then_valid(self, mock_input, capsys):
        """Тест введення поза діапазоном, потім валідного"""
        result = get_player_guess(1, 7)
        captured = capsys.readouterr()

        assert result == 50
        assert "Число має бути від 1 до 100!" in captured.out

    @mock.patch('builtins.input', return_value='exit')
    def test_exit_command(self, mock_input):
        """Тест команди виходу"""
        result = get_player_guess(1, 7)
        assert result is None

    @mock.patch('builtins.input', return_value='quit')
    def test_quit_command(self, mock_input):
        """Тест команди quit"""
        result = get_player_guess(1, 7)
        assert result is None

    @mock.patch('builtins.input', return_value='вихід')
    def test_exit_ukrainian(self, mock_input):
        """Тест української команди виходу"""
        result = get_player_guess(1, 7)
        assert result is None


class TestGiveHint:
    """Тести для функції give_hint"""

    def test_guess_too_small(self, capsys):
        """Тест підказки коли число занадто мале"""
        give_hint(30, 50)
        captured = capsys.readouterr()
        assert "Занадто маленьке!" in captured.out

    def test_guess_too_big(self, capsys):
        """Тест підказки коли число занадто велике"""
        give_hint(70, 50)
        captured = capsys.readouterr()
        assert "Занадто велике!" in captured.out

    def test_guess_equal_no_output(self, capsys):
        """Тест що немає виводу коли числа рівні"""
        give_hint(50, 50)
        captured = capsys.readouterr()
        assert captured.out == ""


class TestAskPlayAgain:
    """Тести для функції ask_play_again"""

    @mock.patch('builtins.input', return_value='так')
    def test_yes_ukrainian(self, mock_input):
        """Тест позитивної відповіді українською"""
        result = ask_play_again()
        assert result is True

    @mock.patch('builtins.input', return_value='yes')
    def test_yes_english(self, mock_input):
        """Тест позитивної відповіді англійською"""
        result = ask_play_again()
        assert result is True

    @mock.patch('builtins.input', return_value='ні')
    def test_no_ukrainian(self, mock_input):
        """Тест негативної відповіді українською"""
        result = ask_play_again()
        assert result is False

    @mock.patch('builtins.input', return_value='no')
    def test_no_english(self, mock_input):
        """Тест негативної відповіді англійською"""
        result = ask_play_again()
        assert result is False

    @mock.patch('builtins.input', side_effect=['maybe', 'так'])
    def test_invalid_then_valid(self, mock_input, capsys):
        """Тест неправильної відповіді, потім правильної"""
        result = ask_play_again()
        captured = capsys.readouterr()

        assert result is True
        assert "Введіть 'так' або 'ні'" in captured.out


class TestPlayGame:
    """Тести для основної функції гри"""

    @mock.patch('random.randint', return_value=50)
    @mock.patch('main.get_player_guess', return_value=50)
    @mock.patch('main.display_welcome')
    def test_win_first_try(self, mock_welcome, mock_guess, mock_random, capsys):
        """Тест перемоги з першої спроби"""
        play_game()
        captured = capsys.readouterr()

        assert "ВІТАЄМО! ВИ ВГАДАЛИ!" in captured.out
        assert "Неймовірна удача!" in captured.out
        mock_welcome.assert_called_once()
        mock_guess.assert_called_once_with(1, 7)

    @mock.patch('random.randint', return_value=50)
    @mock.patch('main.get_player_guess', side_effect=[30, 70, 50])
    @mock.patch('main.display_welcome')
    def test_win_third_try(self, mock_welcome, mock_guess, mock_random, capsys):
        """Тест перемоги з третьої спроби"""
        play_game()
        captured = capsys.readouterr()

        assert "ВІТАЄМО! ВИ ВГАДАЛИ!" in captured.out
        assert "Відмінний результат!" in captured.out
        assert "Занадто маленьке!" in captured.out
        assert "Занадто велике!" in captured.out
        assert mock_guess.call_count == 3

    @mock.patch('random.randint', return_value=50)
    @mock.patch('main.get_player_guess', return_value=None)
    @mock.patch('main.display_welcome')
    def test_early_exit(self, mock_welcome, mock_guess, mock_random, capsys):
        """Тест дострокового виходу з гри"""
        play_game()

        mock_welcome.assert_called_once()
        mock_guess.assert_called_once_with(1, 7)

    @mock.patch('random.randint', return_value=50)
    @mock.patch('main.get_player_guess', side_effect=[1, 2, 3, 4, 5, 6, 7])
    @mock.patch('main.display_welcome')
    def test_lose_game(self, mock_welcome, mock_guess, mock_random, capsys):
        """Тест поразки (всі спроби вичерпані)"""
        play_game()
        captured = capsys.readouterr()

        assert "СПРОБИ ЗАКІНЧИЛИСЬ!" in captured.out
        assert "Загадане число було: 50" in captured.out
        assert mock_guess.call_count == 7


class TestMainFunction:
    """Тести для головної функції main"""

    @mock.patch('main.ask_play_again', return_value=False)
    @mock.patch('main.play_game')
    def test_single_game(self, mock_play, mock_ask, capsys):
        """Тест однієї гри без повторення"""
        main()
        captured = capsys.readouterr()

        mock_play.assert_called_once()
        mock_ask.assert_called_once()
        assert "Дякуємо за гру!" in captured.out

    @mock.patch('main.ask_play_again', side_effect=[True, False])
    @mock.patch('main.play_game')
    def test_two_games(self, mock_play, mock_ask, capsys):
        """Тест двох ігор підряд"""
        main()
        captured = capsys.readouterr()

        assert mock_play.call_count == 2
        assert mock_ask.call_count == 2
        assert "Початок нової гри!" in captured.out


class TestGameLogic:
    """Інтеграційні тести логіки гри"""

    def test_random_number_generation(self):
        """Тест генерації випадкових чисел у правильному діапазоні"""
        random.seed(42)  # Для відтворюваності

        for _ in range(100):
            num = random.randint(1, 100)
            assert 1 <= num <= 100

    def test_hint_logic_comprehensive(self):
        """Комплексний тест логіки підказок"""
        test_cases = [
            (1, 50, "маленьке"),
            (49, 50, "маленьке"),
            (51, 50, "велике"),
            (100, 50, "велике"),
            (50, 50, "")  # Без підказки при вгадуванні
        ]

        for guess, target, expected_word in test_cases:
            with mock.patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
                give_hint(guess, target)
                output = mock_stdout.getvalue()

                if expected_word:
                    assert expected_word in output.lower()
                else:
                    assert output == ""


class TestEdgeCases:
    """Тести граничних випадків"""

    @mock.patch('builtins.input', side_effect=['1'])
    def test_minimum_valid_guess(self, mock_input):
        """Тест мінімального валідного числа"""
        result = get_player_guess(1, 7)
        assert result == 1

    @mock.patch('builtins.input', side_effect=['100'])
    def test_maximum_valid_guess(self, mock_input):
        """Тест максимального валідного числа"""
        result = get_player_guess(1, 7)
        assert result == 100

    @mock.patch('builtins.input', side_effect=['-1', '1'])
    def test_negative_number(self, mock_input, capsys):
        """Тест від'ємного числа"""
        result = get_player_guess(1, 7)
        captured = capsys.readouterr()

        assert result == 1
        assert "Число має бути від 1 до 100!" in captured.out

    @mock.patch('builtins.input', side_effect=['1000', '50'])
    def test_very_large_number(self, mock_input, capsys):
        """Тест дуже великого числа"""
        result = get_player_guess(1, 7)
        captured = capsys.readouterr()

        assert result == 50
        assert "Число має бути від 1 до 100!" in captured.out


# Pytest fixtures
@pytest.fixture
def mock_random():
    """Фікстура для мокування random.randint"""
    with mock.patch('random.randint') as mock_rand:
        yield mock_rand


@pytest.fixture
def capture_output():
    """Фікстура для захоплення виводу"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    yield captured_output
    sys.stdout = old_stdout


# Додаткові утилітарні тести
class TestUtilities:
    """Тести допоміжних функцій"""

    def test_game_constants(self):
        """Тест констант гри"""
        # Перевіряємо що константи використовуються правильно
        with mock.patch('random.randint') as mock_rand:
            mock_rand.return_value = 50

            # Викликаємо функцію і перевіряємо параметри
            with mock.patch('main.display_welcome'), \
                    mock.patch('main.get_player_guess', return_value=50):
                play_game()

            # Перевіряємо що random.randint викликався з правильними параметрами
            mock_rand.assert_called_with(1, 100)


if __name__ == "__main__":
    # Запуск тестів з детальним виводом
    pytest.main(["-v", "--tb=short", __file__])