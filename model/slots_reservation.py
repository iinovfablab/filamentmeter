from connections.connection_db import ConnectionDB
from src.read_file import jsonify
import datetime as dt
from src.tools import convert_dt, check_period




class SlotsModel(ConnectionDB):

    def __init__(self):
        super().__init__()
        self.params_db(jsonify())
        self.__conn = self.connection_db()

    
    def slots(self):
        
        
        past_date = dt.datetime.now()
        #limits_month = [1,6,12]
        fdate = convert_dt(dt)
        date_now = dt.datetime(*fdate)
        date_next_day = dt.datetime.now() + dt.timedelta(1)


        fmt = "%Y-%m-%d %H:%M"
        

        
        #first, last = check_period(actual_month)
        first_date = f"{past_date.year}-{past_date.month}-{past_date.day} 05:00"
        last_date = f"{date_next_day.year}-{date_next_day.month}-{date_next_day.day} 01:30"

        fdate = dt.datetime.strptime(first_date, fmt)
        ldate = dt.datetime.strptime(last_date, fmt)
        
        
        self.params_db(jsonify())
        conn = self.connection_db()
        query = f"""select (s.end_at-s.start_at) as consumo, u.id, u.username, s.start_at, s.end_at, g."name" as "curso", u.email  from slots s
                        inner join slots_reservations sr on sr.slot_id = s.id
                        inner join reservations r on r.id = sr.reservation_id
                        inner join statistic_profiles sp on r.statistic_profile_id = sp.id
                        inner join users u on u.id = sp.user_id
                        inner join "groups" g on g.id = sp.group_id    
                        where s.start_at between  %s and %s  and r.reservable_id = 8
                        order by s.end_at desc"""

        cursor = conn.cursor()
        cursor.execute(query,(first_date, last_date,))
        result = cursor.fetchall()
        conn.close()
        return result