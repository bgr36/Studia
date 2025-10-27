import binascii
import binary_text

SEPARATOR = "01111110"
CRC_SIZE = 32

def destuff_bits(data):
    destuffed = ""
    count = 0
    i = 0
    while i < len(data):
        bit = data[i]
        destuffed += bit
        if bit == "1":
            count += 1
            if count == 5:
                i += 1
                count = 0
        else:
            count = 0
        i += 1
    return destuffed

def read_frames(input_file="file_encrypted.txt"):
    with open(input_file, 'r', encoding='ASCII') as f:
        data = f.read()
    overall=[]
    all_corect = 0
    pos = 0
    while True:
        start = data.find(SEPARATOR, pos)
        if start == -1:
            break
        end = data.find(SEPARATOR, start + len(SEPARATOR))
        if end == -1:
            break
        frame = data[start + len(SEPARATOR):end]
        while start and end and len(frame) < binary_text.FRAME_SIZE:
            start = end
            end = data.find(SEPARATOR, start + len(SEPARATOR))
            frame = data[start + len(SEPARATOR):end]
            
        destuffed = destuff_bits(frame)
        payload = destuffed[:-CRC_SIZE]
        crc_received = destuffed[-CRC_SIZE:]
        computed_crc = binascii.crc32(payload.encode("ASCII"))
        computed_crc_bin = format(computed_crc, f'0{CRC_SIZE}b')


        
        print("\n--- ODEBRANA RAMKA ---")
        crc_ok = crc_received == computed_crc_bin
        all_corect += crc_ok
        print("CRC OK:", crc_ok)
        text = binary_text.binary_to_text(payload)
        print("Dane: ", text)
        overall.append(text)
        pos = end + len(SEPARATOR)

    print(f'\nLiczba udanych: {all_corect}')
    print(f'Treść pliku: {"".join(overall)}')
if __name__ == "__main__":
    read_frames()
