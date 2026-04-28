import customtkinter as ctk
import json
import os
import tkinter.messagebox as messagebox
import socket
import requests

# --- SETUP TEMA ---
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

CONFIG_FILE = "config.json"

class AppConfig(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("⚙️ Konfigurasi Mesin Absensi")
        self.geometry("480x700") 
        self.resizable(False, False)

        # ==========================================
        # 1. INISIALISASI VARIABEL STATE
        # ==========================================
        self.api_url_var = ctk.StringVar(value="")
        self.sync_url_var = ctk.StringVar(value="")
        self.det_model_var = ctk.StringVar(value="hog")
        self.source_var = ctk.StringVar(value="Webcam Laptop (0)")
        self.rtsp_url_var = ctk.StringVar(value="")
        self.company_var = ctk.StringVar(value="DMO")
        self.lat_var = ctk.StringVar(value="-7.7693546") 
        self.lng_var = ctk.StringVar(value="110.3956848")
        self.city_var = ctk.StringVar(value="Yogyakarta")
        self.ip_var = ctk.StringVar(value=self.get_current_ip())

        # ==========================================
        # 2. LOAD DATA DARI JSON (JIKA ADA)
        # ==========================================
        self.load_config()

        # ==========================================
        # 3. MEMBANGUN UI (USER INTERFACE)
        # ==========================================
        # Judul Utama (Fixed di atas)
        self.lbl_title = ctk.CTkLabel(self, text="Konfigurasi Mesin & Lokasi", font=ctk.CTkFont(size=20, weight="bold"))
        self.lbl_title.pack(pady=(20, 10))

        # Container Scrollable untuk Form
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # --- SECTION: API ENDPOINTS ---
        self.create_label("Attendance API URL (POST):", master=self.scroll_frame)
        ctk.CTkEntry(self.scroll_frame, textvariable=self.api_url_var, placeholder_text="https://api.perusahaan.com/v1/attendance", width=370).pack(pady=5)

        self.create_label("Sync API URL (GET):", master=self.scroll_frame)
        ctk.CTkEntry(self.scroll_frame, textvariable=self.sync_url_var, placeholder_text="https://api.perusahaan.com/v1/karyawan/sync", width=370).pack(pady=5)

        # --- SECTION: KAMERA & AI ---
        self.create_label("Pilih Sumber Kamera:", master=self.scroll_frame)
        self.dropdown_source = ctk.CTkOptionMenu(
            self.scroll_frame, variable=self.source_var,
            values=["Webcam Laptop (0)", "Webcam External (1)", "CCTV RTSP"],
            command=self.on_source_change, width=370
        )
        self.dropdown_source.pack(pady=5)

        # Frame RTSP Dinamis
        self.frame_rtsp = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        self.create_label("URL RTSP:", master=self.frame_rtsp)
        self.entry_rtsp = ctk.CTkEntry(self.frame_rtsp, textvariable=self.rtsp_url_var, placeholder_text="rtsp://...", width=370)
        self.entry_rtsp.pack(pady=5)
        self.on_source_change(self.source_var.get()) # Trigger awal untuk RTSP

        self.create_label("Model Deteksi AI:", master=self.scroll_frame)
        self.dropdown_model = ctk.CTkOptionMenu(
            self.scroll_frame, variable=self.det_model_var,
            values=["hog", "cnn"], width=370
        )
        self.dropdown_model.pack(pady=5)

        # --- SECTION: LOKASI & PERUSAHAAN ---
        self.create_label("Company Code:", master=self.scroll_frame)
        ctk.CTkEntry(self.scroll_frame, textvariable=self.company_var, width=370).pack(pady=5)

        self.create_label("Latitude:", master=self.scroll_frame)
        ctk.CTkEntry(self.scroll_frame, textvariable=self.lat_var, width=370).pack(pady=5)

        self.create_label("Longitude:", master=self.scroll_frame)
        ctk.CTkEntry(self.scroll_frame, textvariable=self.lng_var, width=370).pack(pady=5)

        self.create_label("City:", master=self.scroll_frame)
        ctk.CTkEntry(self.scroll_frame, textvariable=self.city_var, width=370).pack(pady=5)

        # --- SECTION: JARINGAN ---
        self.create_label("IP Address Mesin:", master=self.scroll_frame)
        self.ip_entry = ctk.CTkEntry(self.scroll_frame, textvariable=self.ip_var, width=370)
        self.ip_entry.pack(pady=(5, 20)) # Padding bawah lebih besar

        # Tombol Save (Fixed di bawah, di luar scroll frame)
        self.btn_save = ctk.CTkButton(self, text="💾 Simpan Konfigurasi", command=self.save_config, width=370, height=45)
        self.btn_save.pack(side="bottom", pady=20)

    # ==========================================
    # 4. FUNGSI LOGIKA (METHODS)
    # ==========================================
    def create_label(self, text, master=None):
        m = master if master else self
        lbl = ctk.CTkLabel(m, text=text, font=ctk.CTkFont(size=13, weight="bold"))
        lbl.pack(anchor="w", padx=30, pady=(10, 0))

    def get_current_ip(self):
        try:
            return requests.get('https://api.ipify.org', timeout=3).text
        except:
            return socket.gethostbyname(socket.gethostname())

    def on_source_change(self, choice):
        if choice == "CCTV RTSP":
            self.frame_rtsp.pack(fill="x", pady=0)
        else:
            self.frame_rtsp.pack_forget()

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    data = json.load(f)
                    self.api_url_var.set(data.get("api_url", ""))
                    self.sync_url_var.set(data.get("sync_url", ""))
                    self.source_var.set(data.get("video_source", "Webcam Laptop (0)"))
                    self.rtsp_url_var.set(data.get("rtsp_url", ""))
                    self.det_model_var.set(data.get("detection_model", "hog"))
                    self.company_var.set(data.get("company_code", "DMO"))
                    self.lat_var.set(data.get("latitude", "-7.7693546"))
                    self.lng_var.set(data.get("longitude", "110.3956848"))
                    self.city_var.set(data.get("city", "Yogyakarta"))
                    self.ip_var.set(data.get("ip_address", self.get_current_ip()))
            except Exception as e: 
                print(f"Gagal meload config: {e}")

    def save_config(self):
        data = {
            "api_url": self.api_url_var.get(),
            "sync_url": self.sync_url_var.get(),
            "video_source": self.source_var.get(),
            "rtsp_url": self.rtsp_url_var.get(),
            "detection_model": self.det_model_var.get(),
            "company_code": self.company_var.get(),
            "latitude": self.lat_var.get(),
            "longitude": self.lng_var.get(),
            "city": self.city_var.get(),
            "ip_address": self.ip_var.get()
        }
        with open(CONFIG_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        messagebox.showinfo("Sukses", "Konfigurasi Berhasil Disimpan!")
        self.destroy()

if __name__ == "__main__":
    app = AppConfig()
    app.mainloop()