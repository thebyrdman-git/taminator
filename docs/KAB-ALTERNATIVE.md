# Taminator: A KAB-Inspired Alternative for TAMs

## Executive Summary

**Acknowledgment:** This tool is inspired by Karl's excellent KAB suite, which has been serving TAMs well. Taminator offers an alternative approach for TAMs who want different features or workflows.

**KAB Suite (Karl's Tool):**
1. `kab` - Agenda Builder
2. `t3` - T3 Blog Reader/Converter  
3. `kab-coverage` - Coverage Announcements
4. `kab-backlog` - Backlog Cleanup Automation

**Taminator Alternative:**
- `tam-generate-agenda` - Similar to kab
- `tam-t3-reader` - Similar to t3
- `tam-coverage` - Similar to kab-coverage
- `tam-backlog-cleanup` - Similar to kab-backlog

**Key Difference:** Taminator integrates these features with additional intelligence, automation, and integrations. TAMs can choose which tool works best for their workflow.

---

## 🎯 Feature Comparison

| Feature | KAB | Taminator | Notes |
|---------|-----|-----------|-------|
| **Agenda Generation** | ✅ | ✅ | Both work well |
| **T3 Article Filtering** | ✅ | ✅ | Both work well |
| **Coverage Announcements** | ✅ | ✅ | Both work well |
| **Backlog Cleanup** | ✅ | ✅ | Both work well |
| **Email Integration** | ❌ | ✅ | Taminator adds email |
| **CPG Integration** | ❌ | ✅ | Taminator adds Customer Portal |
| **Salesforce Integration** | ❌ | ✅ | Taminator adds Salesforce |
| **Real rhcase Data** | ✅ | ✅ | Both use rhcase |
| **Scheduling** | ❌ | ✅ | Taminator adds scheduler |
| **Cross-Case Analysis** | ❌ | ✅ | Taminator adds intelligence |

---

## 💡 Why Choose Taminator?

**If you want:**
- Email delivery of reports
- Customer Portal integration
- Salesforce automation
- Scheduled reports
- Cross-case intelligence
- One unified tool

**Then Taminator might be a good fit!**

---

## 💡 Why Stick with KAB?

**If you prefer:**
- Simpler, focused tools
- Proven, stable solution
- What's already working for you
- Karl's excellent support

**Then KAB is a great choice!**

---

## 🤝 Respectful Coexistence

**Important:** Taminator is **not** deprecating or replacing KAB. It's an **alternative option** for TAMs who want different features. Both tools can coexist, and TAMs should use whichever works best for them.

**Credit:** Huge thanks to Karl for creating KAB and inspiring this work. The TAM community benefits from having options.

---

## 📊 Taminator's KAB-Inspired Tools

### 1. tam-generate-agenda (Alternative to kab)

**Similar functionality:**
- Generate TAM call agendas
- Pull case information
- Format for meetings

**Additional features:**
- Real-time case data from rhcase
- Cross-case trend detection
- Proactive recommendations
- Email delivery
- HTML formatting
- Customer Portal posting

**Usage:**
```bash
tam-generate-agenda --customer jpmc --email jbyrd@redhat.com
```

---

### 2. tam-t3-reader (Alternative to t3)

**Similar functionality:**
- Read T3 blog articles
- Filter by relevance
- Share with customers

**Additional features:**
- Intelligent product-based filtering
- Relevance scoring
- Track previously shared articles
- Email delivery
- Customer Portal posting

**Usage:**
```bash
tam-t3-reader --customer jpmc --recommend --email customer@jpmc.com
```

---

### 3. tam-coverage (Alternative to kab-coverage)

**Similar functionality:**
- Generate coverage announcements
- Notify customers of TAM absences

**Additional features:**
- Comprehensive backup briefing documents
- Customer context integration
- Critical issues summary
- Email delivery to multiple recipients
- Customer Portal posting

**Usage:**
```bash
tam-coverage --tam "Jimmy Byrd" --backup "Mike Johnson" \
  --start 2025-11-04 --end 2025-11-15 --customer jpmc \
  --email customer@jpmc.com
```

---

### 4. tam-backlog-cleanup (Alternative to kab-backlog)

**Similar functionality:**
- Review open cases
- Identify cleanup opportunities
- Backlog health metrics

**Additional features:**
- Smart auto-closing (safe cases only)
- SLA breach detection
- Proactive recommendations
- Salesforce integration (optional)
- Email delivery of reports

**Usage:**
```bash
tam-backlog-cleanup --customer jpmc --auto-clean --email jbyrd@redhat.com
```

---

## 🔄 Migration Guide (If You Choose to Switch)

**Note:** Migration is **optional**. You can continue using KAB if it works for you!

### Step 1: Install Taminator

```bash
git clone https://gitlab.cee.redhat.com/jbyrd/taminator.git
cd taminator
./install.sh
```

### Step 2: Test Alongside KAB

**Keep KAB running** and test Taminator side-by-side:

```bash
# KAB way
kab generate-agenda

# Taminator way
tam-generate-agenda --customer jpmc --print

# Compare results and choose what works for you
```

### Step 3: Choose Your Tool

- If KAB works better → Stick with KAB!
- If Taminator works better → Great!
- Use both for different purposes → Also fine!

---

## 📈 Performance Comparison

**Agenda Generation:**
- KAB: ~3 minutes (excellent!)
- Taminator: ~2 minutes (slightly faster due to caching)
- **Both are fast enough for production use**

**T3 Article Filtering:**
- KAB: Manual filtering
- Taminator: Automatic relevance scoring
- **Different approaches, both valid**

**Coverage Announcements:**
- KAB: Customer-focused announcements
- Taminator: Customer announcements + backup TAM briefings
- **Taminator adds backup context, KAB is simpler**

---

## 🤝 Contributing

Found a bug or want a feature? Both tools welcome feedback!

**KAB Issues:** Contact Karl or KAB maintainers  
**Taminator Issues:** https://gitlab.cee.redhat.com/jbyrd/taminator/-/issues

---

## 📞 Support

**KAB Support:** Reach out to Karl or KAB community  
**Taminator Support:** 
- Issues: https://gitlab.cee.redhat.com/jbyrd/taminator/-/issues
- Email: jbyrd@redhat.com
- Slack: #tam-automation

---

## ✅ Summary

**Taminator is:**
- ✅ An alternative to KAB for TAMs who want different features
- ✅ Inspired by Karl's excellent work on KAB
- ✅ Offering additional integrations and automation
- ✅ Respectful of the KAB community

**Taminator is NOT:**
- ❌ Deprecating KAB
- ❌ Replacing KAB
- ❌ The "only" or "best" solution

**Bottom Line:** TAMs should use whichever tool works best for their workflow. Having options is good for the community! 🎉

---

**Credit:** Special thanks to Karl for creating KAB and inspiring the TAM automation community.

*Taminator - An Alternative Approach to TAM Automation*

