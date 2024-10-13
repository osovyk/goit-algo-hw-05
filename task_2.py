def binary_search_with_iterations(arr, x):
    low = 0
    high = len(arr) - 1
    mid = 0
    iterations = 0

    while low <= high:
        iterations += 1
        mid = (high + low) // 2

        if arr[mid] < x:
            low = mid + 1
        elif arr[mid] > x:
            high = mid - 1
        else:
            return iterations, arr[mid]

    # Якщо елемент не знайдений, повертаємо кількість ітерацій та верхню межу
    upper_bound = arr[low] if low < len(arr) else None
    return iterations, upper_bound

def main():
    # Приклад використання
    arr = [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7]
    x = 3.4
    result = binary_search_with_iterations(arr, x)
    print(result)

if __name__ == "__main__":
    main()
