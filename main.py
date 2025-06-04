import random

# === КОНСТАНТИ ===
MIN_NUMBER = 1
MAX_NUMBER = 100
MAX_ATTEMPTS = 7
EXIT_COMMANDS = ['exit', 'quit', 'вихід']
YES_ANSWERS = ['так', 'yes', 'y', 'т', '1']
NO_ANSWERS = ['ні', 'no', 'n', 'н', '0']


def display_welcome():
    """Виводить привітальне повідомлення та правила гри"""
    print("=" * 50)
    print("🎯 Вітаємо у грі 'Вгадай число'! 🎯")
    print("=" * 50)
    print("Правила:")
    print(f"\u2022 Комп'ютер загадав число від {MIN_NUMBER} до {MAX_NUMBER}")
    print(f"\u2022 У вас є {MAX_ATTEMPTS} спроб, щоб його вгадати")
    print("\u2022 Після кожної спроби ви отримаєте підказку")
    print("• Удачі! 🍀")
    print("=" * 50)


def get_player_guess(attempt_num, max_attempts):
    """Отримує та валідує введення гравця"""
    while True:
        try:
            print(f"\n📝 Спроба {attempt_num}/{max_attempts}")
            guess = input(f"Введіть ваше число ({MIN_NUMBER}-{MAX_NUMBER}): ")

            if guess.lower() in EXIT_COMMANDS:
                print("👋 Дякуємо за гру! До побачення!")
                return None

            guess = int(guess)

            if guess < MIN_NUMBER or guess > MAX_NUMBER:
                print(f"❌ Помилка: Число має бути від {MIN_NUMBER} до {MAX_NUMBER}!")
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
    target_number = random.randint(MIN_NUMBER, MAX_NUMBER)
    display_welcome()

    for attempt in range(1, MAX_ATTEMPTS + 1):
        player_guess = get_player_guess(attempt, MAX_ATTEMPTS)

        if player_guess is None:
            return

        if player_guess == target_number:
            print("\n" + "🎉" * 20)
            print(f"🏆 ВІТАЄМО! ВИ ВГАДАЛИ! 🏆")
            print(f"🎯 Загадане число: {target_number}")
            print(f"⭐ Кількість спроб: {attempt}")

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

        give_hint(player_guess, target_number)

        remaining = MAX_ATTEMPTS - attempt
        if remaining > 0:
            print(f"💡 Залишилось спроб: {remaining}")

    print("\n" + "💔" * 20)
    print("😔 УВИ, СПРОБИ ЗАКІНЧИЛИСЬ!")
    print(f"🎯 Загадане число було: {target_number}")
    print("🔄 Спробуйте ще раз!")
    print("💔" * 20)


def ask_play_again():
    """Запитує чи хоче гравець зіграти ще раз"""
    while True:
        choice = input("\n🔄 Бажаєте зіграти ще раз? (так/ні): ").lower().strip()
        if choice in YES_ANSWERS:
            return True
        elif choice in NO_ANSWERS:
            return False
        else:
            print("❌ Введіть 'так' або 'ні'")


def main():
    """Головна функція програми"""
    print("🎮 Запуск гри 'Вгадай число'...")

    while True:
        play_game()
        if not ask_play_again():
            print("\n👋 Дякуємо за гру! До побачення!")
            break

        print("\n" + "🔄" * 30)
        print("Початок нової гри!")
        print("🔄" * 30)


if __name__ == "__main__":
    main()
