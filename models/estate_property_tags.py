from odoo import api, models, fields

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tags"

    name = fields.Char(required=True)
    _sql_constraints = [
        ('unique_tag_name', 'UNIQUE(name)', 'A property tag must be unique!'),
    ]