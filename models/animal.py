from odoo import api, models, fields
from odoo.exceptions import UserError, ValidationError

class Animal(models.Model):
    _name = "pawsafe.animal"
    _description = "Rescued Animal"

    # Basic Info
    name = fields.Char(string="Animal Name", required=True)
    species = fields.Selection([
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('bird', 'Bird'),
        ('cow', 'Cow'),
        ('horse', 'Horse'),
        ('rabbit', 'Rabbit'),
        ('other', 'Other')
    ], required=True, default='dog')
    breed = fields.Char(string="Breed")
    age_years = fields.Integer(string="Age (Years)")
    age_months = fields.Integer(string="Age (Months)")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('unknown', 'Unknown')
    ], default='unknown')
    color = fields.Char(string="Color/Markings")
    weight = fields.Float(string="Weight (kg)")
    microchip_id = fields.Char(string="Microchip ID")
    photo = fields.Binary(string="Photo")

    # Status & Location
    state = fields.Selection([
        ('stray', 'Stray/Reported'),
        ('rescued', 'Rescued'),
        ('in_treatment', 'In Treatment'),
        ('recovering', 'Recovering'),
        ('available', 'Available for Adoption'),
        ('fostered', 'In Foster Care'),
        ('adopted', 'Adopted'),
        ('deceased', 'Deceased'),
    ], default='stray', string="Status")

    shelter_id = fields.Many2one("pawsafe.shelter", string="Current Shelter")
    rescue_location = fields.Char(string="Rescue Location")
    rescue_date = fields.Date(string="Rescue Date")

    # Personality Profile
    temperament = fields.Selection([
        ('friendly', 'Friendly'),
        ('shy', 'Shy'),
        ('aggressive', 'Aggressive'),
        ('playful', 'Playful'),
        ('calm', 'Calm'),
    ], string="Temperament")
    good_with_kids = fields.Boolean(string="Good with Kids")
    good_with_animals = fields.Boolean(string="Good with Other Animals")
    trained = fields.Boolean(string="House Trained")
    special_needs = fields.Text(string="Special Needs")

    # Medical
    is_vaccinated = fields.Boolean(string="Vaccinated")
    is_neutered = fields.Boolean(string="Neutered/Spayed")
    last_vaccination_date = fields.Date(string="Last Vaccination Date")
    next_vaccination_date = fields.Date(string="Next Vaccination Date")
    last_deworming_date = fields.Date(string="Last Deworming Date")
    next_deworming_date = fields.Date(string="Next Deworming Date")
    medical_severity = fields.Selection([
        ('critical', 'Critical'),
        ('moderate', 'Moderate'),
        ('stable', 'Stable'),
        ('healthy', 'Healthy'),
    ], string="Medical Severity", default='stable')

    # Relations
    rescue_case_ids = fields.One2many("pawsafe.rescue.case", "animal_id", string="Rescue Cases")
    vet_record_ids = fields.One2many("pawsafe.vet.record", "animal_id", string="Vet Records")
    foster_ids = fields.One2many("pawsafe.foster", "animal_id", string="Foster History")
    adoption_ids = fields.One2many("pawsafe.adoption", "animal_id", string="Adoption Records")
    sponsor_ids = fields.One2many("pawsafe.sponsor", "animal_id", string="Sponsors")

    # Computed
    vet_visits = fields.Integer(compute="_compute_vet_visits", string="Total Vet Visits")
    total_sponsorship = fields.Float(compute="_compute_total_sponsorship", string="Total Sponsorship (₹)")
    days_in_shelter = fields.Integer(compute="_compute_days_in_shelter", string="Days in Shelter")

    # Happy Tails
    adoption_story = fields.Text(string="Happy Tails Story")

    _sql_constraints = [
        ('unique_microchip', 'UNIQUE(microchip_id)', 'Microchip ID must be unique!'),
    ]

    @api.depends("vet_record_ids")
    def _compute_vet_visits(self):
        for record in self:
            record.vet_visits = len(record.vet_record_ids)

    @api.depends("sponsor_ids.amount")
    def _compute_total_sponsorship(self):
        for record in self:
            record.total_sponsorship = sum(record.sponsor_ids.mapped("amount"))

    @api.depends("rescue_date")
    def _compute_days_in_shelter(self):
        from datetime import date
        for record in self:
            if record.rescue_date:
                delta = date.today() - record.rescue_date
                record.days_in_shelter = delta.days
            else:
                record.days_in_shelter = 0

    def action_rescue(self):
        for record in self:
            if record.state != 'stray':
                raise UserError("Animal is already rescued!")
            record.state = 'rescued'

    def action_start_treatment(self):
        for record in self:
            record.state = 'in_treatment'

    def action_mark_recovering(self):
        for record in self:
            record.state = 'recovering'

    def action_make_available(self):
        for record in self:
            if not record.is_vaccinated:
                raise ValidationError("Animal must be vaccinated before being made available for adoption!")
            record.state = 'available'

    def action_mark_adopted(self):
        for record in self:
            record.state = 'adopted'

    def action_mark_deceased(self):
        for record in self:
            record.state = 'deceased'