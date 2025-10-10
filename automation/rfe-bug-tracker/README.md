# RFE Bug Tracker Automation - Group ID Integration

## Overview
Automated customer group ID discovery and integration for Red Hat Customer Portal API posting.

## Group ID Integration Status

### ✅ Discovered & Integrated
- **Wells Fargo**: 4357341 (CONFIRMED - Production Ready)
- **TD Bank**: 7028358 (EXTRACTED - Sandbox Ready)

### ❌ Manual Discovery Needed
- **JPMC**: Account #334224 - Group ID pending
- **Fannie Mae**: Account #1460290 - Group ID pending

## Key Files

### Source Files (`src/`)
- `automated_group_id_extractor.py` - Automated group ID discovery tool
- `rfe_discussion_api_client.py` - API client with integrated group IDs
- `weekly_discussion_poster.py` - Weekly troubleshooting reports
- `tam_call_notes_poster.py` - TAM call notes automation

### Configuration Files (`config/`)
- `weekly_troubleshooting_schedule.yaml` - Customer scheduling configuration
- `customer_group_ids_config.json` - Discovered group IDs (JSON)
- `customer_group_ids.py` - Python group ID configuration
- `customer_group_ids.yaml` - YAML group ID configuration

## Production Ready Systems
- ✅ Wells Fargo API posting (group 4357341)
- ✅ TD Bank sandbox testing (group 7028358)
- ✅ Weekly troubleshooting reports
- ✅ TAM call notes automation
- ✅ RFE/Bug tracker API integration

## Usage
See individual Python files for usage instructions and examples.

## Integration Status: 50% Complete
Ready for deployment: Wells Fargo, TD Bank
Pending: JPMC & Fannie Mae manual discovery
