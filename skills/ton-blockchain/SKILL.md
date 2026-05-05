---
name: ton-blockchain
description: "TON blok zinciri ile etkileşim: tonapi.js, REST API, wallet interaction, balance sorgulama, transaction gönderme."
version: 1.0.0
author: TON Developer Hermes
license: MIT
tags: [ton, blockchain, api, wallet, tonapi, toncenter]
metadata:
  ton:
    category: blockchain-interaction
    network: [mainnet, testnet]
---

# TON Blockchain Interaction

TON blok zinciri ile etkileşim için skill. API'ler, wallet işlemleri, balance sorguları ve transaction yönetimi.

## Prerequisites

```bash
# Node.js SDK (tonapi.js)
npm install @ton-api/client

# veya toncenter API için
npm install @toncenter/tonapi-js
```

## TON API Uç Noktaları

### TonAPI (Resmi SDK)

```javascript
import { TonApiClient } from "@ton-api/client";

const client = new TonApiClient({
  baseUrl: "https://tonapi.io",  // veya testnet: "https://testnet.tonapi.io"
  apiKey: "YOUR_API_KEY"        // https://tonconsole.com'dan al
});
```

### TonCenter HTTP API

```
Mainnet: https://toncenter.com/api/v2/
Testnet: https://testnet.toncenter.com/api/v2/
```

### API Key Alma

1. https://tonconsole.com adresine git
2. API key oluştur
3. Free tier: 10 req/s rate limit

## Yaygın İşlemler

### Balance Sorgula

```javascript
// TonApiClient ile
const client = new TonApiClient({ apiKey: "YOUR_KEY" });
const account = await client.accounts.get("EQDj...");
console.log(account.balance); // nanoTON cinsinden
```

```bash
# HTTP API ile
curl "https://tonapi.io/v2/accounts/EQDj..." \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### TON Transfer Et

```javascript
const { TonClient } = require("@ton/ton");
const { mnemonicToWalletKey } = require("@ton-crypto/mnemonic");

async function transfer() {
  const key = await mnemonicToWalletKey("word1 word2 ... words24".split(" "));
  const wallet = UserWallet.create({ workchain: 0, publicKey: key.publicKey });
  
  const client = new TonClient({ endpoint: "https://tonapi.io" });
  
  await client.sendTransaction({
    from: wallet.address,
    to: "EQDj...receiver...",
    amount: "1000000000", // 1 TON nanoTON cinsinden
    secretKey: key.secretKey
  });
}
```

### Transaction Geçmişi

```javascript
const transactions = await client.accounts.getTransactions("EQDj...", {
  limit: 10
});

for (const tx of transactions) {
  console.log(tx.utime, tx.in_msg.source, tx.out_msg[0]?.dst);
}
```

### Get Method Çalıştır

```bash
# CLI ile
npx blueprint run get_method <address> seqno

# HTTP API ile
curl -X POST "https://tonapi.io/v2/runGetMethod" \
  -H "Content-Type: application/json" \
  -d '{
    "address": "EQDj...",
    "method": "seqno",
    "stack": []
  }'
```

## Wallet Entegrasyonu

### Tonkeeper/TON Space Wallet

```javascript
// TON Connect ile wallet bağlantısı
import { TonConnectUI } from "@tonconnect/ui";

const tonConnectUI = new TonConnectUI({
  manifestUrl: "https://your-app.com/tonconnect-manifest.json",
  buttonRootId: "ton-connect-btn"
});

// Bağlı wallet adresi
tonConnectUI.account?.address
```

### Jetton Transfer

```javascript
const jettonWallet = await client.accounts.getJettonWallet(
  "EQC...jetton_master...",
  "EQD...user_wallet..."
);

await jettonWallet.transfer({
  amount: "1000000", // Jetton decimals cinsinden
  destination: "EQD...receiver...",
  responseAddress: "EQD...sender..."
});
```

## Testnet Kullanımı

```javascript
// Testnet client
const testnetClient = new TonApiClient({
  baseUrl: "https://testnet.tonapi.io",
  apiKey: "YOUR_TESTNET_KEY"
});

// Test TON alma: https://t.me/tonfaqbot -> /testnet
```

## Rate Limits

| Plan | Free | Pro |
|------|------|-----|
| Requests/sec | 10 | 100 |
| Daily limit | 10,000 | Unlimited |

## Resources

- TonAPI Docs: https://tonapi.io/
- TonAPI SDK: https://www.npmjs.com/package/@ton-api/client
- TonConsole (API keys): https://tonconsole.com/
- Testnet Faucet: https://t.me/tonfaqbot
