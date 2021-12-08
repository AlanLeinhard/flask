from flask import Blueprint, render_template, url_for, redirect
from app import db, app
import base64

from wtforms.form import Form

from app.models import Item, Post, Project
from app.site.forms import SearchForm

bp = Blueprint("site", __name__)


@bp.route('/', methods=['POST', 'GET'])
def index():
    """Show all the posts, most recent first."""
    form = SearchForm()
    post = Post.query.order_by(Post.created.desc()).all()
    item = Item.query.order_by(Item.click.desc()).all()

    for el in post:
        el.image = base64.b64encode(el.image).decode('ascii')

    for el in item:

        el.image = base64.b64encode(el.image).decode('ascii')

    if form.validate_on_submit():
        request = form.search.data
        if form.select.data == "google":
            return redirect("https://www.google.com/search?q="+request+"&sxsrf=AOaemvJV6dEIBTrjqBnthtVJRGnqAp7zVQ%3A1638082607415&source=hp&ei=LyijYbuGF8GprgTOupG4DQ&iflsig=ALs-wAMAAAAAYaM2P6alZ2L_AwgQ0amZuP4nctZ5n-Ai&ved=0ahUKEwj72bOfvbr0AhXBlIsKHU5dBNcQ4dUDCAg&uact=5&oq="+request+"&gs_lcp=Cgdnd3Mtd2l6EAMyBwgAELEDEEMyCAgAEIAEELEDMggIABCABBCxAzIICAAQgAQQsQMyCwgAEIAEELEDEIMBMggIABCABBCxAzIICAAQgAQQsQMyCAgAEIAEELEDMgUIABCABDIFCAAQgAQ6BAgAEAM6DgguEIAEELEDEMcBEKMCOg4ILhCABBCxAxDHARDRAzoRCC4QgAQQsQMQgwEQxwEQowI6BAgAEEM6EQguEIAEELEDEIMBEMcBENEDOgsILhCABBCxAxCDAToNCC4QsQMQxwEQ0QMQQzoHCAAQyQMQQzoFCAAQkgM6BAgAEA06BggAEA0QCjoNCC4QsQMQxwEQ0QMQDToKCC4QxwEQ0QMQDToHCCMQ6gIQJzoHCC4QsQMQQzoECC4QQ1AAWIYkYPUsaAFwAHgAgAHPAYgBkA-SAQYwLjEyLjGYAQCgAQGwAQU&sclient=gws-wiz")
        elif form.select.data == "yandex":
            return redirect("https://yandex.ru/yandsearch?clid=2028026&text="+request+"&lr=11373")
        elif form.select.data == "duckduckgo":
            return redirect("https://duckduckgo.com/?q="+request+"&t=h_&ia=web")
        pass

    return render_template("site/index.html", data=list, item=item, post=post, form=form)


@bp.route("/<int:id>")
def news(id):
    """Show all the posts, most recent first."""
    post = Post.query.get_or_404(id)
    post.image = base64.b64encode(post.image).decode('ascii')
    return render_template("site/news.html", post=post)


@bp.route("/projects")
def projects():

    form = SearchForm()
    post = Post.query.order_by(Post.created.desc()).all()
    item = Project.query.order_by(Project.click.desc()).all()

    for el in post:
        el.image = base64.b64encode(el.image).decode('ascii')

    for el in item:

        el.image = base64.b64encode(el.image).decode('ascii')

    return render_template("site/projects.html", data=list, item=item, post=post, form=form)


@bp.route("/service/<int:id>")
def service_url(id):
    service =Item.query.get_or_404(id)
    service.click = service.click + 1
    db.session.commit()
    return redirect(service.url_serv)


@bp.route("/project/<int:id>")
def project_url(id):
    project =Project.query.get_or_404(id)
    project.click = project.click + 1
    db.session.commit()
    return redirect(project.url_serv)