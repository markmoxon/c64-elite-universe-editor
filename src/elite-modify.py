#!/usr/bin/env python
#
# ******************************************************************************
#
# COMMODORE 64 ELITE UNIVERSE EDITOR MODIFICATION SCRIPT
#
# Written by Mark Moxon
#
# This script applies flicker-free ship-drawing to Commodore 64 Elite, as
# described here:
#
# https://elite.bbcelite.com/deep_dives/flicker-free_ship_drawing.html
#
# It does the following:
#
#   * Decrypt the gma6 file
#   * Modify the gma6 file to draw flicker-free ships
#   * Encrypt the gma6 file
#   * Modify the gma1 file to remove disk protection
#
# Run this script by changing directory to the folder containing the disk files
# and running the script with "python elite-modify.py"
#
# This modification script works with the following disk images from the
# Commodore 64 Preservation Project:
#
#   * elite[firebird_1986](pal)(v040486).g64
#   * elite[firebird_1986](ntsc)(v060186)(!).g64
#
# You can find the Commodore 64 Preservation Project on archive.org here:
#
# https://archive.org/details/C64_Preservation_Project_10th_Anniversary_Collection
#
# ******************************************************************************

from __future__ import print_function
import os
import sys


# Convert a C64 address into the corresponding offset within the gma6 file

def get_offset(addr):
    return addr - load_address


# Insert a binary file into the game code, overwriting what's there

def insert_binary_file(data_block, addr, filename):
    file = open(filename, "rb")
    file_size = os.path.getsize(filename)
    insert_from = get_offset(addr)
    insert_to = insert_from + file_size
    data_block[insert_from:insert_to] = file.read()
    file.close()
    print("[ Modify  ] insert file {} at 0x{:02X}".format(filename, addr))


# Insert an array of bytes into the game code, overwriting what's there

def insert_bytes(data_block, addr, insert):
    insert_from = get_offset(addr)
    insert_to = insert_from + len(insert)
    data_block[insert_from:insert_to] = insert
    print("[ Modify  ] insert {} bytes at 0x{:02X}".format(len(insert), addr))


# Insert a block of NOPs into the game code, overwriting what's there

def insert_nops(data_block, addr, count):
    insert = [0xEA] * count
    insert_bytes(data_block, addr, insert)
    print("[ Modify  ] insert {} NOPs at 0x{:02X}".format(count, addr))


# Fetch the platform (NTSC or PAL) from the command line arguments

if len(sys.argv) >= 2:
    platform = sys.argv[1]
else:
    platform = "pal"

# Print a progess message

print()
print("Modifying Commodore 64 Elite")
print("Platform: {}".format(platform.upper()))

# Configuration variables for gma6

load_address = 0x6A00 - 2
seed = 0x49
scramble_from = 0x6A00
scramble_to = 0x6A00 + 0x62D6

# Set up an array to hold the game binary, so we can modify it

data_block = bytearray()

# Load the main code file into data_block

elite_file = open("gma6", "rb")
data_block.extend(elite_file.read())
elite_file.close()

print()
print("[ Read    ] gma6")

# Decrypt the main code file

updated_seed = seed

for n in range(scramble_to, scramble_from - 1, -1):
    new = (data_block[n - load_address] - updated_seed) % 256
    data_block[n - load_address] = new
    updated_seed = new

print("[ Decrypt ] gma6")

# Write an output file containing the decrypted but unmodified game code, which
# we can use for debugging

output_file = open("gma6.decrypted", "wb")
output_file.write(data_block)
output_file.close()

print("[ Save    ] gma6.decrypted")

# Set the addresses for the extra routines (LSPUT, PATCH1, PATCH2) that we will
# append to the end of the main game code (where there is a bit of free space)

lsput = 0xCCE0
patch1 = 0xCD1E
patch2 = 0xCD35

# We now modify the code to implement flicker-free ship drawing. The code
# changes are described here, which can be read alongside the following:
#
# https://elite.bbcelite.com/deep_dives/backporting_the_flicker-free_algorithm.html
#
# The addresses in the following are from when the game binary is loaded into
# memory. They were calculated by analysing a memory dump of the running game,
# searching for patterns in the bytes to match them with the corrsponding code
# from the BBC Micro version (which is very similar, if you ignore any different
# addresses).

# SHPPT
#
# We start with the new version of SHPPT, which we have already assembled in
# BeebAsm and saved as the binary file shppt.bin, so we simply drop this over
# the top of the existing routine (which is slightly longer, so there is room).

insert_binary_file(data_block, 0x9932, "shppt.bin")

# LL9 (Part 1)
#
# This is the modification just after LL9. We insert the extra code with a call
# to the new PATCH1 routine, which implements the original instructions before
# moving on to the new code.
#
# From: LDA #31
#       STA XX4
#
# To:   JSR PATCH1
#       NOP

insert_bytes(data_block, 0x9A8A, [
    0x20, patch1 % 256, patch1 // 256   # JSR PATCH1
])
insert_nops(data_block, 0x9A8D, 1)

# LL9 (Part 9)
#
# This is the modification at EE31.
#
# From: LDA #%00001000
#       BIT XX1+31
#       BEQ LL74
#       JSR LL155
#
# To:   LDY #9
#       LDA (XX0),Y
#       STA XX20
#       NOP
#       NOP
#       NOP

insert_bytes(data_block, 0x9F2A, [
    0xA0, 0x09,                         # LDY #9
    0xB1, 0x57,                         # LDA (XX0),Y
    0x85, 0xAE                          # STA XX20
])
insert_nops(data_block, 0x9F30, 3)

# LL9 (Part 9)
#
# This is the modification just after LL74.
#
# From: LDY #9
#       LDA (XX0),Y
#       STA XX20
#       LDY #0
#       STY U
#       STY XX17
#       INC U
#
# To:   LDY #0
#       STY XX17
#       NOP x10

insert_bytes(data_block, 0x9F39, [
    0xA0, 0x00,                         # LDY #0
    0x84, 0x9F                          # STY XX17
])
insert_nops(data_block, 0x9F3D, 10)

# LL9 (Part 9)
#
# This is the modification at the end of the routine.
#
# From: LDA XX15
#       STA (XX19),Y
#       INY
#       LDA XX15+1
#       STA (XX19),Y
#       INY
#       LDA XX15+2
#       STA (XX19),Y
#       INY
#       LDA XX15+3
#       STA (XX19),Y
#       INY
#       STY U
#
# To:   JSR LSPUT
#       NOP x21

insert_bytes(data_block, 0x9F87, [
    0x20, lsput % 256, lsput // 256     # JSR LSPUT
])
insert_nops(data_block, 0x9F8A, 21)

# LL9 (Part 10)
#
# This is the modification around LL75.
#
# From: STA T1
#       LDY XX17
#
# To:   STA CNT
#       LDY #0

insert_bytes(data_block, 0x9FB4, [
    0x85, 0x30,                         # STA CNT
    0xA0, 0x00                          # LDY #0
])

# LL9 (Part 10)
#
# This is the second INY after LL75.
#
# From: INY
#
# To:   NOP

insert_nops(data_block, 0x9FC1, 1)

# LL9 (Part 10)
#
# These are the two modifications at LL79.
#
# From: LDA (V),Y
#       TAX
#       INY
#       LDA (V),Y
#       STA Q
#       ... four lots of unchanged LDA/STA, 5 bytes each ...
#       LDX Q
#
# To:   INY
#       LDA (V),Y
#       TAX
#       ... shuffle the LDA/STA block down by 4 bytes ...
#       INY
#       LDA (V),Y
#       TAX
#       NOP
#       NOP

insert_bytes(data_block, 0x9FD9, [
    0xC8,                               # INY
    0xB1, 0x5B,                         # LDA (V),Y
    0xAA                                # TAX
])

lda_sta_block = get_offset(0x9FDD)
for n in range(lda_sta_block, lda_sta_block + 4 * 5):
    data_block[n] = data_block[n + 4]

insert_bytes(data_block, 0x9FF1, [
    0xC8,                               # INY
    0xB1, 0x5B,                         # LDA (V),Y
    0xAA                                # TAX
])
insert_nops(data_block, 0x9FF5, 2)

# LL9 (Part 10)
#
# This is the modification at the end of the routine. The C64 version has an
# extra JMP LL80 instruction at this point that we can modify to jump to a
# new routine PATCH2, which lets us insert the extra JSR LSPUT without taking
# up any more bytes.
#
# From: JMP LL80
#
# To:   JMP PATCH2

insert_bytes(data_block, 0xA010, [
    0x4C, patch2 % 256, patch2 // 256   # JMP PATCH2
])

# LL9 (Part 11)
#
# This is the modification at LL80.
#
# We blank out the .LL80 section with 28 NOPs

insert_nops(data_block, 0xA13F, 28)

# LL9 (Part 11)
#
# We have already assembled the modified part 11 in BeebAsm and saved it as
# the binary file ll78.bin, so now we drop this over the top of the existing
# routine (which is exactly the same size).

insert_binary_file(data_block, 0xA15B, "ll78.bin")

# LL9 (Part 12)
#
# We have already assembled the modified part 11 in BeebAsm and saved it as
# the binary file ll115.bin, so now we drop this over the top of the existing
# routine (which is slightly longer, so there is room).

insert_binary_file(data_block, 0xA178, "ll155.bin")

# We now append the three extra routines required by the modifications to the
# end of the main binary (where there is enough free space for them):
#
#   LSPUT
#   PATCH1
#   PATCH2
#
# We have already assembled these in BeebAsm and saved them as the binary file
# extra.bin, so we simply append this file to the end.

elite_file = open("extra.bin", "rb")
data_block.extend(elite_file.read())
elite_file.close()

print("[ Modify  ] append file extra.bin")

# We now add the Universe Editor, which lives in the block of memory that's
# normally taken up by the title and docking music

# Set the addresses for the patch routines that we will inject into the main
# game code to call the Universe Editor

patch1 = 0xB72D
patch2 = 0xB738
patch3 = 0xB745

# The first step is to disable the music, which we can do easily by simply
# returning from the music routine at $920D, so that the music never gets
# played.

insert_bytes(data_block, 0x920D, [
    0x60                                # RTS
])

# BR1
#
# Next we patch the BR1 routine to detect the "0" key press to start the
# Universe Editor. We change the call to TITLE to jump to the PATCH1 routine,
# which implements the original instructions before checking for the Universe
# Editor key press.
#
# From: JSR TITLE
#
# To:   JSR PATCH1

insert_bytes(data_block, 0x8899, [
    0x20, patch1 % 256, patch1 // 256     # JSR PATCH1
])

# TITLE
#
# This is the modification to TITLE to display the Universe Editor subtitle.
#
# From: LDA #6
#       JSR DOXC
#       LDA PATG
#       BEQ awe
#       LDA #13
#       JSR DETOK
#
# To:   JSR PATCH2
#       NOP x12

insert_bytes(data_block, 0x8969, [
    0x20, patch2 % 256, patch2 // 256     # JSR PATCH2
])
insert_nops(data_block, 0x896C, 12)

# BEGIN
#
# Next, we patch the game entry point so the game defaults to disk rather than
# tape, which we can do by changing the option relevant byte from 0 to &FF.

# From: JSR JAMESON
#
# To:   JSR PATCH3

insert_bytes(data_block, 0x8879, [
    0x20, patch3 % 256, patch3 // 256     # JSR PATCH3
])

# UniverseEditor
#
# We have already assembled the Universe Editor in BeebAsm and saved it as
# the binary file editor.bin, so now we drop this over the top of the music
# data at $B72D.

insert_binary_file(data_block, 0xB72D, "editor.bin")

# All the modifications are done, so write the output file for gma6.modified,
# which we can use for debugging

output_file = open("gma6.modified", "wb")
output_file.write(data_block)
output_file.close()

print("[ Save    ] gma6.modified")

# Encrypt the main code file

for n in range(scramble_from, scramble_to):
    data_block[n - load_address] = (data_block[n - load_address] + data_block[n + 1 - load_address]) % 256

data_block[scramble_to - load_address] = (data_block[scramble_to - load_address] + seed) % 256

print("[ Encrypt ] gma6.modified")

# Write the output file for gma6.encrypted, which contains our modified game
# binary with the flicker-free code

output_file = open("gma6.encrypted", "wb")
output_file.write(data_block)
output_file.close()

print("[ Save    ] gma6.encrypted")

# Finally, we need to remove the disk protection from gma1, as described here:
# https://www.lemon64.com/forum/viewtopic.php?t=67762&start=90

data_block = bytearray()

elite_file = open("gma1", "rb")
data_block.extend(elite_file.read())
elite_file.close()

print()
print("[ Read    ] gma1")

if platform == "pal":
    # For elite[firebird_1986](pal)(v040486).g64
    data_block[0x25] = 0xEA
    data_block[0x26] = 0xEA
    data_block[0x27] = 0xEA
    data_block[0x2C] = 0xD0
else:
    # For elite[firebird_1986](ntsc)(v060186)(!).g64
    data_block[0x14] = 0xEA
    data_block[0x16] = 0xEA
    data_block[0x15] = 0xEA

print("[ Modify  ] gma1")

output_file = open("gma1.modified", "wb")
output_file.write(data_block)
output_file.close()

print("[ Save    ] gma1.modified")
print()
