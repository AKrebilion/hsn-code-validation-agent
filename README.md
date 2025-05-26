# 🧾 HSN Code Validation Agent

This project implements an intelligent agent that validates HSN (Harmonized System of Nomenclature) codes using a master dataset. It uses Python, Pandas, and Flask (for local execution), and is structured to conceptually align with Google's ADK (Agent Developer Kit) framework.

---

## 📌 Objective

To create a system that:
- Accepts a single or multiple HSN codes
- Validates the code format (2, 4, 6, or 8 digits)
- Checks for existence in the master dataset (HSN_SAC.xlsx)
- Returns description if valid, or appropriate error messages if invalid

---

## 🧠 Features

- 🔎 Format validation using regex
- 📂 Excel-based existence validation
- 💬 API-style design with Flask
- 🔁 Bulk code testing with `test_agent.py`
- 🔧 Ready to integrate into conversational agents (like ADK-based)

---

## 📁 Project Structure

```
hsn-code-validation-agent/
├── test_agent.py             # Script to run test validations
├── hsn_agent/
│   └── agent.py              # Encapsulated agent validation logic
│   └── HSN_SAC.xlsx          # Master dataset of HSN codes
├── Screenshots/              # Output screenshots (demo)
│   ├── valid_code_output.png
│   └── invalid_code_output.png
├── README.md                 # This file
└── requirements.txt          # Python dependencies
```

---

## 🚀 Getting Started

### 📦 Set up your environment

```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate    # On Windows

# Install required packages
pip install -r requirements.txt
```

---

### ▶️ Run Validation Script

To test the validation logic:

```bash
python test_agent.py
```

**Sample Output:**
```
Input: 0101 → Output: {'code': '0101', 'valid': True, 'description': 'LIVE HORSES, ASSES, MULES AND HINNIES.'}
Input: abcd → Output: {'code': 'abcd', 'valid': False, 'reason': 'Invalid format. Must be 2–8 digits.'}
```

---

## 🔮 Future Enhancements

- Hierarchical code validation (parent-child relationships)
- Interactive CLI or web interface
- Real-time dataset updates via API or database

---


