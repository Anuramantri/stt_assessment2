"""Sorting algorithms: merge sort, heap sort, and bubble sort."""

def mergesort(arr):
    """Merge sort algorithm."""
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    l = mergesort(arr[:mid])
    r = mergesort(arr[mid:])

    merged = []
    i = j = 0
    while i < len(l) and j < len(r):
        if l[i] < r[j]:
            merged.append(l[i])
            i += 1
        else:
            merged.append(r[j])
            j += 1
    merged += l[i:]
    merged += r[j:]
    return merged


def heapify(arr, n, i):
    """Maintains the heap property."""
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2

    if l < n and arr[l] > arr[largest]:
        largest = l
    if r < n and arr[r] > arr[largest]:
        largest = r
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


def heapsort(arr):
    """Heap sort algorithm."""
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)
    return arr


def bubblesort(arr):
    """Bubble sort algorithm."""
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr
