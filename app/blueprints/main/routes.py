from app.blueprints.auth.routes import login
from . import bp as main
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .forms import NewToolForm
from ...models import Tool, Toolbox

@main.route('/', methods=["GET"])
@login_required
def user():
    u = current_user
#    mytools = Toolbox.query.all(userid)
    return render_template('user.html.j2')#, mytools=mytools)

@main.route('/newtool', methods=["GET",'POST'])
@login_required
def newtool():
    form = NewToolForm()
    if request.method == 'POST' and form.validate_on_submit():

        new_tool_data={
            "tool_name" : form.tool_name.data,
            "tool_brand" : form.tool_brand.data,
            "quantity" : form.quantity.data
        }

        new_tool_object = Tool()
        new_tool_object.tool_from_dict(new_tool_data)
        new_tool_object.save()

        new_toolbox_tool = Tool()
        new_toolbox_tool.user_id=current_user.id
#        new_toolbox_tool.toolbox_id=new_tool_object.toolbox_id
#        my_tools=Tool.query.filter_by(user_id=current_user.id).all()

        # show Tool list
        flash("Successfully Added Tool", 'success')
        return redirect(url_for('main.newtool'))
    return render_template('newTool.html.j2', form=form)

@main.route('/alltools', methods=["GET"])
@login_required
def alltools():
    tools = Tool.query.all()
    return render_template('alltools.html.j2', tools=tools)
