---
name: ton-smart-contract
description: "TON blok zinciri için Tolk ve Blueprint ile akıllı sözleşme geliştirme. Tolk dili, Blueprint CLI, test, debug ve deployment workflow."
version: 1.0.0
author: TON Developer Hermes
license: MIT
tags: [ton, blockchain, tolk, blueprint, smart-contract]
metadata:
  ton:
    category: development
    language: [tolk]
    network: [mainnet, testnet]
---

# TON Smart Contract Development

TON akıllı sözleşme geliştirme için Hermes Agent TON Developer skill'i. **Tolk** dili ve **Blueprint** toolkit'i kullanılır.

## Prerequisites

```bash
# Node.js v22+ gerekli
node -v  # v22.x.x kontrol et

# Blueprint (TON'un resmi geliştirme toolkit'i)
npm install -g @ton/blueprint

# TON wallet (testnet için gerekli)
# https://ton.org/ wallet indir, testnet TON al
```

## Tolk Dili (Önerilen)

Tolk, FunC'in üzerine inşa edilmiş modern bir dildir ve daha güvenli bir geliştirme deneyimi sunar.

### Basit Contract Örneği

```tolk
import "@stdlib/deploy";

contract Counter with Deployable {
    counter: Int as uint32;

    init() {
        self.counter = 0;
    }

    receive("increment") {
        self.counter = self.counter + 1;
    }

    get fun counter(): Int {
        return self.counter;
    }
}
```

### Deploy with Init Data

```tolk
import "@stdlib/deploy";

contract SafeMultisig with Deployable {
    owners: map<Address, Int>;
    requiredConfirmations: Int;

    init(owners: Address[], requiredConfirmations: Int) {
        self.owners = owners.toMap();
        self.requiredConfirmations = requiredConfirmations;
    }
}
```

## Development Workflow

### 1. Yeni Proje Oluştur (Blueprint)

```bash
# Boş proje
npm create ton@latest -- MyContract --contractName MyContract --type tolk-empty

# Önceden hazırlanmış şablonlarla
npm create ton@latest -- MyContract --contractName MyContract --type tolk # Standart
npm create ton@latest -- MyContract --contractName MyContract --type funcs  # FunC (eski)
```

### 2. Proje Yapısı

```
MyContract/
├── contracts/
│   └── my_contract.tolk          # Ana sözleşme dosyası
├── scripts/
│   └── deploy.ts                 # Deployment scripti
├── tests/
│   └── my_contract.spec.ts       # Test dosyaları
└── blueprint.config.ts           # Blueprint yapılandırması
```

### 3. Kod Yaz

```bash
# contracts/ dizinine .tolk dosyaları ekle
```

### 4. Derle

```bash
npx blueprint build
```

### 5. Test Et

```bash
# Testleri çalıştır
npx blueprint test

# Detaylı output için
npx blueprint test --verbose
```

### 6. Debug

```bash
# Debug mode
npx blueprint debug

# TVM instruction trace
npx blueprint trace
```

### 7. Deploy

```bash
# Testnet'e deploy
npx blueprint deploy --testnet

# Mainnet'e deploy (onay gerektirir)
npx blueprint deploy --mainnet
```

## Blueprint CLI Komutları

```bash
# Proje oluştur
npx blueprint create

# Derle
npx blueprint build

# Test
npx blueprint test

# Debug
npx blueprint debug

# Deploy
npx blueprint deploy

# Get methods çağır
npx blueprint run get_method <address> <method_name> [args]

# Trace
npx blueprint trace <address>
```

## Common Pitfalls

1. **Gas estimation**: TON'da gas = compute + forward fees. `~dump()` sadece debug için.
2. **Address format**: `0:<hex>` basechain, `-1:<hex>` masterchain
3. **Message fees**: Minimum 0.05 TON transfer için, deploy daha fazla gerektirir
4. **Integer overflow**: Tolk otomatik checked arithmetic yapar, FunC'ten farklı

## Resources

- TON Docs: https://docs.ton.org/
- Blueprint: https://docs.ton.org/develop/smart-contracts/sdk/typescript/blueprint
- Tolk: https://docs.ton.org/develop/tolk/
- FunC (eski): https://docs.ton.org/develop/func/
