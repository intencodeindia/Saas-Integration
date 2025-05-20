# SaaS Integration for ERPNext

**SaaS Integration** is a custom Frappe application designed to integrate subscription data from external SaaS platforms into ERPNext. It centralizes customer and billing data, enabling better visibility, automation, and reporting for businesses.

---

## ✨ Features

- **Automated Data Import**: Pulls subscription data from SaaS platforms effortlessly.
- **ERPNext Integration**: Seamlessly connects with ERPNext for unified data management.
- **Flexible Sync Options**: Supports real-time or scheduled data synchronization.
- **Modular Design**: Scalable and adaptable for additional SaaS platforms.
- **Extensible**: Built to support future integrations and customizations.

---

## 📦 Installation

Follow these steps to install the SaaS Integration app on your ERPNext (v15) instance:

### 1. Clone the Repository

```bash
cd ~/frappe-bench/apps
git clone https://github.com/intencodeindia/Saas-Integration.git
```

### 2. Install the App

```bash
bench --site your-site-name install-app saas_integration
```

> **Note**: Replace `your-site-name` with the name of your ERPNext site.

### 3. Restart Bench

```bash
bench restart
```

---

## 📂 Project Structure

```
Saas-Integration/
├── saas_integration/      # Core application module
├── .github/              # GitHub workflows and configurations
├── .gitignore            # Git ignore rules
├── license.txt           # License file
├── pyproject.toml        # Python project configuration
└── README.md             # This file
```

---

## 📋 Requirements

- **ERPNext**: v15.x
- **Frappe Framework**: v15.x
- **Python**: 3.10 or higher

---

## 📜 License

This project is licensed under the MIT License. See the [license.txt](license.txt) file for details.

---

## 👨‍💻 Maintainers

Developed and maintained by [Intencode India](https://github.com/intencodeindia).

---

## 🤝 Contributing

We welcome contributions! To contribute:

1. Fork the repository.
2. Create a feature branch:

   ```bash
   git checkout -b feature/your-feature
   ```

3. Commit your changes:

   ```bash
   git commit -m "Add your feature"
   ```

4. Push to the branch:

   ```bash
   git push origin feature/your-feature
   ```

5. Open a Pull Request.

For major changes, please open an issue first to discuss your proposed changes.

---

## 📬 Support

For questions or support, open an issue on [GitHub](https://github.com/intencodeindia/Saas-Integration/issues) or contact the maintainers.
