from cards.models import JobCard
from invoice.models import *

def check_payments(inv):
    """
    Checks payment events and marks invoice as
    paid if all payments are in.
    """
    payments = PaymentEvent.objects.filter(invoice=inv).\
            filter(payment_received=True)
    amount = 0

    for payment in payments:
        amount += payment.payment_amount

    if amount >= inv.grand_total:
        inv.paid = True
        inv.save()


