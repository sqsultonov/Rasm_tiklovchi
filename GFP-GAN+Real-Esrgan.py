import os
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk, ImageFilter
import warnings

# === AI kutubxonalar ===
try:
    import torch
    import numpy as np
    from gfpgan import GFPGANer
    from realesrgan import RealESRGANer
    from basicsr.archs.rrdbnet_arch import RRDBNet
    MODELS_AVAILABLE = True
except ImportError as e:
    torch = None
    np = None
    GFPGANer = None
    RealESRGANer = None
    RRDBNet = None
    MODELS_AVAILABLE = False
    print(f"[WARNING] AI kutubxonalari yuklanmadi: {e}")

warnings.filterwarnings("ignore")


# === Gradient Background Class ===
class GradientFrame(tk.Canvas):
    def __init__(self, parent, color1, color2, **kwargs):
        super().__init__(parent, **kwargs)
        self.color1 = color1
        self.color2 = color2
        self.bind("<Configure>", self._draw_gradient)

    def _draw_gradient(self, event=None):
        self.delete("gradient")
        width, height = self.winfo_width(), self.winfo_height()
        (r1, g1, b1) = self.winfo_rgb(self.color1)
        (r2, g2, b2) = self.winfo_rgb(self.color2)
        r_ratio, g_ratio, b_ratio = (r2 - r1) / height, (g2 - g1) / height, (b2 - b1) / height
        for i in range(height):
            nr, ng, nb = int(r1 + (r_ratio * i)), int(g1 + (g_ratio * i)), int(b1 + (b_ratio * i))
            color = f"#{nr >> 8:02x}{ng >> 8:02x}{nb >> 8:02x}"
            self.create_line(0, i, width, i, fill=color, tags=("gradient",))
        self.lower("gradient")


# === Asosiy Ilova ===
class ModernAIRestorerApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("🎨 AI Rasm Tiklovchi Studio")
        self.root.geometry("1300x850")
        self.root.minsize(950, 650)

        # === Gradient fon ===
        self.bg = GradientFrame(root, "#1e1b4b", "#312e81")
        self.bg.pack(fill="both", expand=True)
        self.bg.bind("<Configure>", self._on_resize)

        # === Markaziy panel ===
        self.card = tk.Frame(self.bg, bg="#201f4a", highlightthickness=2, highlightbackground="#3f3f77")
        self.card.place(relx=0.5, rely=0.5, anchor="center")

        # === O'zgaruvchilar ===
        self.original_image = None
        self.restored_image = None
        self.input_path = None
        self.is_processing = False

        # Natijalar papkasi
        self.output_dir = os.path.join(os.getcwd(), "results", "restored_imgs")
        os.makedirs(self.output_dir, exist_ok=True)

        # Model yo'llari
        self.gfpgan_weights = r"D:\Granfather\GFPGAN\experiments\pretrained_models\GFPGANv1.4.pth"
        self.realesrgan_weights = r"D:\Granfather\GFPGAN\weights\RealESRGAN_x4plus.pth"

        # UI yaratish
        self._create_ui()

    def _create_ui(self):
        # Sarlavha
        header = tk.Label(self.card, text="🎨 AI Rasm Tiklovchi Studio",
                          font=("Segoe UI", 26, "bold"),
                          bg="#201f4a", fg="#a5b4fc")
        header.pack(pady=(25, 15))

        # Rasm oynalari
        img_frame = tk.Frame(self.card, bg="#2e2a67", bd=2, relief="flat")
        img_frame.pack(fill="both", expand=True, padx=25, pady=(5, 25))
        img_frame.columnconfigure((0, 1), weight=1)
        img_frame.rowconfigure(0, weight=1)

        self.left_label = tk.Label(img_frame, text="📥 Asl Rasm Yuklanmagan", bg="#0f172a",
                                   fg="#94a3b8", font=("Segoe UI", 12))
        self.left_label.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.right_label = tk.Label(img_frame, text="✨ Tiklangan Rasm Bu Yerda", bg="#0f172a",
                                    fg="#94a3b8", font=("Segoe UI", 12))
        self.right_label.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Progress va status
        self.progress = ttk.Progressbar(self.card, mode="indeterminate", length=450)
        self.progress.pack(pady=(0, 8))

        self.status_label = tk.Label(self.card, text="✨ Tayyor — rasmni tanlang!",
                                     bg="#201f4a", fg="#10b981", font=("Segoe UI", 13, "bold"))
        self.status_label.pack(pady=(0, 15))

        # Tugmalar
        button_frame = tk.Frame(self.card, bg="#201f4a")
        button_frame.pack(pady=(0, 25))

        self._create_button(button_frame, "📂 Rasm Tanlash", "#10b981", self.select_image)
        self._create_button(button_frame, "⚙️ Tiklashni Boshlash", "#6366f1", self.run_restore_thread)
        self._create_button(button_frame, "🗂️ Natijalar Papkasi", "#f59e0b", self.open_results_folder)

    def _create_button(self, frame, text, color, command):
        btn = tk.Button(frame, text=text, bg=color, fg="white",
                        font=("Segoe UI", 11, "bold"), relief="flat", bd=0,
                        activebackground=color, cursor="hand2", command=command)
        btn.pack(side="left", padx=12, ipadx=10, ipady=6)
        btn.bind("<Enter>", lambda e: btn.config(bg=self._darken(color)))
        btn.bind("<Leave>", lambda e: btn.config(bg=color))

    @staticmethod
    def _darken(color):
        color = color.lstrip("#")
        rgb = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))
        darker = tuple(max(0, int(c * 0.85)) for c in rgb)
        return f"#{''.join(f'{c:02x}' for c in darker)}"

    # === Funksiyalar ===
    def select_image(self):
        path = filedialog.askopenfilename(
            title="Rasmni tanlang",
            filetypes=[("Rasm fayllari", "*.jpg *.jpeg *.png *.bmp *.tiff *.webp")]
        )
        if not path:
            return
        try:
            img = Image.open(path)
            self.original_image = img
            self.input_path = path
            self._display_image(img, self.left_label)
            self.status_label.config(text=f"✅ Tanlandi: {os.path.basename(path)}", fg="#10b981")
        except Exception as e:
            messagebox.showerror("Xato", f"Rasmni ochishda xatolik: {e}")

    def run_restore_thread(self):
        if not self.input_path:
            messagebox.showerror("Xato", "❌ Iltimos, rasm tanlang!")
            return
        if self.is_processing:
            return
        self.is_processing = True
        self.status_label.config(text="🎨 Tiklanmoqda... bu biroz vaqt oladi", fg="#f59e0b")
        self.progress.start(15)
        threading.Thread(target=self._restore_process, daemon=True).start()

    def _restore_process(self):
        try:
            device = "cuda" if torch and torch.cuda.is_available() else "cpu"
            img_input = np.array(self.original_image.convert("RGB"))

            model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64,
                            num_block=23, num_grow_ch=32, scale=4)
            upsampler = RealESRGANer(scale=4, model_path=self.realesrgan_weights,
                                     model=model, device=device)
            restorer = GFPGANer(model_path=self.gfpgan_weights, upscale=2,
                                bg_upsampler=upsampler, device=device)

            _, _, restored_img = restorer.enhance(img_input, has_aligned=False,
                                                  only_center_face=False, paste_back=True)
            if restored_img is None:
                raise RuntimeError("Tiklash natijasi olinmadi.")

            self.restored_image = Image.fromarray(restored_img)
            self._display_image(self.restored_image, self.right_label)

            out_path = os.path.join(self.output_dir, f"restored_{os.path.basename(self.input_path)}")
            self.restored_image.save(out_path, quality=95)

            self.status_label.config(text="✅ Muvaffaqiyatli tiklandi!", fg="#10b981")
            messagebox.showinfo("Tayyor!", f"Rasm muvaffaqiyatli tiklandi!\n📁 {out_path}")

        except Exception as e:
            self.status_label.config(text="❌ Xato yuz berdi!", fg="#ef4444")
            messagebox.showerror("Xato", f"Jarayon davomida xatolik: {e}")
        finally:
            self.progress.stop()
            self.is_processing = False

    def _display_image(self, img: Image.Image, label: tk.Label):
        w, h = label.winfo_width() or 500, label.winfo_height() or 400
        img_copy = img.copy()
        img_copy.thumbnail((w - 20, h - 20), Image.Resampling.LANCZOS)
        tk_img = ImageTk.PhotoImage(img_copy.filter(ImageFilter.SMOOTH_MORE))
        label.config(image=tk_img, text="")
        label.image = tk_img

    def open_results_folder(self):
        path = os.path.abspath(self.output_dir)
        if not os.path.exists(path):
            os.makedirs(path)
        if sys.platform.startswith("win"):
            os.startfile(path)
        elif sys.platform.startswith("darwin"):
            os.system(f"open {path}")
        else:
            os.system(f"xdg-open {path}")

    def _on_resize(self, event):
        # Markaziy panelni avtomatik joylashtirish
        w, h = event.width, event.height
        cw, ch = min(1000, w * 0.75), min(700, h * 0.8)
        self.card.place_configure(width=cw, height=ch, relx=0.5, rely=0.5)


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernAIRestorerApp(root)
    root.mainloop()
