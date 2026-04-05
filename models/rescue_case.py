from odoo import api, models, fields
from odoo.exceptions import UserError

class RescueCase(models.Model):
    _name = "pawsafe.rescue.case"
    _description = "Rescue Case"

    name = fields.Char(string="Case ID", required=True, default="New")
    animal_id = fields.Many2one("pawsafe.animal", string="Animal", required=True)
    rescuer_id = fields.Many2one("pawsafe.rescuer", string="Assigned Rescuer")
    shelter_id = fields.Many2one("pawsafe.shelter", string="Target Shelter")
    reported_by = fields.Char(string="Reported By")
    reporter_phone = fields.Char(string="Reporter Phone")
    location = fields.Char(string="Location", required=True)
    description = fields.Text(string="Situation Description")
    priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ], default='medium', string="Priority")
    state = fields.Selection([
        ('reported', 'Reported'),
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], default='reported', string="Status")
    reported_date = fields.Datetime(string="Reported Date")
    completed_date = fields.Datetime(string="Completed Date")
    notes = fields.Text(string="Field Notes")

    def action_assign(self):
        for record in self:
            if not record.rescuer_id:
                raise UserError("Please assign a rescuer before proceeding!")
            record.state = 'assigned'

    def action_start(self):
        for record in self:
            record.state = 'in_progress'

    def action_complete(self):
        for record in self:
            from datetime import datetime
            record.state = 'completed'
            record.completed_date = datetime.now()
            if record.animal_id:
                record.animal_id.state = 'rescued'

    def action_cancel(self):
        for record in self:
            if record.state == 'completed':
                raise UserError("Cannot cancel a completed rescue case!")
            record.state = 'cancelled'