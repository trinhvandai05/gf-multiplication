"""Phep nhan trong GF(2^4) tu phep cong XOR va nhan voi x (xtime)."""

BITS = 4
MASK = (1 << BITS) - 1       # 0b1111: giu 4 bit thap
TOP_BIT = 1 << (BITS - 1)  # 0b1000: bit he so x^3

# Ca 3 da thuc bat kha quy bac 4 tren GF(2).
MODULI = (0x13, 0x19, 0x1F)
DEFAULT_MODULUS = 0x13    # x^4 + x + 1


def xor(a: int, b: int) -> int:
    """Cong hai da thuc co he so thuoc GF(2)."""
    return a ^ b


def xtime(g: int, m: int = DEFAULT_MODULUS) -> int:
    """Tra ve (x * g(x)) mod m(x)."""
    if not 0 <= g <= MASK:
        raise ValueError("g phai nam trong khoang 0..15")
    if m not in MODULI:
        raise ValueError("m khong thuoc danh sach da thuc bat kha quy bac 4")

    carry = (g & TOP_BIT) != 0
    shifted = (g << 1) & MASK

    if carry:
        shifted = xor(shifted, m & MASK)

    return shifted


def multiply(f: int, g: int, m: int = DEFAULT_MODULUS,
             show_steps: bool = False) -> int:
    """Tra ve (f(x) * g(x)) mod m(x), su dung xtime va XOR."""
    if not (0 <= f <= MASK and 0 <= g <= MASK):
        raise ValueError("f va g phai nam trong khoang 0..15")
    if m not in MODULI:
        raise ValueError("m khong thuoc danh sach da thuc bat kha quy bac 4")

    result = 0
    term = g   # Ban dau la x^0 * g(x) mod m(x)

    if show_steps:
        print("\ni | bit f_i | x^i*g mod m | result sau XOR")
        print("--+---------+-------------+----------------")

    for i in range(BITS):
        bit = (f >> i) & 1
        if bit:
            result = xor(result, term)

        if show_steps:
            print(f"{i} |    {bit}    |    {term:04b}     |      {result:04b}")

        if i < BITS - 1:
            term = xtime(term, m)

    return result
