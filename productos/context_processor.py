def total_carrito(request):
    total = 0
    if 'carrito' in request.session:
        try:
            for key, value in request.session['carrito'].items():
                total += float(value['precio']) * value['cantidad']
        except KeyError:
            request.session['carrito'] = {}
            total = 0
    return {'carrito_total': total}