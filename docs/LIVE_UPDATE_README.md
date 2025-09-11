# 🚀 Panduan Live Update - DevServer Manager

> **Catatan**: Untuk dokumentasi teknis lengkap, lihat [LIVE_UPDATE.md](LIVE_UPDATE.md)

## ✨ **Pengenalan**

DevServer Manager memiliki fitur **Live Update** yang memungkinkan Anda mengupdate aplikasi secara otomatis dengan satu klik. Tidak perlu download manual atau instalasi kompleks!

### **🎯 Fitur Utama**
- 🚀 **Update Otomatis** - Download, install, dan restart otomatis
- 💾 **Backup Aman** - Backup otomatis sebelum update
- 📊 **Progress Real-time** - Lihat progress download dan kecepatan
- 🔄 **Rollback** - Kembali ke versi lama jika diperlukan

---

## 🚀 **Cara Menggunakan**

### **📋 Langkah-langkah Update**

#### **1. Update Otomatis (Direkomendasikan)**
- Aplikasi mengecek update otomatis setiap 24 jam
- Jika ada update tersedia, akan muncul notifikasi
- Klik **"🚀 Live Update Now"** untuk memulai

#### **2. Update Manual**
- Buka menu **Help** → **🚀 Live Update**
- Klik untuk mengecek update secara manual

#### **3. Proses Update**
1. **Download** - File update didownload dengan progress bar
2. **Backup** - Versi lama di-backup otomatis
3. **Install** - File baru menggantikan file lama
4. **Restart** - Aplikasi restart dengan versi baru

---

## 🎨 **Tampilan Interface**

### **Dialog Live Update**
```
┌─────────────────────────────────────────┐
│  🔄 Live Update Available!             │
├─────────────────────────────────────────┤
│  Versi Saat Ini: 1.0.1                 │
│  Versi Baru: 1.0.2                     │
├─────────────────────────────────────────┤
│  ✨ Fitur Live Update:                 │
│  • Download otomatis dengan progress    │
│  • Instalasi di background              │
│  • Restart aplikasi otomatis            │
│  • Backup dan rollback                  │
├─────────────────────────────────────────┤
│  [Nanti] [Download Manual] [🚀 Update Sekarang] │
└─────────────────────────────────────────┘
```

### **Dialog Progress**
```
┌─────────────────────────────────────────┐
│  Progress Live Update                   │
├─────────────────────────────────────────┤
│  Mendownload update... 45.2%           │
│  ████████████████░░░░░░░░░░░░░░░░░░░░   │
│  Kecepatan: 2.3 MB/s    ETA: 00:15     │
│                              [Batal]   │
└─────────────────────────────────────────┘
```

---

## 🚨 **Pemecahan Masalah**

### **Masalah Umum & Solusi**

| Masalah | Solusi Cepat |
|---------|---------------|
| Download gagal | Cek koneksi internet, coba download manual |
| Instalasi gagal | Pastikan aplikasi ditutup, cek permission |
| Update tidak terdeteksi | Coba check manual melalui menu Help |

### **Recovery Darurat**
- **Rollback**: Buka folder `backup/` dan restore file lama
- **Download Manual**: Kunjungi [GitHub Releases](https://github.com/idpcks/DevServerManager/releases)

> **Info**: Untuk troubleshooting lengkap, lihat [LIVE_UPDATE.md](LIVE_UPDATE.md#troubleshooting)

---

## 🎉 **Tips & Rekomendasi**

### **📝 Best Practices**
- ✅ **Selalu backup** konfigurasi penting sebelum update
- ✅ **Tutup server** yang sedang berjalan sebelum update
- ✅ **Update reguler** untuk mendapatkan fitur terbaru
- ✅ **Cek koneksi** internet sebelum memulai update

### **🔧 Settings Update**
- **Interval Check**: 24 jam (otomatis)
- **Backup Retention**: 3 backup terbaru disimpan
- **Download Cache**: File di-cache selama 1 jam

---

## 📚 **Dokumentasi Lengkap**

Untuk informasi teknis detail:
- **[LIVE_UPDATE.md](LIVE_UPDATE.md)** - Dokumentasi teknis lengkap
- **[BACKUP_IMPORT_GUIDE.md](BACKUP_IMPORT_GUIDE.md)** - Panduan backup konfigurasi
- **[USER_GUIDE.md](USER_GUIDE.md)** - Panduan lengkap aplikasi

---

**🚀 Selamat menggunakan fitur Live Update! Update aplikasi kini semudah satu klik!**
