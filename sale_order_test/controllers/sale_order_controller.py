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
        
    @http.route('/api/sale_order/<int:order_id>', type='http', auth='public', methods=['GET', 'PUT', 'DELETE'], csrf=False, cors='*')
    def record(self, order_id, **params):
        try:
            Order = request.env['sale.order'].sudo()
            order = Order.browse(order_id)
            if not order.exists():
                return self._json_response({'error': 'Not found', 'message': 'Sale order not found'}, status=404)
            
            if request.httprequest.method == 'GET':
                data = order.read(self._read_fields)[0]
                return self._json_response({'status': 'ok', 'record': data})
            
            elif request.httprequest.method == 'PUT':                
                raw_body = request.httprequest.get_data(as_text=True)

                # Intentar obtener JSON real
                try:
                    data = request.jsonrequest or {}
                except Exception:
                    data = {}

                # Si no vino nada, intentar parsear el raw_body
                if not data and raw_body:
                    try:
                        data = json.loads(raw_body)
                    except Exception:
                        data = {}

                # Como último intento, usar params (?campo=valor)
                if not data:
                    data = dict(params)

                # Campos permitidos
                allowed = {
                    'partner_id', 'date_order', 'payment_term_id',
                    'x_validez', 'x_metodo_pago', 'x_nota_cotizacion'
                }

                update_vals = {k: v for k, v in data.items() if k in allowed}
                
                if not update_vals:
                    return self._json_response(
                        {
                            'error': 'No valid fields to update',
                            'received_data': data,
                            'received_keys': list(data.keys()),
                            'allowed_fields': list(allowed),
                            'raw_body': raw_body,
                            'content_type': request.httprequest.headers.get("Content-Type"),
                        },
                        status=400
                    )
                
                order.write(update_vals)
                updated = order.read(self._read_fields)[0]

                return self._json_response(
                    {'status': 'updated', 'id': order.id, 'record': updated},
                    status=200
                )            
            elif request.httprequest.method == 'DELETE':
                order.unlink()
                return self._json_response(
                    {'status': 'deleted', 'id': order_id}, status=200
                )

            else:
                return self._json_response(
                    {'error': 'Method not allowed'}, status=405
                )

        except AccessError as e:
            return self._json_response(
                {'error': 'Access denied', 'message': str(e)}, status=403
            )
        except MissingError as e:            
            return self._json_response(
                {'error': 'Not found', 'message': str(e)}, status=404
            )
        except Exception as e:
            return self._json_response(
                {'error': 'Server error', 'message': str(e)}, status=500
            )
