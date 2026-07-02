# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError

APPROVER_GROUP = 'payment_control_shipping.group_shipping_approver'


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    payment_control_approval_state = fields.Selection(
        selection=[
            ('none', 'Onay Yok'),
            ('requested', 'Onay Bekliyor'),
            ('approved', 'Onaylandı'),
        ],
        string='Ödeme Onay Durumu',
        default='none',
        copy=False,
        tracking=True,
    )
    payment_control_approved_by = fields.Many2one(
        'res.users', string='Onaylayan', copy=False, readonly=True)
    payment_control_approved_date = fields.Datetime(
        string='Onay Tarihi', copy=False, readonly=True)
    payment_control_is_approver = fields.Boolean(
        string='Onaycı mı?', compute='_compute_payment_control_is_approver')

    @api.depends_context('uid')
    def _compute_payment_control_is_approver(self):
        is_approver = self.env.user.has_group(APPROVER_GROUP)
        for order in self:
            order.payment_control_is_approver = is_approver

    def action_request_payment_approval(self):
        approver_group = self.env.ref(APPROVER_GROUP, raise_if_not_found=False)
        approvers = approver_group.users if approver_group else self.env['res.users']
        template = self.env.ref(
            'payment_control_shipping.mail_template_payment_approval_request',
            raise_if_not_found=False)
        for order in self:
            if order.payment_control_approval_state == 'approved':
                continue
            order.payment_control_approval_state = 'requested'
            body = _(
                "%s siparişi için ödeme kontrolü onayı talep edildi. "
                "Talep eden: %s"
            ) % (order.name, self.env.user.name)
            # İç bildirim / yapılacak (aktivite)
            for user in approvers:
                order.activity_schedule(
                    'mail.mail_activity_data_todo',
                    user_id=user.id,
                    summary=_("Ödeme kontrolü onayı bekleniyor"),
                    note=body,
                )
            # Denetim izi (chatter notu)
            order.message_post(body=body, subtype_xmlid='mail.mt_note')
            # Gerçek e-posta: kullanıcının bildirim tercihinden bağımsız
            # olarak onaycıların e-posta adresine gönderilir.
            partner_ids = approvers.mapped('partner_id').filtered('email').ids
            if template and partner_ids:
                template.send_mail(
                    order.id,
                    force_send=True,
                    email_values={'recipient_ids': [(6, 0, partner_ids)]},
                )
        return True

    def action_approve_payment_control(self):
        if not self.env.user.has_group(APPROVER_GROUP):
            raise UserError(_("Bu işlem için 'Sevkiyat Onaycısı' yetkiniz yok."))
        for order in self:
            order.write({
                'payment_control_approval_state': 'approved',
                'payment_control_approved_by': self.env.user.id,
                'payment_control_approved_date': fields.Datetime.now(),
            })
            order.activity_feedback(['mail.mail_activity_data_todo'])
            order.message_post(
                body=_("Ödeme kontrolü onaylandı. Onaylayan: %s")
                % self.env.user.name)
        return True

    def action_reset_payment_approval(self):
        if not self.env.user.has_group(APPROVER_GROUP):
            raise UserError(_("Bu işlem için 'Sevkiyat Onaycısı' yetkiniz yok."))
        for order in self:
            order.write({
                'payment_control_approval_state': 'none',
                'payment_control_approved_by': False,
                'payment_control_approved_date': False,
            })
            order.message_post(
                body=_("Ödeme kontrolü onayı sıfırlandı. İşlemi yapan: %s")
                % self.env.user.name)
        return True
