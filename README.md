# Türkçe Teknik Doküman Asistanı

Teknik PDF dosyaları üzerinden soru sormayı sağlayan basit bir RAG/LLM projesidir. PDF içindeki metin parçalara ayrılır, soruyla en alakalı bölümler embedding kullanılarak bulunur ve bu bilgiler LLM'e verilerek cevap oluşturulur.

## Çalıştırma

Gerekli paketleri yükleyin:

```bash
pip install -r requirements.txt
