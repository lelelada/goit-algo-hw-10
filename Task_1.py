import time
import sys

# Набір монет. Задається від більшого номіналу до меншого.
COINS = [50, 25, 10, 5, 2, 1]

def find_coins_greedy(amount):
    """
    Видає решту за допомогою жадібного алгоритму.
    Алгоритм завжди вибирає найбільший доступний номінал монети.
    
    Args:
        amount (int): Сума, яку потрібно видати.
    
    Returns:
        dict: Словник з кількістю монет кожного номіналу.
    """
    if not isinstance(amount, (int, float)) or amount < 0:
        print("Помилка: Сума має бути невід'ємним числом.", file=sys.stderr)
        return {}

    result = {}
    remaining_amount = int(amount)
    
    for coin in COINS:
        if remaining_amount >= coin:
            count = remaining_amount // coin
            result[coin] = count
            remaining_amount %= coin
    
    return result

def find_min_coins(amount):
    """
    Видає решту за допомогою динамічного програмування, знаходячи
    мінімальну кількість монет.
    
    Args:
        amount (int): Сума, яку потрібно видати.
    
    Returns:
        dict: Словник з кількістю монет кожного номіналу.
    """
    if not isinstance(amount, (int, float)) or amount < 0:
        print("Помилка: Сума має бути невід'ємним числом.", file=sys.stderr)
        return {}
    
    amount = int(amount)
    # Створюємо масив для зберігання мінімальної кількості монет для кожної суми
    min_coins = [0] + [float('inf')] * amount
    # Створюємо масив для відновлення використаних монет
    coin_used = [0] * (amount + 1)
    
    for i in range(1, amount + 1):
        for coin in COINS:
            if coin <= i and min_coins[i - coin] != float('inf'):
                if min_coins[i - coin] + 1 < min_coins[i]:
                    min_coins[i] = min_coins[i - coin] + 1
                    coin_used[i] = coin
    
    # Відновлюємо набір монет
    result = {}
    current_amount = amount
    while current_amount > 0:
        coin = coin_used[current_amount]
        result[coin] = result.get(coin, 0) + 1
        current_amount -= coin
        
    return result

# Приклад використання та порівняння ефективності
if __name__ == "__main__":
    test_amount_small = 113
    test_amount_large = 99999

    print("--- Тестування на сумі 113 ---")
    start_time_greedy_small = time.time()
    result_greedy_small = find_coins_greedy(test_amount_small)
    end_time_greedy_small = time.time()
    print(f"Жадібний алгоритм: {result_greedy_small}")
    print(f"Час початку виконання: {start_time_greedy_small:.25f} сек.")
    print(f"Час кінця виконання: {start_time_greedy_small:.25f} сек.")
    print(f"Час виконання: {end_time_greedy_small - start_time_greedy_small:.20f} сек.")

    start_time_dp_small = time.time()
    result_dp_small = find_min_coins(test_amount_small)
    end_time_dp_small = time.time()
    print(f"\nДинамічне програмування: {result_dp_small}")
    print(f"Час виконання: {end_time_dp_small - start_time_dp_small:.20f} сек.")

    print("\n--- Тестування на сумі 99999 ---")
    start_time_greedy_large = time.time()
    result_greedy_large = find_coins_greedy(test_amount_large)
    end_time_greedy_large = time.time()
    print(f"Жадібний алгоритм: {result_greedy_large}")
    print(f"Час виконання: {end_time_greedy_large - start_time_greedy_large:.20f} сек.")
    
    start_time_dp_large = time.time()
    result_dp_large = find_min_coins(test_amount_large)
    end_time_dp_large = time.time()
    print(f"\nДинамічне програмування: {result_dp_large}")
    print(f"Час виконання: {end_time_dp_large - start_time_dp_large:.10f} сек.")
