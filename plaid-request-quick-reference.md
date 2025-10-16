# Plaid API Access Request - Quick Reference

**30-Second Pitch:**
> "I'm building a self-hosted personal finance automation system using Actual Budget and AI-powered analysis tools. I need Plaid to replace manual bank transaction entry (currently 5 hours/month) with automated sync. Personal development project, no commercial intent, all data stays local."

---

## Request Form Answers

### Account Type
**Personal Development**

### Company Name
Personal Project / N/A

### Project Name
PAI Personal Finance System

### Project Description (250 chars)
```
Self-hosted finance automation combining Actual Budget + AI tools.
Plaid will automate transaction sync from banks to my local server.
Personal use only. Learning project. ~10 accounts, ~500 trans/month.
```

### Use Case
**Personal Financial Management**

### Products Needed
- ✅ Transactions
- ✅ Auth  
- ✅ Balance
- ⬜ Investments (future)

### Expected Volume
- **Users:** 1
- **Institutions:** 3-5
- **Transactions/month:** ~500
- **API calls/day:** ~100

### Timeline
- **Sandbox:** 2-4 weeks
- **Production:** After testing complete

---

## Key Points If Asked

### "What are you building?"
Personal finance automation. Self-hosted Actual Budget with AI-powered analysis. Plaid automates bank sync.

### "Why do you need Plaid?"
Replace manual CSV downloads (5 hrs/month). Need real-time transaction data for AI analysis and debt tracking.

### "Commercial plans?"
None. Personal project only. Learning experience. Managing my own $27K debt payoff.

### "Data security?"
All local. Self-hosted server. Encrypted tokens. Read-only access. Following Plaid best practices.

### "When do you need production access?"
2-4 weeks for Sandbox testing, then production. No rush - want to test thoroughly first.

---

## Current Infrastructure

**What I have:**
- Actual Budget server (self-hosted on miraclemax)
- 25+ PAI finance tools (bash/node.js)
- Finance dashboard with net worth tracking
- Bill payment monitoring system
- AI spending analysis tools

**What I'm adding:**
- Plaid integration layer (8 new tools)
- Automated transaction sync
- Real-time balance updates
- Webhook handling for notifications

**Where data lives:**
- All local: `~/.config/pai/actual-budget/cache/`
- Self-hosted: `miraclemax:5006`
- No cloud services

---

## Technical Details (If Needed)

### Stack
- Node.js (Plaid SDK)
- Actual Budget (open source)
- Bash automation scripts
- Local PostgreSQL/SQLite

### Architecture
```
Banks → Plaid API → Local Connector → Actual Budget → PAI Analysis
```

### Security
- GPG-encrypted token storage
- Local network only
- TLS 1.2+
- Webhook signature verification
- No third-party data sharing

### API Usage Pattern
- Daily transaction sync (morning cron)
- Balance checks (2-3x/day)
- Webhooks for updates
- No polling (webhook-driven)

---

## Success Metrics

**Time savings:** 5 hours/month → 20 minutes/month  
**Data quality:** 100% transaction capture vs. manual gaps  
**Debt tracking:** Real-time progress on $27K → $0 payoff  
**Analysis:** Better AI insights with complete transaction data

---

## Alternative: Demo with SimpleFIN First

**RECOMMENDED:** Build working demo with SimpleFIN before requesting Plaid

### Why SimpleFIN First?
- ✅ No approval needed - start today
- ✅ Works with Capital One (your accounts)
- ✅ $3/month for checking + savings
- ✅ Proves your concept works
- ✅ **Strengthens Plaid request**

### Quick Demo Path
```bash
# 1. Sign up: https://beta-bridge.simplefin.org/simplefin/signup
# 2. Connect Capital One checking + savings
# 3. Build integration (2-3 hours)
cd ~/pai/repositories/pai-personal-finance/simplefin
npm install
# See QUICK-START.md

# 4. Use for Plaid request:
# "I built this with SimpleFIN, now want to expand with Plaid"
```

**This approach:**
- Shows working code
- Proves technical capability  
- Demonstrates real value
- Makes Plaid request much stronger

---

## Follow-Up Items

### Option A: SimpleFIN First (Recommended)
1. [ ] Sign up for SimpleFIN (today)
2. [ ] Connect Capital One accounts
3. [ ] Build custom PAI tools (this week)
4. [ ] Document working system
5. [ ] Use demo in Plaid request (next week)

### Option B: Plaid Only
After Plaid approval:
1. [ ] Set up Plaid dashboard account
2. [ ] Get API credentials (client_id, secret)
3. [ ] Install Node SDK: `npm install plaid`
4. [ ] Test Sandbox connection
5. [ ] Build `pai-plaid-setup` tool
6. [ ] Create Plaid Link integration
7. [ ] Test with sandbox institutions
8. [ ] Deploy to production after 2-4 weeks

---

## Links to Share (If Asked)

**GitHub:** (if you have public repos showing PAI infrastructure)  
**Actual Budget:** https://actualbudget.org (the tool you're enhancing)  
**Documentation:** `/home/jbyrd/pai/plaid-api-request-prep.md` (full detail)

---

## Contact Info

**Name:** [Your Name]  
**Email:** [Your Email]  
**Purpose:** Personal Development  
**Expected Start:** Immediately (Sandbox)  
**Production Date:** 2-4 weeks

---

*Keep this page open during request submission for quick reference*

