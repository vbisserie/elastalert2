import json

import mock
import pytest
from requests import RequestException

from elastalert.alerters.datadog import DatadogAlerter
from elastalert.loaders import FileRulesLoader
from elastalert.util import EAException


def test_datadog_alerter():
    rule = {
        'name': 'Test Datadog Event Alerter',
        'type': 'any',
        'datadog_api_key': 'test-api-key',
        'datadog_app_key': 'test-app-key',
        'alert': [],
        'alert_subject': 'Test Datadog Event Alert'
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = DatadogAlerter(rule)
    match = {
        '@timestamp': '2021-01-01T00:00:00',
        'name': 'datadog-test-name'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        'title': rule['alert_subject'],
        'text': "Test Datadog Event Alerter\n\n@timestamp: 2021-01-01T00:00:00\nname: datadog-test-name\n"
    }
    mock_post_request.assert_called_once_with(
        "https://api.datadoghq.com/api/v1/events",
        data=mock.ANY,
        headers={
            'Content-Type': 'application/json',
            'DD-API-KEY': rule['datadog_api_key'],
            'DD-APPLICATION-KEY': rule['datadog_app_key']
        }
    )
    actual_data = json.loads(mock_post_request.call_args_list[0][1]['data'])
    assert expected_data == actual_data


def test_datadog_alerterea_exception():
    try:
        rule = {
            'name': 'Test Datadog Event Alerter',
            'type': 'any',
            'datadog_api_key': 'test-api-key',
            'datadog_app_key': 'test-app-key',
            'alert': [],
            'alert_subject': 'Test Datadog Event Alert'
        }
        rules_loader = FileRulesLoader({})
        rules_loader.load_modules(rule)
        alert = DatadogAlerter(rule)
        match = {
            '@timestamp': '2021-01-01T00:00:00',
            'name': 'datadog-test-name'
        }
        mock_run = mock.MagicMock(side_effect=RequestException)
        with mock.patch('requests.post', mock_run), pytest.raises(RequestException):
            alert.alert([match])
    except EAException:
        assert True
