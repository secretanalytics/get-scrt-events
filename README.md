# get-scrt-events

### Summary

Application runs forever, algorithm is:
1. Query the remote node for chaintip(most recent block)
2. If the most recent block in the database(db_tip) is lessthan the chaintip.
    - the remote node is queried for the block resultsfrom db_tip to chaintip
    - these results are stored in postgresql
   else:
       - wait 1 second, then repeat from Step 1.