# Find max diff to array arr
def maxdiff(arr):
    if len(arr) < 2:
        return 0

    c = int(len(arr) / 2)
    left = arr[:c]
    right = arr[c:]

    i_prime = min(left)
    j_prime = max(right)

    max_diff_cross = j_prime - i_prime

    # Returns the max of three
    return max(max_diff_cross, maxdiff(left), maxdiff(right))


a = [-5, 3, -1, 8, 3, -6, 10]
print(maxdiff(a))  # Should be 16
print(maxdiff([5]))  # should be 0

# Should be 0 because of decreasing list
print(maxdiff(list(range(100, 0, -1))))
