---
name: ton-deployment
description: "TON akıllı sözleşme deploy workflow: testnet/mainnet deployment, fee estimation, contract initialization."
version: 1.0.0
author: TON Developer Hermes
license: MIT
tags: [ton, blockchain, deployment, testnet, mainnet]
metadata:
  ton:
    category: deployment
    network: [mainnet, testnet]
---

# TON Deployment Workflow

TON akıllı sözleşme deployment rehberi. Testnet ve mainnet deploy işlemleri.

## Önemli Notlar

1. **Minimum balance**: Deploy için en az 0.5-1 TON gerekli
2. **Fee tahmini**: Blueprint ile önceden hesapla
3. **Testnet önce**: Mutlaka testnet'te test et
4. **State init**: Yeni contract için gerekli, mevcut contract için gereksiz

## Deployment Adımları

### 1. Hazırlık

```bash
cd my-ton-project

# .env dosyası oluştur
cat > .env << 'EOF'
TONAPI_API_KEY=your_api_key_here
WALLET_MNEMONIC="word1 word2 ... words24"
EOF
```

### 2. Derle

```bash
npx blueprint build
```

Çıktı: `build/MyContract.cell` ve `build/MyContract.fc`

### 3. Fee Tahmini

```bash
npx blueprint deploy --testnet --estimate
```

### 4. Testnet Deploy

```bash
# Mnemonic'i olan wallet ile
npx blueprint deploy --testnet

# Ledger gibi hardware wallet ile
npx blueprint deploy --testnet --ledger
```

### 5. Mainnet Deploy

```bash
# Dikkatli ol - gerçek TON gönderilecek!
npx blueprint deploy --mainnet
```

## Deployment Script (Programmatik)

```typescript
// scripts/deploy.ts
import { contractAddress } from "ton-core";
import { TonClient, CellMessage, InternalMessage, CommonMessageInfo } from "ton";
import { KeyPair, sign } from "ton-crypto";

export async function deploy() {
  const client = new TonClient({
    endpoint: "https://tonapi.io",
    apiKey: process.env.TONAPI_API_KEY
  });

  const keyPair: KeyPair = await mnemonicToKeyPair(
    process.env.WALLET_MNEMONIC!.split(" ")
  );

  // Contract cell'ini yükle
  const codeCell = Cell.fromBoc(
    require("fs").readFileSync("build/MyContract.cell")
  )[0];

  const dataCell = new CellMessage(); // Init data

  // State init oluştur
  const stateInit = { code: codeCell, data: dataCell };

  // Contract adresini hesapla
  const address = contractAddress(0, stateInit);

  console.log("Deploying to:", address);

  // Deploy transaction oluştur
  const message = new InternalMessage({
    info: new CommonMessageInfo({
      type: "internal",
      value: "1000000000", // 1 TON, deploy için yeterli
      dst: address,
      stateInit: stateInit
    }),
    body: new CellMessage()
  });

  // Imzalı transaction gönder
  // (Gerçek implementasyon ton-core veya tonapi client kullanır)
}
```

## Contract Çağırma (After Deploy)

```bash
# Get method
npx blueprint run get_method <address> counter

# External message gönder
npx blueprint send <address> <message_body>
```

## Troubleshooting

### "Insufficient balance"
- Cüzdan'da yeterli TON yok (min 0.5-1 TON)
- Testnet: https://t.me/tonfaqbot -> /testnet

### "Contract already exists"
- Bu adres zaten deploy edilmiş
- Yeni bir adres için yeni key pair oluştur

### "State init error"
- Init data yanlış
- `always inline` veya `init()` fonksiyonunu kontrol et

## Deployment Maliyeti (Tahmini)

| Ağ | Tipik Maliyet |
|-----|---------------|
| Testnet | Ücretsiz (test TON ile) |
| Mainnet | 0.05 - 0.5 TON |

Maliyet şunlara bağlı:
- Contract boyutu (code + data)
- Storage fees
- Gas (compute)

## Resources

- Blueprint Deploy: https://docs.ton.org/develop/smart-contracts/sdk/typescript/blueprint#deployment
- Fee Calculation: https://docs.ton.org/learn/fees
