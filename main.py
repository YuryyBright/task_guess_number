import random


def display_welcome():
    """Виводить привітальне повідомлення та правила гри"""
    print("=" * 50)
    print("🎯 Вітаємо у грі 'Вгадай число'! 🎯")
    print("=" * 50)
    print("Правила:")
    print("• Комп'ютер загадав число від 1 до 100")
    print("• У вас є 7 спроб, щоб його вгадати")
    print("• Після кожної спроби ви отримаєте підказку")
    print("• Удачі! 🍀")
    print("=" * 50)


def get_player_guess(attempt_num, max_attempts):
    """Отримує та валідує введення гравця"""
    while True:
        try:
            print(f"\n📝 Спроба {attempt_num}/{max_attempts}")
            guess = input("Введіть ваше число (1-100): ")

            # Перевірка на вихід з гри
            if guess.lower() in ['exit', 'quit', 'вихід']:
                print("👋 Дякуємо за гру! До побачення!")
                return None

            # Конвертація в число
            guess = int(guess)

            # Перевірка діапазону
            if guess < 1 or guess > 100:
                print("❌ Помилка: Число має бути від 1 до 100!")
                continue

            return guess

        except ValueError:
            print("❌ Помилка: Введіть ціле число!")


def give_hint(guess, target):
    """Надає підказку гравцю на основі його здогадки"""
    if guess < target:
        print(f"📈 Занадто маленьке! Спробуйте більше число.")
    elif guess > target:
        print(f"📉 Занадто велике! Спробуйте менше число.")


def play_game():
    """Основна функція гри"""
    # Ініціалізація
    MIN_NUMBER = 1
    MAX_NUMBER = 100
    MAX_ATTEMPTS = 7

    # Генерація випадкового числа
    target_number = random.randint(MIN_NUMBER, MAX_NUMBER)

    # Показ привітання
    display_welcome()

    # Основний цикл гри
    for attempt in range(1, MAX_ATTEMPTS + 1):
        # Отримання здогадки гравця
        player_guess = get_player_guess(attempt, MAX_ATTEMPTS)

        # Перевірка на вихід
        if player_guess is None:
            return

        # Перевірка на перемогу
        if player_guess == target_number:
            print("\n" + "🎉" * 20)
            print(f"🏆 ВІТАЄМО! ВИ ВГАДАЛИ! 🏆")
            print(f"🎯 Загадане число: {target_number}")
            print(f"⭐ Кількість спроб: {attempt}")

            # Оцінка результату
            if attempt == 1:
                print("🌟 Неймовірна удача!")
            elif attempt <= 3:
                print("🌟 Відмінний результат!")
            elif attempt <= 5:
                print("👍 Хороший результат!")
            else:
                print("👌 Непогано!")

            print("🎉" * 20)
            return

        # Надання підказки
        give_hint(player_guess, target_number)

        # Показ залишкових спроб
        remaining = MAX_ATTEMPTS - attempt
        if remaining > 0:
            print(f"💡 Залишилось спроб: {remaining}")

    # Гра закінчена - поразка
    print("\n" + "💔" * 20)
    print("😔 УВИ, СПРОБИ ЗАКІНЧИЛИСЬ!")
    print(f"🎯 Загадане число було: {target_number}")
    print("🔄 Спробуйте ще раз!")
    print("💔" * 20)


def ask_play_again():
    """Запитує чи хоче гравець зіграти ще раз"""
    while True:
        choice = input("\n🔄 Бажаєте зіграти ще раз? (так/ні): ").lower().strip()
        if choice in ['так', 'yes', 'y', 'т', '1']:
            return True
        elif choice in ['ні', 'no', 'n', 'н', '0']:
            return False
        else:
            print("❌ Введіть 'так' або 'ні'")


def main():
    """Головна функція програми"""
    print("🎮 Запуск гри 'Вгадай число'...")

    # Основний цикл програми
    while True:
        play_game()

        # Запит на повторну гру
        if not ask_play_again():
            print("\n👋 Дякуємо за гру! До побачення!")
            break

        print("\n" + "🔄" * 30)
        print("Початок нової гри!")
        print("🔄" * 30)


if __name__ == "__main__":
    main()