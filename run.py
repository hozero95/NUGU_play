from flask import (
    render_template,
    redirect,
    request,
    abort,
    url_for,
    session,
    Flask
)
from flask_ask import(
    Ask,
    statement
)
from api import *

app = Flask(__name__)
ask = Ask(app, '/')

@app.route("/health")
def healthCheck():
    return "OK"

@app.route("/action.sale_info", methods=['POST'])
def sale_info():
    req = request.json
    action = req['action']['actionName']
    if action == 'action.sale_info':
        return result(req)
    return ''

if __name__ == '__main__':
    app.run(debug=True)

{
    "version": "2.0",
    "action": {
         "actionName": "sale_info",
         "parameters": {
              "brand": {
                 "type": "BRAND",
                 "value": "BRAND_NAME"
               },
              "product":{
                 "type": "PRODUCT",
                 "value": "PRODUCT_NAME"
               }
          }
    }
}