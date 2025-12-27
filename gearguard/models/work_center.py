# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta


class WorkCenter(models.Model):
    """Work Center Model
    
    Represents a physical location where maintenance work is performed.
    Tracks costs, capacity, and utilization as shown in the mockup diagram.
    """
    _name = 'maintenance.work.center'
    _description = 'Maintenance Work Center'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, name'

    # -------------------------------------------------------------------------
    # BASIC FIELDS
    # -------------------------------------------------------------------------
    
    name = fields.Char(
        string='Work Center',
        required=True,
        tracking=True,
        help="Name of the work center (e.g., Machine Shop, Electronics Lab)"
    )
    
    code = fields.Char(
        string='Code',
        required=True,
        tracking=True,
        index=True,
        help="Short code for the work center (e.g., WC001, MSHOP)"
    )
    
    active = fields.Boolean(
        string='Active',
        default=True,
        tracking=True
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10
    )
    
    note = fields.Html(
        string='Notes',
        help="Internal notes about this work center"
    )
    
    color = fields.Integer(
        string='Color Index'
    )
    
    # -------------------------------------------------------------------------
    # LOCATION & CAPACITY
    # -------------------------------------------------------------------------
    
    location = fields.Char(
        string='Location',
        help="Physical location of the work center"
    )
    
    capacity = fields.Float(
        string='Capacity (Hours/Day)',
        default=8.0,
        tracking=True,
        help="Maximum working hours per day"
    )
    
    resource_calendar_id = fields.Many2one(
        'resource.calendar',
        string='Working Hours',
        help="Working hours calendar for this work center"
    )
    
    # -------------------------------------------------------------------------
    # COST TRACKING (FROM MOCKUP)
    # -------------------------------------------------------------------------
    
    hourly_cost = fields.Float(
        string='Hourly Cost',
        digits='Product Price',
        tracking=True,
        help="Cost per hour for using this work center"
    )
    
    capacity_cost = fields.Float(
        string='Capacity Cost/Hr',
        digits='Product Price',
        tracking=True,
        help="Additional capacity cost per hour"
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id.id
    )
    
    total_cost = fields.Float(
        string='Total Cost/Hr',
        compute='_compute_total_cost',
        store=True,
        help="Total hourly cost (Hourly + Capacity)"
    )
    
    # -------------------------------------------------------------------------
    # ALTERNATE WORK CENTERS (FROM MOCKUP)
    # -------------------------------------------------------------------------
    
    alternate_workcenter_ids = fields.Many2many(
        'maintenance.work.center',
        'work_center_alternate_rel',
        'workcenter_id',
        'alternate_id',
        string='Alternate Workcenters',
        help="Alternative work centers that can perform the same work"
    )
    
    # -------------------------------------------------------------------------
    # TEAM ASSIGNMENT
    # -------------------------------------------------------------------------
    
    maintenance_team_id = fields.Many2one(
        'maintenance.team',
        string='Maintenance Team',
        tracking=True,
        help="Team responsible for this work center"
    )
    
    # -------------------------------------------------------------------------
    # STATISTICS
    # -------------------------------------------------------------------------
    
    equipment_count = fields.Integer(
        string='Equipment Count',
        compute='_compute_counts'
    )
    
    request_count = fields.Integer(
        string='Request Count',
        compute='_compute_counts'
    )
    
    utilization_rate = fields.Float(
        string='Utilization Rate (%)',
        compute='_compute_utilization',
        help="Percentage of capacity being used"
    )
    
    # -------------------------------------------------------------------------
    # SQL CONSTRAINTS (ORM Best Practice)
    # -------------------------------------------------------------------------
    
    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'Work Center code must be unique!'),
        ('hourly_cost_positive', 'CHECK(hourly_cost >= 0)', 'Hourly cost must be positive!'),
        ('capacity_positive', 'CHECK(capacity > 0)', 'Capacity must be greater than zero!'),
    ]
    
    # -------------------------------------------------------------------------
    # COMPUTE METHODS
    # -------------------------------------------------------------------------
    
    @api.depends('hourly_cost', 'capacity_cost')
    def _compute_total_cost(self):
        """Compute total hourly cost"""
        for center in self:
            center.total_cost = center.hourly_cost + center.capacity_cost
    
    def _compute_counts(self):
        """Compute equipment and request counts"""
        Equipment = self.env['equipment.equipment']
        Request = self.env['maintenance.request']
        for center in self:
            center.equipment_count = Equipment.search_count([
                ('work_center_id', '=', center.id)
            ])
            center.request_count = Request.search_count([
                ('work_center_id', '=', center.id)
            ])
    
    def _compute_utilization(self):
        """Compute utilization rate based on recent requests"""
        Request = self.env['maintenance.request']
        for center in self:
            if not center.capacity:
                center.utilization_rate = 0
                continue
            
            # Get total hours from last 30 days
            thirty_days_ago = fields.Date.today() - timedelta(days=30)
            domain = [
                ('work_center_id', '=', center.id),
                ('close_date', '>=', thirty_days_ago),
                ('stage_id.is_closed', '=', True),
            ]
            requests = Request.search(domain)
            total_hours = sum(requests.mapped('duration'))
            
            # Calculate utilization (assuming 30 working days)
            max_capacity = center.capacity * 30
            if max_capacity > 0:
                center.utilization_rate = (total_hours / max_capacity) * 100
            else:
                center.utilization_rate = 0
    
    # -------------------------------------------------------------------------
    # ACTIONS
    # -------------------------------------------------------------------------
    
    def action_view_equipment(self):
        """View equipment assigned to this work center"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Equipment - %s', self.name),
            'res_model': 'equipment.equipment',
            'view_mode': 'tree,kanban,form',
            'domain': [('work_center_id', '=', self.id)],
            'context': {'default_work_center_id': self.id},
        }
    
    def action_view_requests(self):
        """View maintenance requests for this work center"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Requests - %s', self.name),
            'res_model': 'maintenance.request',
            'view_mode': 'kanban,tree,form',
            'domain': [('work_center_id', '=', self.id)],
            'context': {'default_work_center_id': self.id},
        }
