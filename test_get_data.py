"""Testing commands by click."""
import click
from click.testing import CliRunner
from my_commands import list_all, slug, main, list_export
import json


runner = CliRunner()


def test_get_single_article():
    """Test get single article."""
    result = runner.invoke(slug, ["new_wangonya"])
    json_result = json.loads(result.output)

    assert result.exit_code == 0
    assert not result.exception
    assert "slug" in result.output
    assert json_result['slug'] == 'new_wangonya'


def test_get_all_article():
    """Test get all articles."""
    result = runner.invoke(list_all)
    json_result = json.loads(result.output)

    assert result.exit_code == 0
    assert not result.exception
    assert "slug" in result.output
    assert "id" in json_result[0]

