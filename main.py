from PIL import Image

DELIMITER = "######"

def encode_image(image_path, secret_message, output_path):
    # Open the cover image
    cover_image = Image.open(image_path).convert('RGB')
    width, height = cover_image.size

    # Append the delimiter to the secret message
    secret_message += DELIMITER

    # Convert the secret message to binary
    binary_secret = ''.join(format(ord(char), '08b') for char in secret_message)

    # Check if the secret message can fit in the cover image
    if len(binary_secret) > (width * height * 3):
        raise ValueError("Secret message is too large to be encoded in the cover image.")

    # Iterate through the pixels of the image
    pixels = cover_image.load()
    index = 0
    for x in range(width):
        for y in range(height):
            # Get the RGB values of the pixel
            r, g, b = pixels[x, y]

            # Modify the least significant bits of the RGB values with the secret message
            if index < len(binary_secret):
                r = r & 254 | int(binary_secret[index])
                index += 1
            if index < len(binary_secret):
                g = g & 254 | int(binary_secret[index])
                index += 1
            if index < len(binary_secret):
                b = b & 254 | int(binary_secret[index])
                index += 1

            # Update the pixel with the modified RGB values
            pixels[x, y] = (r, g, b)

    # Save the stego image
    cover_image.save(output_path)
    print("Encoding successful. Stego image saved at", output_path)

def decode_image(stego_image_path):
    # Open the stego image
    stego_image = Image.open(stego_image_path)
    width, height = stego_image.size

    # Initialize the binary_secret variable to store the decoded secret message
    binary_secret = ""

    # Iterate through the pixels of the image
    pixels = stego_image.load()
    for x in range(width):
        for y in range(height):
            # Get the RGB values of the pixel
            r, g, b = pixels[x, y]

            # Extract the least significant bits from each channel and add them to the binary_secret
            binary_secret += str(r & 1)
            binary_secret += str(g & 1)
            binary_secret += str(b & 1)

    # Convert the binary secret to ASCII characters
    secret_message = ""
    for i in range(0, len(binary_secret), 8):
        byte = binary_secret[i:i+8]
        char = chr(int(byte, 2))
        if char == DELIMITER:
            break
        secret_message += char

    return secret_message

def steganography():
    i = 1
    while i != 0:
        print("Image Steganography\n1. Encode\n2. Decode ")
        userInp = int((input("\nEnter your choice: ")))
        if userInp == 1:
            imgName = input("Enter image name: ")
            msg = input("Enter message: ")
            encImg = input("Enter name of encoded image: ")
            encode_image(imgName, msg, encImg)
        else:
            imgName = input("Enter image name: ")
            ans = decode_image(imgName)
            print("The message hidden in the image is: " + ans)
        i = int(input("\nEnter 1 to continue and 0 to exit: "))
        
# Function Call

steganography()