import binascii
import binary_text

SEPARATOR = "01111110"
CRC_SIZE = 32

def stuff_bits(data):
    stuffed = ""
    count = 0
    for bit in data:
        stuffed += bit
        if bit == "1":
            count += 1
            if count == 5:
                stuffed += "0"
                count = 0
        else:
            count = 0
    return stuffed

def send_frames(input_file="binary.txt", output_file="file_encrypted.txt", payload_size=binary_text.FRAME_SIZE):
    with open(input_file, 'r', encoding='ASCII') as f:
        text = f.read()
    
    total_bits = len(text)
    frames = []
    i = 0
    
    while i < total_bits:
        payload = text[i:i+payload_size]
        crc = binascii.crc32(payload.encode("ASCII"))
        crc_bits = format(crc, f'0{CRC_SIZE}b')
        full_frame = payload + crc_bits
        stuffed = stuff_bits(full_frame)
        framed = SEPARATOR + stuffed + SEPARATOR
        frames.append(framed)
        i += payload_size
    
    with open(output_file, 'w') as f:
        f.write(''.join(frames))

if __name__ == "__main__":
    send_frames()
