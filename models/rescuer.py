from odoo import api, models, fields

class Rescuer(models.Model):
    _name = "pawsafe.rescuer"
    _description = "Animal Rescuer/Volunteer"

    name = fields.Char(string="Rescuer Name", required=True)
    phone = fields.Char(string="Phone", required=True)
    email = fields.Char(string="Email")
    address = fields.Text(string="Address")
    city = fields.Char(string="City")
    area_coverage = fields.Char(string="Area Coverage")
    is_active = fields.Boolean(string="Active Volunteer", default=True)
    joined_date = fields.Date(string="Joined Date")
    
    # Skills & Certifications
    has_vehicle = fields.Boolean(string="Has Vehicle")
    is_trained = fields.Boolean(string="First Aid Trained")
    can_foster = fields.Boolean(string="Can Foster Animals")
    notes = fields.Text(string="Notes")

    # Relations
    rescue_case_ids = fields.One2many("pawsafe.rescue.case", "rescuer_id", string="Rescue Cases")
    foster_ids = fields.One2many("pawsafe.foster", "rescuer_id", string="Foster Cases")

    # Computed
    total_rescues = fields.Integer(compute="_compute_stats", string="Total Rescues")
    total_fosters = fields.Integer(compute="_compute_stats", string="Total Fosters")

    _sql_constraints = [
        ('unique_phone', 'UNIQUE(phone)', 'A rescuer with this phone number already exists!'),
    ]

    @api.depends("rescue_case_ids", "foster_ids")
    def _compute_stats(self):
        for record in self:
            record.total_rescues = len(record.rescue_case_ids)
            record.total_fosters = len(record.foster_ids)