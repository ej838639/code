"""
Query Teradata
Eric Johnson
Jan 2018
"""

import teradata

udaExec = teradata.UdaExec (appName="HelloWorld", version="1.0",
        logConsole=False)
 
session = udaExec.connect(method="odbc", system="prd_qtan.eng.t-mobile.com",
        username="td_ejohnson", password="td_ejohnson");
 
for row in session.execute('''select Top 10* from PRD_LSR_ERC_v.LTE_ERC WHERE src_file_date = '2017-12-15' AND market_name = 'PHILADELPHIA';'''):
    print(row)
    


from sqlalchemy import create_engine
user = 'td_ejohnson'
pasw=user
host = 'prd_qtan.eng.t-mobile.com'

# connect
td_engine = create_engine('teradata://'+ user +':' + pasw + '@'+ host + ':22/')

# execute sql
sql = '''select Top 10* from PRD_LSR_ERC_v.LTE_ERC WHERE src_file_date = '2017-12-15' AND market_name = 'PHILADELPHIA';'''
result = td_engine.execute(sql)