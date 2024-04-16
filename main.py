from PIL import Image

def encrypt(text):
    binary_data = ''.join(f'{ord(c):08b}' for c in text)
    length_prefix = f'{len(binary_data):032b}'
    return length_prefix + binary_data

def encode_into_image():
    text = input('Enter Text: ')
    output_path = "Encoded.png"
    image_path = 'Original.png'

    image = Image.open(image_path)
    pixels = list(image.getdata())
    binary_data = encrypt(text)
    
    if len(binary_data) > len(pixels) * 3:
        print("Error: Image is too small to hold the data.")
        return

    data_index = 0
    new_pixels = []
    for pixel in pixels:
        r, g, b = pixel
        if data_index < len(binary_data):
            r = r & ~1 | int(binary_data[data_index])
            data_index += 1
        if data_index < len(binary_data):
            g = g & ~1 | int(binary_data[data_index])
            data_index += 1
        if data_index < len(binary_data):
            b = b & ~1 | int(binary_data[data_index])
            data_index += 1
        new_pixels.append((r, g, b))

    encoded_image = Image.new("RGB", image.size)
    encoded_image.putdata(new_pixels)
    encoded_image.save(output_path)
    print("Encoding Successful!")

def decode_from_image(image_path):
    image = Image.open(image_path)
    pixels = list(image.getdata())
    binary_string = ''

    for pixel in pixels:
        r, g, b = pixel
        binary_string += (bin(r)[-1] + bin(g)[-1] + bin(b)[-1])

    data_length = int(binary_string[:32], 2) 
    binary_string = binary_string[32:32+data_length]

    decoded_text = ''
    for i in range(0, len(binary_string), 8):
        byte = binary_string[i:i+8]
        if byte:
            decoded_text += chr(int(byte, 2))

    print("Decoded Text:", decoded_text)


if __name__ == "__main__":
    encode_into_image()
    decode_from_image('Encoded.png')

