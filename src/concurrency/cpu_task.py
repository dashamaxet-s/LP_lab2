def count_primes(limit: int) -> int:
    total = 0
    for n in range(2, limit):        # перебираем числа от 2 до limit
        is_prime = True
        for d in range(2, int(n**0.5) + 1):  # перебираем делители до корня из n
            if n % d == 0:
                is_prime = False
                break
        total += is_prime            # True = 1, False = 0
    return total