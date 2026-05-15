import random
from math import gcd
import ast
import sys

#Generate a superincreasing sequence n where each element is higher than the sum of the previous elements
def sequence_generater(n):
    e = []
    total = 0
    for i in range(n):
        next_value = total + random.randint(1, 10)   
        e.append(next_value)
        total += next_value
    return e

#Test if a number is prime
def prime(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True

#Generate public and private keys
def key_generater(n):
    e = sequence_generater(n)

    while True:
        q = random.randint(2 * e[-1] + 5, 2 * e[-1] + 500) #q > 2 * e_n
        if prime(q):
            break

    while True:
        w = random.randint(2, q - 1)
        if gcd(w, q) == 1: #w and q has to be coprime
            break
    h = [(w * ei) % q for ei in e]
    return e, q, w, h

#Encrypt the bits using the public key
def encrypt(bits, h, size):
    cipher_block = []

    original_size = len(bits)
    if len(bits) % size != 0:
        padding = size - (len(bits) % size) #pad bits to make it possible to divide it evenly
        bits = bits + [0] * padding

    for i in range(0, len(bits), size):
        block = bits[i:i + size]
        c = 0
        for j in range(size):
            c += h[j] * block[j]
        cipher_block.append(c)
    return cipher_block, original_size

#Calculate modular inverse
def inverse(a, b):
    try:
        return pow(a, -1, b)
    except:
        return None

#Decrypt the cipher using the private key
def decrypt(cipher_block, e, q, w, size, original_size):
    inv_w = inverse(w, q)
    if inv_w is None:
        raise ValueError("Error: inverse dosnt exist")
    all_bits = []

    for c in cipher_block: #Decrypt each block 
        prime_c = (c * inv_w) % q
        bits = [0] * size
        remaining = prime_c

        for i in range(size - 1, -1, -1): #Recover bits 
            if remaining >= e[i]:
                bits[i] = 1
                remaining -= e[i]
        all_bits.extend(bits)
    return all_bits[:original_size]

#Convert text to bits
def convert_text(text):
    bits = []
    for d in text:
        t = format(ord(d), "08b")
        for bit in t:
            bits.append(int(bit))
    return bits

#Convert bits to text
def convert_bit(bits):
    td = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i + 8]
        if len(byte) < 8:
            byte = byte + [0] * (8 - len(byte))
        value = int("".join(str(t) for t in byte), 2)
        td.append(chr(value))
    return "".join(td)


#menu to choose what to do
def menu():
    print("\nPublic key encryption program")
    print("--------------------------------------")
    
   #Choose size of n
    while True:
        n_in = input("Enter sequence length n (recommended 8): ")
        try:
            size = int(n_in)
            if size <= 0:
                print("Error: n must be a positive integer.")
                continue
            break
        except ValueError:
            print("Error: please enter a whole number (e.g. 8).")

    keys_generated = False
    e = q = w = h = None

    last_cipher_block = None
    last_original_size = None

    while True:
        print("\nMenu:")
        print("1. Generate key pair")
        print("2. Encrypt text")
        print("3. Decrypt ciphertext")
        print("4. Run long test")
        print("5. Exit")

        choice = input("Choose option: ")

        
        if choice == "1":
            e, q, w, h = key_generater(size)
            print("e =", e)
            print("q =", q)
            print("w =", w)
            print("h =", h)
            keys_generated = True

        elif choice == "2":
            if not keys_generated:
                print (" choose option 1 to generate keys, then u can encrypt")
                continue

            text = input("Enter plaintext: ")
            bits = convert_text(text)

           
            while True:
                h_in = input(f"Enter public key h as a list {size}  ")
                try:
                    h = ast.literal_eval(h_in)
                except Exception:
                    print(" h format is wrong")
                    continue

                if not isinstance(h, list):
                    print(" h should be a list of numbers in square brackets.")
                    continue

                if len(h) != size:
                    print(f" h must have length {size}.")
                    continue

                if not all(isinstance(x, int) for x in h):
                    print("h must only contain integers.")
                    continue

                break  

            try:
                cipher_block, original_size = encrypt(bits, h, size)
            except Exception as ex:
                print("Encryption error:", ex)
                continue

            print("Ciphertext:", cipher_block)

            last_cipher_block = cipher_block
            last_original_size = original_size

        
        elif choice == "3":
            if not keys_generated:
                print (" choose option 1 to generate keys so u can decrypt")
                continue
            
            if last_cipher_block is None:
                print("Nothing is encrypted so you cannot decrypt.")
                continue

            cipher_block = last_cipher_block
            original_size = last_original_size
            print("Using stored ciphertext.")

           
            while True:
                e_in = input(f"Enter private key e as a list of {size}  ")
                try:
                    e = ast.literal_eval(e_in)
                except Exception as e:
                    print("Invalid e format:", e)
                    print(" e should be numbers")
                    continue

                if not isinstance(e, list):
                    print(" e should be a list in square brackets.")
                    continue

                if len(e) != size:
                    print(f"Error: e must have length {size}.")
                    continue

                if not all(isinstance(x, int) for x in e):
                    print(" e should only contain numbers.")
                    continue

                break  

            
            while True:
                q_in = input("Enter q: ")
                try:
                    q = int(q_in)
                    if q <= 0:
                        print(" q should be a positive number.")
                        continue
                    break
                except ValueError:
                    print(" q should be a whole number.")

            
            while True:
                w_in = input("Enter w: ")
                try:
                    w = int(w_in)
                    if w <= 0:
                        print(" w should be a positive number.")
                        continue
                    break
                except ValueError:
                    print(" w should be a whole number.")

            try:
                bits = decrypt(cipher_block, e, q, w, size, original_size)
                text = convert_bit(bits)
                print("Decrypted:", text)
            except Exception as err:
                print("Decryption error:", err)

        
        elif choice == "4":
            try:
                run_test()
            except Exception as err:
                print(" error while running long test:", err)

        
        elif choice == "5":
            print("Exiting program.")
            sys.exit()

        else:
            print("Not an option.")


def run_test():
    size = 8  
    plaintext = (
        "To Ameer: Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum. Nam quam nunc, blandit vel, luctus pulvinar, hendrerit id, lorem. Maecenas nec odio et ante tincidunt tempus. Donec vitae sapien ut libero venenatis faucibus. Nullam quis ante. Etiam sit amet orci eget eros faucibus tincidunt. Duis leo. Sed fringilla mauris sit amet nibh. Donec sodales sagittis magna. Sed consequat, leo eget bibendum sodales, augue velit cursus nunc, "
    )
    print("\n Running long test ")
    print("Plaintext length:", len(plaintext), "characters\n")
    bits = convert_text(plaintext)
    original_size = len(bits)

    # Key pair 1
    print("Generating key pair 1...")
    e1, q1, w1, h1 = key_generater(size)
    cipher_block1, _ = encrypt(bits, h1, size)
    decrypted_bits1 = decrypt(cipher_block1, e1, q1, w1, size, original_size)
    decrypted_text1 = convert_bit(decrypted_bits1)
    print("\nKey pair 1:")
    print("q1:", q1)
    print("w1:", w1)
    print("e1:", e1)
    print("h1:", h1)
    print("Correct decryption:", decrypted_text1 == plaintext)

    # Key pair 2
    print("\nGenerating key pair 2...")
    e2, q2, w2, h2 = key_generater(size)
    cipher_block2, _ = encrypt(bits, h2, size)
    decrypted_bits2 = decrypt(cipher_block2, e2, q2, w2, size, original_size)
    decrypted_text2 = convert_bit(decrypted_bits2)
    print("\nKey pair 2:")
    print("q2:", q2)
    print("w2:", w2)
    print("e2:", e2)
    print("h2:", h2)
    print("Correct decryption:", decrypted_text2 == plaintext)
    print("\n Test finished \n")

if __name__ == "__main__":
    menu()
