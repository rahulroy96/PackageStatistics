from click.testing import CliRunner
from unittest.mock import patch
from src.constants import K_VALUE
from requests.exceptions import HTTPError, ConnectionError


@patch('src.package_statistics.download_file')
@patch('os.path.isfile')
def test_package_statistics_using_local(mock_isfile, mock_download_file):
    from src import package_statistics
    mock_isfile.return_value = True
    mock_download_file.return_value = True

    with patch.object(package_statistics.ContentsParser, 'top_k_packages_max_files') as mock_top_k_packages_max_files:
        top_k_return_value = [('package1', 2), ('package2', 1)]
        mock_top_k_packages_max_files.return_value = top_k_return_value
        runner = CliRunner()
        result = runner.invoke(package_statistics.package_statistics, ['arm64'])
        mock_download_file.assert_not_called()
        mock_top_k_packages_max_files.assert_called_once_with(K_VALUE)
        assert result.exit_code == 0
        assert "Using the local" in result.output
        assert top_k_return_value[0][0] in result.output
        assert str(top_k_return_value[0][1]) in result.output
        assert str(top_k_return_value[1][0]) in result.output
        assert str(top_k_return_value[1][1]) in result.output


@patch('src.package_statistics.download_file')
@patch('os.path.isfile')
def test_package_statistics_downloading_when_not_available(mock_isfile, mock_download_file):
    from src import package_statistics
    mock_isfile.return_value = False
    mock_download_file.return_value = True

    with patch.object(package_statistics.ContentsParser, 'top_k_packages_max_files') as mock_top_k_packages_max_files:
        top_k_return_value = [('package1', 2), ('package2', 1)]
        mock_top_k_packages_max_files.return_value = top_k_return_value
        runner = CliRunner()
        result = runner.invoke(package_statistics.package_statistics, ['arm64', '--force=false'])
        mock_download_file.assert_called_once()
        mock_top_k_packages_max_files.assert_called_once_with(K_VALUE)
        assert result.exit_code == 0
        assert "Downloading" in result.output
        assert top_k_return_value[0][0] in result.output
        assert str(top_k_return_value[0][1]) in result.output
        assert str(top_k_return_value[1][0]) in result.output
        assert str(top_k_return_value[1][1]) in result.output


@patch('src.package_statistics.download_file')
@patch('os.path.isfile')
def test_package_statistics_force_downloading_when_available_success(mock_isfile, mock_download_file):
    from src import package_statistics
    mock_isfile.return_value = True
    mock_download_file.return_value = True

    with patch.object(package_statistics.ContentsParser, 'top_k_packages_max_files') as mock_top_k_packages_max_files:
        top_k_return_value = [('package1', 2), ('package2', 1)]
        mock_top_k_packages_max_files.return_value = top_k_return_value
        runner = CliRunner()
        result = runner.invoke(package_statistics.package_statistics, ['arm64', '--force=true'])
        mock_download_file.assert_called_once()
        mock_top_k_packages_max_files.assert_called_once_with(K_VALUE)
        assert result.exit_code == 0
        assert "Downloading" in result.output
        assert top_k_return_value[0][0] in result.output
        assert str(top_k_return_value[0][1]) in result.output
        assert str(top_k_return_value[1][0]) in result.output
        assert str(top_k_return_value[1][1]) in result.output


def test_package_statistics_no_architecture():
    from src import package_statistics
    runner = CliRunner()
    result = runner.invoke(package_statistics.package_statistics)
    assert result.exit_code == 2
    assert "Missing argument" in result.output


@patch('src.package_statistics.download_file')
@patch('os.path.isfile')
def test_package_statistics_invalid_architecture(mock_isfile, mock_download_file):
    from src import package_statistics
    mock_isfile.return_value = False
    mock_download_file.side_effect = HTTPError('Test')
    runner = CliRunner()
    result = runner.invoke(package_statistics.package_statistics, ['ar'])
    assert result.exit_code == 1
    assert "Couldn't download the contents file!! Please check the architecture name" in result.output


@patch('src.package_statistics.download_file')
@patch('os.path.isfile')
def test_package_statistics_invalid_architecture(mock_isfile, mock_download_file):
    from src import package_statistics
    mock_isfile.return_value = False
    mock_download_file.side_effect = ConnectionError('Test')
    runner = CliRunner()
    result = runner.invoke(package_statistics.package_statistics, ['ar'])
    assert result.exit_code == 1
    assert "Couldn't connect to the server!! Please check your network connection" in result.output


@patch('src.package_statistics.download_file')
@patch('os.path.isfile')
def test_package_statistics_invalid_content_file_format_exception(mock_isfile, mock_download_file):
    from src import package_statistics
    mock_isfile.return_value = True
    mock_download_file.return_value = True

    with patch.object(package_statistics.ContentsParser, 'top_k_packages_max_files') as mock_top_k_packages_max_files:
        mock_top_k_packages_max_files.side_effect = package_statistics.InvalidContentFileFormat()
        runner = CliRunner()
        result = runner.invoke(package_statistics.package_statistics, ['arm64', '--force=true'])
        assert result.exit_code == 1
        assert "Invalid contents File format! Table header(FILE LOCATION) not found" in result.output
