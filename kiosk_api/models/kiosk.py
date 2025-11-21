import json
import logging
import requests
from odoo import models, fields, api , _
_logger = logging.getLogger(__name__)
from odoo.exceptions import UserError

class Kiosk(models.Model):
    _name = 'kiosk.kiosk'
    _description = 'Kiosk API Integration'

    name = fields.Char(string='Kiosk Name', required=True)
    external_id = fields.Integer(string='External Kiosk ID', readonly=True, help='ID of the kiosk in the external Kiosk API')
    status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ], string='Status', default='inactive')
    kiosk_code = fields.Char(string='Kiosk Code', help='Unique code for the kiosk in the external Kiosk API')
    model_hw=fields.Char(string="Hardware Model", help="Model of the kiosk hardware")
    serial_number=fields.Char(string="Serial Number", help="Serial number of the kiosk hardware")
    firmware=fields.Char(string="Firmware Version", help="Firmware version of the kiosk hardware")
    location=fields.Json(string="Location Data", help="Location data of the kiosk in JSON format")
    components=fields.Json(string="Components Data", help="Components data of the kiosk in JSON format")
    network_status=fields.Json(string="Network Status", help="Network status of the kiosk in JSON format")
    last_seen=fields.Char(string="Last Seen", help="Timestamp of the last time the kiosk was seen online")
    install_date=fields.Char(string="Install Date", help="Installation date of the kiosk")
    last_maintenance=fields.Char(string="Last Maintenance", help="Date of the last maintenance performed on the kiosk")
    notes=fields.Text(string="Notes", help="Additional notes about the kiosk")
    created_at=fields.Char(string="Created At", readonly=True, help="Timestamp when the kiosk record was created in the external Kiosk API")
    updated_at=fields.Char(string="Updated At", readonly=True, help="Timestamp when the kiosk record was last updated in the external Kiosk API")
    cash_level=fields.Integer(string="Cash Level", help="Current cash level in the kiosk")
    cash_capacity=fields.Integer(string="Cash Capacity", help="Maximum cash capacity of the kiosk")

    def _get_api_base_url(self):
        # Placeholder for actual API base URL retrieval logic
        icp=self.enf["ir.config_parameter"].sudo()
        return icp.get_param('kiosk_api.base_url', default='http://194.163.154.201:4000/api/kiosks')
    
    def _get_api_headers(self):

        return {
            'Content-Type': 'application/json',
                    }
    def _api_request(self, method, endpoint='', data=None):
        base_url = self._get_api_base_url().rstrip('/')
        url= f"{base_url}/{endpoint}"

        try:
            _logger.info(f"Kiosk API %s %s payloead=%s",method,url,data)
            resp=requests.request(method=method, url=url, headers=self._get_api_headers(),data=json.dumps(data) if data is not None else None,timeout=10)
        except Exception as e:
            _logger.exception("Error de conexion con la API de kiosks")
            raise UserError(_("No se pudo conectar con la api %S") % e)
        
        if not resp.ok:
            try:
                err_json=resp
            except Exception:
                err_json={}
            msg=err_json.get("error") or resp.text or resp.reason
            raise UserError(_("Kiosk API Error (%s): %s") % (resp.status_code, msg))
        
        if resp.status_code == 204 or not resp.content:
            return None
        try:
            return resp.json()
        except Exception:
            return None
        
    def _prepare_api_payload(self,vals=None):
        self.ensure_one()
        vals= vals or {}

        def _get(field_name,default=None):
            if field_name in vals:
                return vals.get(field_name)
            return getattr(self,field_name,default)

        name=_get('name')
        kiosk_code=_get('kiosk_code')
        model_hw=_get('model_hw')
        serial_number=_get('serial_number')
        firmware=_get('firmware')
        location=_get('location')
        components=_get('components')
        network_status=_get('network_status')   
        cash_level=_get('cash_level')
        cash_capacity=_get('cash_capacity')
        status=_get('status','inactive')
        last_seen=_get('last_seen')
        install_date=_get('install_date')
        last_maintenance=_get('last_maintenance')
        notes=_get('notes')

        payload={
            'name':name,  
            'kiosk_code':kiosk_code or None,
            'model_hw':model_hw or None,
            'serial_number':serial_number or None,
            'firmware':firmware or None,
            'location':location or None,
            'components':components or None,
            'network_status':network_status or None,
            'cash_level':cash_level or 0,
            'cash_capacity':cash_capacity or 0,
            'status':status or "inactive",
            'last_seen':last_seen or None,
            'install_date':install_date or None,
            'last_maintenance':last_maintenance or None,
            'notes':notes or None,

        }
        return payload
    
