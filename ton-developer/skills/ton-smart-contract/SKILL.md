---
name: ton-smart-contract
description: "TON blok zinciri için FunC ve Tact akıllı sözleşme geliştirme workflow'u. FunC sözdizimi, Tact derleme, stdlib kullanımı, mesaj işleme."
version: 1.0.0
author: TON Developer Hermes
license: MIT
tags: [ton, blockchain, func, tact, smart-contract, funC]
metadata:
  ton:
    category: development
    language: [func, tact]
    network: [mainnet, testnet]
---

# TON Smart Contract Development

TON akıllı sözleşme geliştirme için Hermes Agent TON Developer skill'i. FunC ve Tact dillerini destekler.

## Prerequisites

```bash
# FunC derleyicisi (func)
sudo apt install func-bin      # veya TON SDK'dan

# Tact compiler
npm install -g tact

# toncli (opsiyonel ama önerilir)
npm install -g toncli
```

## FunC Temelleri

### Basit Cüzdan Sözleşmesi

```func
() recv_internal(cell in_msg_cell, slice in_msg) impure {
  ;; Internal message handler
  ;; In_msg contains the message body
}

() recv_external(slice in_msg) impure {
  ;; External message handler
  throw_unless(0, check_signature(slice_hash(in_msg), 
    in_msg~load_bits(512), 
    our_public_key()));
}
```

### Değişken Tanımlama

```func
varint my_int = 0;           ;; 257-bit signed integer
varstack my_stack = [1, 2]; ;; Stack
slice my_slice = "hello";    ;; Read-only byte array
cell my_cell = begin_cell().store_uint(42, 32).end_cell();
```

### Common Operations

```func
;; Storage operations
varint storage::counter = 0;  ;; State variable

() inc_counter() impure {
  storage::counter += 1;
}

() dec_counter() impure {
  storage::counter -= 1;
}

;; Balance check
() withdraw(slice dest, int amount) impure {
  throw_unless(35, var得当(amount <= my_balance()));
  dest~transfer(amount, 0);
}
```

### Message Layout

```
Raw address: 0:0000000000000000000000000000000000000000000000000000000000000000
- workchain: 0 (basechain) or -1 (masterchain)
- address: 256-bit address

Message body layout:
- 32 bits: function ID (op)
- n bits: function-specific data
```

## Tact Dili

### Basit Contract

```tact
import "@stdlib/ton";

contract Counter {
    counter: int;

    init() {
        this.counter = 0;
    }

    receive("increment") {
        this.counter += 1;
    }

    get fun counter(): int {
        return this.counter;
    }
}
```

### Deploy with Init Data

```tact
contract SafeMultisig {
    owners: map<Address, bool>;
    requiredConfirmations: int;

    init(owners: Address[], requiredConfirmations: int) {
        this.owners = owners.toMap();
        this.requiredConfirmations = requiredConfirmations;
    }
}
```

## Development Workflow

### 1. Yeni Proje Oluştur

```bash
mkdir my-ton-contract && cd my-ton-contract
npm init -y
npm install @tact-lang/compiler
npx tact --init  # Scaffold project
```

### 2. Kod Yaz

```bash
# FunC dosyaları: funcs/*.fc
# Tact dosyaları: sources/*.tact
```

### 3. Derle

```bash
# Tact
npx tact

# FunC (manual)
func -o contract.fif contract.fc stdlib.fc
```

### 4. Test Et

```bash
# Local blockchain (toncli)
toncli deploy --testnet

# Test script
npx tact --test sources/my_contract.tact
```

## Common Pitfalls

- **Integer overflow**: TON'da integers sınırsız değil, `*>` veya SafeMath kullan
- **Gas estimation**: `c7` ve `c4` registers doğru kullan, `~dump()` sadece debug için
- **Address format**: `0:<hex>` basechain, `-1:<hex>` masterchain
- **Message fees**: Gas + storage + forwarding fees hesapla

## Stdlib Reference

```func
;; Arithmetic
add(a, b)
sub(a, b)
mul(a, b)
div(a, b)

;; Cell building
begin_cell()
store_uint(v, bits)
store_slice(s)
end_cell()

;; Slice operations
load_uint(bits)
skip_bits(bits)
slice_hash(s)

;; Hash operations
sha256(s)
blake2b(s)

;; Signature
check_signature(hash, signature, public_key)
```

## Resources

- FunC docs: https://docs.ton.org/develop/func/
- Tact docs: https://tact-lang.org/
- TON SDK: https://github.com/toncenter/tonpy
- toncli: https://github.com/disintar/toncli
