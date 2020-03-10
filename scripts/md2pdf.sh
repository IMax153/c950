#!/bin/bash

pandoc "../README.md" \
    -V linkcolor:blue \
    -V geometry:a4paper \
    -V geometry:margin=2cm \
    --include-in-header chapter_break.tex \
    --include-in-header inline_code.tex \
    -V mainfont="Source Sans Pro" \
    -V monofont="Source Code Pro" \
    --pdf-engine=xelatex \
    -o "../dsa_brown.pdf"