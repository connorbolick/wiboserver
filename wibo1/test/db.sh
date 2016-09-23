#!/bin/sh
#ASSIGNING MYSQL
#MYSQL=/usr/local/mysql/bin/mysql -u root -pcubanners13!
#$MYSQL -e"select * from ftp.ftp" -u root
#$MYSQL -e"select * cards_jobcard"
# usr/local/mysql/bin/mysql wibo -uroot -pcubanners13! -e "SELECT job_number,name,due_date,assigneduser_id  FROM wibo.cards_jobcard where status='in production';" >> test.txt
#/usr/local/mysql/bin/mysql wibo -uroot -pcubanners13! -e "SELECT job_number,name,due_date,assigneduser_id  FROM wibo.cards_jobcard where status='in production';" >> test.xlsx
#/usr/local/mysql/bin/mysql wibo -uroot -pcubanners13! -e "SELECT job_number,name,due_date,assigneduser_id  FROM test.testtable2 where status='in production' INTO OUTFILE '/Users/campusbanners/repos/wibo_master/wibo/test/file.csv' FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n';"
#/usr/local/mysql/bin/mysql wibo -uroot -pcubanners13! -e "SELECT job_number,name,due_date,assigneduser_id  FROM test.testtable2 where status='in production' INTO OUTFILE '/Users/campusbanners/repos/wibo_master/wibo/test/file.csv' FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n';"
rm file.csv
>final.csv
>final_inprod_list.csv
/usr/local/mysql/bin/mysql wibo -uroot -pcubanners13! -e "SELECT assigneduser_id,job_number,name,due_date,client_notes  
FROM test.testtable2 where status='in production'
INTO OUTFILE '/Users/campusbanners/repos/wibo_master/wibo/test/file.csv'
FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\n';"

#>>file.csv
#chmod 775 file.csv
cat list.csv file.csv >> final.csv
chmod 777 final.csv
rm /Users/campusbanners/repos/wibo_master/wibo/test/final_inprod_list.csv
cat final.csv |  sed 's/"10"/"Carson Culver "/' | sed 's/"11"/"Savannah Younts"/' | sed 's/"12"/"Alli Thomas"/' | sed 's/"13"/"Toni Trout "/' | sed 's/"14"/"Katherine Redmond "/' | sed 's/"16"/"Ginger Li "/' | sed 's/"25"/"Samantha Arnold "/' | sed 's/"26"/"Katie Runge"/' | sed 's/"27"/"Colleen Kiceluk "/' | sed 's/"28"/"Jenna Burke "/' | sed 's/"30"/"Kelly Siciliano "/' | sed 's/"43"/"Jeff Fellers "/' | sed 's/"44"/"Ciara Hautau "/' | sed 's/"45"/"Kayla Fulton "/' | sed 's/"46"/"Austin Williams "/' | sed 's/"47"/"Laura Genise "/' | sed 's/"48"/"Joseph Neely "/' | sed 's/"50"/"Elizabeth Rogers "/'  | sed 's/"52"/"Austin Ferguson "/' | sed 's/"57"/"James Pepper "/' | sed 's/"58"/"Alyssa Zingaro"/' | sed 's/"59"/"Todd Erickson "/' | sed 's/"60"/"Kayla Queen "/' | sed 's/"61"/"Courtney Pringle "/' | sed 's/"62"/"Kendyle Seay "/' | sed 's/"64"/"Meredith Lenti "/' | sed 's/"69"/"Jordan Salisbury "/' | sed 's/"70"/"Jamie Harding "/' | sed 's/"71"/"Olivia Wagner "/' | sed 's/"72"/"Brooke Sidener "/' | sed 's/"74"/"Tisha Burch "/' | sed 's/"9"/"Nathan Smith "/'| sed 's/"42"/"Garrett Mozingo "/' > /Users/campusbanners/repos/wibo_master/wibo/test/final_inprod_list.csv
chmod 777 /Users/campusbanners/repos/wibo_master/wibo/test/final_inprod_list.csv
rm file.csv
