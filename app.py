from flask import Flask, g, request, jsonify
from database import get_db

app = Flask(__name__)

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/details', methods=['GET'])
def get_details():
    db = get_db()
    details_cur = db.execute('select YEAR, LOCALITY, SUBURB, STATE, POSTCODE, COUNT from NSW_BIRTH_RATE')
    details = details_cur.fetchall()

    return_values = []

    for detail in details:
        detail_dict = {}
        detail_dict['YEAR']      = detail['YEAR']
        detail_dict['LOCALITY']  = detail['LOCALITY']
        detail_dict['SUBURB']    = detail['SUBURB']
        detail_dict['STATE']     = detail['STATE']
        detail_dict['POSTCODE']  = detail['POSTCODE']
        detail_dict['COUNT']     = detail['COUNT']

        return_values.append(detail_dict)

    return jsonify({'details' : return_values})

@app.route('/detail/<string:SUBURB>', methods=['GET'])
def get_detail(SUBURB):    
    db = get_db()
    detail_cur = db.execute('select YEAR, LOCALITY, SUBURB, STATE, POSTCODE, COUNT from NSW_BIRTH_RATE where SUBURB = ?', [SUBURB])
    detail = detail_cur.fetchone()

    return jsonify({'detail' : {'YEAR'     : detail['YEAR'], 
    	                        'LOCALITY' : detail['LOCALITY'], 
    	                        'SUBURB'   : detail['SUBURB'], 
    	                        'STATE'    : detail['STATE'], 
    	                        'POSTCODE' : detail['POSTCODE'], 
    	                        'COUNT'    : detail['COUNT']}}) 

if __name__ == '__main__':
    app.run(debug=True)