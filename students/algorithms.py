def generate_luhn_check_digit(number):
    """Generates a Luhn check digit for the given number."""
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = 0
    checksum += sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))
    check_digit = (10 - checksum % 10) % 10
    return check_digit