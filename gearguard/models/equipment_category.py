# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EquipmentCategory(models.Model):
    """Equipment Category Model
    
    Categories help organize equipment types (e.g., Machinery, Vehicles, IT Equipment)
    """
    _name = 'equipment.category'
    _description = 'Equipment Category'
    _order = 'name'

    name = fields.Char(
        string='Category Name',
        required=True,
        help="Name of the equipment category (e.g., CNC Machines, Vehicles, Computers)"
    )
    
    code = fields.Char(
        string='Category Code',
        help="Short code for the category"
    )
    
    color = fields.Integer(
        string='Color Index',
        help="Color used in kanban views"
    )
    
    note = fields.Text(
        string='Description',
        help="Additional notes about this category"
    )
    
    equipment_count = fields.Integer(
        string='Equipment Count',
        compute='_compute_equipment_count',
        help="Number of equipment in this category"
    )
    
    # -------------------------------------------------------------------------
    # COMPUTE METHODS
    # -------------------------------------------------------------------------
    
    def _compute_equipment_count(self):
        """Compute the number of equipment in each category"""
        for category in self:
            category.equipment_count = self.env['equipment.equipment'].search_count([
                ('category_id', '=', category.id)
            ])
    
    # -------------------------------------------------------------------------
    # ACTIONS
    # -------------------------------------------------------------------------
    
    def action_view_equipment(self):
        """Open list of equipment in this category"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': f'Equipment - {self.name}',
            'res_model': 'equipment.equipment',
            'view_mode': 'tree,form',
            'domain': [('category_id', '=', self.id)],
            'context': {'default_category_id': self.id},
        }
