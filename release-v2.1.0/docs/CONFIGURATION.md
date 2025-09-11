# ⚙️ Configuration Guide - DevServer Manager

## 📋 Daftar Isi

- [Overview](#overview)
- [File Konfigurasi](#file-konfigurasi)
- [Server Configuration](#server-configuration)
- [Template Configuration](#template-configuration)
- [Theme Configuration](#theme-configuration)
- [Advanced Settings](#advanced-settings)
- [Environment Variables](#environment-variables)
- [Custom Commands](#custom-commands)

---

## 🔍 Overview

DevServer Manager menggunakan beberapa file konfigurasi untuk mengatur behavior aplikasi. Semua file konfigurasi berada di folder `config/` dan menggunakan format JSON.

### Struktur Folder Config
```
config/
├── server_config.json          # Konfigurasi server aktif
├── server_config_example.json  # Template konfigurasi server
├── server_templates.json       # Template untuk berbagai teknologi
├── theme_config.json          # Konfigurasi tema UI
└── update_cache.json          # Cache untuk update checking
```

---

## 📁 File Konfigurasi

### server_config.json
File utama yang menyimpan konfigurasi semua server yang telah dibuat.

**Lokasi**: `config/server_config.json`

**Format**:
```json
{
  "server_name": {
    "name": "Server Name",
    "path": "C:\\path\\to\\project",
    "port": "8000",
    "command": "python -m http.server",
    "template_id": "python-http",
    "category": "Python",
    "env_vars": {},
    "description": "Server description"
  }
}
```

### server_config_example.json
Template untuk membuat konfigurasi server baru.

**Lokasi**: `config/server_config_example.json`

**Format**:
```json
{
  "name": "Example Server",
  "path": "C:\\path\\to\\your\\project",
  "port": "8000",
  "command": "python -m http.server",
  "template_id": "python-http",
  "category": "Python",
  "env_vars": {},
  "description": "Example server configuration"
}
```

---

## 🖥️ Server Configuration

### Basic Server Settings

#### Name
- **Type**: String
- **Required**: Yes
- **Description**: Nama unik untuk server
- **Example**: `"My Laravel App"`

#### Path
- **Type**: String
- **Required**: Yes
- **Description**: Path absolut ke folder project
- **Example**: `"C:\\Users\\User\\Projects\\laravel-app"`

#### Port
- **Type**: String/Number
- **Required**: Yes
- **Description**: Port yang digunakan server
- **Example**: `"8000"` atau `8000`

#### Command
- **Type**: String
- **Required**: Yes
- **Description**: Command untuk menjalankan server
- **Example**: `"php artisan serve --port={port}"`

### Advanced Server Settings

#### Template ID
- **Type**: String
- **Required**: No
- **Description**: ID template yang digunakan
- **Example**: `"laravel"`

#### Category
- **Type**: String
- **Required**: No
- **Description**: Kategori server
- **Example**: `"PHP"`, `"Node.js"`, `"Python"`

#### Environment Variables
- **Type**: Object
- **Required**: No
- **Description**: Environment variables untuk server
- **Example**:
```json
{
  "APP_ENV": "local",
  "APP_DEBUG": "true",
  "DB_CONNECTION": "sqlite"
}
```

#### Description
- **Type**: String
- **Required**: No
- **Description**: Deskripsi server
- **Example**: `"Laravel development server for e-commerce project"`

---

## 📋 Template Configuration

### server_templates.json
File yang berisi template untuk berbagai teknologi development.

**Lokasi**: `config/server_templates.json`

**Format**:
```json
{
  "templates": {
    "template_id": {
      "name": "Template Name",
      "description": "Template description",
      "command": "command with {port} placeholder",
      "default_port": 8000,
      "category": "Technology",
      "env_vars": {},
      "requirements": ["file1", "file2"],
      "icon": "icon_name"
    }
  }
}
```

### Template Fields

#### Name
- **Type**: String
- **Description**: Nama template yang ditampilkan di UI
- **Example**: `"Laravel Project"`

#### Description
- **Type**: String
- **Description**: Deskripsi template
- **Example**: `"Laravel development server with artisan serve"`

#### Command
- **Type**: String
- **Description**: Command template dengan placeholder {port}
- **Example**: `"php artisan serve --port={port}"`

#### Default Port
- **Type**: Number
- **Description**: Port default untuk template
- **Example**: `8000`

#### Category
- **Type**: String
- **Description**: Kategori teknologi
- **Example**: `"PHP"`, `"Node.js"`, `"Python"`

#### Requirements
- **Type**: Array
- **Description**: File yang diperlukan untuk template
- **Example**: `["composer.json", "artisan"]`

### Built-in Templates

#### Laravel/PHP
```json
{
  "laravel": {
    "name": "Laravel Project",
    "description": "Laravel development server",
    "command": "php artisan serve --port={port}",
    "default_port": 8000,
    "category": "PHP",
    "env_vars": {
      "APP_ENV": "local"
    },
    "requirements": ["artisan", "composer.json"]
  }
}
```

#### Node.js/Express
```json
{
  "nodejs": {
    "name": "Node.js Project",
    "description": "Node.js development server",
    "command": "npm start",
    "default_port": 3000,
    "category": "Node.js",
    "env_vars": {
      "NODE_ENV": "development"
    },
    "requirements": ["package.json"]
  }
}
```

#### Python/Flask
```json
{
  "python-flask": {
    "name": "Python Flask",
    "description": "Python Flask development server",
    "command": "python app.py",
    "default_port": 5000,
    "category": "Python",
    "env_vars": {
      "FLASK_ENV": "development"
    },
    "requirements": ["app.py"]
  }
}
```

---

## 🎨 Theme Configuration

### theme_config.json
File konfigurasi untuk tema UI aplikasi.

**Lokasi**: `config/theme_config.json`

**Format**:
```json
{
  "current_theme": "dark",
  "themes": {
    "dark": {
      "bg": "#2c3e50",
      "frame_bg": "#34495e",
      "fg": "#ecf0f1",
      "button_bg": "#3498db",
      "button_fg": "#ffffff",
      "button_active_bg": "#2980b9",
      "text_bg": "#2c3e50",
      "text_fg": "#ecf0f1",
      "entry_bg": "#34495e",
      "entry_fg": "#ecf0f1",
      "select_bg": "#3498db",
      "select_fg": "#ffffff",
      "scrollbar_bg": "#34495e",
      "scrollbar_fg": "#3498db"
    }
  }
}
```

### Theme Fields

#### Current Theme
- **Type**: String
- **Description**: Tema yang sedang aktif
- **Values**: `"system"`, `"dark"`, `"light"`

#### Color Definitions
- **bg**: Background utama
- **frame_bg**: Background frame/panel
- **fg**: Foreground/text color
- **button_bg**: Background tombol
- **button_fg**: Text color tombol
- **button_active_bg**: Background tombol aktif
- **text_bg**: Background text area
- **text_fg**: Text color
- **entry_bg**: Background input field
- **entry_fg**: Text color input field
- **select_bg**: Background selection
- **select_fg**: Text color selection
- **scrollbar_bg**: Background scrollbar
- **scrollbar_fg**: Foreground scrollbar

### Built-in Themes

#### Dark Theme
```json
{
  "dark": {
    "bg": "#2c3e50",
    "frame_bg": "#34495e",
    "fg": "#ecf0f1",
    "button_bg": "#3498db",
    "button_fg": "#ffffff",
    "button_active_bg": "#2980b9",
    "text_bg": "#2c3e50",
    "text_fg": "#ecf0f1",
    "entry_bg": "#34495e",
    "entry_fg": "#ecf0f1",
    "select_bg": "#3498db",
    "select_fg": "#ffffff",
    "scrollbar_bg": "#34495e",
    "scrollbar_fg": "#3498db"
  }
}
```

#### Light Theme
```json
{
  "light": {
    "bg": "#ffffff",
    "frame_bg": "#f8f9fa",
    "fg": "#212529",
    "button_bg": "#007bff",
    "button_fg": "#ffffff",
    "button_active_bg": "#0056b3",
    "text_bg": "#ffffff",
    "text_fg": "#212529",
    "entry_bg": "#ffffff",
    "entry_fg": "#212529",
    "select_bg": "#007bff",
    "select_fg": "#ffffff",
    "scrollbar_bg": "#f8f9fa",
    "scrollbar_fg": "#007bff"
  }
}
```

---

## 🔧 Advanced Settings

### Update Configuration

#### update_cache.json
File cache untuk update checking.

**Lokasi**: `config/update_cache.json`

**Format**:
```json
{
  "last_check": "2025-01-11T10:00:00Z",
  "current_version": "1.0.1",
  "latest_version": "1.0.1",
  "update_available": false,
  "auto_check": true,
  "check_interval": 86400
}
```

### Log Configuration

#### Log Levels
- **DEBUG**: Informasi detail untuk debugging
- **INFO**: Informasi umum
- **WARNING**: Peringatan
- **ERROR**: Error yang tidak fatal
- **CRITICAL**: Error fatal

#### Log Files
- **devservermanager.log**: Log aplikasi utama
- **servermanager.log**: Log server management

---

## 🌍 Environment Variables

### Global Environment Variables

Aplikasi mendukung environment variables global:

```json
{
  "env_vars": {
    "NODE_ENV": "development",
    "APP_ENV": "local",
    "DEBUG": "true"
  }
}
```

### Server-specific Environment Variables

Setiap server bisa memiliki environment variables sendiri:

```json
{
  "server_name": {
    "env_vars": {
      "DATABASE_URL": "sqlite:///app.db",
      "SECRET_KEY": "your-secret-key",
      "PORT": "8000"
    }
  }
}
```

### Environment Variable Precedence

1. Server-specific env vars
2. Global env vars
3. System env vars

---

## 💻 Custom Commands

### Command Templates

Anda bisa membuat custom command template:

```json
{
  "custom_commands": {
    "git_status": {
      "name": "Git Status",
      "command": "git status",
      "description": "Check git status"
    },
    "npm_install": {
      "name": "NPM Install",
      "command": "npm install",
      "description": "Install npm packages"
    }
  }
}
```

### Command Variables

Commands mendukung variable substitution:

- `{port}`: Port server
- `{path}`: Path server
- `{name}`: Nama server

**Example**:
```json
{
  "command": "cd {path} && npm run dev -- --port {port}"
}
```

---

## 🔒 Security Configuration

### File Permissions

Pastikan file konfigurasi memiliki permission yang tepat:

```bash
# Windows
icacls config\*.json /grant Users:F

# Linux/Mac
chmod 644 config/*.json
```

### Sensitive Data

Jangan simpan data sensitif di file konfigurasi:

```json
{
  "env_vars": {
    "API_KEY": "${API_KEY}",  // Gunakan environment variable
    "SECRET": "***"           // Jangan hardcode
  }
}
```

---

## 📝 Best Practices

### Configuration Management

1. **Backup Regular**
   - Backup folder `config/` secara regular
   - Simpan backup di lokasi aman

2. **Version Control**
   - Commit file konfigurasi ke Git
   - Exclude file dengan data sensitif

3. **Documentation**
   - Dokumentasikan custom template
   - Update dokumentasi saat ada perubahan

### Performance Optimization

1. **Limit Server Count**
   - Maksimal 10 server aktif
   - Stop server yang tidak digunakan

2. **Log Management**
   - Rotate log files secara regular
   - Set log level yang sesuai

3. **Resource Monitoring**
   - Monitor CPU dan memory usage
   - Restart aplikasi jika perlu

---

## 🆘 Troubleshooting

### Common Issues

#### Configuration Not Saved
- Cek permission folder `config/`
- Pastikan aplikasi punya akses write

#### Invalid JSON Format
- Validasi JSON dengan online validator
- Cek syntax error di file

#### Template Not Loading
- Cek format file `server_templates.json`
- Pastikan template ID unik

### Debug Mode

Aktifkan debug mode untuk troubleshooting:

```json
{
  "debug": true,
  "log_level": "DEBUG",
  "verbose_logging": true
}
```

---

**Last Updated**: 11 September 2025  
**Version**: 1.0.1  
**Developer**: idpcks
