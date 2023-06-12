def login_status(request):
    customer_id = request.session.get('customer_id')
    context = {}
    
    if customer_id:
        # 用户已登录
        context['is_logged_in'] = True
    else:
        # 用户未登录
        context['is_logged_in'] = False
    
    return context