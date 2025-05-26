import pandas as pd
from google.adk.agents import Agent


# Load Excel once, when the agent starts
try:
    df = pd.read_excel("HSN_SAC.xlsx", engine="openpyxl")
    # df = pd.read_excel("D:\from ssd\Downloads\settyl\settyl\HSN_SAC.xlsx", engine="openpyxl")
    print("opened excel")
    df["HSNCode"] = df["HSNCode"].astype(str).str.strip()
    hsn_lookup = dict(zip(df["HSNCode"], df["Description"]))
except Exception as e:
    hsn_lookup = {}
    print(f"Error loading Excel file: {e}")

def validate_hsn(hsn_code: str) -> dict:
    code = hsn_code.strip()
    print(f"the lookup is {hsn_lookup}")

    if not code.isdigit() or not (2 <= len(code) <= 8):
        return {"status": "error", "message": f"{code} is not a valid HSN code format (2–8 digits)."}

    description = hsn_lookup.get(code)
    if description:
        return {"status": "success", "description": description}
    else:
        return {"status": "error", "message": f"{code} not found in HSN master data."}
    

def get_parent_hsn_codes(hsn_code: str) -> list:
    """
    Returns a list of parent HSN codes for a given HSN code.
    E.g., for '01012003' -> ['010120', '0101', '01']
    """
    code = hsn_code.strip()
    parents = []
    # Only consider even-length parent codes >= 2 digits
    for i in range(len(code) - 2, 1, -2):
        parents.append(code[:i])
    if len(code) > 2:
        parents.append(code[:2])  # Always include the 2-digit parent
    return list(dict.fromkeys(parents))  # Remove duplicates, preserve order

def validate_hsn_with_parents(hsn_code: str) -> dict:
    code = hsn_code.strip()
    if not code.isdigit() or not (2 <= len(code) <= 8):
        return {"status": "error", "message": f"{code} is not a valid HSN code format (2–8 digits)."}

    result = {}
    description = hsn_lookup.get(code)
    result["input_code"] = code
    result["input_description"] = description if description else None

    # Get parent codes and their descriptions
    parents = get_parent_hsn_codes(code)
    parent_matches = []
    for parent in parents:
        desc = hsn_lookup.get(parent)
        if desc:
            parent_matches.append({"code": parent, "description": desc})

    result["parent_matches"] = parent_matches
    if description or parent_matches:
        result["status"] = "success"
    else:
        result["status"] = "error"
        result["message"] = f"{code} and its parents not found in HSN master data."
    return result

root_agent = Agent(
    name="hsn_validator",
    model="gemini-1.5-flash",
    description="Agent that validates HSN codes using data from Excel",
    instruction="You are a helpful assistant that checks if HSN codes are valid using HSN master data.",
    tools=[validate_hsn, validate_hsn_with_parents],
)