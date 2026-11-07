# MIRA CPU Monitor v1.0

Windows, macOS ve Linux üzerinde işlemci ve bellek kullanımını gerçek zamanlı izleyen hafif bir masaüstü uygulaması.

## Özellikler

- Anlık toplam işlemci kullanımı ve son 90 saniyelik grafik
- Bellek kullanım oranı ve kullanılan/toplam bellek bilgisi
- Mantıksal çekirdek sayısı
- Türkçe arayüz ve saniyede bir otomatik yenileme

## Gereksinimler

- Python 3.9 veya üzeri
- Tkinter (çoğu Python kurulumunda dahildir; Linux'ta dağıtımınızın `python3-tk` paketini yüklemeniz gerekebilir)

## Kurulum ve çalıştırma

```bash
python -m venv .venv
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Bağımlılığı kurup uygulamayı başlatın:

```bash
python -m pip install -r requirements.txt
python main.py
```

## Lisans

Bu proje MIT Lisansı ile dağıtılır. Ayrıntılar için [LICENSE](LICENSE) dosyasına bakın.
