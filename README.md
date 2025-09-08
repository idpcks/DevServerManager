# 🚀 DevServer Manager - Modern Development Server Management

A modern, modular GUI application for managing multiple development servers with clean architecture and robust functionality. This application replaces traditional batch scripts with an intuitive interface and advanced features.

## ✨ Key Features

### 🏗️ Core Architecture
- **Modular Design**: Clean separation of concerns with service layers, models, and GUI components
- **Modern GUI**: User-friendly interface with customizable themes and responsive design
- **Multi-threading**: Non-blocking UI with proper thread management
- **Extensible Design**: Base classes and interfaces for easy feature extension

### 🎯 Server Management
- **📋 Server Templates**: Pre-configured templates for Laravel, Node.js, Python, Go, .NET, and more
- **🔍 Auto-Detection**: Automatic project type detection based on file markers (package.json, composer.json, requirements.txt, etc.)
- **🚦 Process Monitoring**: Real-time server status and resource monitoring
- **⚙️ Environment Variables**: Support for environment-specific configurations
- **🛡️ Graceful Shutdown**: Safe server termination with confirmation dialogs

### 📊 Advanced Features
- **📋 Real-time Logging**: Advanced logging system with color coding, file output, and log rotation
- **💻 Command Execution**: Execute custom commands with real-time output capture
- **📁 Smart Configuration**: Robust configuration management with backup and validation
- **🛡️ Error Handling**: Comprehensive error handling with proper logging and user feedback
- **⚙️ Auto-save Configuration**: Automatic configuration persistence with backup support
- **🔔 System Tray**: Minimize to system tray with quick access controls

## 🖥️ Fitur Interface

### 🎛️ Server Controls
- Start/Stop individual servers dengan satu klik
- Start/Stop all servers sekaligus dengan delay otomatis
- Real-time status indicator dengan color coding
- Port dan path information yang dapat diedit
- Template selection untuk setup server baru
- Environment variables configuration

### 📊 Log Terminal
- Color-coded log messages (INFO, ERROR, WARNING, SUCCESS)
- Timestamp untuk setiap log entry
- Auto-scroll ke log terbaru
- Clear log functionality
- Export log ke file

### ⚡ Advanced Features
- Execute command apapun langsung dari GUI
- Output ditampilkan di log terminal
- Support untuk command dengan timeout
- System tray integration
- Confirmation dialog saat menutup aplikasi dengan server aktif
- Auto-detection project type saat menambah server baru

## 🚀 Cara Penggunaan

### 1. Menjalankan Aplikasi
```bash
python main.py
```

Atau gunakan batch file:
```bash
launch_gui.bat
```

### 2. Setup Server Baru
#### 🎯 Menggunakan Template (Recommended)
1. Klik tombol "➕ Add Server"
2. Pilih template yang sesuai (Laravel, Node.js, Python, Go, .NET, dll)
3. Pilih folder project
4. Aplikasi akan otomatis mendeteksi konfigurasi yang diperlukan
5. Sesuaikan port dan environment variables jika diperlukan

#### 📁 Manual Configuration
1. Klik tombol "➕ Add Server"
2. Pilih "Custom" template
3. Atur nama, path, port, dan command secara manual
4. Simpan konfigurasi

### 3. Mengelola Server
#### 🚀 Menjalankan Server
- **Individual**: Klik tombol "▶️ Start" pada server yang diinginkan
- **Semua**: Klik "🚀 Start All Servers" untuk menjalankan semua server dengan delay otomatis

#### 🛑 Menghentikan Server
- **Individual**: Klik tombol "⏹️ Stop" pada server yang berjalan
- **Semua**: Klik "🛑 Stop All Servers" untuk menghentikan semua server
- **Graceful Shutdown**: Dialog konfirmasi akan muncul saat menutup aplikasi dengan server aktif

#### ⚙️ Mengubah Konfigurasi
- Klik tombol "⚙️ Edit" untuk mengubah konfigurasi server
- Klik tombol "📁" untuk mengubah path server
- Konfigurasi akan otomatis tersimpan

### 4. Fitur Lanjutan
#### 💻 Custom Command Execution
- Ketik command di field "Custom Command"
- Tekan Enter atau klik "Execute"
- Output akan ditampilkan di log terminal dengan real-time

#### 🔔 System Tray
- Minimize aplikasi ke system tray
- Quick access untuk start/stop servers
- Notifikasi status server

## 🔧 Konfigurasi

### 📁 Struktur File
```
runserver/
├── config/
│   ├── server_config.json          # Konfigurasi server aktif
│   ├── server_config_example.json   # Template konfigurasi
│   ├── server_templates.json        # Template untuk berbagai teknologi
│   └── theme_config.json           # Konfigurasi tema UI
├── src/
│   ├── gui/                        # Komponen GUI
│   ├── models/                     # Data models
│   └── services/                   # Business logic
├── utils/                          # Utility functions
├── assets/                         # Assets (logo, icons)
└── logs/                          # Log files
```

### 🎯 Server Templates
Aplikasi menyediakan template untuk berbagai teknologi:

#### Laravel/PHP
```json
{
  "name": "Laravel Project",
  "command": "php artisan serve --port={port}",
  "default_port": 8000,
  "file_markers": ["artisan", "composer.json"],
  "env_vars": {
    "APP_ENV": "local",
    "APP_DEBUG": "true"
  }
}
```

#### Node.js
```json
{
  "name": "Node.js Project",
  "command": "npm run dev",
  "default_port": 3000,
  "file_markers": ["package.json", "node_modules"],
  "env_vars": {
    "NODE_ENV": "development",
    "PORT": "{port}"
  }
}
```

#### Python
```json
{
  "name": "Python Project",
  "command": "python manage.py runserver {port}",
  "default_port": 8000,
  "file_markers": ["manage.py", "requirements.txt"],
  "env_vars": {
    "DJANGO_SETTINGS_MODULE": "settings.local"
  }
 }

## 🛡️ Error Handling & Safety

Aplikasi dilengkapi dengan comprehensive error handling:
- **🔍 Path Validation**: Cek keberadaan direktori dan file markers sebelum menjalankan server
- **🔄 Process Management**: Handle process termination dengan graceful shutdown
- **⏱️ Command Timeout**: Timeout yang dapat dikonfigurasi untuk custom commands
- **🧵 Thread Safety**: Queue-based logging untuk thread safety
- **🛡️ Exception Handling**: Try-catch di semua operasi critical
- **💾 Auto-backup**: Backup otomatis konfigurasi sebelum perubahan
- **⚠️ Confirmation Dialogs**: Dialog konfirmasi untuk operasi berbahaya
- **📊 Health Monitoring**: Monitoring status server secara real-time

## 🎨 Customization

### 🎯 Menambah Template Baru
Edit file `config/server_templates.json`:
```json
{
  "My Custom Framework": {
    "name": "My Custom Framework",
    "command": "my-framework serve --port={port}",
    "default_port": 4000,
    "file_markers": ["my-config.json", "src/"],
    "env_vars": {
      "ENVIRONMENT": "development"
    },
    "description": "Template for My Custom Framework"
  }
}
```

### 🎨 Mengubah Theme
Edit file `config/theme_config.json` untuk mengubah warna dan font:
```json
{
  "colors": {
    "primary": "#2196F3",
    "success": "#4CAF50",
    "warning": "#FF9800",
    "error": "#F44336"
  },
  "fonts": {
    "default": "Segoe UI",
    "monospace": "Consolas"
  }
}
```

## 📋 Requirements

### 🐍 Python Dependencies
- Python 3.8+ (recommended)
- Tkinter (biasanya sudah include di Python)
- Pillow (PIL) untuk image processing
- psutil untuk process monitoring

### 💻 System Requirements
- Windows 10/11 (primary support)
- macOS dan Linux (experimental support)
- Minimum 4GB RAM
- 100MB disk space

### 📦 Installation
```bash
# Clone repository
git clone <repository-url>
cd runserver

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

## 🔄 Migration Guide

### Dari runserver.bat Legacy
1. Backup file `runserver.bat` lama
2. Jalankan `python main.py`
3. Gunakan "➕ Add Server" untuk menambah server dengan template
4. Import konfigurasi lama jika diperlukan
5. Gunakan "🚀 Start All Servers" untuk menjalankan semua server

### Dari Versi Lama DevServer Manager
1. Backup folder `config/`
2. Update ke versi terbaru
3. Jalankan aplikasi - konfigurasi akan otomatis di-migrate
4. Verifikasi semua server berfungsi dengan baik

## 🐛 Troubleshooting

### 🚫 Server Tidak Bisa Start
- **Path Issues**: Pastikan path server benar dan folder exists
- **Port Conflict**: Cek apakah port sudah digunakan aplikasi lain dengan `netstat -an`
- **Permission**: Jalankan sebagai administrator jika diperlukan
- **Dependencies**: Pastikan semua dependencies project terinstall
- **Logs**: Lihat log terminal dan file `logs/devserver_manager.log` untuk detail error

### ⚡ Command Tidak Berfungsi
- **Syntax**: Pastikan command valid untuk OS yang digunakan
- **Timeout**: Sesuaikan timeout di pengaturan jika command butuh waktu lama
- **Environment**: Cek environment variables sudah benar
- **Path**: Pastikan executable ada di PATH atau gunakan full path

### 🖥️ GUI Issues
- **Freeze**: Semua operasi berjalan di background thread, tunggu sebentar
- **Theme**: Reset theme ke default jika ada masalah tampilan
- **Memory**: Restart aplikasi jika memory usage tinggi
- **Display**: Cek scaling display Windows jika UI terlihat aneh

### 🔧 Configuration Issues
- **Corrupt Config**: Hapus file di `config/` untuk reset ke default
- **Template Error**: Validasi syntax JSON di file template
- **Backup**: Gunakan backup otomatis di folder `config/backups/`

## 📝 Log Levels

- **🟢 SUCCESS**: Operasi berhasil (hijau)
- **ℹ️ INFO**: Informasi umum (biru)
- **⚠️ WARNING**: Peringatan (kuning)
- **❌ ERROR**: Error/kesalahan (merah)
- **🔧 DEBUG**: Debug information (abu-abu)

## 🚀 Changelog

### v2.0.0 (Latest)
- ✨ **Server Templates**: Pre-configured templates untuk berbagai teknologi
- 🔍 **Auto-Detection**: Deteksi otomatis jenis project
- 🛡️ **Graceful Shutdown**: Dialog konfirmasi saat menutup dengan server aktif
- 🏗️ **Modular Architecture**: Refactor ke arsitektur yang lebih bersih
- 🔔 **System Tray**: Integration dengan system tray
- ⚙️ **Environment Variables**: Support untuk environment-specific config
- 📊 **Enhanced Logging**: Improved logging system dengan file rotation
- 🎨 **Theme System**: Customizable themes dan UI improvements

### v1.x (Legacy)
- Basic server management
- Simple GUI interface
- Manual configuration

## 🤝 Contributing

### 🐛 Bug Reports
1. Cek existing issues terlebih dahulu
2. Buat issue baru dengan template yang disediakan
3. Sertakan log files dan screenshot jika memungkinkan

### 💡 Feature Requests
1. Diskusikan di GitHub Discussions terlebih dahulu
2. Buat detailed proposal dengan use case
3. Consider backward compatibility

### 🔧 Development
1. Fork repository
2. Buat feature branch: `git checkout -b feature/amazing-feature`
3. Follow coding standards dan add tests
4. Commit changes: `git commit -m 'Add amazing feature'`
5. Push branch: `git push origin feature/amazing-feature`
6. Create Pull Request

### 📋 Development Setup
```bash
# Setup development environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies

# Run tests
python -m pytest tests/

# Run with debug mode
python main.py --debug
```

## 📄 License

MIT License - bebas digunakan dan dimodifikasi.

## 🙏 Acknowledgments

### 👨‍💻 Developer
**DevServer Manager** dikembangkan oleh **idpcks**

Sebuah aplikasi GUI untuk mengelola multiple development servers dengan fitur modern dan user-friendly interface.

### 🤝 Credits
- Terima kasih kepada semua contributors
- Inspired by modern development workflows
- Built with ❤️ untuk developer community

---

**📞 Support**: Jika mengalami masalah, silakan buat issue di GitHub atau hubungi maintainer.

**⭐ Star**: Jika project ini membantu, jangan lupa berikan star di GitHub!