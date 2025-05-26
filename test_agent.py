from hsn_agent.agent import validate_hsn

# Try different codes
codes = ["0101", "01", "9999", "abcd"]

for code in codes:
    result = validate_hsn(code)
    print(f"Input: {code} → Output: {result}")
