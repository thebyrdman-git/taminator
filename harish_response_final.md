Hi Harish,

**Answer: Work on batches of servers to avoid full outage - DO NOT restart all at once.**

## **Staged Approach for Tomorrow's UAT Patching (9/30)**

### **Phase 1: Execution Environments (Batches)**
- Process EEs in **25-50% batches** (not all at once)
- **Procedure per batch**:
  ```bash
  systemctl stop receptor
  rm -rf /tmp/receptor
  systemctl start receptor
  receptor status  # verify connectivity
  ```
- **Downtime**: 2-3 minutes per EE, but job capacity maintained

### **Phase 2: Controllers (Sequential Only)** 
- Process controllers **ONE AT A TIME** (never simultaneously)
- Same procedure as EEs
- **Critical**: Always keep at least one controller active

### **Verification After Each Batch**
```bash
# Check mesh health
receptor status

# Verify no stuck work units (per KCS 7035560)
receptorctl --socket /var/run/awx-receptor/receptor.sock work list

# Check for errors
grep -i "error locating unit\|already connected to" /var/log/receptor/receptor.log
```

### **Timeline**
- **EE Batches**: 30-45 minutes total
- **Controllers**: 30-45 minutes (sequential processing)
- **Total Impact**: ~90 minutes with minimal service disruption

### **Risk Mitigation**
✅ **Low risk** - maintains partial capacity throughout  
✅ **Quick rollback** - receptor restarts are fast  
✅ **Proven procedure** - established KCS 7035560 solution

I'll be available during your maintenance window for real-time support.

Best regards,  
Jimmy
