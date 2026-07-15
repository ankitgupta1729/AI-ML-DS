# ITEMS — Demo Video Narration Script

Voiceover script, one block per slide. Timings are approximate; the build script
uses the actual synthesized audio length for each slide so audio and video stay
perfectly in sync. Total runtime ≈ 3½ minutes.

---

**Slide 1 — Title**
Welcome to ITEMS, the Income Tax Evaluation and Maintenance System. In this short walkthrough, you will see what the project does, the modules it offers, and how your team can use it from any device.

**Slide 2 — The problem**
Tax practitioners traditionally maintain client records, income tax returns, and firm accounts by hand. This is slow, error prone, and hard to search. ITEMS replaces that paperwork with a single, secure, computerised system.

**Slide 3 — Objectives**
ITEMS maintains a record for every client. Based on the client's category, it files their original return for a fiscal year, and lets you file a revised return to correct mistakes. For firms, it maintains the trading account, profit and loss account, and balance sheet. And it generates ready to print reports.

**Slide 4 — Architecture**
The production system is built with Visual Basic dot NET and an Oracle database, exactly as required. To let anyone try it instantly, we also ship a live web version, with the same modules and the same tax engine, deployed online with no installation needed.

**Slide 5 — Security & login**
Access is protected. Every user signs in with a user id and password. Passwords are stored only as secure hashes, and every change to the data is recorded in an audit log.

**Slide 6 — Dashboard**
After signing in, the dashboard gives a live overview. Total clients, returns filed, revised returns, and the net tax recorded, along with recent activity, so you always know where things stand.

**Slide 7 — Client Information**
The Client Information module is the master record. You can add, edit, and delete clients. The PAN is validated and used as the unique key, and deleting a client safely removes all of their linked returns and accounts.

**Slide 8 — Return filing & tax computation**
Filing a return is the heart of the system. Enter the income under each head, and ITEMS computes the tax live, applying the slab rates, rebate, surcharge, and cess, and shows the final balance payable or refund instantly.

**Slide 9 — Firm accounts**
For firm clients, ITEMS maintains the trading account, profit and loss account, and balance sheet. Each has two sides that are totalled automatically, and the system tells you at a glance whether they balance.

**Slide 10 — Reports**
The Reports module generates the four statutory reports. A client's return history, all returns in a fiscal year, and revised returns by a client. Each report can be printed, or saved as a P D F for the client file.

**Slide 11 — Works on any device**
The application is fully responsive. It works on a laptop, a tablet, or a mobile phone, and includes a polished light and dark theme, so your team gets a great experience on any device.

**Slide 12 — Get started**
That's ITEMS. A complete, modern income tax maintenance system. Open the live link, sign in with the demo credentials shown here, and explore every feature yourself. Thank you for watching.
