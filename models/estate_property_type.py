from odoo import api, models, fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Types"

    name = fields.Char(required=True)
    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', 'A property type must be unique!'),
    ]