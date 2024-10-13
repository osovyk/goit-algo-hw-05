import timeit

# Завантаження статей
def load_article(file_path, encoding="utf-8"):
    with open(file_path, "r", encoding=encoding) as file:
        return file.read()

file_1 = load_article("article_1.txt")
file_2 = load_article("article_2.txt")

# Підрядки для пошуку
substring_from_article_1 = "Розглянемо деякі реалізації відомих алгоритмів пошуку [2] на Java"
substring_from_article_2 = "Масштабовані розподілені сховища (Column Family (Bigtable) stores)"

# Алгоритми пошуку
def boyer_moore_search(text, pattern):
    # Реалізація алгоритму Боєра-Мура
    table = {}
    length = len(pattern)
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    table.setdefault(pattern[-1], length)

    i = 0
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1
        if j < 0:
            return i
        i += table.get(text[i + len(pattern) - 1], len(pattern))
    return -1

def kmp_search(text, pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    i = j = 0
    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == len(pattern):
            return i - j
        elif i < len(text) and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1

def polynomial_hash(s, base=256, modulus=101):
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, len(s) - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value

def rabin_karp_search(main_string, substring):
    base = 256
    modulus = 101
    substring_length = len(substring)
    main_string_length = len(main_string)

    substring_hash = polynomial_hash(substring, base, modulus)
    current_slice_hash = polynomial_hash(main_string[:substring_length], base, modulus)
    h_multiplier = pow(base, substring_length - 1) % modulus

    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash and main_string[i:i + substring_length] == substring:
            return i
        if i < main_string_length - substring_length:
            current_slice_hash = (current_slice_hash - ord(main_string[i]) * h_multiplier) % modulus
            current_slice_hash = (current_slice_hash * base + ord(main_string[i + substring_length])) % modulus
            current_slice_hash = (current_slice_hash + modulus) % modulus
    return -1

# Вимірювання часу
def measure_search_time(search_func, text, pattern, iterations=1000):
    return timeit.timeit(lambda: search_func(text, pattern), number=iterations)


def main():
    # Дані для тестування
    algorithms = {
        "Алгоритм Боєра-Мура": boyer_moore_search,
        "Алгоритм Кнута-Морріса-Пратта": kmp_search,
        "Алгоритм Рабіна-Карпа": rabin_karp_search
    }

    articles = {
        "Стаття 1": file_1,
        "Стаття 2": file_2
    }

    substrings = {
        "Текст з статті 1": substring_from_article_1,
        "Текст з статті 2": substring_from_article_2
    }

    # Вимірювання часу та запис результатів
    results = {}

    for article_name, article_text in articles.items():
        results[article_name] = {}
        for substring_desc, substring in substrings.items():
            results[article_name][substring_desc] = {}
            for algorithm_name, algorithm_func in algorithms.items():
                time_taken = measure_search_time(algorithm_func, article_text, substring)
                results[article_name][substring_desc][algorithm_name] = time_taken


    for article, data in results.items():
        for substring_type, times in data.items():
            print(f"У {article} шукаємо {substring_type}:")
            for algorithm, time in times.items():
                print(f"  {algorithm}: {time:.6f} секунд")
            fastest_algorithm = min(times, key=times.get)
            print(f"Найшвидший алгоритм для {article} + {substring_type}: {fastest_algorithm}")
            print("-" * 5)
        print("*" * 20)

if __name__ == "__main__":
    main()