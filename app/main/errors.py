from flask import render_template, request
from . import main
from .. import db
from ..models import Subscribers

@main.app_errorhandler(404)
def notfound(error):
    """
    Function to render the 404 error page
    """
    if request.method == "POST":
        new_sub = Subscribers(email = request.form.get("subscriber"))
        db.session.add(new_sub)
        db.session.commit()
    return render_template("notfound.html"),404