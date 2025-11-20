# Agent Seçim Rehberi

## 🎯 Hangi Agent'ı Kullanmalıyım?

### Hızlı Karar

```
Production deployment? → run_batch_production.py ✅
State tracking gerekli? → about_graph.py
Test/Debug? → run_about_extraction.py
```

---

## 📊 Agent Karşılaştırması

| Özellik | Production Batch | LangGraph | Simple Batch |
|---------|-----------------|-----------|--------------|
| **Hız** | ⚡⚡⚡ (5 worker) | ⚡ (Sıralı) | ⚡ (Sıralı) |
| **Retry** | ✅ 3 deneme | ❌ | ❌ |
| **Rate Limit** | ✅ 20/dk | ❌ | ❌ |
| **Logging** | ✅ File+Console | Print | Print |
| **İstatistik** | ✅✅ JSON | ✅ Temel | ✅ Temel |
| **Production** | ✅✅ | ⚠️ | ❌ |

---

## 🚀 Kullanım Örnekleri

### Production Deployment
```bash
# En hızlı ve güvenilir
python src/agents/run_batch_production.py

# Çıktı:
# 🚀 Starting production batch extraction...
# 👥 Max Workers: 5
# 🔄 Retry Count: 3
# ⏱️  Rate Limit: 20 req/min
#
# [1/100] ✅ file1.md (2.34s)
# [2/100] ✅ file2.md (1.89s)
# ...
# 📊 Success Rate: 95.0%
```

### LangGraph Workflow
```bash
# State tracking ile
python src/agents/about_graph.py

# Çıktı:
# 🚀 Starting LangGraph extraction workflow...
# 📁 Listing markdown files...
# [1/10] Processing: file1.md
# ✓ Extracted: Mustermann GmbH
```

### Simple Testing
```bash
# Basit ve anlaşılır
python src/agents/run_about_extraction.py

# Çıktı:
# 🚀 Starting batch extraction...
# [1/10] Processing: file1.md
# ✓ Extracted: Mustermann GmbH
```

---

## 💡 Performans

**100 dosya için:**
- Production Batch: ~4-5 dakika (95%+ başarı)
- LangGraph: ~12-15 dakika (95% başarı)
- Simple Batch: ~12-15 dakika (90% başarı)

---

## 🔧 Konfigürasyon

### Yüksek Hacim
```bash
# .env
EXTRACTION_MAX_WORKERS=10
RATE_LIMIT_REQUESTS_PER_MINUTE=60
```

### Düşük API Quota
```bash
# .env
EXTRACTION_MAX_WORKERS=2
RATE_LIMIT_DELAY_BETWEEN_REQUESTS=6
```

---

**🎉 Öneri**: %90+ durumda **Production Batch** kullanın!
