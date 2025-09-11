# 📖 User Guide - DevServer Manager

## 📋 Daftar Isi

- [Pengenalan](#pengenalan)
- [Instalasi](#instalasi)
- [Quick Start](#quick-start)
- [Fitur Utama](#fitur-utama)
- [Konfigurasi Server](#konfigurasi-server)
- [Template Server](#template-server)
- [System Tray](#system-tray)
- [Custom Commands](#custom-commands)
- [Themes](#themes)
- [Tips & Tricks](#tips--tricks)

---

## 🚀 Pengenalan

**DevServer Manager** adalah aplikasi GUI modern untuk mengelola multiple development servers dengan mudah. Aplikasi ini memungkinkan Anda untuk:

- ✅ Menjalankan multiple server development sekaligus
- ✅ Menggunakan template untuk berbagai teknologi (Laravel, Node.js, Python, dll)
- ✅ Monitoring real-time status server
- ✅ System tray integration
- ✅ Custom command execution
- ✅ Theme customization

### System Requirements

- **OS**: Windows 10/11 (64-bit)
- **RAM**: Minimum 4GB
- **Storage**: 100MB free space
- **Network**: Internet connection (untuk update checking)

---

## 📦 Instalasi

### Untuk Pengguna (Executable)

1. **Download**
   ```
   - Buka: https://github.com/idpcks/DevServerManager/releases
   - Download file .zip terbaru
   - Extract ke folder yang diinginkan
   ```

2. **Jalankan**
   ```
   - Double-click DevServerManager.exe
   - Aplikasi akan terbuka dengan splash screen
   - Tidak perlu install Python atau dependencies
   ```

### Untuk Developer

1. **Clone Repository**
   ```bash
   git clone https://github.com/idpcks/DevServerManager.git
   cd DevServerManager/runserver
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Jalankan Aplikasi**
   ```bash
   python main.py
   ```

---

## ⚡ Quick Start

### 1. Buka Aplikasi
- Double-click `DevServerManager.exe`
- Tunggu splash screen selesai
- Aplikasi akan terbuka dengan interface utama

### 2. Tambah Server Pertama
1. Klik **"➕ Add Server"**
2. Pilih template yang sesuai (misal: Laravel, Node.js, Python)
3. Isi detail server:
   - **Name**: Nama server (misal: "My Laravel App")
   - **Path**: Path ke project folder
   - **Port**: Port untuk server (misal: 8000)
4. Klik **"Create Server"**

### 3. Start Server
1. Di panel kiri, cari server yang baru dibuat
2. Klik **"🚀 Start"** untuk menjalankan server
3. Status akan berubah menjadi "Running"
4. Server akan muncul di log dengan URL akses

### 4. Akses Server
- Buka browser
- Akses URL yang ditampilkan di log (misal: http://localhost:8000)
- Server Anda sudah berjalan!

---

## 🎯 Fitur Utama

### Server Management

#### Start/Stop Server
- **Start**: Klik tombol "🚀 Start" untuk menjalankan server
- **Stop**: Klik tombol "⏹️ Stop" untuk menghentikan server
- **Status**: Lihat status real-time di panel server

#### Global Controls
- **Start All**: Menjalankan semua server sekaligus
- **Stop All**: Menghentikan semua server sekaligus
- **Clear Log**: Membersihkan log display

### Server Information
- **Name**: Nama server
- **Path**: Lokasi project folder
- **Port**: Port yang digunakan
- **Status**: Running/Stopped
- **URL**: Link akses server

---

## ⚙️ Konfigurasi Server

### Manual Configuration

1. **Klik "➕ Add Server"**
2. **Pilih "Manual Configuration"**
3. **Isi Detail Server**:
   ```
   Name: Nama server Anda
   Path: C:\path\to\your\project
   Port: 8000
   Command: python -m http.server
   ```

### Edit Server

1. **Klik tombol "✏️ Edit"** di panel server
2. **Ubah konfigurasi** yang diperlukan
3. **Klik "Save"** untuk menyimpan perubahan

### Delete Server

1. **Klik tombol "🗑️ Delete"** di panel server
2. **Konfirmasi** penghapusan
3. **Server akan dihapus** dari daftar

---

## 📋 Template Server

### Laravel/PHP
```json
{
  "name": "Laravel Project",
  "command": "php artisan serve --port={port}",
  "port": 8000,
  "description": "Laravel development server"
}
```

### Node.js/Express
```json
{
  "name": "Node.js Project", 
  "command": "npm start",
  "port": 3000,
  "description": "Node.js development server"
}
```

### Python/Flask
```json
{
  "name": "Python Flask",
  "command": "python app.py",
  "port": 5000,
  "description": "Python Flask development server"
}
```

### Python/HTTP Server
```json
{
  "name": "Python HTTP Server",
  "command": "python -m http.server {port}",
  "port": 8000,
  "description": "Simple Python HTTP server"
}
```

### React/Vite
```json
{
  "name": "React Vite",
  "command": "npm run dev -- --port {port}",
  "port": 5173,
  "description": "React Vite development server"
}
```

---

## 🔔 System Tray

### Minimize to Tray
- **Klik tombol minimize** di window
- **Aplikasi akan minimize** ke system tray
- **Icon akan muncul** di system tray

### Tray Menu
- **Show**: Menampilkan window aplikasi
- **Hide**: Menyembunyikan ke system tray
- **Start All Servers**: Menjalankan semua server
- **Stop All Servers**: Menghentikan semua server
- **Exit**: Keluar dari aplikasi

### Tray Icon
- **Normal**: Aplikasi berjalan normal
- **Running**: Ada server yang sedang berjalan
- **Error**: Ada error atau masalah

---

## 💻 Custom Commands

### Menjalankan Custom Command

1. **Buka tab "Commands"** di panel kanan
2. **Ketik command** yang ingin dijalankan
3. **Tekan Enter** atau klik "Execute"
4. **Output akan muncul** di log

### Contoh Commands

```bash
# Git commands
git status
git pull origin main
git checkout -b new-feature

# Package managers
npm install
composer install
pip install -r requirements.txt

# System commands
dir
ls
pwd
```

### Command Features
- **Real-time output**: Output muncul langsung
- **Error handling**: Error ditampilkan dengan jelas
- **Timeout protection**: Command otomatis timeout setelah 30 detik

---

## 🎨 Themes

### Mengganti Theme

1. **Klik dropdown "Theme"** di title bar
2. **Pilih theme** yang diinginkan:
   - **System**: Mengikuti theme sistem
   - **Dark**: Theme gelap
   - **Light**: Theme terang
3. **Theme akan berubah** secara real-time

### Theme Features
- **Real-time switching**: Tidak perlu restart
- **Persistent**: Theme tersimpan di konfigurasi
- **Consistent**: Semua komponen menggunakan theme yang sama

---

## 💡 Tips & Tricks

### Productivity Tips

1. **Gunakan Template**
   - Pilih template yang sesuai dengan project
   - Template sudah dikonfigurasi dengan optimal

2. **Organize Servers**
   - Beri nama yang deskriptif
   - Group berdasarkan project atau teknologi

3. **Monitor Logs**
   - Pantau log untuk error atau warning
   - Gunakan "Clear Log" untuk membersihkan

4. **System Tray**
   - Minimize ke tray untuk menghemat space
   - Gunakan tray menu untuk quick access

### Troubleshooting Tips

1. **Port Conflict**
   - Ganti port jika ada konflik
   - Cek port yang sedang digunakan

2. **Path Issues**
   - Pastikan path project benar
   - Gunakan absolute path jika perlu

3. **Permission Issues**
   - Jalankan sebagai administrator jika perlu
   - Cek permission folder project

### Performance Tips

1. **Limit Server Count**
   - Maksimal 10 server untuk performa optimal
   - Stop server yang tidak digunakan

2. **Monitor Resources**
   - Pantau CPU dan memory usage
   - Restart aplikasi jika perlu

---

## 🔧 Advanced Configuration

### Environment Variables

Beberapa template mendukung environment variables:

```json
{
  "name": "Laravel with Env",
  "command": "php artisan serve --port={port}",
  "env_vars": {
    "APP_ENV": "local",
    "APP_DEBUG": "true",
    "DB_CONNECTION": "sqlite"
  }
}
```

### Custom Commands

Anda bisa membuat custom command untuk project spesifik:

```json
{
  "name": "Custom Project",
  "command": "npm run dev:custom -- --port {port}",
  "port": 3000,
  "description": "Custom development server"
}
```

---

## 📞 Support

### Bantuan

- **Documentation**: [GitHub Wiki](https://github.com/idpcks/DevServerManager/wiki)
- **Issues**: [GitHub Issues](https://github.com/idpcks/DevServerManager/issues)
- **Discussions**: [GitHub Discussions](https://github.com/idpcks/DevServerManager/discussions)

### Kontak

- **Email**: idpcks.container103@slmail.me
- **GitHub**: [@idpcks](https://github.com/idpcks)

---

**Last Updated**: 11 September 2025  
**Version**: 1.0.1  
**Developer**: idpcks
