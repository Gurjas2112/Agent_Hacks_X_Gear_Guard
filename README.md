# 🔧 GearGuard - The Ultimate Maintenance Tracker

<div align="center">

![GearGuard Logo](https://img.shields.io/badge/GearGuard-Maintenance%20Tracker-00A09D?style=for-the-badge&logo=odoo&logoColor=white)

**A comprehensive maintenance management system for Odoo 17**

[![Odoo Version](https://img.shields.io/badge/Odoo-17.0-875A7B?style=flat-square&logo=odoo)](https://www.odoo.com)
[![License](https://img.shields.io/badge/License-LGPL--3-blue?style=flat-square)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white)](docker-compose.yml)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)

[Features](#-features) • [Installation](#-installation) • [Docker Setup](#-docker-setup) • [Usage](#-usage) • [API Reference](#-api-reference)

</div>

---

## 📋 Overview

**GearGuard** is a powerful Odoo 17 module designed for tracking and managing company assets including machines, vehicles, computers, and other equipment. It provides a complete solution for maintenance teams to handle corrective and preventive maintenance with advanced features like work center management, cost tracking, and smart reminders.

### 🎯 Perfect For
- Manufacturing facilities
- IT departments
- Fleet management
- Facility maintenance teams
- Equipment rental companies

---

## ✨ Features

### 📦 Equipment Management
- **Central Database** - Track all company assets in one place
- **Ownership Types** - Company, Department, or Employee-owned equipment
- **Categories** - Organize equipment by type (Machinery, Vehicles, IT, Office)
- **Work Center Assignment** - Link equipment to maintenance work centers
- **Warranty Tracking** - Monitor purchase dates and warranty expiration
- **Location Management** - Track where equipment is located

### 👥 Maintenance Teams
- **Specialized Teams** - Create teams for different expertise (Mechanics, Electricians, IT)
- **Team Members** - Assign technicians to teams
- **Color Coding** - Visual identification in Kanban views
- **Workload Tracking** - Monitor open requests per team

### 🔧 Maintenance Requests
- **Request Types** - Corrective (breakdown) and Preventive (routine)
- **Stage Workflow** - New → In Progress → Repaired → Scrap
- **Priority Levels** - Low, Medium, High, Critical
- **Duration Tracking** - Automatic calculation of maintenance time
- **Smart Reminders** - Configurable reminder days before deadline
- **Cost Tracking** - Estimated and actual cost fields
- **Work Center Assignment** - Route requests to specific work centers

### 🏭 Work Centers
- **Maintenance Bays** - Define physical locations for maintenance work
- **Cost Management** - Hourly cost and capacity cost tracking
- **Capacity Planning** - Set work center capacity limits
- **Utilization Rate** - Monitor work center efficiency
- **Alternate Centers** - Define backup work centers
- **Team Assignment** - Link work centers to maintenance teams

### 📊 Reporting & Analytics
- **Kanban Boards** - Visual drag-and-drop management
- **Calendar View** - Schedule maintenance activities
- **Pivot Tables** - Analyze data by multiple dimensions
- **Graph Reports** - Visual charts for trends analysis
- **Smart Buttons** - Quick access to related records

---

## 🚀 Installation

### Prerequisites
- Odoo 17.0 Community or Enterprise
- PostgreSQL 12+
- Python 3.10+
- Docker & Docker Compose (for containerized setup)

### Method 1: Docker Compose (Recommended)

The fastest way to get started:

```bash
# Clone the repository
git clone https://github.com/Gurjas2112/GearGuard.git
cd GearGuard

# Start with Docker Compose
docker-compose up -d

# Access Odoo at http://localhost:8069
```

### Method 2: Build Custom Docker Image

```bash
# Build the image
docker build -t gearguard-odoo:17.0 .

# Run with PostgreSQL
docker run -d -e POSTGRES_USER=odoo -e POSTGRES_PASSWORD=odoo \
  -e POSTGRES_DB=postgres --name db postgres:15

docker run -p 8069:8069 --name odoo --link db:db -t gearguard-odoo:17.0
```

### Method 3: Manual Installation

```bash
# Clone to your Odoo addons directory
cd /path/to/odoo/addons
git clone https://github.com/Gurjas2112/GearGuard.git

# Or copy the gearguard folder
cp -r /path/to/GearGuard/gearguard /path/to/odoo/addons/

# Restart Odoo and update apps list
sudo systemctl restart odoo
```

---

## 🐳 Docker Setup

### Project Structure

```
GearGuard/
├── Dockerfile              # Custom Odoo image
├── docker-compose.yml      # Multi-container setup
├── gearguard/              # Odoo module
│   ├── __manifest__.py
│   ├── models/
│   ├── views/
│   ├── security/
│   └── ...
└── README.md
```

### Dockerfile

```dockerfile
# GearGuard - Odoo 17 Maintenance Module
FROM odoo:17.0

LABEL maintainer="GearGuard Team <gearguard@example.com>"
LABEL description="GearGuard - The Ultimate Maintenance Tracker for Odoo 17"
LABEL version="17.0.1.0.0"

USER root

# Install dependencies
RUN pip3 install --no-cache-dir python-dateutil pytz

# Copy module
RUN mkdir -p /mnt/extra-addons/gearguard
COPY ./gearguard /mnt/extra-addons/gearguard
RUN chown -R odoo:odoo /mnt/extra-addons/gearguard

USER odoo

EXPOSE 8069 8071 8072

CMD ["odoo"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    container_name: gearguard-db
    environment:
      - POSTGRES_DB=postgres
      - POSTGRES_PASSWORD=odoo
      - POSTGRES_USER=odoo
    volumes:
      - odoo-db-data:/var/lib/postgresql/data
    restart: unless-stopped

  odoo:
    image: odoo:17.0
    container_name: gearguard-odoo
    depends_on:
      - db
    ports:
      - "8069:8069"
    environment:
      - HOST=db
      - USER=odoo
      - PASSWORD=odoo
    volumes:
      - odoo-web-data:/var/lib/odoo
      - ./gearguard:/mnt/extra-addons/gearguard
    command: ["odoo", "--addons-path=/mnt/extra-addons,/usr/lib/python3/dist-packages/odoo/addons"]
    restart: unless-stopped

volumes:
  odoo-db-data:
  odoo-web-data:
```

### Docker Commands Reference

| Command | Description |
|---------|-------------|
| `docker-compose up -d` | Start all containers in background |
| `docker-compose down` | Stop and remove containers |
| `docker-compose logs -f odoo` | View Odoo logs in real-time |
| `docker-compose restart odoo` | Restart Odoo after changes |
| `docker-compose down -v` | Remove containers AND volumes (data) |
| `docker-compose ps` | Check container status |
| `docker-compose exec odoo bash` | Shell into Odoo container |

### Troubleshooting Docker

**Container won't start:**
```bash
# Check logs
docker-compose logs odoo

# Verify PostgreSQL is ready
docker-compose logs db
```

**Module not appearing:**
```bash
# Restart Odoo to reload addons
docker-compose restart odoo

# Then in Odoo: Apps → Update Apps List
```

**Database errors:**
```bash
# Reset everything
docker-compose down -v
docker-compose up -d
```

---

## 📖 Usage

### First-Time Setup

1. **Access Odoo** at `http://localhost:8069`
2. **Create Database**:
   - Database Name: `gearguard`
   - Email: `admin@example.com`
   - Password: (your choice)
   - ✅ Check "Demo Data" for sample records
3. **Enable Developer Mode**: Settings → Activate Developer Mode
4. **Update Apps List**: Apps → ☰ Menu → Update Apps List
5. **Install GearGuard**: Remove "Apps" filter → Search "GearGuard" → Install

### Module Navigation

| Menu | Description |
|------|-------------|
| **GearGuard** | Main application menu |
| **Equipment** | Manage all company assets |
| **Maintenance** | Handle maintenance requests |
| **Work Centers** | Configure maintenance bays |
| **Configuration** | Teams, Categories settings |
| **Reporting** | Analytics and reports |

### Quick Workflows

#### Creating Equipment
1. **GearGuard → Equipment → All Equipment → Create**
2. Enter: Name, Serial Number, Category
3. Select: Ownership Type, Work Center, Team
4. Add: Purchase Date, Warranty Expiry, Location

#### Creating Maintenance Requests
1. **GearGuard → Maintenance → All Requests → Create**
2. Enter: Subject, Description
3. Select: Equipment (auto-fills team & work center)
4. Set: Request Type, Priority, Estimated Cost
5. Configure: Reminder Days

#### Setting Up Work Centers
1. **GearGuard → Work Centers → Create**
2. Enter: Name, Code, Location
3. Set: Capacity, Hourly Cost, Capacity Cost
4. Assign: Maintenance Team, Alternate Centers

---

## 🗂️ Module Structure

```
gearguard/
├── __init__.py                     # Package init
├── __manifest__.py                 # Module manifest
│
├── models/                         # Business logic
│   ├── __init__.py
│   ├── equipment_category.py       # Equipment categories
│   ├── equipment.py                # Main equipment model
│   ├── maintenance_team.py         # Maintenance teams
│   ├── maintenance_stage.py        # Workflow stages
│   ├── maintenance_request.py      # Maintenance requests
│   └── work_center.py              # Work centers
│
├── views/                          # User interface
│   ├── equipment_category_views.xml
│   ├── equipment_views.xml
│   ├── maintenance_team_views.xml
│   ├── maintenance_stage_views.xml
│   ├── maintenance_request_views.xml
│   ├── work_center_views.xml
│   └── menu_views.xml
│
├── security/                       # Access control
│   ├── ir.model.access.csv
│   └── security.xml
│
├── data/                           # Default data
│   └── maintenance_stage_data.xml
│
├── demo/                           # Demo records
│   └── demo_data.xml
│
└── static/description/             # Module assets
    └── icon.png
```

---

## 🔌 API Reference

### Models Overview

#### `equipment.equipment`
| Field | Type | Description |
|-------|------|-------------|
| `name` | Char | Equipment name (required) |
| `serial_number` | Char | Unique serial number |
| `category_id` | Many2one | Equipment category |
| `ownership_type` | Selection | company/department/employee |
| `department_id` | Many2one | Owner department |
| `employee_id` | Many2one | Owner employee |
| `work_center_id` | Many2one | Assigned work center |
| `maintenance_team_id` | Many2one | Responsible team |
| `location` | Char | Physical location |
| `purchase_date` | Date | Date of purchase |
| `warranty_expiry` | Date | Warranty end date |
| `note` | Html | Additional notes |

#### `maintenance.request`
| Field | Type | Description |
|-------|------|-------------|
| `name` | Char | Request subject (required) |
| `description` | Html | Detailed description |
| `equipment_id` | Many2one | Related equipment |
| `request_type` | Selection | corrective/preventive |
| `priority` | Selection | 0=Low, 1=Medium, 2=High, 3=Critical |
| `stage_id` | Many2one | Current workflow stage |
| `maintenance_team_id` | Many2one | Assigned team |
| `work_center_id` | Many2one | Assigned work center |
| `user_id` | Many2one | Assigned technician |
| `schedule_date` | Date | Scheduled date |
| `estimated_cost` | Float | Estimated repair cost |
| `actual_cost` | Float | Final cost after repair |
| `reminder_days` | Integer | Days before reminder |
| `reminder_date` | Date | Computed reminder date |
| `duration` | Float | Time spent (hours) |

#### `maintenance.work.center`
| Field | Type | Description |
|-------|------|-------------|
| `name` | Char | Work center name (required) |
| `code` | Char | Unique identifier code |
| `location` | Char | Physical location |
| `active` | Boolean | Active status |
| `capacity` | Float | Maximum capacity |
| `hourly_cost` | Float | Cost per hour ($) |
| `capacity_cost` | Float | Cost per capacity unit ($) |
| `total_cost` | Float | Computed: hourly + (capacity × capacity_cost) |
| `utilization_rate` | Float | Current utilization percentage |
| `maintenance_team_id` | Many2one | Assigned maintenance team |
| `alternate_workcenter_ids` | Many2many | Backup work centers |
| `note` | Text | Additional notes |

#### `maintenance.team`
| Field | Type | Description |
|-------|------|-------------|
| `name` | Char | Team name (required) |
| `color` | Integer | Kanban color index |
| `member_ids` | Many2many | Team members (res.users) |
| `note` | Html | Team description |
| `request_ids` | One2many | Related maintenance requests |
| `request_count` | Integer | Computed request count |

---

## 🔒 Security

### User Groups

| Group | Access Level |
|-------|--------------|
| **Maintenance / User** | View, Create, Edit own records |
| **Maintenance / Manager** | Full CRUD on all records |

### Access Rights Summary

| Model | User | Manager |
|-------|------|---------|
| Equipment | Read, Create, Write | Full |
| Maintenance Request | Read, Create, Write | Full |
| Work Center | Read | Full |
| Maintenance Team | Read | Full |
| Equipment Category | Read | Full |

---

## 🧪 Testing

### Validate Python Syntax
```bash
python -m py_compile gearguard/models/*.py
python -m py_compile gearguard/__init__.py
python -m py_compile gearguard/__manifest__.py
```

### Validate XML Files
```bash
python -c "
import xml.etree.ElementTree as ET
import glob
for f in glob.glob('gearguard/**/*.xml', recursive=True):
    try:
        ET.parse(f)
        print(f'✓ {f}')
    except Exception as e:
        print(f'✗ {f}: {e}')
"
```

### Run Odoo Unit Tests
```bash
./odoo-bin -d test_db -i gearguard --test-enable --stop-after-init
```

---

## 📝 Changelog

### Version 17.0.1.0.0
- Initial release for Odoo 17
- Equipment management with categories
- Maintenance request workflow
- Work center management with cost tracking
- Kanban, Calendar, Pivot, Graph views
- Docker support with Compose

---

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** changes (`git commit -m 'Add amazing feature'`)
4. **Push** to branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/GearGuard.git
cd GearGuard

# Create branch
git checkout -b feature/my-feature

# Start Docker for testing
docker-compose up -d

# Make changes and test...

# Commit and push
git add .
git commit -m "Add my feature"
git push origin feature/my-feature
```

---

## 📄 License

This project is licensed under the **LGPL-3.0** License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**GearGuard Team**

- 🌐 GitHub: [@Gurjas2112](https://github.com/Gurjas2112/GearGuard)
- 📧 Repository: [GearGuard](https://github.com/Gurjas2112/GearGuard)

---

## 🙏 Acknowledgments

- [Odoo SA](https://www.odoo.com) - The amazing open-source ERP platform
- [Odoo Community Association](https://odoo-community.org/) - OCA modules inspiration
- [Docker](https://www.docker.com) - Containerization platform
- All contributors and testers

---

<div align="center">

### ⭐ Star this repository if you find it helpful!

**Built with ❤️ for the Odoo Hackathon**

[![GitHub stars](https://img.shields.io/github/stars/Gurjas2112/GearGuard?style=social)](https://github.com/Gurjas2112/GearGuard/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Gurjas2112/GearGuard?style=social)](https://github.com/Gurjas2112/GearGuard/network/members)

</div>
