# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MaintenanceTeam(models.Model):
    """Maintenance Team Model
    
    Specialized teams that handle maintenance (e.g., Mechanics, Electricians, IT Support)
    """
    _name = 'maintenance.team'
    _description = 'Maintenance Team'
    _inherit = ['mail.thread']
    _order = 'name'

    # -------------------------------------------------------------------------
    # BASIC FIELDS
    # -------------------------------------------------------------------------
    
    name = fields.Char(
        string='Team Name',
        required=True,
        tracking=True,
        help="Name of the maintenance team (e.g., Mechanics, Electricians, IT Support)"
    )
    
    active = fields.Boolean(
        string='Active',
        default=True
    )
    
    color = fields.Integer(
        string='Color Index',
        help="Color used in kanban views"
    )
    
    note = fields.Text(
        string='Description',
        help="Description of the team's responsibilities"
    )
    
    # -------------------------------------------------------------------------
    # TEAM MEMBERS
    # -------------------------------------------------------------------------
    
    member_ids = fields.Many2many(
        'res.users',
        'maintenance_team_users_rel',
        'team_id',
        'user_id',
        string='Team Members',
        help="Technicians who belong to this team"
    )
    
    team_leader_id = fields.Many2one(
        'res.users',
        string='Team Leader',
        domain="[('id', 'in', member_ids)]",
        help="Leader/Manager of this team"
    )
    
    member_count = fields.Integer(
        string='Member Count',
        compute='_compute_member_count'
    )
    
    # -------------------------------------------------------------------------
    # RELATED COUNTS
    # -------------------------------------------------------------------------
    
    equipment_count = fields.Integer(
        string='Equipment Count',
        compute='_compute_counts',
        help="Number of equipment assigned to this team"
    )
    
    request_count = fields.Integer(
        string='Request Count',
        compute='_compute_counts',
        help="Number of maintenance requests for this team"
    )
    
    open_request_count = fields.Integer(
        string='Open Requests',
        compute='_compute_counts',
        help="Number of open requests"
    )
    
    # -------------------------------------------------------------------------
    # COMPUTE METHODS
    # -------------------------------------------------------------------------
    
    def _compute_member_count(self):
        """Compute number of team members"""
        for team in self:
            team.member_count = len(team.member_ids)
    
    def _compute_counts(self):
        """Compute equipment and request counts"""
        Equipment = self.env['equipment.equipment']
        Request = self.env['maintenance.request']
        
        for team in self:
            team.equipment_count = Equipment.search_count([
                ('maintenance_team_id', '=', team.id)
            ])
            team.request_count = Request.search_count([
                ('maintenance_team_id', '=', team.id)
            ])
            team.open_request_count = Request.search_count([
                ('maintenance_team_id', '=', team.id),
                ('stage_id.is_closed', '=', False)
            ])
    
    # -------------------------------------------------------------------------
    # ACTIONS
    # -------------------------------------------------------------------------
    
    def action_view_equipment(self):
        """View equipment assigned to this team"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': f'Equipment - {self.name}',
            'res_model': 'equipment.equipment',
            'view_mode': 'tree,form',
            'domain': [('maintenance_team_id', '=', self.id)],
            'context': {'default_maintenance_team_id': self.id},
        }
    
    def action_view_requests(self):
        """View maintenance requests for this team"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': f'Requests - {self.name}',
            'res_model': 'maintenance.request',
            'view_mode': 'kanban,tree,form,calendar',
            'domain': [('maintenance_team_id', '=', self.id)],
            'context': {'default_maintenance_team_id': self.id},
        }
