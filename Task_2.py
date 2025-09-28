import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as spi

# --- 1. Визначення функції та межі інтегрування ---
def f(x):
    """Функція, яку ми інтегруємо: f(x) = x^2"""
    return x ** 2

a = 0  # Нижня межа
b = 2  # Верхня межа

# --- 2. Аналітичне обчислення та перевірка (Використання SciPy quad) ---
# Аналітичний розрахунок: Інтеграл від x^2 dx від 0 до 2 дорівнює [x^3/3] від 0 до 2,
# що становить (2^3)/3 - (0^3)/3 = 8/3 ≈ 2.666667
result_analytical, error_analytical = spi.quad(f, a, b)

# --- 3. Обчислення інтеграла методом Монте-Карло ---
def monte_carlo_integration(f, a, b, num_points=100000):
    """
    Обчислює визначений інтеграл функції f(x) на інтервалі [a, b] 
    за допомогою методу Монте-Карло.

    Args:
        f (function): Функція, яку потрібно інтегрувати.
        a (float): Нижня межа інтегрування.
        b (float): Верхня межа інтегрування.
        num_points (int): Кількість випадкових точок для симуляції.

    Returns:
        float: Оцінка значення інтеграла.
    """
    # 1. Визначення максимальної висоти (M) на інтервалі [a, b]
    # Оскільки f(x) = x^2 зростає на [0, 2], максимальне значення буде в b.
    M = f(b)
    
    # 2. Визначення площі прямокутника (Area)
    width = b - a
    Area_rect = width * M
    
    # 3. Генерація випадкових точок
    # Генерація x-координат рівномірно на інтервалі [a, b]
    random_x = np.random.uniform(a, b, num_points)
    # Генерація y-координат рівномірно на інтервалі [0, M]
    random_y = np.random.uniform(0, M, num_points)
    
    # 4. Підрахунок точок, що потрапили під криву
    # Точка (x, y) потрапляє під криву f(x), якщо y <= f(x)
    points_under_curve = np.sum(random_y <= f(random_x))
    
    # 5. Оцінка інтеграла
    # Площа інтеграла ≈ Area_rect * (Кількість точок під кривою / Загальна кількість точок)
    integral_estimate = Area_rect * (points_under_curve / num_points)
    
    return integral_estimate, Area_rect, random_x, random_y, M

# Запуск Монте-Карло
num_points = 100000
mc_estimate, area_rect, random_x, random_y, M = monte_carlo_integration(f, a, b, num_points)

# --- 4. Виведення результатів та порівняння ---
print("--- Результати обчислень інтеграла f(x) = x^2 від {a} до {b} ---".format(a=a, b=b))
print(f"1. Аналітичний розрахунок (SciPy quad): {result_analytical:.6f}")
print(f"2. Метод Монте-Карло (N={num_points}): {mc_estimate:.6f}")

# Розрахунок похибки Монте-Карло
error_mc = abs(result_analytical - mc_estimate)
print(f"Похибка методу Монте-Карло: {error_mc:.6f}")
print("-" * 60)

# --- 5. Створення графічного представлення ---
# Створення діапазону значень для x
x = np.linspace(a - 0.5, b + 0.5, 400)
y = f(x)

# Створення графіка
fig, ax = plt.subplots(figsize=(10, 6))

# Малювання функції
ax.plot(x, y, 'r', linewidth=2, label='f(x) = x^2')

# Заповнення області під кривою (область інтегрування)
ix = np.linspace(a, b, 100)
iy = f(ix)
ax.fill_between(ix, iy, color='gray', alpha=0.3, label='Площа інтеграла')

# Відображення випадкових точок Монте-Карло
# Точки, що потрапили під криву (для візуалізації)
is_under = random_y <= f(random_x)

# Точки під кривою (зелені)
ax.scatter(random_x[is_under], random_y[is_under], color='green', s=1, alpha=0.5, label='Точки під кривою')
# Точки над кривою (сині)
ax.scatter(random_x[~is_under], random_y[~is_under], color='blue', s=1, alpha=0.1, label='Точки над кривою')


# Малювання прямокутника Монте-Карло
ax.hlines(M, a, b, color='purple', linestyle=':', label=f'Макс. висота M={M}')

# Налаштування графіка
ax.set_xlim([x[0], x[-1]])
ax.set_ylim([0, max(y) + 0.5])
ax.set_xlabel('x')
ax.set_ylabel('f(x)')

# Додавання меж інтегрування та назви графіка
ax.axvline(x=a, color='gray', linestyle='--')
ax.axvline(x=b, color='gray', linestyle='--')
ax.set_title(f'Інтегрування f(x) = x^2 від {a} до {b} методом Монте-Карло (N={num_points})')
ax.legend(loc='upper left')
plt.grid(True)
plt.show()

# --- 6. Висновки ---
print("\n--- Висновки про ефективність методу Монте-Карло ---")
print(f"Аналітичне значення: {result_analytical:.6f}")
print(f"Оцінка Монте-Карло: {mc_estimate:.6f}")
print(f"Похибка: {error_mc:.6f}")

print("\n**1. Точність:**")
print(f"При використанні {num_points} точок, метод Монте-Карло дав оцінку, яка дуже близька до точного аналітичного значення. Похибка становить лише {error_mc:.6f}.")

print("\n**2. Ефективність:**")
print("Метод Монте-Карло не вимагає складних аналітичних розрахунків. Його точність пропорційна $\\frac{1}{\\sqrt{N}}$, де $N$ — кількість точок. Це означає, що для подвоєння точності потрібно збільшити кількість точок у чотири рази.")

print("\n**3. Порівняння з quad (Аналітичний метод):**")
print("Функція `spi.quad` (яка використовує адаптивні квадратурні методи) є набагато точнішою та швидшою для простих одновимірних інтегралів, як цей. Вона дає результат з машинною точністю.")
print("Монте-Карло стає незамінним для інтегралів високої розмірності (наприклад, 4, 5 і більше змінних), де класичні квадратурні методи стають обчислювально надто дорогими.")
