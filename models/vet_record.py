from odoo import api, models, fields
from odoo.exceptions import ValidationError

class VetRecord(models.Model):
    _name = "pawsafe.vet.record"
    _description = "Veterinary Record"

    animal_id = fields.Many2one("pawsafe.animal", string="Animal", required=True)
    vet_name = fields.Char(string="Veterinarian Name", required=True)
    visit_date = fields.Date(string="Visit Date", required=True)
    diagnosis = fields.Text(string="Diagnosis")
    treatment = fields.Text(string="Treatment Given")
    medicines = fields.Text(string="Medicines Prescribed")
    cost = fields.Float(string="Treatment Cost (₹)")
    follow_up_date = fields.Date(string="Follow-up Date")
    severity = fields.Selection([
        ('critical', 'Critical'),
        ('moderate', 'Moderate'),
        ('stable', 'Stable'),
        ('healthy', 'Healthy'),
    ], string="Severity", required=True, default='stable')
    is_vaccinated = fields.Boolean(string="Vaccination Given")
    vaccine_name = fields.Char(string="Vaccine Name")
    notes = fields.Text(string="Additional Notes")

    _sql_constraints = [
        ('check_cost', 'CHECK(cost >= 0)', 'Treatment cost cannot be negative!'),
    ]

    @api.constrains('follow_up_date', 'visit_date')
    def _check_follow_up_date(self):
        for record in self:
            if record.follow_up_date and record.visit_date:
                if record.follow_up_date < record.visit_date:
                    raise ValidationError("Follow-up date cannot be before visit date!")