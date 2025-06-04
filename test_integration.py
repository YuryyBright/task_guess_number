import pytest
import unittest.mock as mock
import io
import sys
import time
import threading
from contextlib import contextmanager
from main import main, play_game


class TestGameIntegration:
    """Інтеграційні тести повного циклу гри"""

    @pytest.mark.integration
    def test_complete_winning_game_scenario(self, capsys):
        """Повний сценарій виграшної гри"""
        # Симулюємо повну гру: 50 -> 25 -> 75 -> 60 -> 55 -> 58 -> 57 (вгадав)
        inputs = ['50', '25', '75', '60', '55', '58', '57']

        with mock.patch('random.randint', return_value=57), \
                mock.patch('builtins.input', side_effect=inputs):
            play_game()
            captured = capsys.readouterr()

            # Перевіряємо всі етапи гри
            assert "Занадто маленьке!" in captured.out
            assert "Занадто велике!" in captured.out
            assert "ВІТАЄМО! ВИ ВГАДАЛИ!" in captured.out
            assert "Загадане число: 57" in captured.out

    @pytest.mark.integration
    def test_complete_losing_game_scenario(self, capsys):
        """Повний сценарій програшної гри"""
        # 7 невдалих спроб
        losing_inputs = ['1', '2', '3', '4', '5', '6', '7']

        with mock.patch('random.randint', return_value=50), \
                mock.patch('builtins.input', side_effect=losing_inputs):
            play_game()
            captured = capsys.readouterr()

            assert "СПРОБИ ЗАКІНЧИЛИСЬ!" in captured.out
            assert "Загадане число було: 50" in captured.out
            assert captured.out.count("Занадто маленьке!") == 7

    @pytest.mark.integration
    def test_multiple_games_session(self, capsys):
        """Тест сесії з кількома іграми"""
        game_inputs = [
            # Перша гра: вгадуємо 30 за 2 спроби
            '20', '30',
            # Запит на повторну гру
            'так',
            # Друга гра: вгадуємо 80 за 3 спроби
            '50', '90', '80',
            # Відмова від третьої гри
            'ні'
        ]

        with mock.patch('random.randint', side_effect=[30, 80]), \
                mock.patch('builtins.input', side_effect=game_inputs):
            main()
            captured = capsys.readouterr()

            # Перевіряємо що було дві гри
            assert captured.out.count("ВІТАЄМО! ВИ ВГАДАЛИ!") == 2
            assert "Початок нової гри!" in captured.out
            assert "Дякуємо за гру! До побачення!" in captured.out


class TestGamePerformance:
    """Тести продуктивності"""

    @pytest.mark.slow
    def test_game_startup_performance(self):
        """Тест швидкості запуску гри"""
        start_time = time.time()

        with mock.patch('random.randint', return_value=50), \
                mock.patch('builtins.input', return_value='50'), \
                mock.patch('sys.stdout', new_callable=io.StringIO):
            play_game()

        execution_time = time.time() - start_time
        # Гра повинна запускатися швидко (менше 1 секунди)
        assert execution_time < 1.0

    @pytest.mark.slow
    def test_multiple_games_memory_usage(self):
        """Тест використання пам'яті при багатьох іграх"""
        import tracemalloc

        tracemalloc.start()

        # Симулюємо 10 швидких ігор
        for i in range(10):
            with mock.patch('random.randint', return_value=50), \
                    mock.patch('builtins.input', return_value='50'), \
                    mock.patch('sys.stdout', new_callable=io.StringIO):
                play_game()

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # Перевіряємо що пік пам'яті розумний (менше 10MB)
        assert peak < 10 * 1024 * 1024


class TestErrorHandling:
    """Тести обробки помилок"""

    @pytest.mark.integration
    def test_keyboard_interrupt_handling(self):
        """Тест обробки переривання клавіатурою"""

        def interrupt_input(*args, **kwargs):
            raise KeyboardInterrupt()

        with mock.patch('builtins.input', side_effect=interrupt_input), \
                pytest.raises(KeyboardInterrupt):
            play_game()

    @pytest.mark.integration
    def test_eof_error_handling(self):
        """Тест обробки EOF помилки"""

        def eof_input(*args, **kwargs):
            raise EOFError()

        with mock.patch('builtins.input', side_effect=eof_input), \
                pytest.raises(EOFError):
            play_game()

    def test_invalid_input_recovery(self, capsys):
        """Тест відновлення після невалідного введення"""
        # Багато різних типів невалідного введення
        inputs = [
            '',  # Порожній рядок
            ' ',  # Тільки пробіл
            'abc123',  # Змішаний текст
            '12.5',  # Десяткове число
            '-50',  # Від'ємне число
            '150',  # Поза діапазоном
            '50'  # Нарешті валідне
        ]

        with mock.patch('random.randint', return_value=50), \
                mock.patch('builtins.input', side_effect=inputs):
            play_game()
            captured = capsys.readouterr()

            assert "ВІТАЄМО! ВИ ВГАДАЛИ!" in captured.out
            assert "Введіть ціле число!" in captured.out
            assert "Число має бути від 1 до 100!" in captured.out


class TestGameLogicEdgeCases:
    """Тести граничних випадків ігрової логіки"""

    @pytest.mark.integration
    def test_boundary_numbers_guessing(self):
        """Тест вгадування граничних чисел"""
        # Тест мінімального числа
        with mock.patch('random.randint', return_value=1), \
                mock.patch('builtins.input', return_value='1'), \
                mock.patch('sys.stdout', new_callable=io.StringIO) as mock_out:
            play_game()
            output = mock_out.getvalue()
            assert "ВІТАЄМО! ВИ ВГАДАЛИ!" in output
            assert "Загадане число: 1" in output

        # Тест максимального числа
        with mock.patch('random.randint', return_value=100), \
                mock.patch('builtins.input', return_value='100'), \
                mock.patch('sys.stdout', new_callable=io.StringIO) as mock_out:
            play_game()
            output = mock_out.getvalue()
            assert "ВІТАЄМО! ВИ ВГАДАЛИ!" in output
            assert "Загадане число: 100" in output

    @pytest.mark.integration
    def test_optimal_strategy_simulation(self, capsys):
        """Симуляція оптимальної стратегії бінарного пошуку"""
        target = 73

        # Оптимальна стратегія бінарного пошуку
        optimal_guesses = ['50', '75', '62', '69', '72', '74', '73']


        with mock.patch('random.randint', return_value=target), \
                mock.patch('builtins.input', side_effect=optimal_guesses):
            play_game()
            captured = capsys.readouterr()

            assert "ВІТАЄМО! ВИ ВГАДАЛИ!" in captured.out
            assert f"Загадане число: {target}" in captured.out
            # Перевіряємо що використано 7 спроб (максимум для бінарного пошуку в діапазоні 1-100)
            assert "Кількість спроб: 7" in captured.out


class TestConcurrency:
    """Тести конкурентності (якщо гра розширюється)"""

    @pytest.mark.slow
    def test_multiple_simultaneous_games(self):
        """Тест одночасного запуску кількох ігор"""
        results = []

        def run_game():
            with mock.patch('random.randint', return_value=50), \
                    mock.patch('builtins.input', return_value='50'), \
                    mock.patch('sys.stdout', new_callable=io.StringIO) as mock_out:
                play_game()
                results.append("ВІТАЄМО! ВИ ВГАДАЛИ!" in mock_out.getvalue())

        # Запускаємо 5 ігор паралельно
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=run_game)
            threads.append(thread)
            thread.start()

        # Очікуємо завершення всіх потоків
        for thread in threads:
            thread.join(timeout=5.0)  # 5 секунд таймаут

        # Перевіряємо що всі ігри завершились успішно
        assert len(results) == 5
        assert all(results)


class TestDataValidation:
    """Тести валідації даних"""

    @pytest.mark.integration
    def test_unicode_input_handling(self, capsys):
        """Тест обробки Unicode символів"""
        unicode_inputs = [
            '五十',  # Китайські цифри
            '٥٠',  # Арабські цифри
            'пятьдесят',  # Текст
            '🎯',  # Емодзі
            '50'  # Нормальне число
        ]

        with mock.patch('random.randint', return_value=50), \
                mock.patch('builtins.input', side_effect=unicode_inputs):
            play_game()
            captured = capsys.readouterr()

            assert "ВІТАЄМО! ВИ ВГАДАЛИ!" in captured.out
            assert "Введіть ціле число!" in captured.out

    def test_very_long_input(self, capsys):
        """Тест дуже довгого введення"""
        long_input = 'a' * 10000  # 10k символів
        valid_input = '50'

        with mock.patch('random.randint', return_value=50), \
                mock.patch('builtins.input', side_effect=[long_input, valid_input]):
            play_game()
            captured = capsys.readouterr()

            assert "ВІТАЄМО! ВИ ВГАДАЛИ!" in captured.out
            assert "Введіть ціле число!" in captured.out


class TestGameStateConsistency:
    """Тести консистентності стану гри"""

    @pytest.mark.integration
    def test_attempt_counter_accuracy(self, capsys):
        """Тест точності лічильника спроб"""
        inputs = ['10', '20', '30', '40', '50']

        with mock.patch('random.randint', return_value=50), \
                mock.patch('builtins.input', side_effect=inputs):
            play_game()
            captured = capsys.readouterr()

            # Перевіряємо що лічильник спроб відображається правильно
            for i in range(1, 6):  # 5 спроб
                assert f"Спроба {i}/7" in captured.out

            assert "Кількість спроб: 5" in captured.out

    @pytest.mark.integration
    def test_remaining_attempts_display(self, capsys):
        """Тест відображення залишкових спроб"""
        inputs = ['10', '20', '30', 'вихід']  # 3 неправильні спроби

        with mock.patch('random.randint', return_value=50), \
                mock.patch('builtins.input', side_effect=inputs):
            play_game()
            captured = capsys.readouterr()

            # Перевіряємо послідовність залишкових спроб: 6, 5, 4
            assert "Залишилось спроб: 6" in captured.out
            assert "Залишилось спроб: 5" in captured.out
            assert "Залишилось спроб: 4" in captured.out


class TestUserExperienceScenarios:
    """Тести сценаріїв користувацького досвіду"""

    @pytest.mark.integration
    def test_frustrated_user_scenario(self, capsys):
        """Сценарій розчарованого користувача"""
        # Користувач вводить багато неправильних значень
        inputs = [
            'abc', 'xyz', '-10', '200', '0.5',
            'quit'  # Нарешті виходить
        ]

        with mock.patch('random.randint', return_value=50), \
                mock.patch('builtins.input', side_effect=inputs):
            play_game()
            captured = capsys.readouterr()

            assert "Дякуємо за гру! До побачення!" in captured.out
            assert "Введіть ціле число!" in captured.out
            assert "Число має бути від 1 до 100!" in captured.out

    @pytest.mark.integration
    def test_perfectionist_user_scenario(self, capsys):
        """Сценарій перфекціоніста (вгадує з першої спроби)"""
        with mock.patch('random.randint', return_value=42), \
                mock.patch('builtins.input', return_value='42'):
            play_game()
            captured = capsys.readouterr()

            assert "Неймовірна удача!" in captured.out
            assert "Кількість спроб: 1" in captured.out

    @pytest.mark.integration
    def test_persistent_user_scenario(self, capsys):
        """Сценарій наполегливого користувача"""
        # Користувач використовує всі спроби до кінця
        inputs = ['10', '20', '30', '40', '50', '60', '70']  # 7 спроб, не вгадав

        with mock.patch('random.randint', return_value=80), \
                mock.patch('builtins.input', side_effect=inputs):
            play_game()
            captured = capsys.readouterr()

            assert "СПРОБИ ЗАКІНЧИЛИСЬ!" in captured.out
            assert "Загадане число було: 80" in captured.out


@pytest.fixture
def game_session():
    """Фікстура для ігрової сесії"""

    class GameSession:
        def __init__(self):
            self.games_played = 0
            self.games_won = 0
            self.total_attempts = 0

    return GameSession()


class TestSessionStatistics:
    """Тести статистики сесії (розширення функціональності)"""

    def test_session_tracking(self, game_session):
        """Тест відстеження статистики сесії"""
        # Цей тест показує як можна розширити гру статистикою

        # Симулюємо кілька ігор
        game_results = [
            (True, 3),  # Виграв за 3 спроби
            (False, 7),  # Програв за 7 спроб
            (True, 1),  # Виграв за 1 спробу
        ]

        for won, attempts in game_results:
            game_session.games_played += 1
            game_session.total_attempts += attempts
            if won:
                game_session.games_won += 1

        # Перевірки статистики
        assert game_session.games_played == 3
        assert game_session.games_won == 2
        assert game_session.total_attempts == 11

        win_rate = game_session.games_won / game_session.games_played
        avg_attempts = game_session.total_attempts / game_session.games_played

        assert win_rate == pytest.approx(0.667, rel=1e-2)
        assert avg_attempts == pytest.approx(3.667, rel=1e-2)


class TestAccessibility:
    """Тести доступності"""

    @pytest.mark.integration
    def test_screen_reader_friendly_output(self, capsys):
        """Тест виводу, дружнього до скрін-рідерів"""
        with mock.patch('random.randint', return_value=50), \
                mock.patch('builtins.input', return_value='50'):
            play_game()
            captured = capsys.readouterr()

            # Перевіряємо що є описовий текст без тільки емодзі
            assert "Вітаємо у грі" in captured.out
            assert "Спроба 1/7" in captured.out
            assert "ВІТАЄМО! ВИ ВГАДАЛИ!" in captured.out

    def test_clear_instructions(self, capsys):
        """Тест чіткості інструкцій"""
        with mock.patch('random.randint', return_value=50), \
                mock.patch('builtins.input', return_value='50'):
            play_game()
            captured = capsys.readouterr()

            # Перевіряємо наявність чітких інструкцій
            assert "Правила:" in captured.out
            assert "Комп'ютер загадав число від 1 до 100" in captured.out
            assert "У вас є 7 спроб" in captured.out


# Маркери для категоризації тестів
pytestmark = [
    pytest.mark.integration,
]

if __name__ == "__main__":
    # Запуск тільки інтеграційних тестів
    pytest.main([
        "-v",
        "--tb=short",
        "-m", "integration",
        __file__
    ])