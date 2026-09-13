"""
Sample Contracts Library for LegalLens AI.
Contains realistic legal documents for instant zero-friction demonstration and evaluation.
"""

SAMPLE_CONTRACTS = {
    "msa_freelance": {
        "id": "msa_freelance",
        "title": "Freelance Master Services Agreement (MSA)",
        "category": "Services & Independent Contractor",
        "parties": "Acme Innovations Inc. (Client) & Alex Rivera (Contractor)",
        "summary": "A typical software consulting agreement containing hidden uncapped indemnity and IP transfer risks.",
        "text": """MASTER SERVICES AGREEMENT

This Master Services Agreement ("Agreement") is entered into as of March 15, 2026 ("Effective Date"), by and between Acme Innovations Inc., a Delaware corporation with its principal office at 500 Market St, San Francisco, CA ("Client"), and Alex Rivera, an independent software engineer residing at 120 Pine Lane, Austin, TX ("Contractor").

1. SCOPE OF SERVICES
Contractor agrees to perform software development, architectural design, and consulting services as specified in Statements of Work ("SOW") executed by both parties. All work shall be performed in a professional and workmanlike manner in accordance with industry standards.

2. COMPENSATION AND PAYMENT TERMS
Client shall compensate Contractor at the agreed rate of $120.00 per hour. Contractor shall submit invoices on the 1st and 15th of each calendar month. Client shall pay all undisputed invoices within Net-60 days of receipt. In the event of a disputed line item, Client may withhold payment for the entire invoice until resolution. No late interest or penalties shall accrue on overdue payments.

3. TERM AND TERMINATION
(a) Term: This Agreement shall commence on the Effective Date and remain in effect for two (2) years, unless terminated earlier.
(b) Termination for Convenience: Client may terminate this Agreement or any SOW at any time, with or without cause, upon three (3) calendar days' prior written notice to Contractor. Contractor may terminate this Agreement only upon sixty (60) calendar days' prior written notice.
(c) Termination Penalty: If Contractor terminates prior to milestone completion, Contractor shall forfeit fifty percent (50%) of all accrued, unpaid compensation for that milestone.

4. INTELLECTUAL PROPERTY & ASSIGNMENT
(a) Work Product: Contractor agrees that all code, documentation, discoveries, inventions, algorithms, designs, and materials created, conceived, or reduced to practice by Contractor during the term of this Agreement—whether created during business hours, on weekends, using Client equipment, or on Contractor's personal devices—shall be deemed "Work Made for Hire" and shall be the sole and exclusive property of Client.
(b) Pre-Existing IP: Contractor hereby assigns, transfers, and conveys to Client all rights, titles, and interests in any pre-existing background code, tools, libraries, or frameworks incorporated into the Work Product, without royalty or restriction.

5. CONFIDENTIALITY AND NON-SOLICITATION
Contractor shall maintain the strict confidentiality of Client's proprietary information for a period of ten (10) years following termination. For a period of eighteen (18) months following termination, Contractor shall not directly or indirectly solicit, recruit, or hire any employee, contractor, or customer of Client.

6. INDEMNIFICATION (UNLIMITED)
Contractor shall defend, indemnify, and hold harmless Client, its affiliates, directors, officers, employees, and agents from and against any and all claims, liabilities, losses, damages, costs, judgments, and legal fees (including attorney fees) arising out of or resulting from: (i) any breach of this Agreement by Contractor; (ii) any claim that Work Product infringes any patent, copyright, trademark, or trade secret of any third party; and (iii) any bodily injury, property damage, or negligence committed by Contractor. Contractor's indemnification obligations under this Section are uncapped and shall not be subject to any limitation of liability.

7. LIMITATION OF LIABILITY
TO THE MAXIMUM EXTENT PERMITTED BY LAW:
(a) CLIENT'S TOTAL AGGREGATE LIABILITY ARISING OUT OF OR RELATED TO THIS AGREEMENT SHALL BE STRICTLY CAPPED AT $1,000.00 OR THE FEES PAID IN THE PRIOR ONE (1) MONTH, WHICHEVER IS LESS.
(b) CONTRACTOR'S LIABILITY SHALL BE UNLIMITED FOR INDEMNITY, BREACH OF CONFIDENTIALITY, AND INTELLECTUAL PROPERTY INFRINGEMENTS.
(c) IN NO EVENT SHALL CLIENT BE LIABLE FOR ANY CONSEQUENTIAL, INDIRECT, SPECIAL, OR PUNITIVE DAMAGES.

8. GOVERNING LAW AND EXCLUSIVE ARBITRATION
This Agreement shall be governed by and construed under the laws of the State of Delaware, without regard to conflicts of law. Any controversy or claim arising out of this Agreement shall be resolved exclusively through confidential binding arbitration administered by JAMS in Wilmington, Delaware. Each party waives any right to a jury trial or to participate in any class-action proceeding. All arbitration filing and administration fees shall be borne equally, but Contractor shall advance the initial retainer fee.

IN WITNESS WHEREOF, the parties hereto have executed this Agreement as of the date first above written.

ACME INNOVATIONS INC.                    CONTRACTOR
By: ____________________                 By: ____________________
Name: Sarah Jenkins, VP Eng              Name: Alex Rivera
"""
    },

    "msa_comparison_v2": {
        "id": "msa_comparison_v2",
        "title": "Freelance MSA - Counter-Party Markup (Version 2)",
        "category": "Services & Independent Contractor",
        "parties": "Acme Innovations Inc. & Alex Rivera (Revised Edition)",
        "summary": "Counterparty markup introducing accelerated payment terms, mutual termination, IP carve-outs, and mutual liability caps.",
        "text": """MASTER SERVICES AGREEMENT (REVISED REDLINE v2)

This Master Services Agreement ("Agreement") is entered into as of March 15, 2026 ("Effective Date"), by and between Acme Innovations Inc., a Delaware corporation ("Client"), and Alex Rivera ("Contractor").

1. SCOPE OF SERVICES
Contractor agrees to perform software development, architectural design, and consulting services as specified in mutually executed Statements of Work ("SOW"). All work shall be performed in a professional and workmanlike manner.

2. COMPENSATION AND PAYMENT TERMS (REVISED)
Client shall compensate Contractor at the agreed rate of $135.00 per hour. Contractor shall submit bi-weekly invoices. Client shall pay all undisputed invoices within Net-15 days of receipt. If Client disputes any item, Client shall pay the undisputed portion immediately and provide written explanation within 5 business days. Overdue payments shall accrue interest at 1.5% per month or the legal maximum.

3. TERM AND TERMINATION (MUTUAL)
(a) Term: One (1) year from the Effective Date, renewable upon mutual written consent.
(b) Termination for Convenience: Either party may terminate this Agreement or any SOW upon thirty (30) calendar days' prior written notice to the other party.
(c) Early Termination Compensation: Upon early termination, Client shall pay Contractor for all hours worked and milestone progress achieved up to the effective termination date. All termination forfeiture penalties are hereby deleted.

4. INTELLECTUAL PROPERTY & BACKGROUND TOOLS (REVISED)
(a) Work Product: Upon full payment of all applicable fees, Client shall own all custom deliverables specifically commissioned and created for Client under an SOW.
(b) Pre-Existing IP & Tools: Contractor retains exclusive ownership of all pre-existing libraries, open-source modules, methodologies, and general code snippets ("Contractor Tools"). Contractor grants Client a non-exclusive, perpetual, worldwide, royalty-free license to use Contractor Tools solely as embedded within the deliverable.

5. CONFIDENTIALITY AND NON-SOLICITATION
Both parties agree to protect each other's Confidential Information with reasonable care for a period of two (2) years. Contractor agrees not to directly solicit Client employees for twelve (12) months.

6. MUTUAL INDEMNIFICATION
Each party shall defend and indemnify the other party against direct third-party claims arising from: (a) gross negligence or willful misconduct; or (b) copyright infringement of deliverable materials, provided the indemnifying party has sole control of defense and prompt written notice.

7. BALANCED LIMITATION OF LIABILITY (MUTUAL CAP)
EXCEPT FOR WILLFUL MISCONDUCT OR BREACH OF CONFIDENTIALITY, EACH PARTY'S TOTAL AGGREGATE LIABILITY UNDER THIS AGREEMENT SHALL BE MUTUALLY LIMITED TO THE TOTAL FEES PAID OR PAYABLE TO CONTRACTOR IN THE TWELVE (12) MONTHS PRECEDING THE CLAIM. NEITHER PARTY SHALL BE LIABLE FOR INDIRECT OR CONSEQUENTIAL DAMAGES.

8. GOVERNING LAW AND DISPUTE RESOLUTION
This Agreement shall be governed by the laws of Texas. The parties agree to attempt good-faith executive mediation for thirty (30) days prior to initiating legal proceedings in Travis County, Texas.

IN WITNESS WHEREOF, the parties hereto have executed this Revised Agreement.
"""
    },

    "saas_tos": {
        "id": "saas_tos",
        "title": "CloudMetrics SaaS Enterprise Terms of Service",
        "category": "Software as a Service",
        "parties": "CloudMetrics Platform Ltd & Enterprise Subscriber",
        "summary": "An enterprise SaaS license agreement containing aggressive auto-renewal traps, unilateral price hikes, and complete warranty disclaimers.",
        "text": """CLOUDMETRICS ENTERPRISE TERMS OF SERVICE

Last Updated: January 1, 2026

PLEASE READ CAREFULLY. BY CLICKING "I AGREE" OR ACCESSING THE CLOUDMETRICS PLATFORM, YOU ("CUSTOMER") AGREE TO BE BOUND BY THESE ENTERPRISE TERMS.

1. SUBSCRIPTION AND ACCESS
CloudMetrics grants Customer a non-exclusive, non-transferable, revocable license to access the CloudMetrics analytics engine during the Subscription Term. Customer shall not reverse engineer, decompile, or create derivative works.

2. FEES, BILLING & UNILATERAL PRICE ESCALATION
Customer shall pay all annual fees upfront. CloudMetrics reserves the right to increase annual subscription fees by up to fifteen percent (15%) upon each renewal period without prior notification. Invoices not paid within Net-10 days shall incur immediate suspension of access to Customer data.

3. EVERGREEN AUTO-RENEWAL TRAP
THE SUBSCRIPTION TERM SHALL AUTOMATICALLY RENEW FOR SUCCESSIVE TWELVE (12) MONTH TERMS UNLESS CUSTOMER PROVIDES FORMAL WRITTEN NOTICE OF CANCELLATION AT LEAST NINETY (90) DAYS PRIOR TO THE EXPIRATION OF THE CURRENT TERM VIA CERTIFIED POSTAL MAIL TO CLOUDMETRICS' CORPORATE HEADQUARTERS. EMAIL OR DASHBOARD CANCELLATIONS ARE STRICTLY VOID.

4. SERVICE LEVEL AGREEMENT & EXCLUSION OF REMEDIES
CloudMetrics targets an uptime availability of 99.0% per quarter, excluding planned maintenance. If uptime falls below 99.0%, Customer's SOLE AND EXCLUSIVE REMEDY shall be a service credit equal to 2% of the monthly fee. Under no circumstances shall downtime entitle Customer to termination or cash refund.

5. CUSTOMER DATA AND AI MODEL TRAINING RIGHTS
Customer grants CloudMetrics a perpetual, irrevocable, worldwide, royalty-free license to ingest, store, process, analyze, and use Customer Data (including proprietary trade data and user analytics) to train, refine, and commercially deploy CloudMetrics' proprietary machine learning models and public AI features.

6. DISCLAIMER OF ALL WARRANTIES
THE PLATFORM IS PROVIDED "AS IS" AND "AS AVAILABLE". CLOUDMETRICS DISCLAIMS ALL WARRANTIES, EXPRESS OR IMPLIED, INCLUDING MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT. CLOUDMETRICS DOES NOT WARRANT UNINTERRUPTED OR ERROR-FREE OPERATION.

7. LIABILITY CAP OF $100
IN NO EVENT SHALL CLOUDMETRICS' AGGREGATE LIABILITY ARISING FROM OR RELATED TO THIS AGREEMENT OR LOSS OF CUSTOMER DATA EXCEED THE SUM OF ONE HUNDRED DOLLARS ($100.00 USD), REGARDLESS OF THE NATURE OF THE CLAIM OR FAILURE OF ESSENTIAL PURPOSE.

8. MANDATORY ARBITRATION & CLASS ACTION WAIVER
All disputes must be resolved by individual confidential arbitration in Zurich, Switzerland under Swiss Rules. Customer explicitly waives the right to participate in any class action or representative litigation.
"""
    },

    "residential_lease": {
        "id": "residential_lease",
        "title": "Residential Tenancy & Property Lease Agreement",
        "category": "Real Estate & Housing",
        "parties": "Apex Property Management LLC (Landlord) & Tenant",
        "summary": "A residential lease with severe tenant restrictions, immediate eviction waiver, and forfeiture of security deposit.",
        "text": """RESIDENTIAL LEASE AND TENANCY AGREEMENT

THIS LEASE AGREEMENT is made and entered into on this 1st day of February 2026, by and between Apex Property Management LLC ("Landlord"), and the undersigned ("Tenant").

1. PREMISES AND OCCUPANCY
Landlord leases to Tenant the residential apartment located at 742 Evergreen Terrace, Unit 4B ("Premises"). Premises shall be occupied solely by Tenant. Any guest staying more than forty-eight (48) consecutive hours without prior written landlord approval shall incur an unauthorized guest fee of $100 per day.

2. RENT AND COMPOUNDING LATE PENALTIES
Monthly rent is $2,400.00, due on the 1st of each calendar month. If rent is not received by 11:59 PM on the 2nd day of the month, Tenant shall pay an immediate late fee of $150.00, plus an additional $25.00 per day until paid in full.

3. SECURITY DEPOSIT AND NON-REFUNDABLE FORFEITURES
Tenant deposits $4,800.00 as security. Landlord shall retain a mandatory non-refundable turnover fee of $800.00 upon vacancy for administrative inspection, regardless of condition. Landlord shall have ninety (90) days following move-out to return the balance of the deposit.

4. LANDLORD ACCESS WITHOUT NOTICE
Landlord and its maintenance agents retain the unrestricted right to enter the Premises at any hour of the day or night, without prior notice, for inspections, showing prospective buyers, or general renovations.

5. MAINTENANCE AND REPAIRS
Tenant shall be solely responsible for all maintenance, plumbing clogs, appliance repairs, and air conditioning servicing costing under $500.00 per occurrence, regardless of whether damage resulted from ordinary wear and tear or pre-existing defects.

6. PROHIBITION OF LEGAL ACTION AND WAIVER OF NOTICE
Tenant hereby waives all statutory notices to vacate or quit. In the event of any default, Landlord may immediately re-enter and take possession of Premises and remove Tenant's personal property without legal court process. Tenant waives all rights to trial by jury in any landlord-tenant dispute.
"""
    }
}
