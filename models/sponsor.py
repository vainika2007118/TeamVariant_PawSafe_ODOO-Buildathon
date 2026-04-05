from odoo import api, models, fields

class Sponsor(models.Model):
    _name = "pawsafe.sponsor"
    _description = "Animal Sponsor"

    animal_id = fields.Many2one("pawsafe.animal", string="Animal", required=True)
    sponsor_name = fields.Char(string="Sponsor Name", required=True)
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    amount = fields.Float(string="Sponsorship Amount (₹)", required=True)
    date = fields.Date(string="Date")
    purpose = fields.Selection([
        ('food', 'Food'),
        ('medical', 'Medical'),
        ('shelter', 'Shelter'),
        ('general', 'General'),
    ], string="Purpose", default='general')
    notes = fields.Text(string="Notes")

    _sql_constraints = [
        ('check_amount', 'CHECK(amount > 0)', 'Sponsorship amount must be greater than 0!'),
    ]