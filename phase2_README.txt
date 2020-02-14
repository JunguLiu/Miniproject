sort -u terms.txt | perl break.pl | db_load -c duplicates=1 -T -t hash te.idx
sort -u pdates.txt | perl break.pl | db_load -c duplicates=1 -T -t hash da.idx
sort -u prices.txt | perl break.pl | db_load -c duplicates=1 -T -t hash pr.idx
sort -u ads.txt | perl break.pl | db_load -c duplicates=1 -T -t hash ad.idx


check information 

db_dump -d a te.idx
db_dump -d a da.idx
db_dump -d a pr.idx
db_dump -d a ad.idx
