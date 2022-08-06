from flask import Blueprint, redirect, url_for, render_template, request, jsonify, flash
from flask_login import login_required, current_user
from .models import ACdatum, FanData  # FanData
from . import db
from .Backend_Scripts import AC_Calc
from .Backend_Scripts.AC_Calc import input_request as inp
from .Backend_Scripts.Alt import fan_price
from .Backend_Scripts.Tracker import plot_graph, scatter, pie_chart

views = Blueprint('views', __name__)

recent_bill_iter = []


@views.route('')
def default():
    return render_template("home.html", user=current_user)


@views.route('home')
def home():
    return redirect(url_for("views.default"))
    # redirects to default page for people who search url/home


@views.route('base')
@login_required
def webflow():
    return render_template("base2.html", user=current_user)


@views.route('aircalculator', methods=['GET', 'POST'])
@login_required
def aircalculator():
    global recent_bill_iter
    if request.method == 'POST':
        KwH, GOT = AC_Calc.KwH(inp('BTU_rating'), inp('EER'), inp('wattage'), [inp('size'), inp('type')])
        res_iter = AC_Calc.Price(KwH, inp('EER'), inp('hours'), inp('temp'), inp('state'),
                                 inp('major-city'), inp('month'), inp('day-avg-temp'), inp('day-high-temp'),
                                 inp('save'))
        global recent_bill_iter
        recent_bill_iter = res_iter
        sugg = AC_Calc.sugg_temp(res_iter[0], res_iter[1], res_iter[3] - res_iter[2], res_iter[3],
                                 inp('goal_price'),
                                 inp('priority'))
        sugg_hours, sugg_temp = sugg[0], sugg[1]
        if request.form.get("save") == "1":
            new_ACdatum = ACdatum(hours=res_iter[1],
                                  temp=res_iter[2],
                                  estimated_bill=res_iter[0],
                                  user_id=current_user.id)
            db.session.add(new_ACdatum)
            db.session.commit()
            return redirect(url_for("views.actracker"))  # if user wants to save data, redirected to actracker page
        else:
            return render_template("aircalculator.html", user=current_user, display=1,
                                   results=[res_iter[0], sugg_hours,
                                            round(sugg_temp, 2)])  # if user does not want to save data, shows temporary results div
    return render_template("aircalculator.html", user=current_user, display=0)


@views.route('fancalculator', methods=['GET', 'POST'])
@login_required
def fancalculator():
    if request.method == 'POST':
        price = round(fan_price(inp('state'), inp('type'), inp('wattage'), inp('hours')), 1)
        if request.form.get("save") == "1":
            new_fanData = FanData(estimated_bill=price,
                                  user_id=current_user.id)
            db.session.add(new_fanData)
            db.session.commit()
            return redirect(url_for("views.actracker"))
        else:
            return render_template("fancalculator.html", user=current_user, display=1, bill=price)
    return render_template("fancalculator.html", user=current_user, display=0)


def is_empty(iter):
    return False if len(iter) > 0 else True


@views.route('actracker', methods=['GET', 'POST'])
@login_required
def actracker():
    if request.method == 'Post':
        yvals = [current_user.ACdatum.hours, current_user.ACdatum.temp, current_user.ACdatum.estimated_bill]
        y_vals = [x for x in yvals if not is_empty(x)]
        plot = plot_graph(current_user.ACdatum.date, y_vals, ['Hours', 'Temperature', 'Bill'],
                          ['#00A36C', '#088F8F', 'b'],
                          'AC Hours, Temperature, and Bill')
        pie = pie_chart(current_user.ACdatum.estimated_bill, current_user.FanData.estimated_bill,
                        graph_name='AC cost vs Fan Cost')
        scatter = AC_Calc.scatter(current_user.ACdatum.hours, current_user.ACdatum.temp)
        plot.savefig('website/static/plot.png')
        pie.savefig('website/static/pie.png')
        scatter.savefig('website/scatter.png')

        return render_template('actracker.html', user=current_user, acdata_length=len(current_user.ACdata))
    return render_template("actracker.html", user=current_user, acdata_length=len(current_user.ACdata))
