# Cell 21 from UBP_UNIFIED_SYSTEM_1.ipynb

# @title
golay_spring = GolaySpringMechanism()
leech_lattice = LeechLattice()

blood_types = ["O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-"]

print("\n--- Analyzing DataEncoder.blood_type_to_ubp function ---")
print("--------------------------------------------------------\n")

results = {}

for bt in blood_types:
    print(f"Processing blood type: {bt}")
    try:
        # 4a. Use DataEncoder.blood_type_to_ubp to generate the 24-bit representation
        ubp_bits = DataEncoder.blood_type_to_ubp(bt)
        bit_str = ''.join(str(b) for b in ubp_bits)

        # 4b. Print the blood type and its generated 24-bit string
        print(f"  Generated UBP bits: {bit_str}")

        # 4c. Golay Codeword Check
        # A valid codeword should be decoded with 0 errors corrected.
        # The decode function returns (decoded_message, num_errors_corrected, success)
        # For an *already valid codeword*, num_errors_corrected should be 0.
        # We only care if the *input* was a valid codeword, not about error correction here.
        # To check if it's a valid codeword, we encode its implied message and compare.

        # The current DataEncoder fills bits[3:] based on sum(bits[:3])
        # It does NOT use golay_spring.encode() for the full 24 bits.
        # Therefore, we must encode its first 12 bits to see if it matches.
        # If the generated 24 bits are an actual codeword, its first 12 bits should be its message.
        # Let's decode to get the message and then re-encode it.

        # Use a dummy message [0]*12 for decoding. We're interested in num_errors and success.
        # A better way to check if `ubp_bits` is a codeword is to compute its syndrome. If 0, it's a codeword.
        syndrome_for_check = golay_spring.compute_syndrome(ubp_bits)
        is_golay_codeword = all(s == 0 for s in syndrome_for_check)

        if is_golay_codeword:
            print(f"  Golay Codeword Check: PASSED (Syndrome is all zeros)")
            golay_status = "Valid Golay Codeword"
        else:
            print(f"  Golay Codeword Check: FAILED (Syndrome: {syndrome_for_check} - not all zeros)")
            golay_status = "NOT a valid Golay Codeword"

        # 4d. Leech Lattice Coherence Check
        try:
            state = UBPGeometricState(ubp_bits, leech_lattice)
            print(f"  Leech Coherence Check: PASSED (State is coherent)")
            leech_status = "Coherent Leech Point"
        except ValueError as e:
            print(f"  Leech Coherence Check: FAILED ({e})")
            leech_status = f"NOT Coherent Leech Point ({e})"

        results[bt] = {
            "ubp_bits": bit_str,
            "golay_status": golay_status,
            "leech_status": leech_status
        }

    except ValueError as e:
        print(f"  An error occurred during encoding or validation: {e}")
        results[bt] = {
            "ubp_bits": "Error",
            "golay_status": "Error",
            "leech_status": f"Error ({e})"
        }
    print("--------------------------------------------------------")

print("\n--- Summary of Findings ---")
for bt, res in results.items():
    print(f"Blood Type: {bt}")
    print(f"  UBP Bits: {res['ubp_bits']}")
    print(f"  Golay Status: {res['golay_status']}")
    print(f"  Leech Status: {res['leech_status']}")
    print()
