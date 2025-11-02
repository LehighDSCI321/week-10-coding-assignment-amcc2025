import subprocess
import re

# Test 3: Check for unhandled pylint style recommendations
def test_pylint_style():
    result = subprocess.run(['pylint', 'student_code.py'], capture_output=True, text=True)
    assert "C0" not in result.stdout, "Pylint style recommendations found"