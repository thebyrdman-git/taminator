# External Tracker Detection Guide

## 🎯 **How External Tracker Detection Should Work**

### **Current Problem**
The current system searches for external tracker patterns in case descriptions, but you're right - it should look for a specific **"External Trackers"** section in the case data.

### **Correct Approach: Customer Portal API**

#### **1. API Endpoint**
```
GET /v1/cases/{caseNumber}/externaltrackerupdates
```

#### **2. Expected Response Structure**
```json
{
  "external_tracker_updates": [
    {
      "tracker_type": "JIRA",
      "tracker_id": "AAP-3456",
      "url": "https://issues.redhat.com/browse/AAP-3456",
      "status": "In Progress",
      "last_updated": "2024-10-11T00:00:00Z"
    }
  ],
  "bugzillas": [],
  "resource_links": [],
  "kcs_solutions": []
}
```

#### **3. Detection Logic**
```python
def has_external_trackers(case_number):
    """Check if case has external trackers using Customer Portal API"""
    
    # Call Customer Portal API
    response = requests.get(
        f"https://api.access.redhat.com/support/v1/cases/{case_number}/externaltrackerupdates",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    data = response.json()
    
    # Check if external_tracker_updates has entries
    return len(data.get('external_tracker_updates', [])) > 0
```

### **4. Integration with RFE Reports**

#### **Filtering Logic**
```yaml
- name: Detect cases with external trackers
  redhat.rfe_automation.external_tracker_detector:
    cases: "{{ all_cases }}"
  register: external_tracker_results

- name: Filter cases without external trackers
  set_fact:
    cases_without_external_trackers: "{{ external_tracker_results.cases_without_external_trackers }}"
    cases_with_external_trackers: "{{ external_tracker_results.cases_with_external_trackers }}"
```

#### **Report Generation**
- **RFE/Bug Report**: Include all RFE/Bug cases (regardless of external trackers)
- **Active Cases Report**: Exclude cases that have external trackers
- **External Tracker Summary**: Show cases with external trackers and their details

### **5. Benefits of This Approach**

#### **✅ Accurate Detection**
- Uses official Customer Portal API
- Accesses structured "External Trackers" section
- No false positives from description text

#### **✅ Complete Information**
- Gets actual JIRA ticket IDs
- Shows tracker status and URLs
- Provides last updated timestamps

#### **✅ Proper Filtering**
- Excludes cases with external trackers from Active Cases Report
- Prevents duplication with JIRA tracking
- Maintains accurate case counts

### **6. Implementation Status**

#### **✅ What's Ready**
- Customer Portal API client exists
- External tracker detection module created
- Report templates updated
- Integration playbook created

#### **⚠️ What Needs Testing**
- API authentication and access
- External tracker data structure
- Integration with existing workflow

### **7. Next Steps**

1. **Test API Access**: Verify Customer Portal API access for external trackers
2. **Validate Data Structure**: Confirm the actual response format
3. **Update Detection Logic**: Modify the detection to use the API
4. **Test Integration**: Run the complete workflow with real data

### **8. Example Usage**

```bash
# Generate reports with proper external tracker detection
ansible-playbook generate_reports_with_external_trackers.yml -e "customer=jpmc" -e @vars/accounts.yml

# This will:
# 1. Get all cases from rhcase
# 2. Check each case for external trackers using Customer Portal API
# 3. Generate reports excluding cases with external trackers
# 4. Create an external tracker summary report
```

## 🎯 **The Bottom Line**

**You're absolutely right** - the system should use the Customer Portal API to check the **"External Trackers"** section of each case, not search through description text. This provides:

- **Accurate detection** of cases tracked in JIRA
- **Complete information** about external trackers
- **Proper filtering** to avoid duplication
- **Professional reports** with correct case counts

**The infrastructure is ready - we just need to test the API access and validate the data structure!** 🚀
