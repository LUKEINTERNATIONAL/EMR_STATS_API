def current_user_where(request):
    where_clause = ''
    if(request.user.zone_id is not 0):
        where_clause = ''' AND d.zone_id = {}'''.format(request.user.zone_id)
    elif(request.user.district_id is not 0):
        where_clause = ''' AND f.district_id = {}'''.format(request.user.district_id)
    return where_clause