from flask import Flask, render_template, request, send_file
from docxtpl import DocxTemplate
import datetime
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def generate_order():
    if request.method == 'POST':
        # Отримання даних з форми
        data = {
            'location': request.form['location'],
            'commander': request.form['commander'],
            'mission': request.form['mission'],
            'date': datetime.datetime.now().strftime('%Y-%m-%d')
        }

        # Завантаження шаблону та рендер
        tpl = DocxTemplate("templates_docx/order_template.docx")
        tpl.render(data)

        # Збереження файлу
        output_path = f"generated/temp_order_{data['date']}.docx"
        tpl.save(output_path)

        return send_file(output_path, as_attachment=True)

    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)
