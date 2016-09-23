:mod:`contacts.models` -- Documentation
=======================================

+---------------------+-------------------------------------+------------------+
| Job Number          | Primary key, Auto populates         | Int              |
+---------------------+-------------------------------------+------------------+
| Contact             | The primary contact for the job     | Contact(Object)  |
+---------------------+-------------------------------------+------------------+
| Billed              | If an invoice has been sent to      | bool(yes/no)     |
|                     | the client                          |                  |
+---------------------+-------------------------------------+------------------+
| Invoice Date        | Date the invoice was generated,     | Date             |
|                     | should be at the same time the      |                  |
|                     | invoice is billed                   |                  |
+---------------------+-------------------------------------+------------------+
| Billing Contact     | Person to bill                      | Contact(Object)  |
|                     | (can be the primary contact)        |                  |
+---------------------+-------------------------------------+------------------+
| Department Chartfield String | IDO account number if a Clemson Department is paying | String |
+---------------------+-------------------------------------+------------------+
| Approved By | Name of the person who approved quote/payment | String |
+---------------------+-------------------------------------+------------------+
| Approved Date | The date quote approval was given | Date |
+---------------------+-------------------------------------+------------------+
| Receipt Number | The receipt number from cash payments.
|                | Also used for tracking Clemson's invoice numbers (starting with W4063...) for jobs sent to Accounts Receivable | String |
+---------------------+-------------------------------------+------------------+
| Paid | If payment has been recieved | bool(yes/no) |
+---------------------+-------------------------------------+------------------+
| Payment Date | Date payment is recieved | Date |
+---------------------+-------------------------------------+------------------+
| Payment User | The user who recorded the payment as recieved | User(Object) |
+---------------------+-------------------------------------+------------------+
| Billing Notes | Open text area to hold notes | TextArea |
+---------------------+-------------------------------------+------------------+

=============   ==========================================================
Status          Meaning
=============   ==========================================================
Closed          Product is complete and billed
Design          Artwork is being designed (either internally or externally
Print           Ready to print
In Production   Printing/Printed and being produced
Quoted          Needs quote approval (quote HAS been sent)
Out Sourced     At another agency
On Hold         Client will contact us when ready to resume project
=============   ==========================================================

========        ====
Field           Purpose
========        ====
Due Date        Date the product is due
Prduction Stat  The current production status (see above)
materials       The  
