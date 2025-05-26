from flask import Flask, request, jsonify
import pandas as pd
import re

app = Flask(__name__)

# Load the HSN data at startup
df = pd.read_excel("HSN_SAC.xlsx", engine='openpyxl')
df.columns = df.columns.str.strip()  # removes extra spaces

# Debug print to confirm column names
print("Column names:", df.columns.tolist())

hsn_set = set(df['HSNCode'].astype(str))

hsn_set = set(df['HSNCode'].astype(str))

def validate_hsn_code(hsn_code):
    code = str(hsn_code).strip()
    
    if not re.fullmatch(r'\d{2,8}', code):
        return {"code": code, "valid": False, "reason": "Invalid format. Must be numeric and 2–8 digits."}

    result = {"code": code}
    
    if code in hsn_set:
        description = df[df['HSNCode'].astype(str) == code]['Description'].values[0]
        result.update({"valid": True, "description": description})
        
        # Optional: Check hierarchy
        hierarchy = []
        for i in [2, 4, 6]:
            parent = code[:i]
            if parent != code and parent not in hsn_set:
                hierarchy.append(parent)
        if hierarchy:
            result["hierarchy_warning"] = f"Missing parent levels: {', '.join(hierarchy)}"
    else:
        result.update({"valid": False, "reason": "Code not found in master data."})
    
    return result

@app.route('/validate', methods=['POST'])
def validate():
    data = request.json
    codes = data.get('hsn_codes', [])
    
    results = [validate_hsn_code(code) for code in codes]
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
