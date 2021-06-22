class Helpers():
    def fix_date(self, date):
        if date < 10:
            new_format = '0'+str(date)
        else:
            new_format = str(date)
        
        return new_format
