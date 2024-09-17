#!/bin/bash

# Variables
SCHEDULER_SCRIPT="scheduler-gpt.py"
INPUT_FILES=("c2-fcfs.in" "c2-sjf.in" "c2-rr.in" "c5-fcfs.in" "c5-sjf.in" "c5-rr.in" "c10-fcfs.in" "c10-sjf.in" "c10-rr.in")
EXP_OUTPUT_FILES=("exp-c2-fcfs.out" "exp-c2-sjf.out" "exp-c2-rr.out" "exp-c5-fcfs.out" "exp-c5-sjf.out" "exp-c5-rr.out" "exp-c10-fcfs.out" "exp-c10-sjf.out" "exp-c10-rr.out")
OUTPUT_FILES=("c2-fcfs.out" "c2-sjf.out" "c2-rr.out" "c5-fcfs.out" "c5-sjf.out" "c5-rr.out" "c10-fcfs.out" "c10-sjf.out" "c10-rr.out")

for i in "${!INPUT_FILES[@]}"; do
    INPUT_FILE=${INPUT_FILES[$i]}
    EXP_OUTPUT_FILE=${EXP_OUTPUT_FILES[$i]}
    OUTPUT_FILE=${OUTPUT_FILES[$i]}

    python3 "$SCHEDULER_SCRIPT" "$INPUT_FILE"

    # Check if the generated output matches the expected output
    if diff "$OUTPUT_FILE" "$EXP_OUTPUT_FILE" > /dev/null; then
        echo "Test $i Passed for $INPUT_FILE: Output matches expected output."
    else
        echo "Test $i Failed for $INPUT_FILE: Output does not match expected output."
        diff "$OUTPUT_FILE" "$EXP_OUTPUT_FILE"
    fi

    echo "-----------------------------"
done

for OUTPUT_FILE in "${OUTPUT_FILES[@]}"; do
    if [ -f "$OUTPUT_FILE" ]; then
        rm "$OUTPUT_FILE"
    fi
done