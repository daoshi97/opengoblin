---
name: ton-deployment
description: "TON akıllı sözleşme deploy workflow'u: testnet/mainnet deployment, contract initialization, verification."
version: 1.0.0
author: TON Developer Hermes
license: MIT
tags: [ton, deploy, smart-contract, testnet, mainnet]
metadata:
  ton:
    category: deployment
    network: [testnet, mainnet]
---

# TON Smart Contract Deployment

TON blok zincirine akıllı sözleşme deploy etme workflow'u.

## Deployment Checklist

```
[ ] Contract kodu yazıldı/derlendi
[ ] Testnet'te test edildi
[ ] Gas maliyeti hesaplandı
[ ] Deployment wallet hazır (yeterli TON balance)
[ ] Init data hazırlandı
[ ] Mainnet deploy planlandı
```

## Testnet Deployment

### 1. Testnet Faucet

```bash
# TON Testnet token al
# https://t.me/tontest faucet bot
# veya
curl -X POST "https://testnet.toncenter.com/api/v2/requestCoins" \
  -d "address=0:YOUR_ADDRESS"
```

### 2. Compile Contract

```bash
# Tact
npx tact --output ./build

# FunC
func -o build/contract.fif funcs/contract.fc stdlib.fc
```

### 3. Deploy (toncli)

```bash
# Otomatik deploy
toncli deploy --wallet my_wallet --testnet

# Manuel (advanced)
toncli deploy --wallet my_wallet \
  --address 0:YOUR_DEPLOY_ADDRESS \
  --code ./build/contract.cell \
  --data ./build/contract-data.cell \
  --testnet
```

### 4. Verify

```bash
# Contract address kontrol
toncli info --address 0:DEPLOYED_ADDRESS --testnet

# Get methods çağır
toncli run --method get_counter --address 0:DEPLOYED_ADDRESS --testnet
```

## Mainnet Deployment

### 1. Prepare

```bash
# Mainnet wallet (soğuk cüzdan önerilir)
toncli wallet create deployer --mainnet

# Balance transfer et (minimum 1-2 TON için)
# Deployment fees: ~0.05-0.5 TON depending on contract size
```

### 2. Estimate Fees

```bash
toncli deploy --wallet deployer \
  --estimate-fees \
  --code ./build/contract.cell \
  --data ./build/contract-data.cell \
  --mainnet
```

### 3. Deploy

```bash
toncli deploy --wallet deployer \
  --code ./build/contract.cell \
  --data ./build/contract-data.cell \
  --mainnet \
  --verify  # Blockchain explorer'da doğrula
```

## Deployment with init code/data

### Prepare cells

```bash
# Boc formatında
npx tact --output ./build
ls build/*.cell

# Manuel
func --cell build/code.cell --data build/data.cell
```

### Deploy with custom params

```bash
toncli deploy \
  --wallet my_wallet \
  --wc 0 \               # Workchain (0 = basechain)
  --code build/code.cell \
  --init-code build/init-code.cell \
  --init-data build/init-data.cell \
  --testnet
```

## Contract Initialization

### State Init

```
StateInit = code + data + library (optional)
```

```python
from tonpy import Contract

# Create state init
state_init = Contract.create_state_init(
    code=code_cell,
    data=data_cell
)

# Get address
address = Contract.calc_address(
    state_init=state_init,
    workchain=0
)
print(f"Deploy to: {address}")
```

### Deploy Transaction

```python
from tonpy import Tonapi, Contract, Wallet

ta = Tonapi(api_key="key", testnet=True)
wallet = Wallet.from_mnemonic(mnemonic)

# Deploy
deploy = wallet.deploy(
    state_init=state_init,
    contract=contract,
    amount=toNano("0.5")  # Gas for deployment
)
print(deploy)
```

## Verification

### On-Chain Verify

```bash
# toncenter verify
curl -X POST "https://toncenter.com/api/v2/verifyContract" \
  -H "Content-Type: application/json" \
  -d '{
    "address": "0:DEPLOYED...",
    "compiler": "tact",
    "version": "1.0.0",
    "code": "base64_encoded_code",
    "init_data": "base64_encoded_data"
  }'
```

### Manual Verify

```bash
# Get contract code hash
toncli run --method "serialized" --address 0:CONTRACT --testnet

# Compare with local build
sha256sum build/contract.cell
```

## Fees Summary

| Operation | Approximate Cost |
|-----------|-----------------|
| Simple wallet deploy | 0.01 TON |
| NFT collection | 0.05-0.1 TON |
| DEX pair | 0.2-0.5 TON |
| Complex DeFi | 0.5-2 TON |

## Troubleshooting

### "Account exists"

```bash
# Already deployed, use existing address
# veya farklı address kullan
toncli wallet create new_contract --testnet
```

### "Not enough balance"

```
Deployment wallet'ında yeterli TON yok.
Testnet: Faucet'ten daha fazla token al.
Mainnet: Cüzdanı testnet'ten mainnet'e transfer et.
```

### "Invalid code"

```
- FunC: stdlib.fc import kontrol et
- Tact: versiyon uyumluluğu kontrol et  
- Cell format: .cell vs .fif dosyası karıştırma
```

## Auto-Deploy Scripts

```bash
#!/bin/bash
# deploy.sh
WALLET=$1
NETWORK=${2:-testnet}
CODE=./build/contract.cell
DATA=./build/data.cell

echo "Deploying to $NETWORK..."
toncli deploy \
  --wallet $WALLET \
  --code $CODE \
  --data $DATA \
  --$NETWORK

echo "Deployment complete!"
```
