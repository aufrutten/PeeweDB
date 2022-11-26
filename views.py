from flask import Blueprint, render_template, request, current_app

simple_page = Blueprint('simple_page', __name__,
                        template_folder='templates',
                        )


@simple_page.route('/report/')
@simple_page.route('/')
def parent_route():
    reverse_mode = True if request.values.get('order') else False
    database = current_app.config['drivers']
    data = [[driver.name, driver.car, driver.result] for driver in database.select().order_by(database.result)]
    if reverse_mode:
        data.reverse()
    return render_template('index.html', content=enumerate(data, start=1))


@simple_page.route('/report/drivers/')
def drivers():
    database = current_app.config['drivers']
    list_with_results = [[num, driver.name, driver.abbr] for num, driver in enumerate(
        database.select().order_by(database.result), start=1)]

    abbr = request.values.get('driver')
    reverse_mode = True if request.values.get('order') else False

    if reverse_mode:
        list_with_results.reverse()

    if abbr:
        driver = database.select().where(database.abbr == abbr).get()
        content = [driver.name, driver.car, driver.result]
        return render_template('drivers.html', driver=content)
    else:
        return render_template('drivers.html', drivers=list_with_results)

