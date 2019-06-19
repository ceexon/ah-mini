"""Generating commands to run the app."""

import click
import json
from get_data import GetAndExportArticleData
import sys

MAIN_DOMAIN = 'https://ah-django-staging.herokuapp.com/api/articles/'
GET_ARTICLES_URL = MAIN_DOMAIN + 'feed/'


@click.group(invoke_without_command=True, chain=True)
def main():
    """
    Simple Mini AH APP.

    Consumes Authers Haven API for single or all articles.
    Articles can also be exported as csv and json.
    """


def get_all_articles():
    """Get all articles."""
    get_articles = GetAndExportArticleData(
        GET_ARTICLES_URL).conver_to_json()['results']
    data = json.dumps(get_articles, indent=4, sort_keys=False)
    return data


def get_single_article(slug):
    """Get a single article by slug."""
    article_url = MAIN_DOMAIN + slug + "/"
    data = GetAndExportArticleData(article_url).conver_to_json()
    data = json.dumps(data, indent=4, sort_keys=False)
    return data


@main.command()
@click.option("--list-all", "-l",
              help="This command prints all articles on the terminal")
def list_all(list_all):
    """Print all articles to the terminal."""
    click.echo(get_all_articles())


@main.command()
@click.option("--slug", "-s",
              help="This command gets an article via the slug enter"
              " the article's slug and in return get the article")
@click.argument("slug")
def slug(slug):
    """Print a single article."""
    click.echo(get_single_article(slug))


@main.command()
@click.option("--list-export", "-lc",
              help="This command generates a csv file with all articles\n \
              [command] => ah slug-csv\n \
              [arg 1] => file_type(Req)\n \
              [arg 2] => file_name(Opt) \n"
              )
@click.argument("file_type")
@click.argument("file_name", required=False)
def list_export(list_export, file_type, file_name=None):
    """Export all articles data to csv."""
    click.echo('Your file is being converted.....')
    article_data = GetAndExportArticleData(GET_ARTICLES_URL)
    if(file_type == 'csv'):
        article_data.export_to_csv(file_name)
    elif(file_type == 'json'):
        article_data.export_to_json(file_name)
    else:
        click.echo('File type you entered is not supported')
        sys.exit('Please use csv or json')

    click.echo('Download completed.')


@main.command()
@click.option("--slug-export", "-x",
              help="This command generates a csv file with single articles\n \
              [command] => ah slug-csv\n \
              [arg 1] slug(Req)\n \
              [arg 2] file_type(Req)\n \
              [arg 3] file_name(Opt)\n"
              )
@click.argument("slug")
@click.argument("file_type")
@click.argument("file_name", required=False)
def slug_export(slug_export, slug, file_type, file_name=None):
    """Export single article data to csv."""
    click.echo('Your file is being converted.....')
    article_url = MAIN_DOMAIN + slug + "/"
    article_data = GetAndExportArticleData(article_url)
    if(file_type == 'csv'):
        article_data.export_to_csv(file_name)
    elif(file_type == 'json'):
        print(file_name, file_type)
        article_data.export_to_json(file_name)
    else:
        click.echo('File type you entered is not supported')
        sys.exit('Please use csv or json')
    click.echo('Download completed.')
