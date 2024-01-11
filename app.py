import os

from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from datetime import datetime
import pygal

ALLOWED_EXTENTIONS = set(['csv'])


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENTIONS


def create_app():
    app = Flask(__name__)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                new_filename = f'{filename.split(".")[0]}_{str(datetime.now().year)}.csv'
                save_location = os.path.join('input', new_filename)
                file.save(save_location)

                lines = open('input/' + new_filename, 'r').readlines()
                year_title = list()
                for i in lines:
                    x = i.strip().split(';')
                    if (x[6] == 'Lelouch, Claude'):
                        year_title.append(x[0] + ',' + x[2])

                if (len(year_title) == 0):
                    return render_template('index.html') + '''
                        <h2 style="color: brown">ERROR</h2> '''
                    print(1)
                else:
                    chart = pygal.Pie(half_pie=True)
                    pie_chart = pygal.Pie()
                    pie_chart.title = 'Browser usage in February 2012 (in %)'
                    for y in year_title:
                        data = y.strip().split(',')
                        pie_chart.add(data[1], int(data[0]))

                    # for y in year_title:
                    #     data = y.strip().split(',')
                    #     chart.add(data[1], int(data[0]))

                    chart = pie_chart.render_data_uri()
                    return render_template('index.html', chart=chart)

        return render_template('index.html')

    return app
