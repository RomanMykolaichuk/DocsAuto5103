from flask import Flask, render_template, request, send_file, redirect, url_for
from docxtpl import DocxTemplate
import datetime
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

DB_PARAMS = {
    'dbname': 'doc5103',
    'user': 'postgres',
    'password': 'admin',
    'host': 'localhost',
    'port': 5432
}


def get_all_orders():
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT id, location, commander, mission FROM orders ORDER BY id")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_order_data(order_id):
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT location, commander, mission FROM orders WHERE id = %s", (order_id,))
    row = cursor.fetchone()
    conn.close()
    return row

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = {
            'location': request.form['location'],
            'commander': request.form['commander'],
            'mission': request.form['mission'],
            'date': datetime.datetime.now().strftime('%Y-%m-%d')
        }

        tpl = DocxTemplate("templates_docx/order_template.docx")
        tpl.render(data)

        output_path = f"generated/manual_order_{data['date']}.docx"
        tpl.save(output_path)

        return send_file(output_path, as_attachment=True)

    orders = get_all_orders()
    return render_template('form2.html', orders=orders)

@app.route('/generate/<int:order_id>')
def generate_doc(order_id):
    data = get_order_data(order_id)
    if not data:
        return f"Order ID {order_id} not found", 404

    data['date'] = datetime.datetime.now().strftime('%Y-%m-%d')

    tpl = DocxTemplate("templates_docx/order_template.docx")
    tpl.render(data)

    output_path = f"generated/temp_order_{order_id}_{data['date']}.docx"
    tpl.save(output_path)

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
