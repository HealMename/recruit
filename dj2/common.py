from libs.utils import db


def get_user_id(phone, type_, id_=0):
    """获取用户id"""
    where_sql = ''
    if type_ in [1, 2, 3]:
        if id_:
            where_sql = f" u.id != {id_}"
        sql = f"""
            select DISTINCT u.id from recruit.users u 
            join recruit.user_tea_det d on u.id=d.user_id 
            and d.phone_number ='{phone}' and u.`type` ={type_} 
            {where_sql}
            LIMIT 1;
        """
        user = db.default.fetchone_dict(sql)
        return user.id if user else 0
    elif type_ == 4:
        sql = f"""
            select id from recruit.yonghu where shouji='{phone}'
        """
        user = db.default.fetchone_dict(sql)
        return user.id if user else 0
    elif type_ == 5:
        sql = f"""
            select id from recruit.gongsi where shouji='{phone}'
        """
        user = db.default.fetchone_dict(sql)
        return user.id if user else 0
    else:
        return 0

