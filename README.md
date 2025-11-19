# Rasm_tiklovchi
Eskirgan yuz qiyofasi bor rasmlarni GFP-GAN va Real-Esrgan texnologiyalari yordamida qayta tiklovchi dastur.
# AI Photo Restorer — GFPGAN + Real-ESRGAN (Tkinter Desktop App)

**AI Photo Restorer** — eski, sifatli bo‘lmagan yoki shikastlangan suratlarni tiklash uchun GFPGAN + Real-ESRGAN texnologiyalaridan foydalanadigan desktop (Windows) ilovasi.  
Interfeys zamonaviy, ishlash tez, natija yuqori sifatli.

---

## Asosiy imkoniyatlar

- **GFPGAN 1.4** — yuzni tabiiy, aniq va original shaklga eng yaqin holda tiklaydi  
- **Real-ESRGAN x4** — umumiy rasm sifatini oshiradi (shum yo‘qoladi, detallari to‘ldiriladi)  
- GUI (Tkinter) — aniq, sodda va zamonaviy interfeys  
- CPU va GPU (CUDA) qo‘llab-quvvatlashi  
- Tiklangan rasmni **foydalanuvchi tanlagan papkaga saqlash**  
- Windows uchun .exe yaratish mumkin (PyInstaller orqali)

---

## O‘rnatish

### 1. Repository’ni yuklash

```bash
git clone https://github.com/yourusername/ai-photo-restorer.git
cd ai-photo-restorer

2. Virtual muhiti yaratish
Windows
python -m venv .venv
.venv\Scripts\activate

3. Kerakli kutubxonalarni o‘rnatish
pip install -r requirements.txt

Model og‘irliklarini yuklab olish (MUHIM)
Model fayllari:
- GFPGANv1.4.pth → [Yuklab olish havolasi](https://github.com/TencentARC/GFPGAN/releases/download/v1.4.0/GFPGANv1.4.pth)
- RealESRGAN_x4plus.pth → [Yuklab olish havolasi](https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth)
Ushbu fayllarni `./weights/` papkasiga joylashtiring.


Model og‘irliklar repository’da yo'q, ularni qo‘lda yuklab olib weights/ papkaga joylashtirasiz:

GFPGANv1.4.pth

Yuklab olish:
https://github.com/TencentARC/GFPGAN/releases/tag/v1.3.0

Joylash joyi:
weights/GFPGANv1.4.pth

RealESRGAN_x4plus.pth

Yuklab olish:
https://github.com/xinntao/Real-ESRGAN/releases

Joylash joyi:
weights/RealESRGAN_x4plus.pth

Dasturni ishga tushirish
python gui.py

GUI ochiladi va siz:

Rasm tanlaysiz

“Tiklash” tugmasini bosasiz

Natija o‘zingiz tanlagan papkaga saqlanadi

.EXE fayl yaratish (Windows)

PyInstaller o‘rnating:

pip install pyinstaller


Build qiling:

pyinstaller --name "AI Photo Restorer" --windowed --onefile gui.py


Yakuniy .exe fayl:
dist/AI Photo Restorer.exe

Loyihaning tuzilishi
ai-photo-restorer/
│           
├─ restoration.py              
├─ requirements.txt
├─ README.md
│
├─ weights/                    
│   ├─ GFPGANv1.4.pth
│   └─ RealESRGAN_x4plus.pth
│
├─ examples/                   
└─ results/                    

Litsenziya

Bu loyiha MIT License asosida tarqatiladi.
GFPGAN va Real-ESRGAN mualliflariga tegishli materiallar o‘z litsenziyalariga ko‘ra qo‘llaniladi.

Rahmat

Loyihada foydalanilgan texnologiyalar:

GFPGAN — https://github.com/TencentARC/GFPGAN

Real-ESRGAN — https://github.com/xinntao/Real-ESRGAN

ESRGAN & BasicSR — Xintao et al.

Muallif

Sultonov Sardorbek Qudrat o'g'li
Email: sardorbeksultonov@gmail.com
