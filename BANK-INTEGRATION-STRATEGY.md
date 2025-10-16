# Bank Integration Strategy - Capital One to Actual Budget

**Goal:** Automate transaction sync from Capital One accounts to Actual Budget

---

## Your Situation

**What you have:**
- Capital One checking account
- Capital One savings account  
- Self-hosted Actual Budget server
- 25+ PAI finance tools ready to enhance

**What you want:**
- Eliminate manual CSV downloads
- Automated daily transaction sync
- Real-time balance updates
- AI-powered spending analysis

---

## Two Paths Forward

### Path 1: SimpleFIN (RECOMMENDED FIRST)

**Start today, working in 15 minutes**

#### Pros
✅ **No approval needed** - sign up and start immediately  
✅ **Capital One supported** - checking + savings both work  
✅ **Low cost** - $1.50/month (one institution)  
✅ **Actual Budget native support** - or build custom  
✅ **Perfect demo** - proves concept for Plaid request  
✅ **Production ready** - use it while waiting for Plaid  

#### Cons
⚠️ **Monthly cost** - $18/year  
⚠️ **Fewer institutions** - limited compared to Plaid  
⚠️ **Less metadata** - basic transaction data  

#### Timeline
- **Today:** Sign up, connect Capital One (5 min)
- **This week:** Build custom PAI tools if desired (2-3 hours)
- **Next week:** Use demo in Plaid request

#### Cost
**$1.50/month** = $18/year for Capital One (covers both accounts)

---

### Path 2: Plaid

**Enterprise-grade, but requires approval**

#### Pros
✅ **More institutions** - thousands supported  
✅ **Richer data** - detailed merchant info, categories, location  
✅ **Better long-term** - industry standard  
✅ **Free for personal dev** - likely $0 after approval  
✅ **More features** - investments, liabilities, identity  

#### Cons
⚠️ **Approval required** - may take days/weeks  
⚠️ **More complex** - OAuth flow, webhooks, etc.  
⚠️ **May reject** - enterprise-focused, personal use uncertain  

#### Timeline
- **Week 1:** Submit application, wait for approval
- **Week 2-4:** Sandbox testing and development
- **Week 5+:** Production deployment

#### Cost
**Free in Sandbox**, contact for production pricing (often free for personal use)

---

## RECOMMENDED STRATEGY: Both

### Phase 1: SimpleFIN (This Week)
```bash
# 1. Sign up for SimpleFIN
https://beta-bridge.simplefin.org/simplefin/signup

# 2. Connect Capital One
# - Checking account
# - Savings account

# 3. Quick test with Actual Budget
# Settings → Import Accounts → SimpleFIN
# Paste token, verify transactions sync

# 4. Build custom PAI tools (optional but recommended)
cd ~/pai/repositories/pai-personal-finance/simplefin
npm install
# Follow QUICK-START.md

# Result: Working automation TODAY
```

### Phase 2: Enhanced Plaid Request (Next Week)
```bash
# Update Plaid application with:
# "Working prototype using SimpleFIN with Capital One accounts"
# [Include screenshots]
# "Requesting Plaid to expand beyond SimpleFIN's limitations"

# This makes your request MUCH stronger:
# - Proves technical capability
# - Shows real value delivered
# - Demonstrates you're serious
```

### Phase 3: Plaid Integration (After Approval)
```bash
# Build Plaid integration in parallel
cd ~/pai/repositories/pai-personal-finance/plaid
npm install
# Follow implementation roadmap

# Test in Sandbox while SimpleFIN runs in production
```

### Phase 4: Choose or Combine (Future)
```bash
# Option A: Keep SimpleFIN, add Plaid for other banks
# Option B: Migrate fully to Plaid if better
# Option C: Use both - SimpleFIN for Capital One, Plaid for others
```

---

## Decision Matrix

| Factor | SimpleFIN | Plaid |
|--------|-----------|-------|
| **Time to working** | 15 minutes | 2-4 weeks |
| **Capital One support** | ✅ Yes | ✅ Yes |
| **Cost** | $18/year | Free (likely) |
| **Approval needed** | ❌ No | ✅ Yes |
| **Data richness** | Basic | Advanced |
| **Institutions** | Limited | Thousands |
| **Use for demo** | ✅ Perfect | ⚠️ Sandbox only |
| **Production ready** | ✅ Today | ⏳ After approval |

---

## What to Do RIGHT NOW

### Immediate Action (15 minutes)
1. **Sign up for SimpleFIN**
   ```
   https://beta-bridge.simplefin.org/simplefin/signup
   ```

2. **Connect Capital One**
   - Add Capital One as institution
   - Authenticate with your credentials
   - Select checking + savings accounts

3. **Test with Actual Budget**
   - Settings → Import Accounts → SimpleFIN
   - Paste your SimpleFIN token
   - Verify transactions appear

4. **Verify it works**
   - Check that Capital One accounts show up
   - Transactions should be syncing
   - Balances should be accurate

**Result: Working bank sync in 15 minutes** ✅

### This Week (2-3 hours) - Optional but Recommended
Build custom PAI SimpleFIN tools to:
- Demonstrate technical skills
- Add AI-powered analysis
- Create demo for Plaid request

```bash
cd ~/pai/repositories/pai-personal-finance/simplefin
cat QUICK-START.md  # Follow Option 2
```

### Next Week
Update and submit Plaid request with:
- Screenshots of working SimpleFIN integration
- Proof you've already built and tested the concept
- Clear explanation of why you want Plaid

---

## File Locations

**SimpleFIN documentation:**
- `/home/jbyrd/pai/repositories/pai-personal-finance/simplefin/README.md`
- `/home/jbyrd/pai/repositories/pai-personal-finance/simplefin/QUICK-START.md`

**Plaid documentation:**
- `/home/jbyrd/pai/repositories/pai-personal-finance/plaid/README.md`
- `/home/jbyrd/pai/repositories/pai-personal-finance/plaid/IMPLEMENTATION-ROADMAP.md`
- `/home/jbyrd/pai/plaid-api-request-prep.md` (comprehensive)
- `/home/jbyrd/pai/plaid-request-quick-reference.md` (quick ref)

---

## Bottom Line

**Best approach:**

1. ✅ **SimpleFIN TODAY** - Get Capital One syncing now ($18/year)
2. ✅ **Build custom tools THIS WEEK** - Demonstrate capabilities  
3. ✅ **Submit Plaid request NEXT WEEK** - With working demo
4. ✅ **Add Plaid WHEN APPROVED** - Expand beyond SimpleFIN

**Why this works:**
- You get value immediately (working automation)
- You prove technical capability (custom tools)
- You strengthen Plaid request (working demo)
- You have fallback if Plaid rejects (SimpleFIN works)

---

## Quick Commands

### Start SimpleFIN Today
```bash
# 1. Sign up (browser)
xdg-open https://beta-bridge.simplefin.org/simplefin/signup

# 2. After connecting Capital One and getting token:
cd ~/pai/repositories/pai-personal-finance/simplefin

# 3. Quick test
cat QUICK-START.md

# 4. Option 1: Use Actual Budget native support (5 min)
# Option 2: Build custom PAI tools (2-3 hours)
```

### Check What You've Built
```bash
# SimpleFIN
ls -la ~/pai/repositories/pai-personal-finance/simplefin/

# Plaid (prepared, not implemented yet)
ls -la ~/pai/repositories/pai-personal-finance/plaid/
```

### View Documentation
```bash
# SimpleFIN quick start
cat ~/pai/repositories/pai-personal-finance/simplefin/QUICK-START.md

# Plaid request prep
cat ~/pai/plaid-request-quick-reference.md
```

---

## Questions?

**"Should I do SimpleFIN or Plaid?"**  
→ **Both.** SimpleFIN first (this week), Plaid later (after approval).

**"Will SimpleFIN hurt my Plaid request?"**  
→ **No, it helps!** Shows you've built and validated the concept.

**"Is SimpleFIN secure?"**  
→ **Yes.** Same security model as Plaid (OAuth, encryption, read-only).

**"Can I cancel SimpleFIN later?"**  
→ **Yes.** Cancel anytime if you migrate to Plaid or decide not to use it.

**"What if Plaid rejects my request?"**  
→ **You still have SimpleFIN working.** Problem solved either way.

---

## Support Resources

**SimpleFIN:**
- Signup: https://beta-bridge.simplefin.org/simplefin/signup
- Support: support@simplefin.org
- Pricing: $1.50/month per institution

**Plaid:**
- Dashboard: https://dashboard.plaid.com
- Docs: https://plaid.com/docs/
- Support: Via dashboard after signup

**Your PAI Docs:**
- SimpleFIN: `~/pai/repositories/pai-personal-finance/simplefin/`
- Plaid: `~/pai/repositories/pai-personal-finance/plaid/`

---

*Bank Integration Strategy - Get Capital One syncing today, expand with Plaid later*  
*Start here: https://beta-bridge.simplefin.org/simplefin/signup*


