# get-scrt-events

Monitor function app polls for newest block and peers of node.

Reachable peers are fed back into monitor function. Newest block is fed into get-scrt-events function app.

Durable Azure function app that processes incoming events and passes these messages to other functions depending on the data being parsed.

## Algorithm

Each step denotes a function to be called in the function app.

1. HTTP trigger denoting block range(start-stop) to gather and node to call for latest block.
Parameters are json
```
{
    "start": int to start batch gather,
    "stop": int to stop gathering,
    "node": string with connection details to node
}
```
2. Node is called for events from start-stop at 
endpoint - http://secret-2.node.enigma.co:26657/block_results?height={X}

3. Key value pairs are decoded, decoded values are cached to optimize compute time

4. Transactions and events are output to separate database collections. 