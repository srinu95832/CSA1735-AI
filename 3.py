from itertools import permutations

def solve_cryptarithm():
    # Given problem
    words = ["SEND", "MORE"]
    result = "MONEY"

    # Extract unique characters from the puzzle
    unique_chars = set("".join(words) + result)
    if len(unique_chars) > 10:
        raise ValueError("Too many unique characters for a valid solution")

    # Create a list of all possible permutations of digits 0-9
    digits = range(10)
    perms = permutations(digits, len(unique_chars))

    for perm in perms:
        char_to_digit = dict(zip(unique_chars, perm))
        
        # Make sure that the numbers don't start with zero
        if any(char_to_digit[word[0]] == 0 for word in words + [result]):
            continue

        # Convert words to their respective numeric values
        def word_to_number(word):
            return int("".join(str(char_to_digit[char]) for char in word))
        
        num_words = [word_to_number(word) for word in words]
        num_result = word_to_number(result)

        # Check if the sum of the words equals the result
        if sum(num_words) == num_result:
            return char_to_digit

    return None

# Run the solver
solution = solve_cryptarithm()

if solution:
    print("Solution found:")
    for char, digit in solution.items():
        print(f"{char} -> {digit}")
else:
    print("No solution exists")
