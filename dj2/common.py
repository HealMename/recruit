from libs.utils import db


def get_user_id(phone, type_, id_=0):
    """获取用户id"""
    where_sql = ''
    if type_ in [1, 2, 3, 4]:
        if id_:
            where_sql += f" u.id != {id_}"
        sql = f"""
            select DISTINCT u.id, u.password from recruit.users u 
            join recruit.user_tea_det d on u.id=d.user_id 
            and d.phone_number ='{phone}' and u.`type` ={type_} 
            {where_sql}
            LIMIT 1;
        """
        print(sql)
        user = db.default.fetchone_dict(sql)
    elif type_ == 4:
        sql = f"""
            select id, mima as password from recruit.yonghu where shouji='{phone}'
        """
        user = db.default.fetchone_dict(sql)
    elif type_ == 5:
        sql = f"""
            select id, mima as password from recruit.gongsi where shouji='{phone}'
        """
        user = db.default.fetchone_dict(sql)
    else:
        return 0, ''

    if user:
        return user.id, user.password
    else:
        return 0, ''
