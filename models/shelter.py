from odoo import api, models, fields
from odoo.exceptions import ValidationError

class Shelter(models.Model):
    _name = "pawsafe.shelter"
    _description = "Animal Shelter"

    name = fields.Char(string="Shelter Name", required=True)
    address = fields.Text(string="Address")
    city = fields.Char(string="City")
    state_location = fields.Char(string="State")
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    capacity = fields.Integer(string="Total Capacity")
    
    # Relations
    animal_ids = fields.One2many("pawsafe.animal", "shelter_id", string="Animals")
    
    # Computed
    current_occupancy = fields.Integer(compute="_compute_occupancy", string="Current Occupancy")
    available_space = fields.Integer(compute="_compute_occupancy", string="Available Space")
    occupancy_rate = fields.Float(compute="_compute_occupancy", string="Occupancy Rate (%)")
    is_full = fields.Boolean(compute="_compute_occupancy", string="Is Full")

    _sql_constraints = [
        ('check_capacity', 'CHECK(capacity > 0)', 'Capacity must be greater than 0!'),
    ]

    @api.depends("animal_ids", "capacity")
    def _compute_occupancy(self):
        for record in self:
            # Only count active animals (not adopted or deceased)
            active_animals = record.animal_ids.filtered(
                lambda a: a.state not in ('adopted', 'deceased')
            )
            record.current_occupancy = len(active_animals)
            record.available_space = record.capacity - len(active_animals)
            if record.capacity > 0:
                record.occupancy_rate = (len(active_animals) / record.capacity) * 100
            else:
                record.occupancy_rate = 0.0
            record.is_full = len(active_animals) >= record.capacity

    @api.constrains("animal_ids", "capacity")
    def _check_capacity(self):
        for record in self:
            active_animals = record.animal_ids.filtered(
                lambda a: a.state not in ('adopted', 'deceased')
            )
            if len(active_animals) > record.capacity:
                raise ValidationError(
                    f"Shelter '{record.name}' is at full capacity ({record.capacity} animals)! "
                    "Please find another shelter or increase capacity."
                )