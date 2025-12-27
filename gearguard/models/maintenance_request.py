# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import timedelta


class MaintenanceRequest(models.Model):
    """Maintenance Request Model
    
    The transactional part - handles the lifecycle of a repair job.
    Supports both Corrective (Breakdown) and Preventive (Routine) maintenance.
    """
    _name = 'maintenance.request'
    _description = 'Maintenance Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'priority desc, scheduled_date asc, id desc'
    _rec_name = 'name'
    _rec_names_search = ['name', 'equipment_id']

    # -------------------------------------------------------------------------
    # BASIC FIELDS
    # -------------------------------------------------------------------------
    
    name = fields.Char(
        string='Subject',
        required=True,
        tracking=True,
        help="What is wrong? (e.g., 'Leaking Oil', 'Screen Flickering')"
    )
    
    description = fields.Html(
        string='Description',
        help="Detailed description of the maintenance issue"
    )
    
    active = fields.Boolean(
        string='Active',
        default=True
    )
    
    color = fields.Integer(
        string='Color Index'
    )
    
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Normal'),
        ('2', 'High'),
        ('3', 'Urgent'),
    ], string='Priority', default='1', tracking=True)
    
    # -------------------------------------------------------------------------
    # REQUEST TYPE
    # -------------------------------------------------------------------------
    
    request_type = fields.Selection([
        ('corrective', 'Corrective (Breakdown)'),
        ('preventive', 'Preventive (Routine)'),
    ], string='Request Type', default='corrective', required=True, tracking=True,
        help="Corrective: Unplanned repair | Preventive: Planned maintenance")
    
    # -------------------------------------------------------------------------
    # EQUIPMENT LINKAGE (AUTO-FILL SOURCE)
    # -------------------------------------------------------------------------
    
    equipment_id = fields.Many2one(
        'equipment.equipment',
        string='Equipment',
        required=True,
        tracking=True,
        help="Which machine/equipment is affected?"
    )
    
    # These fields are AUTO-FILLED from equipment
    category_id = fields.Many2one(
        'equipment.category',
        string='Equipment Category',
        related='equipment_id.category_id',
        store=True,
        readonly=True,
        help="Auto-filled from equipment"
    )
    
    equipment_serial = fields.Char(
        string='Serial Number',
        related='equipment_id.serial_number',
        readonly=True
    )
    
    equipment_location = fields.Char(
        string='Location',
        related='equipment_id.location',
        readonly=True
    )
    
    # -------------------------------------------------------------------------
    # WORK CENTER (FROM MOCKUP)
    # -------------------------------------------------------------------------
    
    work_center_id = fields.Many2one(
        'maintenance.work.center',
        string='Work Center',
        tracking=True,
        index=True,
        help="Work center where the maintenance will be performed"
    )
    
    # -------------------------------------------------------------------------
    # TEAM & ASSIGNMENT
    # -------------------------------------------------------------------------
    
    maintenance_team_id = fields.Many2one(
        'maintenance.team',
        string='Maintenance Team',
        required=True,
        tracking=True,
        help="Team responsible for this request"
    )
    
    team_member_ids = fields.Many2many(
        related='maintenance_team_id.member_ids',
        string='Team Members'
    )
    
    technician_id = fields.Many2one(
        'res.users',
        string='Assigned Technician',
        tracking=True,
        domain="[('id', 'in', team_member_ids)]",
        help="Technician assigned to handle this request (must be from the team)"
    )
    
    user_id = fields.Many2one(
        'res.users',
        string='Created By',
        default=lambda self: self.env.user,
        readonly=True
    )
    
    # -------------------------------------------------------------------------
    # STAGE & WORKFLOW
    # -------------------------------------------------------------------------
    
    stage_id = fields.Many2one(
        'maintenance.stage',
        string='Stage',
        tracking=True,
        group_expand='_read_group_stage_ids',
        default=lambda self: self._get_default_stage(),
        help="Current stage of the request"
    )
    
    kanban_state = fields.Selection([
        ('normal', 'In Progress'),
        ('done', 'Ready'),
        ('blocked', 'Blocked'),
    ], string='Kanban State', default='normal', tracking=True)
    
    # -------------------------------------------------------------------------
    # SCHEDULING & TIME
    # -------------------------------------------------------------------------
    
    request_date = fields.Date(
        string='Request Date',
        default=fields.Date.today,
        readonly=True,
        help="Date when request was created"
    )
    
    scheduled_date = fields.Datetime(
        string='Scheduled Date',
        tracking=True,
        index=True,
        help="When should the maintenance happen?"
    )
    
    deadline = fields.Date(
        string='Deadline',
        tracking=True,
        help="Due date for completion"
    )
    
    close_date = fields.Date(
        string='Close Date',
        readonly=True,
        help="Date when request was completed"
    )
    
    duration = fields.Float(
        string='Duration (Hours)',
        tracking=True,
        help="How long did the repair take?"
    )
    
    # -------------------------------------------------------------------------
    # REMINDER (FROM MOCKUP)
    # -------------------------------------------------------------------------
    
    reminder_days = fields.Integer(
        string='Reminder (Days Before)',
        default=1,
        help="Number of days before scheduled date to send reminder"
    )
    
    reminder_date = fields.Date(
        string='Reminder Date',
        compute='_compute_reminder_date',
        store=True,
        help="Date when reminder should be sent"
    )
    
    # -------------------------------------------------------------------------
    # COST TRACKING (FROM MOCKUP)
    # -------------------------------------------------------------------------
    
    estimated_cost = fields.Float(
        string='Estimated Cost',
        digits='Product Price',
        tracking=True
    )
    
    actual_cost = fields.Float(
        string='Actual Cost',
        digits='Product Price',
        tracking=True
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id.id
    )
    
    # -------------------------------------------------------------------------
    # COMPUTED STATUS FIELDS
    # -------------------------------------------------------------------------
    
    is_overdue = fields.Boolean(
        string='Is Overdue',
        compute='_compute_is_overdue',
        store=True,
        help="True if the deadline has passed and request is not closed"
    )
    
    days_until_deadline = fields.Integer(
        string='Days Until Deadline',
        compute='_compute_days_until_deadline'
    )
    
    # -------------------------------------------------------------------------
    # SQL CONSTRAINTS (ORM Best Practice)
    # -------------------------------------------------------------------------
    
    _sql_constraints = [
        ('duration_positive', 'CHECK(duration >= 0)', 'Duration cannot be negative!'),
        ('estimated_cost_positive', 'CHECK(estimated_cost >= 0)', 'Estimated cost cannot be negative!'),
        ('actual_cost_positive', 'CHECK(actual_cost >= 0)', 'Actual cost cannot be negative!'),
    ]
    
    # -------------------------------------------------------------------------
    # PYTHON CONSTRAINTS
    # -------------------------------------------------------------------------
    
    @api.constrains('technician_id', 'maintenance_team_id')
    def _check_technician_in_team(self):
        """Ensure technician is a member of the assigned maintenance team"""
        for request in self:
            if request.technician_id and request.maintenance_team_id:
                if request.technician_id not in request.maintenance_team_id.member_ids:
                    raise ValidationError(
                        f"Technician '{request.technician_id.name}' is not a member of team "
                        f"'{request.maintenance_team_id.name}'. Only team members can be assigned to requests."
                    )
    
    # -------------------------------------------------------------------------
    # DEFAULT METHODS
    # -------------------------------------------------------------------------
    
    def _get_default_stage(self):
        """Get the first stage (New) as default"""
        return self.env['maintenance.stage'].search([('sequence', '=', 1)], limit=1)
    
    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        """Show all stages in kanban view, even empty ones"""
        return self.env['maintenance.stage'].search([], order=order)
    
    # -------------------------------------------------------------------------
    # COMPUTE METHODS
    # -------------------------------------------------------------------------
    
    @api.depends('scheduled_date', 'reminder_days')
    def _compute_reminder_date(self):
        """Compute reminder date based on scheduled date and reminder days"""
        for request in self:
            if request.scheduled_date and request.reminder_days:
                request.reminder_date = (request.scheduled_date - timedelta(days=request.reminder_days)).date()
            else:
                request.reminder_date = False
    
    @api.depends('deadline', 'stage_id.is_closed')
    def _compute_is_overdue(self):
        """Check if request is overdue"""
        today = fields.Date.today()
        for request in self:
            if request.deadline and not request.stage_id.is_closed:
                request.is_overdue = request.deadline < today
            else:
                request.is_overdue = False
    
    def _compute_days_until_deadline(self):
        """Calculate days remaining until deadline"""
        today = fields.Date.today()
        for request in self:
            if request.deadline:
                delta = request.deadline - today
                request.days_until_deadline = delta.days
            else:
                request.days_until_deadline = 0
    
    # -------------------------------------------------------------------------
    # ONCHANGE METHODS - THE KEY AUTO-FILL LOGIC!
    # -------------------------------------------------------------------------
    
    @api.onchange('equipment_id')
    def _onchange_equipment_id(self):
        """AUTO-FILL: When equipment is selected, fetch team and category"""
        if self.equipment_id:
            # Auto-fill maintenance team from equipment
            self.maintenance_team_id = self.equipment_id.maintenance_team_id
            # Auto-fill default technician if set
            if self.equipment_id.technician_id:
                self.technician_id = self.equipment_id.technician_id
            # Category is already related field, but we can add message
            return {
                'warning': {
                    'title': 'Equipment Selected',
                    'message': f"Team auto-set to: {self.equipment_id.maintenance_team_id.name}"
                }
            } if self.equipment_id.maintenance_team_id else {}
    
    @api.onchange('maintenance_team_id')
    def _onchange_maintenance_team_id(self):
        """Reset technician if they're not in the new team"""
        if self.technician_id and self.maintenance_team_id:
            if self.technician_id not in self.maintenance_team_id.member_ids:
                self.technician_id = False
    
    @api.onchange('request_type')
    def _onchange_request_type(self):
        """Set default scheduled date for preventive maintenance"""
        if self.request_type == 'preventive' and not self.scheduled_date:
            # Default to next week for preventive maintenance
            self.scheduled_date = fields.Datetime.now() + timedelta(days=7)
    
    # -------------------------------------------------------------------------
    # CRUD OVERRIDES
    # -------------------------------------------------------------------------
    
    @api.model_create_multi
    def create(self, vals_list):
        """Override create to handle auto-fill if not set"""
        for vals in vals_list:
            if vals.get('equipment_id') and not vals.get('maintenance_team_id'):
                equipment = self.env['equipment.equipment'].browse(vals['equipment_id'])
                vals['maintenance_team_id'] = equipment.maintenance_team_id.id
                if equipment.technician_id and not vals.get('technician_id'):
                    vals['technician_id'] = equipment.technician_id.id
        return super().create(vals_list)
    
    def write(self, vals):
        """Override write to handle stage changes"""
        # Handle scrap logic
        if 'stage_id' in vals:
            new_stage = self.env['maintenance.stage'].browse(vals['stage_id'])
            
            # If moving to SCRAP stage, mark equipment as scrapped
            if new_stage.is_scrap:
                for request in self:
                    if request.equipment_id and not request.equipment_id.is_scrap:
                        request.equipment_id.write({
                            'is_scrap': True,
                            'scrap_date': fields.Date.today(),
                            'scrap_reason': f"Scrapped via maintenance request: {request.name}",
                        })
                        request.equipment_id.message_post(
                            body=f"⚠️ Equipment marked as SCRAP based on maintenance request: {request.name}",
                            message_type='notification'
                        )
            
            # If moving to closed stage, set close date
            if new_stage.is_closed and 'close_date' not in vals:
                vals['close_date'] = fields.Date.today()
        
        return super().write(vals)
    
    # -------------------------------------------------------------------------
    # ACTIONS
    # -------------------------------------------------------------------------
    
    def action_assign_to_me(self):
        """Quick action: Assign request to current user"""
        self.ensure_one()
        if self.env.user not in self.maintenance_team_id.member_ids:
            raise UserError("You cannot assign yourself - you're not a member of the assigned team!")
        self.write({
            'technician_id': self.env.user.id,
        })
        # Move to In Progress if still in New
        in_progress_stage = self.env['maintenance.stage'].search([('sequence', '=', 2)], limit=1)
        if in_progress_stage and self.stage_id.sequence == 1:
            self.write({'stage_id': in_progress_stage.id})
        return True
    
    def action_mark_repaired(self):
        """Quick action: Mark as repaired"""
        self.ensure_one()
        repaired_stage = self.env['maintenance.stage'].search([('name', 'ilike', 'Repaired')], limit=1)
        if repaired_stage:
            self.write({
                'stage_id': repaired_stage.id,
                'close_date': fields.Date.today(),
            })
        return True
    
    def action_open_equipment(self):
        """Open the linked equipment form"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': self.equipment_id.name,
            'res_model': 'equipment.equipment',
            'view_mode': 'form',
            'res_id': self.equipment_id.id,
        }
