import timeit
import chardet

# Функція для визначення кодування файлу
def detect_encoding(file_path):
    with open(file_path, "rb") as f:
        result = chardet.detect(f.read())
    return result["encoding"]

# Шляхи до файлів
file1_path = "стаття 1.txt"
file2_path = "стаття 2 (1).txt"

# Визначення кодування файлів
encoding1 = detect_encoding(file1_path)
encoding2 = detect_encoding(file2_path)

# Завантаження текстів з коректним кодуванням
with open(file1_path, "r", encoding=encoding1) as f:
    text1 = f.read()

with open(file2_path, "r", encoding=encoding2) as f:
    text2 = f.read()

# Підрядки для пошуку
existing_substring = "алгоритм пошуку"  # Існуючий підрядок
non_existing_substring = "вигаданий_підрядок"  # Вигаданий підрядок

# Алгоритм Боєра-Мура
def boyer_moore_search(text, pattern):
    m, n = len(pattern), len(text)
    if m == 0: return -1
    skip = {pattern[i]: m - i - 1 for i in range(m - 1)}
    i = m - 1
    while i < n:
        j = m - 1
        while j >= 0 and text[i] == pattern[j]:
            i -= 1
            j -= 1
        if j == -1:
            return i + 1
        i += skip.get(text[i], m)
    return -1

# Алгоритм Кнута-Морріса-Пратта
def kmp_search(text, pattern):
    m, n = len(pattern), len(text)
    if m == 0: return -1
    lps = [0] * m
    j = 0
    for i in range(1, m):
        while j > 0 and pattern[i] != pattern[j]:
            j = lps[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
            lps[i] = j
    i = j = 0
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
            if j == m:
                return i - j
        else:
            j = lps[j - 1] if j > 0 else 0
            i += 1 if j == 0 else 0
    return -1

# Алгоритм Рабіна-Карпа
def rabin_karp_search(text, pattern, prime=101):
    m, n = len(pattern), len(text)
    if m == 0: return -1
    d = 256
    p, t, h = 0, 0, 1
    for i in range(m - 1):
        h = (h * d) % prime
    for i in range(m):
        p = (d * p + ord(pattern[i])) % prime
        t = (d * t + ord(text[i])) % prime
    for i in range(n - m + 1):
        if p == t:
            if text[i:i + m] == pattern:
                return i
        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % prime
            if t < 0:
                t += prime
    return -1

# Вимірювання часу виконання алгоритмів
results = {}
for text, text_name in zip([text1, text2], ["Стаття 1", "Стаття 2"]):
    for pattern, pattern_name in zip([existing_substring, non_existing_substring], ["Існуючий підрядок", "Вигаданий підрядок"]):
        results[(text_name, pattern_name, "Боєр-Мур")] = timeit.timeit(lambda: boyer_moore_search(text, pattern), number=10)
        results[(text_name, pattern_name, "Кнут-Морріс-Пратт")] = timeit.timeit(lambda: kmp_search(text, pattern), number=10)
        results[(text_name, pattern_name, "Рабін-Карп")] = timeit.timeit(lambda: rabin_karp_search(text, pattern), number=10)

# Виведення результатів
import pandas as pd

df_results = pd.DataFrame.from_dict(results, orient="index", columns=["Час (сек)"])
df_results.index = pd.MultiIndex.from_tuples(df_results.index, names=["Текст", "Підрядок", "Алгоритм"])
print(df_results)

# Визначення найшвидшого алгоритму
grouped = df_results.groupby(level=["Текст", "Підрядок"]).idxmin()
print("\nНайшвидші алгоритми:")
print(grouped)
