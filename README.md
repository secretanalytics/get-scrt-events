# get-scrt-events

The json returned from the Secret Node /block_results endpoint requires some parsing to be useful for analysis. This application queries a remote node for all block_results and stores the parsed data in a [postgresql](https://www.postgresql.org/) database. 

## Summary

Application runs forever, algorithm is:
1. Query the remote node for chaintip(most recent block)
2. If the most recent block in the database(db_tip) is less than the chaintip: The remote node is queried for the block results from db_tip to chaintip. These results are stored in postgres. Else: wait 1 second, then repeat from Step 1.

