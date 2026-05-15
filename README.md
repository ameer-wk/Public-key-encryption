# Public-key-encryption
A Python implementation of a custom public-key encryption system based on superincreasing sequences and modular arithmetic. This project demonstrates the generation of public/private key pairs, encryption of binary messages, and ciphertext decryption using modular inverses and greedy subset-sum reconstruction.

Features
Public and private key generation
Random superincreasing sequence generation
Modular arithmetic operations
Encryption of binary plaintext messages
Decryption using modular inverse computation
Greedy algorithm for plaintext recovery
Command-line interaction for user input/output

Cryptographic Concepts Used
Public-Key Cryptography
Superincreasing Sequences
Modular Arithmetic
Modular Inverses
Greedy Algorithms
Subset Sum / Knapsack-style Encryption

How It Works
Generate a superincreasing sequence e
Select a prime modulus q and multiplier w
Compute the public key h using modular multiplication
Encrypt binary plaintext using the public key
Decrypt ciphertext using the private key and modular inverse

Technologies
Python 3
Standard Python libraries (math, random)

Educational Purpose
This project was developed as part of a cybersecurity and cryptography study project to explore alternative approaches to public-key encryption and understand the mathematical principles behind knapsack-based cryptosystems.
