def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    iterations = 0
    upper_bound = None
    
    while left <= right:
        iterations += 1
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return iterations, arr[mid]
        elif arr[mid] < target:
            left = mid + 1
        else:
            upper_bound = arr[mid]
            right = mid - 1
    
    return iterations, upper_bound

# Тестуємо двійковий пошук
sorted_array = [0.1, 1.2, 3.5, 5.8, 7.3, 10.4]
target_value = 4.0
result = binary_search(sorted_array, target_value)
print(result)  # Виведе кортеж з кількістю ітерацій та верхньою межею
