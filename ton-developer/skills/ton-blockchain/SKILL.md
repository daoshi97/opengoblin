---
name: ton-blockchain
description: "TON blok zinciri ile etkileşim: toncenter API, tonapi.js, wallet interaction, balance sorgulama, transaction gönderme."
version: 1.0.0
author: TON Developer Hermes
license: MIT
tags: [ton, blockchain, api, wallet, toncenter, tonapi]
metadata:
  ton:
    category: blockchain-interaction
    network: [mainnet, testnet]
---

# TON Blockchain Interaction

TON blok zinciri ile etkileşim için skill. API'ler, wallet işlemleri, balance sorguları ve transaction yönetimi.

## Prerequisites

```bash
# Python SDK
pip install tonpy

# Node.js SDK  
npm install @ton-api/client

# CLI tool
npm install -g toncli
```

## TON Center API

### Base URLs

```
Mainnet: https://toncenter.com/api/v2/
Testnet: https://testnet.toncenter.com/api/v2/
```

### Get Account Info

```bash
# cURL
curl -X GET "https://testnet.toncenter.com/api/v2/getAddressInformation?address=0:0000000000000000000000000000000000000000000000000000000000000000"

# Python (tonpy)
python3 << 'EOF'
from tonpy import Tonapi

ta = Tonapi(api_key="your_api_key", testnet=True)
info = ta.get_address_info("0:0000000000000000000000000000000000000000000000000000000000000000")
print(info)
EOF
```

### Get Balance

```bash
# CLI
toncli balance 0:ADDRESS --testnet

# Python
python3 << 'EOF'
from tonpy import Tonapi
ta = Tonapi(api_key="your_key", testnet=True)
balance = ta.get_balance("0:ADDRESS")
print(f"Balance: {balance['balance']} nanoTON")
EOF
```

### Send Transaction

```python
from tonpy import Tonapi, Contract

ta = Tonapi(api_key="your_key", testnet=True)
wallet = Contract.from_seed(secret_key=seed_phrase, version="v3r2")

# Transfer
result = wallet.transfer(
    to="0:ADDRESS",
    amount=1_000_000_000,  # 1 TON in nanoTON
    payload="Hello TON!"
)
print(result)
```

## TonAPI.js (Node.js)

### Setup

```javascript
import { TonClient } from "@ton-api/client";

const client = new TonClient({
  endpoint: "https://testnet.tonapi.io",
  apiKey: "YOUR_API_KEY"
});
```

### Get Wallet Data

```javascript
// Get account balance
const balance = await client.accounts.getBalance({
  address: "0:0000000000000000000000000000000000000000000000000000000000000000"
});
console.log(`Balance: ${balance.balance} nanoTON`);

// Get transactions
const transactions = await client.blocks.getTransactions(...)
```

### Send Ton

```javascript
import { fromNano, toNano } from "@ton-api/client";

// Transfer
const transfer = await client.wallet.send({
  secretKey: Buffer.from(seed),
  messages: [{
    address: "0:RECIPIENT...",
    amount: toNano("1.0"),  // 1 TON
    body: "Payment for services"
  }]
});
```

## Wallet Integration

### Supported Wallet Types

| Version | Description | Contract Address |
|---------|-------------|-----------------|
| v3r2 | Most common | `EQDjCCDbAe-s-2NSubRtTn0RJ6_qf4O_OmqCcmN83SmSK11N` |
| v4r2 | High load | `EQDwqK-rYl1cQ9_pKgr3YmJfLB_Pv7ONOK5qZ1A0R3Z9p7H9` |
| multisig | Multi-sig | `EQD___________________________` |

### Create Wallet

```bash
# toncli
toncli wallet create my_wallet --testnet
# Output: seed phrase, wallet address

# Python
from tonpy import Wallet
w = Wallet.new()
print(f"Seed: {w.mnemonic}")
print(f"Address: {w.address}")
```

### Export/Import

```python
# Export
seed = wallet.mnemonic  # 24 words

# Import
from tonpy import Wallet
w = Wallet.from_mnemonic(seed)
```

## Common Operations

### Deploy Contract

```bash
# toncli
toncli deploy --wallet my_wallet --testnet

# With init data
toncli deploy --wallet my_wallet --wc 0 --init-code code.cell --init-data data.cell
```

### Call Method

```bash
# Read-only (get method)
toncli run --method get_counter --address CONTRACT_ADDR

# External message
toncli send --method submitTransaction --dest CONTRACT --body DATA
```

### NFT Operations

```javascript
// Mint NFT
const mint = await client.nft.sendNftMint({
  collection: "0:COLLECTION...",
  amount: toNano("0.05"),
  ...data
});

// Transfer NFT
await client.nft.transferNft({
  nft: "0:NFT_ITEM...",
  to: "0:RECIPIENT...",
  from: "0:OWNER...",
  forwardAmount: toNano("0.01")
});
```

## Jetton (Token) Operations

### Get Jetton Balance

```javascript
const jetton = await client. jetton.getBalance({
  address: "0:WALLET...",
  jetton: "0:JETTON_MASTER..."
});
console.log(`Jetton balance: ${jetton.balance}`);
```

### Transfer Jetton

```javascript
await client. jetton.transfer({
  secretKey: Buffer.from(seed),
  to: "0:RECIPIENT...",
  jettonMaster: "0:JETTON_MASTER...",
  amount: 1_000_000n,  // Decimals'e göre
  forwardAmount: toNano("0.01")
});
```

## API Rate Limits

```
Public testnet API: ~10 req/sec
With API key: ~100 req/sec
Premium: Unlimited
```

## Error Handling

```python
from tonpy.exceptions import TonException

try:
    result = ta.get_balance("invalid_address")
except TonException as e:
    print(f"Error: {e.code} - {e.message}")
```

Common errors:
- `-13`: Account not found
- `-14`: Invalid address
- `-15`: Wrong signature
- `-37`: Not enough balance
