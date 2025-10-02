# 🛠️ Video #2: TAM Onboarding Process
## Setup Walkthrough Script (15 minutes)

### 🎯 **Video Overview**
**Title**: "TAM Onboarding: From Zero to Automation in 15 Minutes"  
**Duration**: 15 minutes  
**Audience**: TAMs ready to implement the system  
**Goal**: Complete step-by-step onboarding demonstration  

---

## 🎬 **SCRIPT & STORYBOARD**

### **INTRODUCTION (0:00 - 1:00)**
**[VISUAL: Professional TAM workspace setup]**

**NARRATOR**: 
> "Welcome to the TAM RFE Automation onboarding walkthrough. I'm going to show you exactly how to go from zero to full automation in just 15 minutes."

**[VISUAL: Timer showing 15:00 countdown]**

> "By the end of this video, you'll have a complete RFE automation system running for your first customer, saving you 2-3 hours daily."

**[VISUAL: Split screen showing current manual process vs automated result]**

> "Let's get started with a real customer setup - Wells Fargo."

---

### **PREREQUISITES CHECK (1:00 - 3:00)**
**[VISUAL: Terminal window, clean desktop]**

**NARRATOR**:
> "First, let's verify our prerequisites. Don't worry - the system checks everything for you."

**[VISUAL: Typing `pai-tam-onboard`]**

> "The onboarding wizard starts with a comprehensive prerequisites check."

**[VISUAL: Prerequisites validation screen]**

**1:30 - System Requirements**
> "It validates Python 3.8+, rhcase availability, git, and disk space."
**[VISUAL: Green checkmarks appearing for each requirement]**

**2:00 - Authentication**  
> "Next, it checks your Red Hat SSO and rhcase authentication."
**[VISUAL: rhcase config verification]**

**2:30 - Network Connectivity**
> "Finally, it confirms network access to Red Hat systems."
**[VISUAL: Connectivity test results]**

> "All green! We're ready to proceed."

---

### **CUSTOMER INFORMATION COLLECTION (3:00 - 6:00)**
**[VISUAL: Interactive wizard interface]**

**NARRATOR**:
> "Now the wizard guides you through customer information collection."

**3:15 - Customer Name**
**[VISUAL: Typing "Wells Fargo"]**
> "Enter your customer name - this will be used throughout the system."

**3:30 - Customer Key**
**[VISUAL: Auto-suggested "wellsfargo"]**
> "The system suggests a customer key for internal use. You can customize this."

**3:45 - Account Numbers**
**[VISUAL: Entering "838043"]**
> "Enter the customer's account numbers. You can find these in Salesforce or ask your customer."

**4:15 - Portal Group URL**
**[VISUAL: Pasting portal URL]**
> "Paste the customer's Red Hat portal group URL. This is where updates will be posted."

**4:30 - Group ID Extraction**
**[VISUAL: Automatic group ID extraction: 4357341]**
> "The system automatically extracts the group ID from the URL. Smart!"

**5:00 - Information Summary**
**[VISUAL: Summary screen showing all collected information]**
> "Review your customer information. Everything looks correct for Wells Fargo."

**5:30 - Validation**
> "The wizard validates all information before proceeding."

---

### **CONNECTIVITY TESTING (6:00 - 8:00)**
**[VISUAL: Testing interface with progress indicators]**

**NARRATOR**:
> "Next, the system tests connectivity to ensure everything will work in production."

**6:15 - rhcase Testing**
**[VISUAL: rhcase command execution]**
> "It tests rhcase connectivity using your customer's account number."
**[VISUAL: Success message showing cases found]**

**6:45 - Portal Access**
**[VISUAL: Browser opening to portal URL]**
> "It verifies you can access the customer portal group."

**7:15 - Case Discovery**
**[VISUAL: Live case discovery results]**
> "Look at this - it found 23 RFE cases and 8 Bug cases for Wells Fargo automatically!"

**7:45 - Success Confirmation**
> "All connectivity tests passed. We're ready for configuration."

---

### **TEMPLATE CONFIGURATION (8:00 - 10:00)**
**[VISUAL: Template selection interface]**

**NARRATOR**:
> "Now let's configure the portal templates for professional customer communication."

**8:15 - Template Style Selection**
**[VISUAL: Three template options displayed]**
> "Choose from Enterprise, Standard, or Minimal templates. We'll select Standard for Wells Fargo."

**8:45 - Priority Management**
**[VISUAL: Priority management toggle]**
> "Decide whether to include priority management. This is optional but powerful for strategic customers."

**9:15 - Footer Customization**
**[VISUAL: Footer message editor]**
> "Customize the footer message that appears on portal pages. This ensures customers know who to contact."

**9:45 - Template Preview**
**[VISUAL: Live template preview]**
> "Here's a preview of how your customer portal will look. Professional and consistent!"

---

### **SYSTEM TESTING (10:00 - 12:00)**
**[VISUAL: Automated testing interface]**

**NARRATOR**:
> "Before going live, the system runs comprehensive tests to ensure everything works perfectly."

**10:15 - Configuration Validation**
**[VISUAL: Configuration files being created and validated]**
> "It creates and validates all configuration files."

**10:30 - Case Discovery Test**
**[VISUAL: Live case discovery with real data]**
> "Tests case discovery with your actual customer data."

**10:45 - Template Rendering**
**[VISUAL: Portal content being generated]**
> "Generates sample portal content to verify templates work correctly."

**11:15 - Safety Checks**
**[VISUAL: Safety mechanism validation]**
> "Validates all safety mechanisms to prevent accidental customer emails."

**11:45 - Success Report**
**[VISUAL: Comprehensive test results]**
> "All tests passed! Your automation system is ready for production."

---

### **AUTOMATION SETUP (12:00 - 13:30)**
**[VISUAL: Scheduling interface]**

**NARRATOR**:
> "Finally, let's set up automated scheduling so this runs without you thinking about it."

**12:15 - Daily Automation**
**[VISUAL: Cron job configuration]**
> "Enable daily automation to run every morning at 9 AM EST."

**12:30 - Monitoring Setup**
**[VISUAL: Monitoring configuration]**
> "Configure monitoring and alerting so you know if anything needs attention."

**12:45 - Quick Commands**
**[VISUAL: Command generation]**
> "The system creates customer-specific commands for easy access."

**13:00 - Command Demonstration**
**[VISUAL: Running `pai-rfe-wellsfargo`]**
> "Try your new command - `pai-rfe-wellsfargo`. Watch it work!"

**13:15 - Success!**
**[VISUAL: Successful automation run]**
> "Perfect! Your first automated RFE update is complete."

---

### **COMPLETION & NEXT STEPS (13:30 - 15:00)**
**[VISUAL: Completion summary screen]**

**NARRATOR**:
> "Congratulations! You've successfully set up RFE automation for Wells Fargo."

**13:45 - What You've Accomplished**
**[VISUAL: Checklist of completed items]**
- ✅ Customer configured and validated
- ✅ Connectivity tested and confirmed  
- ✅ Templates customized and ready
- ✅ Automation scheduled and active
- ✅ Monitoring and alerting enabled

**14:15 - Available Commands**
**[VISUAL: Command reference card]**
> "You now have these powerful commands available:"
- `pai-rfe-wellsfargo` - Run full automation
- `pai-test-wellsfargo` - Test automation safely
- `pai-alerts --summary` - View system health

**14:30 - Expected Benefits**
**[VISUAL: Benefits visualization]**
> "Starting tomorrow, you'll save 2-3 hours daily on Wells Fargo RFE management."

**14:45 - Next Steps**
> "Add more customers by running `pai-tam-onboard` again. Set up AI development with `pai-cursor-setup`. Practice safely with `pai-sandbox`."

> "Welcome to the future of TAM productivity!"

---

## 🎯 **PRODUCTION NOTES**

### **Visual Requirements**
- **Live screen recording**: Actual onboarding process
- **Picture-in-picture**: Narrator in corner during key moments
- **Callout annotations**: Highlight important UI elements
- **Progress indicators**: Show completion status throughout

### **Interactive Elements**
- **Pause points**: Allow viewers to follow along
- **Chapter markers**: Easy navigation to specific sections
- **Downloadable resources**: Configuration templates, checklists

### **Technical Specifications**
- **Resolution**: 1920x1080 (Full HD)
- **Screen capture**: High-quality system demonstration
- **Audio**: Clear narration with minimal background music
- **Captions**: Full accessibility support

### **Key Learning Objectives**
1. **Confidence**: TAMs feel confident they can do this themselves
2. **Completeness**: Every step is clearly demonstrated
3. **Troubleshooting**: Common issues and solutions shown
4. **Success**: Clear validation that setup worked correctly

### **Success Metrics**
- **Completion Rate**: 85%+ watch entire video
- **Implementation Rate**: 70%+ successfully complete onboarding
- **Support Requests**: <10% need additional help
- **Satisfaction**: 4.7+ stars average rating

---

## 🎬 **CHAPTER BREAKDOWN**

| Chapter | Time | Topic | Key Takeaway |
|---------|------|-------|--------------|
| 1 | 0:00-1:00 | Introduction | 15 minutes to full automation |
| 2 | 1:00-3:00 | Prerequisites | System validates everything |
| 3 | 3:00-6:00 | Customer Info | Guided information collection |
| 4 | 6:00-8:00 | Connectivity | Real-world validation testing |
| 5 | 8:00-10:00 | Templates | Professional customization |
| 6 | 10:00-12:00 | Testing | Comprehensive validation |
| 7 | 12:00-13:30 | Automation | Set-and-forget scheduling |
| 8 | 13:30-15:00 | Success | Ready for daily productivity |

---

**This walkthrough will be the definitive guide for TAM onboarding!**

*Video Script v1.0 - TAM RFE Automation Training*  
*For production support: rfe-automation-support@redhat.com*
