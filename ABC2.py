def float_to_ieee754(num):
    import struct
    return struct.unpack('>I', struct.pack('>f', num))[0]

def ieee754_to_float(hex_val):
    import struct
    return struct.unpack('>f', struct.pack('>I', hex_val))[0]

def add_ieee754_manual_rounding(hex_a, hex_b, rounding_mode="nearest"):
    a = int(hex_a, 16)
    b = int(hex_b, 16)
    
    sign_a = (a >> 31) & 1
    sign_b = (b >> 31) & 1
    exp_a = (a >> 23) & 0xFF
    exp_b = (b >> 23) & 0xFF
    mant_a = a & 0x7FFFFF
    mant_b = b & 0x7FFFFF
    
    if exp_a == 0 and mant_a == 0 and exp_b == 0 and mant_b == 0:
        if sign_a != sign_b:
            return "00000000"
        else:
            return "80000000" if sign_a == 1 else "00000000"
    
    if exp_a == 0xFF or exp_b == 0xFF:
        return "7FC00000"
    
    hidden_a = 1 if exp_a != 0 else 0
    hidden_b = 1 if exp_b != 0 else 0
    full_mant_a = (hidden_a << 23) | mant_a
    full_mant_b = (hidden_b << 23) | mant_b
    real_exp_a = exp_a if exp_a != 0 else 1
    real_exp_b = exp_b if exp_b != 0 else 1
    
    if real_exp_a > real_exp_b:
        exp_diff = real_exp_a - real_exp_b
        full_mant_b >>= exp_diff
        res_exp = real_exp_a
    elif real_exp_b > real_exp_a:
        exp_diff = real_exp_b - real_exp_a
        full_mant_a >>= exp_diff
        res_exp = real_exp_b
    else:
        res_exp = real_exp_a
    
    val_a = full_mant_a if sign_a == 0 else -full_mant_a
    val_b = full_mant_b if sign_b == 0 else -full_mant_b
    sum_mant = val_a + val_b
    
    if sum_mant > 0:
        res_sign = 0
    elif sum_mant < 0:
        res_sign = 1
        sum_mant = -sum_mant
    else:
        return "00000000"
    
    bit_length = sum_mant.bit_length()
    
    if bit_length > 24:
        shift_right = bit_length - 24
        sum_mant >>= shift_right
        res_exp += shift_right
    elif bit_length < 24:
        shift_left = 24 - bit_length
        sum_mant <<= shift_left
        res_exp -= shift_left
    
    res_mant = sum_mant & 0x7FFFFF
    
    if rounding_mode == "nearest":
        pass
    elif rounding_mode == "up":
        pass
    elif rounding_mode == "down":
        pass
    
    res = (res_sign << 31) | (res_exp << 23) | res_mant
    return f"{res:08X}".upper()

if __name__ == "__main__":
    a_hex = "7ED00000"
    b_hex = "7D800000"
    
    print(f"Сложение чисел IEEE 754:")
    print(f"A = {a_hex}")
    print(f"B = {b_hex}")
    
    a_float = ieee754_to_float(int(a_hex, 16))
    b_float = ieee754_to_float(int(b_hex, 16))
    print(f"A в десятичном виде: {a_float}")
    print(f"B в десятичном виде: {b_float}")
    
    result_hex = add_ieee754_manual_rounding(a_hex, b_hex)
    result_float = ieee754_to_float(int(result_hex, 16))
    
    print(f"\nРезультат (hex): {result_hex}")
    print(f"Результат (десятичный): {result_float}")
    print(f"Проверка прямой суммой Python: {a_float + b_float}")