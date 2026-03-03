from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"
    x_external_ref = fields.Char(index=True, copy=False)


class SaleBulkService(models.AbstractModel):
    _name = "sale.bulk.service"

    @api.model
    def import_orders(self, payloads, chunk_size=200):
        created = 0
        skipped = 0
        for i in range(0, len(payloads), chunk_size):
            batch = payloads[i : i + chunk_size]
            refs = [p["external_ref"] for p in batch]
            existing = set(self.env["sale.order"].search([("x_external_ref", "in", refs)]).mapped("x_external_ref"))
            data = []
            for row in batch:
                if row["external_ref"] in existing:
                    skipped += 1
                    continue
                data.append({
                    "partner_id": row["partner_id"],
                    "x_external_ref": row["external_ref"],
                    "order_line": [(0, 0, {
                        "product_id": l["product_id"],
                        "product_uom_qty": l["qty"],
                        "price_unit": l["price_unit"],
                    }) for l in row["lines"]],
                })
            if data:
                self.env["sale.order"].create(data)
                created += len(data)
            self.env.cr.commit()
        return {"created": created, "skipped": skipped}
