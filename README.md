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

**GearGuard** is a powerful Odoo 17 module designed for tracking and managing company assets including machines, vehicles, computers, and other equipment. It provides a complete solution for maintenance teams to handle corrective and preventive maintenance with advanced features like work center management, cost tracking, smart reminders, and intelligent workflow automation.

### 🎯 Core Philosophy

The module seamlessly connects three core entities:
- **Equipment** - What is broken (assets, machines, devices)
- **Teams** - Who fixes it (specialized maintenance teams)
- **Requests** - The work to be done (corrective or preventive)

### � Perfect For
- Manufacturing facilities
- IT departments
- Fleet management
- Facility maintenance teams
- Equipment rental companies
- Any organization with assets requiring maintenance

---

## ✨ Features

### 📦 Equipment Management
- **Central Database** - Track all company assets in one place
- **Flexible Ownership Types**:
  - 🏢 **Company** - Assets owned by the organization
  - 🏛️ **Department** - Assets assigned to departments (e.g., Production, IT)
  - 👤 **Employee** - Assets assigned to specific individuals (e.g., laptops)
- **Categories** - Organize equipment by type (Machinery, Vehicles, IT Equipment, Office, HVAC, Electrical)
- **Work Center Assignment** - Link equipment to maintenance work centers
- **Warranty Tracking** - Monitor purchase dates and warranty expiration with visual status badges
- **Location Management** - Track where equipment is physically located
- **Scrap Management** - Mark equipment as scrapped with full audit trail

### 👥 Maintenance Teams
- **Specialized Teams** - Create teams for different expertise:
  - Mechanics, Electricians, IT Support, HVAC Technicians, Plumbers, Facilities
- **Team Members** - Assign technicians to teams with role-based access
- **Team Leaders** - Designate team leaders for management
- **Color Coding** - Visual identification in Kanban views
- **Workload Tracking** - Monitor open requests per team

### 🔧 Maintenance Requests
- **Request Types**:
  - ⚡ **Corrective** - Unplanned repair (Breakdown)
  - 📅 **Preventive** - Planned maintenance (Routine Checkup)
- **Stage Workflow** - New → In Progress → Repaired → Scrap
- **Priority Levels** - Low, Normal, High, Urgent (with star indicators)
- **Auto-Fill Logic** - Selecting equipment automatically fills team and category
- **Team Validation** - Technicians can only be assigned from the designated team
- **Duration Tracking** - Automatic calculation of maintenance time
- **Smart Reminders** - Configurable reminder days before deadline
- **Cost Tracking** - Estimated and actual cost fields with currency support
- **Overdue Indicators** - Visual red strips for overdue requests

### 🏭 Work Centers
- **Maintenance Bays** - Define physical locations for maintenance work
- **Cost Management** - Hourly cost and capacity cost tracking
- **Capacity Planning** - Set work center capacity limits
- **Utilization Rate** - Monitor work center efficiency
- **Alternate Centers** - Define backup work centers
- **Team Assignment** - Link work centers to maintenance teams

### 📊 Views & Reporting
- **Kanban Board** - Visual drag-and-drop with stage grouping
- **Calendar View** - Schedule preventive maintenance (shows ONLY preventive requests)
- **List View** - Detailed tabular view with inline editing
- **Pivot Tables** - Analyze data by multiple dimensions
- **Graph Reports** - Visual charts for trends analysis
- **Smart Buttons** - Quick access to related records with counts

### 🔐 Business Logic
- **Smart Buttons** - Equipment form shows maintenance count badge
- **Scrap Logic** - Moving request to Scrap stage automatically marks equipment as scrapped
- **Chatter Integration** - Full audit trail with messages and activities
- **Constraint Validation** - Ensures data integrity (technician must be team member)

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
│   ├── __manifest__.py     # Module manifest
│   ├── models/             # Business logic (6 models)
│   │   ├── equipment.py
│   │   ├── equipment_category.py
│   │   ├── maintenance_request.py
│   │   ├── maintenance_stage.py
│   │   ├── maintenance_team.py
│   │   └── work_center.py
│   ├── views/              # User interface (6 view files)
│   ├── security/           # Access control
│   ├── data/              # Default stages & categories
│   └── demo/              # Comprehensive demo data
└── README.md
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
   - Email: `admin@gearguard.com`
   - Password: (your choice)
   - ✅ **Check "Demo Data"** for sample records
3. **Enable Developer Mode**: Settings → Activate Developer Mode
4. **Update Apps List**: Apps → ☰ Menu → Update Apps List
5. **Install GearGuard**: Remove "Apps" filter → Search "GearGuard" → Install

### Module Navigation

| Menu | Description |
|------|-------------|
| **GearGuard** | Main application menu |
| **Maintenance** | All Requests, My Requests, Calendar |
| **Equipment** | All Equipment, By Department, By Employee, Categories |
| **Work Centers** | Configure maintenance bays |
| **Teams** | Manage maintenance teams |
| **Reporting** | Maintenance Analysis (Pivot/Graph) |
| **Configuration** | Categories, Teams (admin only) |

### Quick Workflows

#### Flow 1: The Breakdown (Corrective Maintenance)
1. **Any user creates a request** - GearGuard → Maintenance → All Requests → Create
2. **Auto-Fill Magic** - Select Equipment → Team & Category auto-populate!
3. **Request starts in "New"** stage
4. **Technician assigns themselves** - Click "Assign to Me" button
5. **Stage moves to "In Progress"** - Drag card or use statusbar
6. **Completion** - Record Duration (Hours Spent) → Move to "Repaired"

#### Flow 2: The Routine Checkup (Preventive Maintenance)
1. **Manager creates preventive request** - Set type to "Preventive (Routine)"
2. **Set Scheduled Date** - e.g., Next Monday
3. **View on Calendar** - GearGuard → Maintenance → Calendar
4. **Technician sees job** - Scheduled date appears on calendar

#### Creating Equipment
1. **GearGuard → Equipment → All Equipment → Create**
2. Enter: Name, Serial Number, Category
3. Select: Ownership Type (Company/Department/Employee)
4. Assign: Department or Employee based on ownership
5. Set: Maintenance Team, Work Center, Location
6. Add: Purchase Date, Warranty Expiry

---

## 📦 Demo Data Included

The module comes with comprehensive demo data for testing:

### Organizations
| Entity | Count | Examples |
|--------|-------|----------|
| **Departments** | 6 | Production, IT, Warehouse, Facilities, Sales, Administration |
| **Employees** | 7 | John Miller, Sarah Chen, Alex Kumar, David Brown, etc. |

### Maintenance Infrastructure
| Entity | Count | Examples |
|--------|-------|----------|
| **Teams** | 6 | Mechanics, Electricians, IT Support, HVAC, Plumbers, Facilities |
| **Work Centers** | 6 | Machine Shop, Electronics Lab, IT Service Bay, HVAC Workshop, etc. |

### Equipment (21 Items)
| Category | Count | Ownership Types |
|----------|-------|-----------------|
| Machinery | 4 | CNC Machines, Lathe, Hydraulic Press |
| Vehicles | 4 | Forklifts, Delivery Van, Company Car |
| IT Equipment | 5 | Servers, Network Switch, Laptops |
| Office | 3 | Printers, Projector |
| HVAC | 3 | AC Units, Industrial Fan |
| Electrical | 2 | Generator, UPS System |

### Maintenance Requests (27 Total)
| Stage | Count | Highlights |
|-------|-------|------------|
| **New** | 8 | Includes 3 overdue requests (red indicators!) |
| **In Progress** | 5 | Active repairs being worked |
| **Repaired** | 7 | Recently completed |
| **Scheduled** | 7 | Future preventive maintenance (calendar view) |

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
│   ├── maintenance_request_views.xml
│   ├── work_center_views.xml
│   └── menu_views.xml
│
├── security/                       # Access control
│   ├── ir.model.access.csv
│   └── gearguard_security.xml
│
├── data/                           # Default data
│   ├── maintenance_stage_data.xml  # New, In Progress, Repaired, Scrap
│   └── equipment_category_data.xml # Machinery, Vehicles, IT, etc.
│
├── demo/                           # Demo records
│   └── demo_data.xml               # 21 equipment, 27 requests, 6 teams
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
| `ownership_type` | Selection | **company** / department / employee |
| `department_id` | Many2one | Owner department (if type=department) |
| `employee_id` | Many2one | Owner employee (if type=employee) |
| `work_center_id` | Many2one | Assigned work center |
| `maintenance_team_id` | Many2one | Responsible team (required) |
| `technician_id` | Many2one | Default technician |
| `location` | Char | Physical location |
| `purchase_date` | Date | Date of purchase |
| `warranty_expiry` | Date | Warranty end date |
| `warranty_status` | Selection | Computed: valid/expired/na |
| `is_scrap` | Boolean | Equipment scrapped flag |
| `open_request_count` | Integer | Computed: open maintenance count |

#### `maintenance.request`
| Field | Type | Description |
|-------|------|-------------|
| `name` | Char | Request subject (required) |
| `description` | Html | Detailed description |
| `equipment_id` | Many2one | Related equipment (required) |
| `category_id` | Many2one | Auto-filled from equipment |
| `request_type` | Selection | **corrective** / preventive |
| `priority` | Selection | 0=Low, 1=Normal, 2=High, 3=Urgent |
| `stage_id` | Many2one | Current workflow stage |
| `maintenance_team_id` | Many2one | Assigned team (auto-filled) |
| `technician_id` | Many2one | Assigned technician (must be team member) |
| `work_center_id` | Many2one | Assigned work center |
| `scheduled_date` | Datetime | Scheduled date (for calendar) |
| `deadline` | Date | Due date for completion |
| `is_overdue` | Boolean | Computed: deadline passed? |
| `duration` | Float | Time spent (hours) |
| `estimated_cost` | Float | Estimated repair cost |
| `actual_cost` | Float | Final cost after repair |
| `reminder_days` | Integer | Days before reminder |
| `reminder_date` | Date | Computed reminder date |

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

#### `maintenance.team`
| Field | Type | Description |
|-------|------|-------------|
| `name` | Char | Team name (required) |
| `color` | Integer | Kanban color index |
| `member_ids` | Many2many | Team members (res.users) |
| `team_leader_id` | Many2one | Team leader |
| `note` | Text | Team description |
| `equipment_count` | Integer | Computed: assigned equipment |
| `request_count` | Integer | Computed: total requests |
| `open_request_count` | Integer | Computed: open requests |

---

## 🔒 Security

### User Groups

| Group | Access Level |
|-------|--------------|
| **Maintenance / User** | View requests, create own |
| **Maintenance / Technician** | Edit requests, equipment |
| **Maintenance / Manager** | Full CRUD on all records |

### Access Rights Summary

| Model | User | Technician | Manager |
|-------|------|------------|---------|
| Equipment | Read | Read, Write | Full |
| Maintenance Request | Read, Create, Write | Full Write | Full |
| Work Center | Read | Read, Write | Full |
| Maintenance Team | Read | Read | Full |
| Equipment Category | Read | Read | Full |

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

### Version 17.0.1.1.0 (Current)
- Added **Company** ownership type for equipment
- Enhanced **Calendar View** - now shows ONLY preventive maintenance
- Added **Technician Validation** - must be team member constraint
- Comprehensive **Demo Data** - 21 equipment, 27 requests, 6 teams
- Improved **Overdue Indicators** - red visual strips
- Enhanced **Auto-Fill Logic** on equipment selection

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
