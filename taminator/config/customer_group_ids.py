# Customer Group IDs for API-based Portal Posting
# Auto-generated from Automated Group ID Extraction

CUSTOMER_GROUP_IDS = {
    "wellsfargo": "4357341",  # Wells Fargo (confirmed)
    "tdbank": "7028358",  # TD Bank (extracted)
    "jpmc": "6956770",  # JP Morgan Chase (confirmed)
    "fanniemae": "7095107",  # Fannie Mae (confirmed)
}

# Confidence levels for validation
CUSTOMER_CONFIDENCE = {
    "wellsfargo": "confirmed",
    "tdbank": "extracted",
    "jpmc": "confirmed",
    "fanniemae": "confirmed",
}

def get_group_id(customer_key: str) -> str:
    """Get group ID for customer with validation"""
    if customer_key not in CUSTOMER_GROUP_IDS:
        raise ValueError(f"Unknown customer: {customer_key}")
    
    group_id = CUSTOMER_GROUP_IDS[customer_key]
    confidence = CUSTOMER_CONFIDENCE[customer_key]
    
    if confidence != "confirmed":
        print(f"⚠️  Warning: Group ID {group_id} for {customer_key} is {confidence}, not confirmed")
    
    return group_id
