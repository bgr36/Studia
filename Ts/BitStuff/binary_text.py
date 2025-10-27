FRAME_SIZE = 120
FRAME_COUNT = 30
MAX_BITS = FRAME_SIZE*FRAME_COUNT

def text_file_to_binary_file(input_file, output_file, max_bits = MAX_BITS):
    with open(input_file, 'r', encoding='ASCII') as f:
        text = f.read()

    binary_str = text_to_binary(text, max_bits)[:max_bits]

    with open(output_file, 'w') as f:
        f.write(binary_str)

def binary_file_to_text(input_file):
    with open(input_file, 'r', encoding='ASCII') as f:
        bits = f.read()
    return binary_to_text(bits)

def text_to_binary(text, max_bits = FRAME_SIZE):
    return ''.join(format(ord(char), '08b') for char in text)[:max_bits]

def binary_to_text(binary_text):
    return ''.join([chr(int(binary_text[i:i+8], 2)) for i in range(0, len(binary_text), 8)])

if __name__ == "__main__":
    text_file_to_binary_file("file.txt", "binary.txt")