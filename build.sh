#!/usr/bin/env bash

# Set up program locations (change these if they are not aleady in the path)
beebasm="beebasm"
c1541="c1541"
python="python"

# Create empty work folders
rm -fr work
mkdir work
mkdir work/ntsc
mkdir work/pal

# Get the current date for the build filename
CURRENTDATE=`date +%Y-%m-%d`

# First, we build the NTSC version
cd work/ntsc

# Create an empty file for the build number
touch empty.txt

# Create the readme file for flicker-free ships
$beebasm -i ../../src/elite-flicker-free-readme.asm

# Extract the files from the original disk image
$c1541 -attach "../../original-disks/elite[firebird_1986](ntsc)(v060186)(!).g64" \
       -extract

# Assemble the additional code required for flicker-free ships
$beebasm -i ../../src/elite-flicker-free.asm -v > compile.txt

# Assemble the additional code required for the Universe Editor
$beebasm -i ../../src/elite-universe-editor-c64.asm -v > compile.txt

# Modify the main game code
$python ../../src/elite-modify.py ntsc

# Rebuild the game disk
$c1541 \
    -format "elite uni editor,1" \
            d64 \
            ../../universe-editor-disks/c64-elite-universe-editor-ntsc.d64 \
    -attach ../../universe-editor-disks/c64-elite-universe-editor-ntsc.d64 \
    -write firebird \
    -write gma1.modified gma1 \
    -write gma3 \
    -write gma4 \
    -write gma5 \
    -write gma6.encrypted gma6 \
    -write ../../elite-universe-editor-library/universe-files/u.boxart1.bin "boxart1" \
    -write ../../elite-universe-editor-library/universe-files/u.boxart2.bin "boxart2" \
    -write ../../elite-universe-editor-library/universe-files/u.boxartc.bin "boxartc" \
    -write ../../elite-universe-editor-library/universe-files/u.manual.bin "manual" \
    -write ../../elite-universe-editor-library/universe-files/u.shipid.bin "shipid"

# Report checksums
cd ../..
$python src/crc32.py reference-binaries/ntsc work/ntsc

# Next, we build the PAL version
cd work/pal

# Extract the files from the original disk image
$c1541 -attach "../../original-disks/elite[firebird_1986](pal)(v040486).g64" \
       -extract

# Assemble the additional code required for flicker-free ships
$beebasm -i ../../src/elite-flicker-free.asm -v >> compile.txt

# Assemble the additional code required for the Universe Editor
$beebasm -i ../../src/elite-universe-editor-c64.asm -v > compile.txt

# Modify the main game code
$python ../../src/elite-modify.py pal

# Rebuild the game disk
$c1541 \
    -format "elite uni editor,1" \
            d64 \
            ../../universe-editor-disks/c64-elite-universe-editor-pal.d64 \
    -attach ../../universe-editor-disks/c64-elite-universe-editor-pal.d64 \
    -write firebird \
    -write byebyejulie \
    -write gma1.modified gma1 \
    -write gma3 \
    -write gma4 \
    -write gma5 \
    -write gma6.encrypted gma6 \
    -write ../../elite-universe-editor-library/universe-files/u.boxart1.bin "boxart1" \
    -write ../../elite-universe-editor-library/universe-files/u.boxart2.bin "boxart2" \
    -write ../../elite-universe-editor-library/universe-files/u.boxartc.bin "boxartc" \
    -write ../../elite-universe-editor-library/universe-files/u.manual.bin "manual" \
    -write ../../elite-universe-editor-library/universe-files/u.shipid.bin "shipid"

# Report checksums
cd ../..
$python src/crc32.py reference-binaries/pal work/pal
