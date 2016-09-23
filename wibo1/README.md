# WIBO - Web Invoicing Billing Organizer

**Wibo** was developed to be the ultimate print-shop job tracking and invoicing system. It combines kanban based ideas and advanced reporting to help managers and designers manage workloads and monitor the progress of an entire team.

- **Job Tracking**: The Job Queue provides an at-a-glance snapshot of who's working on what and when everything is due.
- **Product Templating**: Product templates allows managers to save the production information for frequent jobs to reduce error on repeat orders.
- **Automatic Billing**: Every Product carries all the pricing info needed to quote and bill jobs, so creating a quote or an invoice becomes a one-button operation.
- **Waste Tracking**: Detailed waste reports help track exactly where efficiency needs to be improved.
- **Aggregated Reporting**: A Python based reporting system allows an unlimited variety of views in to production and cost data.

Updated: 28-Apr-2014

# Change Log
## v0.2.8 
- Validation when saving jobs now check for thumbnails, waste notes and if the job has been billed
- Improved documentation (both in comments and in docs/cards.md)
- cards/models.py updated to PEP8
- Improved waste reporting to include more user data
- Added timedelta function to cards to calculate the time a card has been in scope
- Job "log" fields now store date and time information (instead of just date)
- Removed links and redirects to Product Details pages to improve user interaction

## v0.2.7
- Improved job detail display
- Web Invoice Number is no longer required, to help track invoices with payments in progress
- Improved invoice list display
- Improved SPAR report (with % of total on products)
- Added definitions of job statuses to top of job index page

# Road Map
- In app notifications
- PEP8 compliance