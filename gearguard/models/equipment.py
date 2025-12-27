# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Equipment(models.Model):
    """Equipment Model
    
    Central database for all company assets - machines, vehicles, computers, etc.
    Tracks ownership, technical details, and links to maintenance teams.
    """
    _name = 'equipment.equipment'
    _description = 'Equipment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    # -------------------------------------------------------------------------
    # BASIC FIELDS
    # -------------------------------------------------------------------------
    
    name = fields.Char(
        string='Equipment Name',
        required=True,
        tracking=True,
        help="Name of the equipment (e.g., CNC Machine #1, Delivery Truck #3)"
    )
    
    serial_number = fields.Char(
        string='Serial Number',
        tracking=True,
        help="Manufacturer's serial number"
    )
    
    active = fields.Boolean(
        string='Active',
        default=True,
        help="Set to false to hide the equipment without deleting it"
    )
    
    image = fields.Binary(
        string='Image',
        attachment=True,
        help="Equipment photo"
    )
    
    note = fields.Html(
        string='Internal Notes',
        help="Additional notes about this equipment"
    )
    
    color = fields.Integer(
        string='Color Index'
    )
    
    # -------------------------------------------------------------------------
    # CATEGORY & CLASSIFICATION
    # -------------------------------------------------------------------------
    
    category_id = fields.Many2one(
        'equipment.category',
        string='Category',
        required=True,
        tracking=True,
        help="Equipment category (e.g., Machinery, Vehicles, IT Equipment)"
    )
    
    # -------------------------------------------------------------------------
    # OWNERSHIP - BY DEPARTMENT OR EMPLOYEE
    # -------------------------------------------------------------------------
    
    ownership_type = fields.Selection([
        ('company', 'Company'),
        ('department', 'Department'),
        ('employee', 'Employee'),
    ], string='Ownership Type', default='company', required=True,
        help="Specify if equipment belongs to the company, a department, or specific employee")
    
    department_id = fields.Many2one(
        'hr.department',
        string='Department',
        tracking=True,
        help="Department that owns this equipment (e.g., Production, IT, Sales)"
    )
    
    employee_id = fields.Many2one(
        'hr.employee',
        string='Assigned Employee',
        tracking=True,
        help="Employee assigned to this equipment"
    )
    
    owner_display = fields.Char(
        string='Owner',
        compute='_compute_owner_display',
        store=True,
        help="Display name of the owner"
    )
    
    # -------------------------------------------------------------------------
    # MAINTENANCE RESPONSIBILITY
    # -------------------------------------------------------------------------
    
    maintenance_team_id = fields.Many2one(
        'maintenance.team',
        string='Maintenance Team',
        required=True,
        tracking=True,
        help="Team responsible for maintaining this equipment"
    )
    
    technician_id = fields.Many2one(
        'res.users',
        string='Default Technician',
        tracking=True,
        domain="[('id', 'in', team_member_ids)]",
        help="Default technician assigned to maintenance requests for this equipment"
    )
    
    team_member_ids = fields.Many2many(
        related='maintenance_team_id.member_ids',
        string='Team Members',
        help="Members of the assigned maintenance team"
    )
    
    # -------------------------------------------------------------------------
    # WORK CENTER (FROM MOCKUP)
    # -------------------------------------------------------------------------
    
    work_center_id = fields.Many2one(
        'maintenance.work.center',
        string='Work Center',
        tracking=True,
        index=True,
        help="Primary work center for maintaining this equipment"
    )
    
    # -------------------------------------------------------------------------
    # PURCHASE & WARRANTY INFORMATION
    # -------------------------------------------------------------------------
    
    purchase_date = fields.Date(
        string='Purchase Date',
        tracking=True,
        help="Date when the equipment was purchased"
    )
    
    purchase_value = fields.Float(
        string='Purchase Value',
        tracking=True,
        help="Original purchase price"
    )
    
    warranty_expiry = fields.Date(
        string='Warranty Expiry',
        tracking=True,
        help="Date when warranty expires"
    )
    
    warranty_status = fields.Selection([
        ('valid', 'Under Warranty'),
        ('expired', 'Warranty Expired'),
        ('na', 'No Warranty'),
    ], string='Warranty Status', compute='_compute_warranty_status', store=True)
    
    vendor_id = fields.Many2one(
        'res.partner',
        string='Vendor',
        help="Equipment vendor/supplier"
    )
    
    # -------------------------------------------------------------------------
    # LOCATION
    # -------------------------------------------------------------------------
    
    location = fields.Char(
        string='Location',
        tracking=True,
        help="Physical location of the equipment (e.g., Building A, Floor 2, Room 101)"
    )
    
    # -------------------------------------------------------------------------
    # SCRAP STATUS
    # -------------------------------------------------------------------------
    
    is_scrap = fields.Boolean(
        string='Scrapped',
        default=False,
        tracking=True,
        help="Indicates if the equipment has been scrapped and is no longer usable"
    )
    
    scrap_date = fields.Date(
        string='Scrap Date',
        tracking=True,
        help="Date when the equipment was scrapped"
    )
    
    scrap_reason = fields.Text(
        string='Scrap Reason',
        help="Reason for scrapping the equipment"
    )
    
    # -------------------------------------------------------------------------
    # SMART BUTTON COUNTERS
    # -------------------------------------------------------------------------
    
    request_count = fields.Integer(
        string='Maintenance Requests',
        compute='_compute_request_count',
        help="Number of maintenance requests for this equipment"
    )
    
    open_request_count = fields.Integer(
        string='Open Requests',
        compute='_compute_request_count',
        help="Number of open (not completed) maintenance requests"
    )
    
    # -------------------------------------------------------------------------
    # SQL CONSTRAINTS (ORM Best Practice)
    # -------------------------------------------------------------------------
    
    _sql_constraints = [
        ('serial_number_unique', 'UNIQUE(serial_number)', 
         'Serial number must be unique! Another equipment already has this serial number.'),
        ('purchase_value_positive', 'CHECK(purchase_value >= 0)', 
         'Purchase value cannot be negative!'),
    ]
    
    # -------------------------------------------------------------------------
    # COMPUTE METHODS
    # -------------------------------------------------------------------------
    
    @api.depends('ownership_type', 'department_id', 'employee_id')
    def _compute_owner_display(self):
        """Compute display name of the owner"""
        for equipment in self:
            if equipment.ownership_type == 'company':
                equipment.owner_display = 'Company'
            elif equipment.ownership_type == 'department' and equipment.department_id:
                equipment.owner_display = equipment.department_id.name
            elif equipment.ownership_type == 'employee' and equipment.employee_id:
                equipment.owner_display = equipment.employee_id.name
            else:
                equipment.owner_display = 'Not Assigned'
    
    @api.depends('warranty_expiry')
    def _compute_warranty_status(self):
        """Compute warranty status based on expiry date"""
        today = fields.Date.today()
        for equipment in self:
            if not equipment.warranty_expiry:
                equipment.warranty_status = 'na'
            elif equipment.warranty_expiry >= today:
                equipment.warranty_status = 'valid'
            else:
                equipment.warranty_status = 'expired'
    
    def _compute_request_count(self):
        """Compute number of maintenance requests for this equipment"""
        Request = self.env['maintenance.request']
        for equipment in self:
            equipment.request_count = Request.search_count([
                ('equipment_id', '=', equipment.id)
            ])
            equipment.open_request_count = Request.search_count([
                ('equipment_id', '=', equipment.id),
                ('stage_id.is_closed', '=', False)
            ])
    
    # -------------------------------------------------------------------------
    # ONCHANGE METHODS
    # -------------------------------------------------------------------------
    
    @api.onchange('ownership_type')
    def _onchange_ownership_type(self):
        """Clear ownership fields when type changes"""
        if self.ownership_type == 'company':
            self.department_id = False
            self.employee_id = False
        elif self.ownership_type == 'department':
            self.employee_id = False
        elif self.ownership_type == 'employee':
            self.department_id = False
    
    @api.onchange('maintenance_team_id')
    def _onchange_maintenance_team_id(self):
        """Reset technician when team changes"""
        if self.technician_id and self.maintenance_team_id:
            if self.technician_id not in self.maintenance_team_id.member_ids:
                self.technician_id = False
    
    # -------------------------------------------------------------------------
    # CONSTRAINT METHODS
    # -------------------------------------------------------------------------
    
    @api.constrains('ownership_type', 'department_id', 'employee_id')
    def _check_ownership(self):
        """Ensure ownership is properly set based on type"""
        for equipment in self:
            # Company ownership doesn't require department or employee
            if equipment.ownership_type == 'department' and not equipment.department_id:
                raise ValidationError("Please select a department for department-owned equipment.")
            if equipment.ownership_type == 'employee' and not equipment.employee_id:
                raise ValidationError("Please select an employee for employee-owned equipment.")
    
    # -------------------------------------------------------------------------
    # SMART BUTTON ACTIONS
    # -------------------------------------------------------------------------
    
    def action_view_maintenance_requests(self):
        """Smart Button: Open maintenance requests for this equipment"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': f'Maintenance - {self.name}',
            'res_model': 'maintenance.request',
            'view_mode': 'tree,kanban,form,calendar',
            'domain': [('equipment_id', '=', self.id)],
            'context': {
                'default_equipment_id': self.id,
                'default_maintenance_team_id': self.maintenance_team_id.id,
                'default_technician_id': self.technician_id.id,
            },
        }
    
    def action_create_request(self):
        """Quick action: Create new maintenance request for this equipment"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'New Maintenance Request',
            'res_model': 'maintenance.request',
            'view_mode': 'form',
            'context': {
                'default_equipment_id': self.id,
                'default_maintenance_team_id': self.maintenance_team_id.id,
                'default_technician_id': self.technician_id.id,
            },
        }
    
    def action_scrap_equipment(self):
        """Mark equipment as scrapped"""
        self.ensure_one()
        self.write({
            'is_scrap': True,
            'scrap_date': fields.Date.today(),
            'active': False,
        })
        self.message_post(
            body="Equipment has been marked as SCRAPPED and is no longer usable.",
            message_type='notification'
        )
        return True
