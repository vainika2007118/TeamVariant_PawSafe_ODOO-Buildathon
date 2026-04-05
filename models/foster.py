from odoo import api, models, fields
from odoo.exceptions import UserError, ValidationError

class Foster(models.Model):
    _name = "pawsafe.foster"
    _description = "Foster Care"

    animal_id = fields.Many2one("pawsafe.animal", string="Animal", required=True)
    rescuer_id = fields.Many2one("pawsafe.rescuer", string="Foster Carer", required=True)
    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date")
    state = fields.Selection([
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], default='active', string="Status")
    notes = fields.Text(string="Notes")
    duration = fields.Integer(compute="_compute_duration", string="Duration (Days)")

    @api.depends("start_date", "end_date")
    def _compute_duration(self):
        from datetime import date
        for record in self:
            if record.start_date and record.end_date:
                record.duration = (record.end_date - record.start_date).days
            else:
                record.duration = 0

    @api.constrains("start_date", "end_date")
    def _check_dates(self):
        for record in self:
            if record.end_date and record.start_date:
                if record.end_date < record.start_date:
                    raise ValidationError("End date cannot be before start date!")

    def action_complete(self):
        for record in self:
            record.state = 'completed'
            record.animal_id.state = 'available'

    def action_cancel(self):
        for record in self:
            if record.state == 'completed':
                raise UserError("Cannot cancel a completed foster case!")
            record.state = 'cancelled'