
import sys
import re

# Hack Assembly tables

DEST = {
    "": "000", "M": "001", "D": "010",
    "MD": "011", "DM": "011",
    "A": "100", "AM": "101",
    "AD": "110", "AMD": "111"
}

JUMP = {
    "": "000", "JGT": "001", "JEQ": "010",
    "JGE": "011", "JLT": "100", "JNE": "101",
    "JLE": "110", "JMP": "111"
}

COMP = {
    "0": "0101010", "1": "0111111",
    "-1": "0111010", "D": "0001100",
    "A": "0110000", "!D": "0001101",
    "!A": "0110001", "-D": "0001111",
    "-A": "0110011", "D+1": "0011111",
    "A+1": "0110111", "D-1": "0001110",
    "A-1": "0110010", "D+A": "0000010",
    "D-A": "0010011", "A-D": "0000111",
    "D&A": "0000000", "D|A": "0010101",
    "M": "1110000", "!M": "1110001",
    "-M": "1110011", "M+1": "1110111",
    "M-1": "1110010", "D+M": "1000010",
    "D-M": "1010011", "M-D": "1000111",
    "D&M": "1000000", "D|M": "1010101"
}

PREDEFINED = {
    "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3,
    "THAT": 4, "SCREEN": 16384, "KBD": 24576
}

for i in range(16):
    PREDEFINED["R" + str(i)] = i


def clean_lines(lines):
    result = []

    for line_no, line in enumerate(lines, 1):
        line = line.split("//")[0].strip()

        if line:
            result.append((line_no, line))

    return result


def assemble(input_file, output_file):
    with open(input_file, "r") as file:
        lines = clean_lines(file.readlines())

    symbols = PREDEFINED.copy()
    instructions = []

    # First pass: Find labels
    rom_address = 0

    for line_no, line in lines:
        if line.startswith("(") and line.endswith(")"):
            label = line[1:-1].strip()

            if not label or not re.fullmatch(r"[A-Za-z_.$:][A-Za-z0-9_.$:]*", label):
                print(f"Line {line_no}: invalid label")
                return

            if label in symbols:
                print(f"Line {line_no}: duplicate or reserved label '{label}'")
                return

            symbols[label] = rom_address

        else:
            instructions.append((line_no, line))
            rom_address += 1

    # Second pass: Translate instructions
    binary_code = []
    next_variable = 16

    for line_no, line in instructions:
        try:
            if line.startswith("@"):
                value = line[1:].strip()

                if value.isdigit():
                    address = int(value)

                elif value in symbols:
                    address = symbols[value]

                elif re.fullmatch(r"[A-Za-z_.$:][A-Za-z0-9_.$:]*", value):
                    address = next_variable
                    symbols[value] = address
                    next_variable += 1

                else:
                    raise ValueError("invalid A-instruction")

                if not 0 <= address <= 32767:
                    raise ValueError("address out of range")

                binary_code.append(format(address, "016b"))

            else:
                dest = ""
                jump = ""

                if "=" in line:
                    dest, line = line.split("=", 1)

                if ";" in line:
                    comp, jump = line.split(";", 1)
                else:
                    comp = line

                dest = dest.strip()
                comp = comp.strip()
                jump = jump.strip()

                if dest not in DEST:
                    raise ValueError("invalid destination")

                if comp not in COMP:
                    raise ValueError("invalid computation")

                if jump not in JUMP:
                    raise ValueError("invalid jump")

                machine_code = "111" + COMP[comp] + DEST[dest] + JUMP[jump]
                binary_code.append(machine_code)

        except (ValueError, KeyError):
            print(f"Line {line_no}: invalid instruction")
            return

    with open(output_file, "w") as file:
        file.write("\n".join(binary_code) + "\n")

    print("Assembly successful!")
    print("Total instructions:", len(binary_code))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python assembler.py input.asm output.hack")
    else:
        assemble(sys.argv[1], sys.argv[2])
