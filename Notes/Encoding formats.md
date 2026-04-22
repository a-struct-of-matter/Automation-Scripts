ASCII : 0-127  plain readable text...
HEX : 0-8 A-F even length, common in malware and flags
Base64 : A–Z a–z 0–9 + / = and often ends with = or == Length divisible by 4
Base32 : A-Z 2-7 padding with = used in TOTP, DNS and malware C2
Base58 : Cypto world doesnt contain 0 O I l for wallet addresses etc
Data Compression
-> Magic Bytes
1F 8B-------------> GZIP
50 4B 03 04-------> ZIP
78 9C  -----------> ZLIB
Stegnography
PNG --> Magic bytes 89 50 4E 47
IEND, IHDR, IDAT

JPEG --> FF D8 FF
Data hide in EXIF or DCT Coefficients

PDF --> %PDF-1.4

MZ -> 4D 5A

