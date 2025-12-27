# -*- coding: utf-8 -*-
{
    'name': 'GearGuard - Maintenance Tracker',
    'version': '17.0.1.0.0',
    'category': 'Maintenance',
    'summary': 'The Ultimate Maintenance Management System',
    'description': """
        GearGuard: Maintenance Management System
        =========================================
        - Track company assets (machines, vehicles, computers)
        - Manage maintenance requests
        - Connect Equipment, Teams, and Requests seamlessly
        - Work Center cost tracking
        
        Features:
        - Equipment tracking by Department and Employee
        - Maintenance Team management
        - Work Centers with hourly costs and capacity
        - Corrective and Preventive maintenance requests
        - Kanban board with drag-and-drop
        - Calendar view for scheduled maintenance
        - Smart buttons and automated workflows
        - Reminder system for upcoming maintenance
    """,
    'author': 'GearGuard Team',
    'website': 'https://github.com/Gurjas2112/GearGuard',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'hr',
        'mail',
        'resource',  # For resource.calendar (working hours)
    ],
    'data': [
        # Security
        'security/gearguard_security.xml',
        'security/ir.model.access.csv',
        
        # Data
        'data/maintenance_stage_data.xml',
        'data/equipment_category_data.xml',
        
        # Views
        'views/equipment_category_views.xml',
        'views/equipment_views.xml',
        'views/maintenance_team_views.xml',
        'views/work_center_views.xml',
        'views/maintenance_request_views.xml',
        'views/menu_views.xml',
    ],
    'demo': [
        'demo/demo_data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'sequence': 1,
}
