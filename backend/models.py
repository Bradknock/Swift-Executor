from extensions import db
from sqlalchemy.sql import func

class rawdata(db.Model):
    name = db.Column(db.String(100), primary_key=True, nullable = False)
    time = db.Column(db.DateTime, primary_key=True, default=func.now(), nullable=False)
    inj_act = db.Column(db.Float, nullable=False)
    inj_setpt = db.Column(db.Float, nullable=False)
    inj_perc = db.Column(db.Float, nullable=False)
    hyd_status = db.Column(db.Integer, nullable=True)
    time_until_hyd = db.Column(db.Integer, nullable=True)


    def to_json(self):
        hours, remainder = divmod(self.time_until_hyd, 3600000)
        minutes, remainder = divmod(remainder, 60000)  
        seconds, milliseconds = divmod(remainder, 1000) 

        return {
            "name": self.name,
            "time": self.time,
            "inj_act": self.inj_act,
            "inj_setpt": self.inj_setpt,
            "inj_perc": self.inj_perc,
            "hyd_status": self.hyd_status,
            "time_until_hyd": f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}",
        }