# TON Developer Fork - Hermes Agent

Hermes Agent'ın TON blok zinciri geliştiricileri için özelleştirilmiş fork'u.

## Özellikler

- **TON Smart Contract Geliştirme** - Tolk dili ve Blueprint toolkit'i ile akıllı sözleşme geliştirme
- **TON Blockchain Etkileşimi** - TonAPI ile balance sorgulama, transfer, transaction yönetimi
- **Deployment Workflow** - Testnet ve mainnet deploy araçları

## Kurulum

### 1. Hermes Agent'ı Çalıştır

```bash
hermes --profile ton-developer
```

### 2. Environment Variables

`.env` dosyası oluştur (veya export et):

```bash
export TONAPI_API_KEY="your_api_key_from_tonconsole.com"
export TON_DEFAULT_NETWORK=testnet  # veya mainnet
```

### 3. Bağımlılıklar

```bash
# Node.js v22+ gerekli
node -v

# Blueprint (TON smart contract geliştirme)
npm install -g @ton/blueprint

# Python dependencies (MCP server için)
pip install tonpy
```

## TON API Key Alma

1. https://tonconsole.com adresine git
2. Hesap oluştur
3. API Keys bölümünden yeni key oluştur
4. Free tier: 10 req/s rate limit

## Kullanım

### Smart Contract Geliştirme

```bash
# Yeni proje oluştur
npx blueprint create

# Derle
npx blueprint build

# Test
npx blueprint test

# Deploy
npx blueprint deploy --testnet
```

### Hermes Agent Komutları

```
# Balance sorgula
Balance sorgula: EQDj...adres...

# Smart contract deploy
TON'da yeni bir jetton deploy et

# Get method çalıştır
Contract'ta seqno metodunu çağır
```

## Proje Yapısı

```
ton-developer/
├── config.yaml          # Hermes profile yapılandırması
├── ton_mcp_server.py    # TON MCP server (Python)
├── skills/
│   ├── ton-smart-contract/   # Smart contract geliştirme
│   ├── ton-blockchain/       # Blockchain etkileşimi
│   └── ton-deployment/       # Deployment workflow
└── .env.example         # Environment template
```

## Skills

### ton-smart-contract
Tolk dili ile akıllı sözleşme geliştirme. Blueprint CLI kullanımı, test ve debug araçları.

### ton-blockchain
TonAPI REST API ve SDK kullanımı. Balance sorgulama, TON transfer, transaction geçmişi.

### ton-deployment
Deploy workflow, fee estimation, contract initialization. Testnet ve mainnet deployment.

## Testnet Kullanımı

Test TON almak için:
1. Telegram'da @tonfaqbot'a git
2. `/start` yaz
3. `/testnet` yaz
4. Adresini ver

## Dokümantasyon

- [TON Docs](https://docs.ton.org/)
- [Blueprint](https://docs.ton.org/develop/smart-contracts/sdk/typescript/blueprint)
- [Tolk](https://docs.ton.org/develop/tolk/)
- [TonAPI](https://tonapi.io/)

## Lisans

MIT - Hermes Agent NousResearch fork'undan türetilmiştir.