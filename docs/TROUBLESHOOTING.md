# 🔧 Troubleshooting Guide

## 📋 Daftar Isi

- [Masalah Umum](#masalah-umum)
- [Masalah Instalasi](#masalah-instalasi)
- [Masalah Server](#masalah-server)
- [Masalah GUI](#masalah-gui)
- [Masalah System Tray](#masalah-system-tray)
- [Masalah Konfigurasi](#masalah-konfigurasi)
- [Masalah Performance](#masalah-performance)
- [Error Messages](#error-messages)
- [FAQ](#faq)
- [Support](#support)

---

## 🚨 Masalah Umum

### Aplikasi Tidak Bisa Dibuka

**Gejala:**
- Double-click tidak membuka aplikasi
- Tidak ada response sama sekali
- Error message muncul

**Solusi:**
1. **Cek Windows Defender**
   ```
   - Buka Windows Security
   - Pergi ke Virus & threat protection
   - Cek Protection history
   - Jika file diblokir, klik "Actions" → "Allow on device"
   ```

2. **Jalankan sebagai Administrator**
   ```
   - Right-click pada DevServerManager.exe
   - Pilih "Run as administrator"
   ```

3. **Cek .NET Framework**
   ```
   - Download .NET Framework 4.8 dari Microsoft
   - Install dan restart komputer
   ```

### Aplikasi Crash atau Freeze

**Gejala:**
- Aplikasi berhenti merespons
- GUI membeku
- Aplikasi tertutup tiba-tiba

**Solusi:**
1. **Restart Aplikasi**
   ```
   - Tutup aplikasi melalui Task Manager
   - Jalankan ulang aplikasi
   ```

2. **Cek Log Files**
   ```
   - Buka folder logs/
   - Cek file devservermanager.log
   - Cari error messages
   ```

3. **Reset Konfigurasi**
   ```
   - Hapus file config/server_config.json
   - Restart aplikasi (akan membuat konfigurasi default)
   ```

---

## 📦 Masalah Instalasi

### Error "Python not found"

**Gejala:**
- Error message: "Python not found"
- Aplikasi tidak bisa start

**Solusi:**
1. **Install Python 3.8+**
   ```
   - Download dari python.org
   - Pastikan "Add to PATH" dicentang
   - Restart command prompt
   ```

2. **Cek PATH Environment**
   ```
   - Buka System Properties → Environment Variables
   - Cek PATH variable
   - Pastikan Python directory ada di PATH
   ```

### Error "Module not found"

**Gejala:**
- Error: "No module named 'tkinter'"
- Error: "No module named 'pystray'"

**Solusi:**
1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Cek Python Version**
   ```bash
   python --version
   # Harus 3.8 atau lebih tinggi
   ```

3. **Reinstall Dependencies**
   ```bash
   pip uninstall -r requirements.txt -y
   pip install -r requirements.txt
   ```

---

## 🖥️ Masalah Server

### Server Tidak Bisa Start

**Gejala:**
- Klik "Start" tidak ada response
- Error message muncul
- Server tidak muncul di log

**Solusi:**
1. **Cek Port Conflict**
   ```
   - Cek apakah port sudah digunakan
   - Ganti port di konfigurasi server
   - Restart aplikasi
   ```

2. **Cek Path Server**
   ```
   - Pastikan path server benar
   - Cek apakah folder ada
   - Pastikan ada file yang diperlukan (index.html, app.py, dll)
   ```

3. **Cek Permission**
   ```
   - Pastikan aplikasi punya akses ke folder
   - Jalankan sebagai administrator jika perlu
   ```

### Server Start Tapi Tidak Bisa Diakses

**Gejala:**
- Server running di log
- Browser tidak bisa akses
- Error "Connection refused"

**Solusi:**
1. **Cek Firewall**
   ```
   - Buka Windows Defender Firewall
   - Allow aplikasi melalui firewall
   - Cek inbound/outbound rules
   ```

2. **Cek Port Binding**
   ```
   - Pastikan server bind ke 0.0.0.0 atau localhost
   - Cek apakah port benar
   ```

3. **Cek Browser**
   ```
   - Coba akses dengan http://localhost:PORT
   - Cek apakah ada proxy settings
   - Coba browser lain
   ```

### Server Stop Tiba-tiba

**Gejala:**
- Server running lalu stop sendiri
- Error di log
- Aplikasi crash

**Solusi:**
1. **Cek Log Files**
   ```
   - Buka logs/devservermanager.log
   - Cari error messages
   - Cek stack trace
   ```

2. **Cek Memory Usage**
   ```
   - Buka Task Manager
   - Cek memory usage
   - Restart jika memory penuh
   ```

3. **Cek Dependencies**
   ```
   - Pastikan semua dependencies terinstall
   - Update ke versi terbaru
   ```

---

## 🎨 Masalah GUI

### GUI Tidak Muncul

**Gejala:**
- Aplikasi start tapi tidak ada window
- Hanya ada icon di system tray
- GUI tidak responsive

**Solusi:**
1. **Cek System Tray**
   ```
   - Klik icon di system tray
   - Pilih "Show" untuk menampilkan window
   ```

2. **Restart GUI**
   ```
   - Tutup aplikasi
   - Jalankan ulang
   - Cek apakah ada error di log
   ```

3. **Cek Display Settings**
   ```
   - Cek resolution display
   - Cek scaling settings
   - Coba di monitor lain
   ```

### GUI Lambat atau Lag

**Gejala:**
- Interface lambat merespons
- Animasi tidak smooth
- Click tidak langsung response

**Solusi:**
1. **Cek CPU Usage**
   ```
   - Buka Task Manager
   - Cek CPU usage
   - Tutup aplikasi lain yang berat
   ```

2. **Cek Memory**
   ```
   - Cek RAM usage
   - Restart aplikasi jika perlu
   ```

3. **Update Graphics Driver**
   ```
   - Update driver graphics card
   - Restart komputer
   ```

### Theme Tidak Berfungsi

**Gejala:**
- Theme tidak berubah
- Interface tetap sama
- Error saat ganti theme

**Solusi:**
1. **Reset Theme**
   ```
   - Pilih theme "system"
   - Restart aplikasi
   - Coba theme lain
   ```

2. **Cek Theme Files**
   ```
   - Cek file config/theme_config.json
   - Pastikan format JSON benar
   - Hapus file jika corrupt
   ```

---

## 🔔 Masalah System Tray

### Icon Tidak Muncul di System Tray

**Gejala:**
- Tidak ada icon di system tray
- Aplikasi minimize tapi tidak ada icon

**Solusi:**
1. **Cek System Tray Settings**
   ```
   - Right-click taskbar
   - Pilih "Taskbar settings"
   - Cek "Select which icons appear on the taskbar"
   ```

2. **Restart System Tray**
   ```
   - Restart Windows Explorer
   - Restart aplikasi
   ```

3. **Cek Dependencies**
   ```
   - Pastikan pystray terinstall
   - Update ke versi terbaru
   ```

### Menu System Tray Tidak Muncul

**Gejala:**
- Icon ada tapi tidak ada menu
- Right-click tidak ada response

**Solusi:**
1. **Cek Permission**
   ```
   - Jalankan sebagai administrator
   - Cek antivirus settings
   ```

2. **Update pystray**
   ```bash
   pip install --upgrade pystray
   ```

---

## ⚙️ Masalah Konfigurasi

### Konfigurasi Tidak Tersimpan

**Gejala:**
- Setting tidak tersimpan
- Kembali ke default setelah restart
- Error saat save

**Solusi:**
1. **Cek Permission Folder**
   ```
   - Pastikan aplikasi punya akses write ke folder config/
   - Jalankan sebagai administrator
   ```

2. **Cek File Format**
   ```
   - Cek format JSON di config files
   - Pastikan tidak ada syntax error
   - Validasi dengan JSON validator online
   ```

3. **Reset Konfigurasi**
   ```
   - Hapus semua file di folder config/
   - Restart aplikasi
   - Konfigurasi akan dibuat ulang
   ```

### Template Server Tidak Muncul

**Gejala:**
- Template kosong
- Error saat load template
- Template tidak sesuai

**Solusi:**
1. **Cek Template File**
   ```
   - Buka config/server_templates.json
   - Pastikan format JSON benar
   - Cek apakah ada template yang valid
   ```

2. **Reset Template**
   ```
   - Hapus file server_templates.json
   - Restart aplikasi
   - Template default akan dibuat
   ```

---

## 🚀 Masalah Performance

### Aplikasi Lambat

**Gejala:**
- Startup lambat
- Response lambat
- Memory usage tinggi

**Solusi:**
1. **Cek System Resources**
   ```
   - Buka Task Manager
   - Cek CPU, Memory, Disk usage
   - Tutup aplikasi lain yang tidak perlu
   ```

2. **Optimize Konfigurasi**
   ```
   - Kurangi jumlah server yang running
   - Cek log level (set ke WARNING jika tidak perlu DEBUG)
   ```

3. **Update Dependencies**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

### Memory Usage Tinggi

**Gejala:**
- Memory usage terus naik
- Aplikasi menjadi lambat
- System menjadi tidak responsive

**Solusi:**
1. **Restart Aplikasi**
   ```
   - Tutup aplikasi
   - Tunggu beberapa detik
   - Jalankan ulang
   ```

2. **Cek Memory Leaks**
   ```
   - Monitor memory usage di Task Manager
   - Cek apakah ada pattern yang tidak normal
   ```

---

## ❌ Error Messages

### "Permission Denied"

**Solusi:**
```
- Jalankan sebagai administrator
- Cek permission folder
- Pastikan tidak ada file yang sedang digunakan
```

### "Port Already in Use"

**Solusi:**
```
- Ganti port di konfigurasi server
- Cek aplikasi lain yang menggunakan port yang sama
- Restart aplikasi
```

### "Module Not Found"

**Solusi:**
```
- Install dependencies: pip install -r requirements.txt
- Cek Python PATH
- Restart command prompt
```

### "File Not Found"

**Solusi:**
```
- Cek path file
- Pastikan file ada
- Cek permission akses file
```

---

## ❓ FAQ

### Q: Apakah aplikasi ini aman?
**A:** Ya, aplikasi ini 100% aman. Sudah di-scan dengan VirusTotal dan tidak ada ancaman terdeteksi.

### Q: Apakah perlu install Python?
**A:** Tidak, untuk pengguna biasa cukup download executable. Python hanya diperlukan untuk developer.

### Q: Apakah bisa digunakan di Linux/Mac?
**A:** Saat ini hanya support Windows. Versi Linux/Mac sedang dalam pengembangan.

### Q: Bagaimana cara backup konfigurasi?
**A:** Backup folder `config/` dan `logs/` untuk menyimpan semua setting dan log.

### Q: Apakah ada limitasi jumlah server?
**A:** Tidak ada limitasi teknis, tapi disarankan maksimal 10 server untuk performa optimal.

---

## 🆘 Support

### Jika Masalah Masih Berlanjut

1. **Cek Log Files**
   ```
   - Buka logs/devservermanager.log
   - Cari error messages
   - Screenshot error yang muncul
   ```

2. **Buat Issue di GitHub**
   ```
   - Buka: https://github.com/idpcks/DevServerManager/issues
   - Klik "New Issue"
   - Jelaskan masalah dengan detail
   - Lampirkan log files dan screenshot
   ```

3. **Kontak Developer**
   ```
   - Email: idpcks.container103@slmail.me
   - GitHub: @idpcks
   - Subject: [DevServer Manager] Masalah: [Deskripsi singkat]
   ```

### Informasi yang Perlu Disertakan

- **OS Version**: Windows 10/11
- **Aplikasi Version**: v1.0.1
- **Error Message**: Screenshot atau copy-paste
- **Log Files**: Lampirkan file log
- **Steps to Reproduce**: Langkah-langkah yang menyebabkan masalah

---

**Last Updated**: 11 September 2025  
**Version**: 1.0.1  
**Developer**: idpcks
