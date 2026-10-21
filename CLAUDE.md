# Proje kuralları

## Karar aşamasında Drex'e yönlendirme

Birden fazla makul seçenek arasında seçim yapman gereken her karar anında (yaklaşım, kütüphane, mimari, araç, kapsam vb.) kararı kendin vermeden önce **Drex**'e danış:

1. Oturumda Drex adında bir MCP aracı (`mcp__drex__*`) varsa onu kullan.
2. Yoksa bu repodaki `drex` alt ajanını (`.claude/agents/drex.md`) Agent aracıyla çağır. Ona kararı, seçenekleri ve ilgili bağlamı ver.
3. İkisi de yoksa bunu kullanıcıya bir satırla söyle ve aynı ilkeyle kendin karar ver.

Drex'in önerisini uygula. Uygulamadan sapacaksan nedenini kullanıcıya söyle.

Önemsiz, tek doğru cevabı olan ya da yerleşik bir varsayılanı olan seçimler için Drex'i çağırma.

İlke: **Balyozla sinek kovalanmaz, sineklik kullanılır.** İşi gören en hafif çözüm seçilir.
