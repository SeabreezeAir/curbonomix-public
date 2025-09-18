VALID_KEYS = {"CURB-ALPHA-001", "CURB-BETA-002", "CURB-TRIAL-003"}

def is_valid_license(key):
    return key in VALID_KEYS
