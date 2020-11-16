from flask import abort, redirect, render_template, request, session, url_for
from flask_login import login_required

from ..search import Recipe
from . import main
from .forms import AdvancedSearchForm, SearchForm


@main.route("/", methods=["GET", "POST"])
def index():
    """View function for the main (index) page

    Returns:
        On a GET request, returns the rendered template for index.html.
        On a POST request (search form submission), redirects to the search page, passing the form data as the query argument.
    """
    form = SearchForm()
    if request.method == "POST" or form.validate_on_submit():
        return redirect(url_for(".search", _method="GET", query=form.query.data))
    return render_template(
        "index.html",
        form=form,
        name=session.get("name"),
        known=session.get("known", False),
    )


@main.route("/search", methods=["GET", "POST"])
def search():
    """View function for the search page

    Returns:
        The rendered template search.html

        On POST request (advanced search form submission), uses the form data for the query.
        On GET request (from index page), uses the GET request argument for the query.
    """
    form = AdvancedSearchForm()
    recipes = []

    if request.method == "GET" and "query" in request.args:
        # i.e. if coming from the index page
        recipes = Recipe.get_recipes_by_name(request.args["query"], page=0, per_page=50)
    elif request.method == "POST" or form.validate_on_submit():
        # i.e. if coming from an advanced search
        recipes = Recipe.get_recipes_by_name(
            form.recipe.query.data, page=0, per_page=50
        )

    return render_template("search.html", recipes=recipes, form=form)


@main.route("/recipe/<recipe_id>", methods=["GET", "POST"])
def recipe(recipe_id):
    """View function for recipe display

    Returns:
        The rendered template recipe.html for the requested recipe (by ID).
    """
    recipe = Recipe.get_recipe_by_id(recipe_id)
    if not recipe:
        abort(404)
    return render_template("recipe.html", recipe=recipe)


@main.route("/fridge", methods=["GET", "POST"])
@login_required
def fridge():
    """View function for fridge/ inventory feature

    Note: This feature is not implemented yet. fridge.html displays a "coming soon" page.

    Returns:
        The rendered template for fridge.html
    """
    return render_template("fridge.html")


@main.route("/list", methods=["GET", "POST"])
@login_required
def list():
    """View function for grocery list feature

    Note: This feature is not implemented yet. list.html displays a "coming soon" page.

    Returns:
        The rendered template for list.html
    """
    return render_template("list.html")
