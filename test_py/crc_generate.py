def process_input(input_str):
    input_str = input_str.replace(" ", "").replace("_", "").replace(",", "")
    result = []
    for i in range(0, len(input_str), 2):
        result.append(int(input_str[i:i+2], 16))
    return result

def generate_crc(in_data):
    crc = 0xFFFFFFFF
    poly = 0xEDB88320
    for data in in_data:
        crc ^= data
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ poly
            else:
                crc >>= 1
    return crc ^ 0xFFFFFFFF

def swap_bytes(original_int):
    # Swap the bytes
    swapped_int = ((original_int & 0xFF) << 24) | \
                  ((original_int & 0xFF00) << 8) | \
                  ((original_int & 0xFF0000) >> 8) | \
                  ((original_int & 0xFF000000) >> 24)
    
    # Convert swapped integer back to hexadecimal
    swapped_hex = hex(swapped_int)
    
    return swapped_hex

def main():
    data = "E20106D7CD0DF0761E8DCD3D08000F101112131415161718191A1B1C1D1E1F202122232425262728292A2B2C2D2E2F303132333435363738393A000329c7bd09"
    hex_numbers = data.replace('_', '').split(',')
    input_str = ','.join([number[i:i+2] for number in hex_numbers for i in range(0, len(number), 2)])
    
    # print(input_str)
    
    my_input = process_input(input_str)
    CRC = generate_crc(my_input)
    # mCRC = (CRC & 0xFFFF0000) | ((CRC ^ 0xFFFFFFFF) & 0x0000FFFF)

    print(swap_bytes(CRC))

if __name__ == "__main__":
    main()
