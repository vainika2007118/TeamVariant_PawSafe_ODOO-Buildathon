from odoo import api, models, fields
from odoo.exceptions import UserError, ValidationError

class Adoption(models.Model):
    _name = "pawsafe.adoption"
    _description = "Animal Adoption"

    animal_id = fields.Many2one("pawsafe.animal", string="Animal", required=True)
    adopter_name = fields.Char(string="Adopter Name", required=True)
    adopter_phone = fields.Char(string="Adopter Phone", required=True)
    adopter_email = fields.Char(string="Adopter Email")
    adopter_address = fields.Text(string="Adopter Address")
    adoption_date = fields.Date(string="Adoption Date")
    state = fields.Selection([
        ('applied', 'Applied'),
        ('screening', 'Screening'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
        ('returned', 'Returned'),
    ], default='applied', string="Status")
    has_other_pets = fields.Boolean(string="Has Other Pets")
    has_children = fields.Boolean(string="Has Children")
    home_type = fields.Selection([
        ('apartment', 'Apartment'),
        ('house', 'House with Garden'),
        ('farm', 'Farm'),
        ('other', 'Other'),
    ], string="Home Type")
    rejection_reason = fields.Text(string="Rejection Reason")
    return_reason = fields.Text(string="Return Reason")
    happy_tails_story = fields.Text(string="Happy Tails Story")
    is_blacklisted = fields.Boolean(string="Blacklisted", default=False)

    def action_screen(self):
        for record in self:
            record.state = 'screening'

    def action_approve(self):
        for record in self:
            if record.is_blacklisted:
                raise UserError("This adopter is blacklisted and cannot adopt!")
            record.state = 'approved'

    def action_complete(self):
        for record in self:
            from datetime import date
            record.state = 'completed'
            record.adoption_date = date.today()
            record.animal_id.state = 'adopted'

    def action_reject(self):
        for record in self:
            if not record.rejection_reason:
                raise ValidationError("Please provide a rejection reason!")
            record.state = 'rejected'
            record.animal_id.state = 'available'

    def action_return(self):
        for record in self:
            if not record.return_reason:
                raise ValidationError("Please provide a return reason!")
            record.state = 'returned'
            record.animal_id.state = 'available'
            record.is_blacklisted = True