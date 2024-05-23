from llamaapi import LlamaAPI
import json
import yaml

config = yaml.safe_load(open("config.yaml"))
# Replace 'Your_API_Token' with your actual API token
llama = LlamaAPI(config['llama']['api_key'])

# API Request JSON Cell
api_request_json = {
    "model": "codellama-7b-instruct",
    "messages": [
        {"role": "system", "content": "Assistant is a smart contract assistant"},
        {"role": "user", "content": """Find the vulnerability in the following smart contract ```/*
 * @source: https://smartcontractsecurity.github.io/SWC-registry/docs/SWC-124#arbitrary-location-write-simplesol
 * @author: Suhabe Bugrara
 * @vulnerable_at_lines: 27
 */

 pragma solidity ^0.4.25;

 contract Wallet {
     uint[] private bonusCodes;
     address private owner;

     constructor() public {
         bonusCodes = new uint[](0);
         owner = msg.sender;
     }

     function () public payable {
     }

     function PushBonusCode(uint c) public {
         bonusCodes.push(c);
     }

     function PopBonusCode() public {
         // <yes> <report> ACCESS_CONTROL
         require(0 <= bonusCodes.length); // this condition is always true since array lengths are unsigned
         bonusCodes.length--; // an underflow can be caused here
     }

     function UpdateBonusCodeAt(uint idx, uint c) public {
         require(idx < bonusCodes.length);
         bonusCodes[idx] = c; // write to any index less than bonusCodes.length
     }

     function Destroy() public {
         require(msg.sender == owner);
         selfdestruct(msg.sender);
     }
 }
```"""},
        {"role": "assistant",
         "content": "Vulnerability detected, it is classified as Access Control due to these instructions ```         require(0 <= bonusCodes.length); // this condition is always true since array lengths are unsigned``` "},
        {"role": "user", "content": "Give me a suggestion for this vulnerability"}
    ]
}

# Make your request and handle the response
response = llama.run(api_request_json)
print(json.dumps(response.json(), indent=2))
