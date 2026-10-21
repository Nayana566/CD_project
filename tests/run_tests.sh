#!/bin/sh
# Runs every test case. Valid tests must exit 0, invalid tests must exit non-zero.

BIN=./ifcompiler
[ -x "$BIN" ] || BIN=./ifcompiler.exe

pass=0
fail=0

for f in tests/valid/*.txt; do
    if $BIN "$f" > /dev/null 2>&1; then
        echo "[PASS] $f"; pass=$((pass + 1))
    else
        echo "[FAIL] $f (expected valid)"; fail=$((fail + 1))
    fi
done

for f in tests/invalid/*.txt; do
    if $BIN "$f" > /dev/null 2>&1; then
        echo "[FAIL] $f (expected error)"; fail=$((fail + 1))
    else
        echo "[PASS] $f"; pass=$((pass + 1))
    fi
done

echo ""
echo "Passed: $pass  Failed: $fail"
[ "$fail" -eq 0 ]
