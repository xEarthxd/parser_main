class Extract_Date:
    
    def __init__(self):
        from datetime import datetime
        import re
        self.datetime = datetime
        self.file_date = re.compile(u'(/[0-9]{8}/)')

    def date_from_file(self, file_name):
        df = self.file_date.search(file_name)
        if not df:
            return self.datetime.fromordinal(1)
        df = df.group()[1:5] + '-' + df.group()[5:7] + '-' + df.group()[7:9] + ' 00:00:00'
        df = self.datetime.strptime(df, '%Y-%m-%d %H:%M:%S')
        return df