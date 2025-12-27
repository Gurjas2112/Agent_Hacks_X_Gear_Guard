# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MaintenanceStage(models.Model):
    """Maintenance Request Stage Model
    
    Stages for the maintenance request workflow (New, In Progress, Repaired, Scrap)
    """
    _name = 'maintenance.stage'
    _description = 'Maintenance Request Stage'
    _order = 'sequence, id'

    name = fields.Char(
        string='Stage Name',
        required=True,
        translate=True,
        help="Name of the stage (e.g., New, In Progress, Repaired)"
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help="Order in which stages appear in kanban"
    )
    
    fold = fields.Boolean(
        string='Folded in Kanban',
        default=False,
        help="If set, this stage will be folded by default in kanban view"
    )
    
    is_closed = fields.Boolean(
        string='Is Closed Stage',
        default=False,
        help="Requests in this stage are considered closed/completed"
    )
    
    is_scrap = fields.Boolean(
        string='Is Scrap Stage',
        default=False,
        help="If true, moving a request to this stage will mark equipment as scrapped"
    )
    
    description = fields.Text(
        string='Description',
        help="Description of what this stage means"
    )
