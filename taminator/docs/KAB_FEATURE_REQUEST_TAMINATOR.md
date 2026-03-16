# Request: Add Taminator as a feature on KAB (Karl's Agenda Builder)

**Purpose:** Propose that RFE and bug report generation (Taminator) be added as a capability or workflow within KAB, following positive feedback from a Taminator presentation.

---

## What is KAB?

**KAB = Karl's Agenda Builder**

- A reporting tool that creates **support-oriented agendas** for leading meetings with Red Hat's strategic clients.
- Produces **detailed, structured reports** that would otherwise take a skilled person **2–4 hours per report**.
- KAB generates these reports in **under 3 minutes**.

**Time savings (example):**

- 5 accounts, meetings every other week → **10 agendas per month** (assuming a 4-week month).
- Manual: ~3 hours per report → **~30 hours/month**.
- With KAB: **~30 minutes/month**.
- Net: **Almost a full business week per month back** for most SCE associates.

**Reference:** Karl Abbott held a KAB overview session (see attached video or internal recording).

---

## KAB tool family

Related tools in the KAB ecosystem:

**t3**

- Reads the latest t3 blog entries and converts them to markdown.
- Lets you edit the markdown, then post to your customer portal private groups and/or emails you a copy.
- The emailed version is in HTML.

**kab-coverage**

- Generates and distributes **coverage announcements** by posting them to the customer portal private group and/or emailing you a copy.

**kab-backlog**

- Goes through your customer's open cases and **automates cleaning up your backlog**.
- At the end of a run it produces: actions you need to take, actions the tool took, what's breached, and what's breaching in the next 24 hours.
- Output is sent to you via email.

---

## What is Taminator?

- A tool for **generating and maintaining RFE and bug reports** for TAMs (Technical Account Managers).
- Uses JIRA and case data; produces consistent, customer-ready RFE/Bug tracker reports; can post to Customer Portal.
- Saves TAMs **2–3 hours per customer per week** (manual work reduced to minutes per report).

**Scope (current roadmap):** Only features directly related to RFE and bug report generation. No other features in plan.

---

## The ask

**Request:** Add Taminator-style **RFE and bug report generation** as a feature or workflow within KAB (Karl's Agenda Builder).

**Rationale:**

- Both tools are **report-generation tools** that replace hours of manual work with minutes.
- KAB is already an **official tool** with adoption; adding a TAM-focused report type could serve SCE/TAM use cases in one place.
- Taminator has been **presented and received positive feedback**; integrating its capabilities into KAB could broaden impact and reduce tool sprawl.

**Possible integration approaches (for discussion with KAB owners):**

- A dedicated "RFE/Bug report" report type or template in KAB.
- A workflow or section in KAB that uses the same data sources and output format as Taminator (JIRA, cases, Customer Portal).
- Or another model the KAB team prefers.

---

## Response from KAB (after watching demo)

**Kevin Niederwanger**, Senior Technical Account Manager — OpenShift, replied in chat (paraphrased):

- **Fit:** This could be placed in KAB as part of a **new or existing application that fetches data via Jira**. Good fit for the platform.
- **Next step:** Approach the team in the **kab channel** to test the waters.
- **Development:** You can work on this during **local development** before the merge is approved. Contributing to KAB is welcomed.
- **Security / hosting:** KAB has gone through the audits and is allowed to host such functionality on **central IT**; that may or may not play a role in security posture moving forward.

---

## Next steps

- [ ] Reach out in the **kab channel** to test the waters and align on approach.
- [ ] If aligned: set up local KAB development and implement RFE/bug report (Jira fetch) as a new or existing application.
- [ ] Share Taminator repo, demo, or docs as needed: https://gitlab.cee.redhat.com/jbyrd/taminator
