#!/bin/bash
uuencode final_inprod_list.csv Current_In_Prod_Queue.csv | sendmail -f  do_not_reply@clemson.edu kramnat@g.clemson.edu 
