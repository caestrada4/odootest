import json
from odoo import http
from odoo.http import request, Response
from odoo.exceptions import AccessError, MissingError

class SaleOrdeAPI(http.Controller):
    _read_fields = ['id','name','partner_id','date_order','payment_term_id','x_validez','x_metodo_pago','x_nota_cotizacion','amount_total']

    def _json_response(self, data, status=200):
        return Response(
            json.dumps(data,default=str),
            status=status,
            mimetype='application/json'
        )
    
    @http.route('/api/sale_order', type='http', auth='public', methods=['GET','POST'], csrf=False,cors='*')
    def collection(self,**params):
        try:
            if request.httprequest.method == 'GET':
                
                limit = int(params.get('limit', 80))
                offset = int(params.get('offset', 0))
                domain = []
                if 'domain' in params:
                    try:
                        domain = json.loads(params['domain'])
                    except Exception:
                        return self._json_response({'error': 'Invalid domain format'}, status=400)
                orders = request.env['sale.order'].sudo().search_read(domain, self._read_fields, limit=limit, offset=offset)
                return self._json_response({'status': 'ok', 'count':len(orders), 'results': orders})
            elif request.httprequest.method == 'POST':
                try:
                    data = request.jsonrequest
                except Exception:
                    data=dict(params)
                allowed={'partner_id','date_order','payment_term_id','x_validez','x_metodo_pago','x_nota_cotizacion'}
                create_vals = {k: v for k, v in data.items() if k in allowed}
                if not create_vals.get('partner_id'):
                    create_vals['partner_id'] = 18
                order=request.env['sale.order'].sudo().create(create_vals)
                order_data=order.read(self._read_fields)[0]
                return self._json_response({'status':'created', 'id':order.id,'record':order_data}, status=201)
            else:
                return self._json_response({'error': 'Method not allowed'}, status=405)
        
        except (AccessError) as e:
            return self._json_response({'error': 'Access denied', 'message':str(e)}, status=403)
        except Exception as e:
            return self._json_response({'error': 'Server error', 'message':str(e)}, status=500)