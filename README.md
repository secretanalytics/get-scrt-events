# get-scrt-events

### Summary

Application runs forever, algorithm is:
1. Query the remote node for chaintip(most recent block)
2. If the most recent block in the database(db_tip) is less than the chaintip: The remote node is queried for the block results from db_tip to chaintip. These results are stored in postgres. Else: wait 1 second, then repeat from Step 1.