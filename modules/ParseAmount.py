class CleanAmount:
    
    def __init__(self):
        
        import re
        import json

        self.re_numeral = re.compile(u'[0-9]+')
        #self.re_inteval = re.compile(u'[0-9]+\s*\-\s*[0-9]+')
        self.re_inteval_closed = re.compile(u'^\s*[0-9]{1,2}\s*(?:\-|/)\s*[0-9]{1,2}\s*$')
        self.re_large_num = re.compile(u'[0-9],{0,1}0{3,}')
        self.re_positions = re.compile(u'[0-9]+\s*(?:(?:ตำแหน่ง)|(?:อัตรา)|(?:คน)|(?:position)|(?:Position))')
        self.num_sep = re.compile(u'(?:\-|/)')
        self.excluded = json.load(open('./modules/excluded_company.json', 'rt', encoding='utf-8'))
    
    def clean_amount(self, document):
        
        for company in self.excluded:
            if document['company'].find(company) != -1:
                return 1
        
        amount = document['amount']
        
        num_list = self.re_numeral.findall(amount)
        
        if len(num_list) == 0:
            return 1
        if len(num_list) == 1:
            ret = int(num_list[0])
            if ret == 0:
                return 1
            else:
                return ret
        
        num_pos = self.re_positions.findall(amount)
        if len(num_pos) >= 1:
            #print(amount)
            #print('  ', num_pos)
            temp = []
            for item in num_pos:
                temp.append(int(self.re_numeral.search(item).group()))
            max_num_pos = max(temp)
            #print('   ', max_num_pos)
            if max_num_pos == 0:
                return 1
            else:
                return max_num_pos
        
        num_int_close = self.re_inteval_closed.findall(amount)
        if len(num_int_close) == 1:
            num_int_close = num_int_close[0].replace(' ', '')
            sep_pos = self.num_sep.search(num_int_close).start(0)
            num_int_close = num_int_close[sep_pos+1:]
            ret = int(num_int_close)
            if ret == 0:
                return 1
            else:
                return ret
        
        #print(amount)
        return 1

