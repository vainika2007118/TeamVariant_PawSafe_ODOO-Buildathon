from odoo import api, fields, models

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offers"

    price = fields.Float()
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    status = fields.Selection(selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    validity = fields.Integer(string="Validity (days)", default=7)
    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)', 'Please submit a proper offer'),
    ]

    def accept_offer(self):
        for record in self:
            record.status = "accepted"
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = "offer_accepted"
            record.property_id.selling_price = record.price

    def refuse_offer(self):
        for record in self:
            record.status = "refused"

    @api.model
    def create(self, vals):
        record = super().create(vals)
        if record.property_id and record.property_id.state == "new":
            record.property_id.state = "offer_received"
        return record