import json

import mock
import pytest
from requests import RequestException

from elastalert.alerters.pagerduty import PagerDutyAlerter
from elastalert.loaders import FileRulesLoader
from elastalert.util import EAException


def test_pagerduty_alerter():
    rule = {
        'name': 'Test PD Rule',
        'type': 'any',
        'pagerduty_service_key': 'magicalbadgers',
        'pagerduty_client_name': 'ponies inc.',
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = PagerDutyAlerter(rule)
    match = {
        '@timestamp': '2017-01-01T00:00:00',
        'somefield': 'foobarbaz'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])
    expected_data = {
        'client': 'ponies inc.',
        'description': 'Test PD Rule',
        'details': {
            'information': 'Test PD Rule\n\n@timestamp: 2017-01-01T00:00:00\nsomefield: foobarbaz\n'
        },
        'event_type': 'trigger',
        'incident_key': '',
        'service_key': 'magicalbadgers',
    }
    mock_post_request.assert_called_once_with('https://events.pagerduty.com/generic/2010-04-15/create_event.json',
                                              data=mock.ANY, headers={'content-type': 'application/json'}, proxies=None)
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])


def test_pagerduty_alerter_v2():
    rule = {
        'name': 'Test PD Rule',
        'type': 'any',
        'pagerduty_service_key': 'magicalbadgers',
        'pagerduty_client_name': 'ponies inc.',
        'pagerduty_api_version': 'v2',
        'pagerduty_v2_payload_class': 'ping failure',
        'pagerduty_v2_payload_component': 'mysql',
        'pagerduty_v2_payload_group': 'app-stack',
        'pagerduty_v2_payload_severity': 'error',
        'pagerduty_v2_payload_source': 'mysql.host.name',
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = PagerDutyAlerter(rule)
    match = {
        '@timestamp': '2017-01-01T00:00:00',
        'somefield': 'foobarbaz'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])
    expected_data = {
        'client': 'ponies inc.',
        'payload': {
            'class': 'ping failure',
            'component': 'mysql',
            'group': 'app-stack',
            'severity': 'error',
            'source': 'mysql.host.name',
            'summary': 'Test PD Rule',
            'custom_details': {
                'information': 'Test PD Rule\n\n@timestamp: 2017-01-01T00:00:00\nsomefield: foobarbaz\n'
            },
            'timestamp': '2017-01-01T00:00:00'
        },
        'event_action': 'trigger',
        'dedup_key': '',
        'routing_key': 'magicalbadgers',
    }
    mock_post_request.assert_called_once_with('https://events.pagerduty.com/v2/enqueue',
                                              data=mock.ANY, headers={'content-type': 'application/json'}, proxies=None)
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])


def test_pagerduty_alerter_v2_payload_class_args():
    rule = {
        'name': 'Test PD Rule',
        'type': 'any',
        'pagerduty_service_key': 'magicalbadgers',
        'pagerduty_client_name': 'ponies inc.',
        'pagerduty_api_version': 'v2',
        'pagerduty_v2_payload_class': 'somefield',
        'pagerduty_v2_payload_class_args': ['@timestamp', 'somefield'],
        'pagerduty_v2_payload_component': 'mysql',
        'pagerduty_v2_payload_group': 'app-stack',
        'pagerduty_v2_payload_severity': 'error',
        'pagerduty_v2_payload_source': 'mysql.host.name',
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = PagerDutyAlerter(rule)
    match = {
        '@timestamp': '2017-01-01T00:00:00',
        'somefield': 'foobarbaz'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])
    expected_data = {
        'client': 'ponies inc.',
        'payload': {
            'class': 'somefield',
            'component': 'mysql',
            'group': 'app-stack',
            'severity': 'error',
            'source': 'mysql.host.name',
            'summary': 'Test PD Rule',
            'custom_details': {
                'information': 'Test PD Rule\n\n@timestamp: 2017-01-01T00:00:00\nsomefield: foobarbaz\n'
            },
            'timestamp': '2017-01-01T00:00:00'
        },
        'event_action': 'trigger',
        'dedup_key': '',
        'routing_key': 'magicalbadgers',
    }
    mock_post_request.assert_called_once_with('https://events.pagerduty.com/v2/enqueue',
                                              data=mock.ANY, headers={'content-type': 'application/json'}, proxies=None)
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])


def test_pagerduty_alerter_v2_payload_component_args():
    rule = {
        'name': 'Test PD Rule',
        'type': 'any',
        'pagerduty_service_key': 'magicalbadgers',
        'pagerduty_client_name': 'ponies inc.',
        'pagerduty_api_version': 'v2',
        'pagerduty_v2_payload_class': 'ping failure',
        'pagerduty_v2_payload_component': 'somefield',
        'pagerduty_v2_payload_component_args': ['@timestamp', 'somefield'],
        'pagerduty_v2_payload_group': 'app-stack',
        'pagerduty_v2_payload_severity': 'error',
        'pagerduty_v2_payload_source': 'mysql.host.name',
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = PagerDutyAlerter(rule)
    match = {
        '@timestamp': '2017-01-01T00:00:00',
        'somefield': 'foobarbaz'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])
    expected_data = {
        'client': 'ponies inc.',
        'payload': {
            'class': 'ping failure',
            'component': 'somefield',
            'group': 'app-stack',
            'severity': 'error',
            'source': 'mysql.host.name',
            'summary': 'Test PD Rule',
            'custom_details': {
                'information': 'Test PD Rule\n\n@timestamp: 2017-01-01T00:00:00\nsomefield: foobarbaz\n'
            },
            'timestamp': '2017-01-01T00:00:00'
        },
        'event_action': 'trigger',
        'dedup_key': '',
        'routing_key': 'magicalbadgers',
    }
    mock_post_request.assert_called_once_with('https://events.pagerduty.com/v2/enqueue',
                                              data=mock.ANY, headers={'content-type': 'application/json'}, proxies=None)
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])


def test_pagerduty_alerter_v2_payload_group_args():
    rule = {
        'name': 'Test PD Rule',
        'type': 'any',
        'pagerduty_service_key': 'magicalbadgers',
        'pagerduty_client_name': 'ponies inc.',
        'pagerduty_api_version': 'v2',
        'pagerduty_v2_payload_class': 'ping failure',
        'pagerduty_v2_payload_component': 'mysql',
        'pagerduty_v2_payload_group': 'somefield',
        'pagerduty_v2_payload_group_args': ['@timestamp', 'somefield'],
        'pagerduty_v2_payload_severity': 'error',
        'pagerduty_v2_payload_source': 'mysql.host.name',
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = PagerDutyAlerter(rule)
    match = {
        '@timestamp': '2017-01-01T00:00:00',
        'somefield': 'foobarbaz'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])
    expected_data = {
        'client': 'ponies inc.',
        'payload': {
            'class': 'ping failure',
            'component': 'mysql',
            'group': 'somefield',
            'severity': 'error',
            'source': 'mysql.host.name',
            'summary': 'Test PD Rule',
            'custom_details': {
                'information': 'Test PD Rule\n\n@timestamp: 2017-01-01T00:00:00\nsomefield: foobarbaz\n'
            },
            'timestamp': '2017-01-01T00:00:00'
        },
        'event_action': 'trigger',
        'dedup_key': '',
        'routing_key': 'magicalbadgers',
    }
    mock_post_request.assert_called_once_with('https://events.pagerduty.com/v2/enqueue',
                                              data=mock.ANY, headers={'content-type': 'application/json'}, proxies=None)
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])


def test_pagerduty_alerter_v2_payload_source_args():
    rule = {
        'name': 'Test PD Rule',
        'type': 'any',
        'pagerduty_service_key': 'magicalbadgers',
        'pagerduty_client_name': 'ponies inc.',
        'pagerduty_api_version': 'v2',
        'pagerduty_v2_payload_class': 'ping failure',
        'pagerduty_v2_payload_component': 'mysql',
        'pagerduty_v2_payload_group': 'app-stack',
        'pagerduty_v2_payload_severity': 'error',
        'pagerduty_v2_payload_source': 'somefield',
        'pagerduty_v2_payload_source_args': ['@timestamp', 'somefield'],
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = PagerDutyAlerter(rule)
    match = {
        '@timestamp': '2017-01-01T00:00:00',
        'somefield': 'foobarbaz'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])
    expected_data = {
        'client': 'ponies inc.',
        'payload': {
            'class': 'ping failure',
            'component': 'mysql',
            'group': 'app-stack',
            'severity': 'error',
            'source': 'somefield',
            'summary': 'Test PD Rule',
            'custom_details': {
                'information': 'Test PD Rule\n\n@timestamp: 2017-01-01T00:00:00\nsomefield: foobarbaz\n'
            },
            'timestamp': '2017-01-01T00:00:00'
        },
        'event_action': 'trigger',
        'dedup_key': '',
        'routing_key': 'magicalbadgers',
    }
    mock_post_request.assert_called_once_with('https://events.pagerduty.com/v2/enqueue',
                                              data=mock.ANY, headers={'content-type': 'application/json'}, proxies=None)
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])


def test_pagerduty_alerter_v2_payload_custom_details():
    rule = {
        'name': 'Test PD Rule',
        'type': 'any',
        'pagerduty_service_key': 'magicalbadgers',
        'pagerduty_client_name': 'ponies inc.',
        'pagerduty_api_version': 'v2',
        'pagerduty_v2_payload_class': 'ping failure',
        'pagerduty_v2_payload_component': 'mysql',
        'pagerduty_v2_payload_group': 'app-stack',
        'pagerduty_v2_payload_severity': 'error',
        'pagerduty_v2_payload_source': 'mysql.host.name',
        'pagerduty_v2_payload_custom_details': {'a': 'somefield', 'c': 'f'},
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = PagerDutyAlerter(rule)
    match = {
        '@timestamp': '2017-01-01T00:00:00',
        'somefield': 'foobarbaz'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])
    expected_data = {
        'client': 'ponies inc.',
        'payload': {
            'class': 'ping failure',
            'component': 'mysql',
            'group': 'app-stack',
            'severity': 'error',
            'source': 'mysql.host.name',
            'summary': 'Test PD Rule',
            'custom_details': {
                'a': 'foobarbaz',
                'c': None,
                'information': 'Test PD Rule\n\n@timestamp: 2017-01-01T00:00:00\nsomefield: foobarbaz\n'
            },
            'timestamp': '2017-01-01T00:00:00'
        },
        'event_action': 'trigger',
        'dedup_key': '',
        'routing_key': 'magicalbadgers',
    }
    mock_post_request.assert_called_once_with('https://events.pagerduty.com/v2/enqueue',
                                              data=mock.ANY, headers={'content-type': 'application/json'}, proxies=None)
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])


def test_pagerduty_alerter_v2_payload_include_all_info():
    rule = {
        'name': 'Test PD Rule',
        'type': 'any',
        'pagerduty_service_key': 'magicalbadgers',
        'pagerduty_client_name': 'ponies inc.',
        'pagerduty_api_version': 'v2',
        'pagerduty_v2_payload_class': 'ping failure',
        'pagerduty_v2_payload_component': 'mysql',
        'pagerduty_v2_payload_group': 'app-stack',
        'pagerduty_v2_payload_severity': 'error',
        'pagerduty_v2_payload_source': 'mysql.host.name',
        'pagerduty_v2_payload_include_all_info': False,
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = PagerDutyAlerter(rule)
    match = {
        '@timestamp': '2017-01-01T00:00:00',
        'somefield': 'foobarbaz'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])
    expected_data = {
        'client': 'ponies inc.',
        'payload': {
            'class': 'ping failure',
            'component': 'mysql',
            'group': 'app-stack',
            'severity': 'error',
            'source': 'mysql.host.name',
            'summary': 'Test PD Rule',
            'custom_details': {},
            'timestamp': '2017-01-01T00:00:00'
        },
        'event_action': 'trigger',
        'dedup_key': '',
        'routing_key': 'magicalbadgers',
    }
    mock_post_request.assert_called_once_with('https://events.pagerduty.com/v2/enqueue',
                                              data=mock.ANY, headers={'content-type': 'application/json'}, proxies=None)
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])


def test_pagerduty_alerter_custom_incident_key():
    rule = {
        'name': 'Test PD Rule',
        'type': 'any',
        'pagerduty_service_key': 'magicalbadgers',
        'pagerduty_client_name': 'ponies inc.',
        'pagerduty_incident_key': 'custom key',
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = PagerDutyAlerter(rule)
    match = {
        '@timestamp': '2017-01-01T00:00:00',
        'somefield': 'foobarbaz'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])
    expected_data = {
        'client': 'ponies inc.',
        'description': 'Test PD Rule',
        'details': {
            'information': 'Test PD Rule\n\n@timestamp: 2017-01-01T00:00:00\nsomefield: foobarbaz\n'
        },
        'event_type': 'trigger',
        'incident_key': 'custom key',
        'service_key': 'magicalbadgers',
    }
    mock_post_request.assert_called_once_with(alert.url, data=mock.ANY, headers={'content-type': 'application/json'}, proxies=None)
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])


def test_pagerduty_alerter_custom_incident_key_with_args():
    rule = {
        'name': 'Test PD Rule',
        'type': 'any',
        'pagerduty_service_key': 'magicalbadgers',
        'pagerduty_client_name': 'ponies inc.',
        'pagerduty_incident_key': 'custom {0}',
        'pagerduty_incident_key_args': ['somefield'],
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = PagerDutyAlerter(rule)
    match = {
        '@timestamp': '2017-01-01T00:00:00',
        'somefield': 'foobarbaz'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])
    expected_data = {
        'client': 'ponies inc.',
        'description': 'Test PD Rule',
        'details': {
            'information': 'Test PD Rule\n\n@timestamp: 2017-01-01T00:00:00\nsomefield: foobarbaz\n'
        },
        'event_type': 'trigger',
        'incident_key': 'custom foobarbaz',
        'service_key': 'magicalbadgers',
    }
    mock_post_request.assert_called_once_with(alert.url, data=mock.ANY, headers={'content-type': 'application/json'}, proxies=None)
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])


def test_pagerduty_alerter_custom_alert_subject():
    rule = {
        'name': 'Test PD Rule',
        'type': 'any',
        'alert_subject': 'Hungry kittens',
        'pagerduty_service_key': 'magicalbadgers',
        'pagerduty_client_name': 'ponies inc.',
        'pagerduty_incident_key': 'custom {0}',
        'pagerduty_incident_key_args': ['somefield'],
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = PagerDutyAlerter(rule)
    match = {
        '@timestamp': '2017-01-01T00:00:00',
        'somefield': 'foobarbaz'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])
    expected_data = {
        'client': 'ponies inc.',
        'description': 'Hungry kittens',
        'details': {
            'information': 'Test PD Rule\n\n@timestamp: 2017-01-01T00:00:00\nsomefield: foobarbaz\n'
        },
        'event_type': 'trigger',
        'incident_key': 'custom foobarbaz',
        'service_key': 'magicalbadgers',
    }
    mock_post_request.assert_called_once_with(alert.url, data=mock.ANY, headers={'content-type': 'application/json'}, proxies=None)
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])


def test_pagerduty_alerter_custom_alert_subject_with_args():
    rule = {
        'name': 'Test PD Rule',
        'type': 'any',
        'alert_subject': '{0} kittens',
        'alert_subject_args': ['somefield'],
        'pagerduty_service_key': 'magicalbadgers',
        'pagerduty_client_name': 'ponies inc.',
        'pagerduty_incident_key': 'custom {0}',
        'pagerduty_incident_key_args': ['someotherfield'],
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = PagerDutyAlerter(rule)
    match = {
        '@timestamp': '2017-01-01T00:00:00',
        'somefield': 'Stinky',
        'someotherfield': 'foobarbaz'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])
    expected_data = {
        'client': 'ponies inc.',
        'description': 'Stinky kittens',
        'details': {
            'information': 'Test PD Rule\n\n@timestamp: 2017-01-01T00:00:00\nsomefield: Stinky\nsomeotherfield: foobarbaz\n'
        },
        'event_type': 'trigger',
        'incident_key': 'custom foobarbaz',
        'service_key': 'magicalbadgers',
    }
    mock_post_request.assert_called_once_with(alert.url, data=mock.ANY, headers={'content-type': 'application/json'}, proxies=None)
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])


def test_pagerduty_alerter_custom_alert_subject_with_args_specifying_trigger():
    rule = {
        'name': 'Test PD Rule',
        'type': 'any',
        'alert_subject': '{0} kittens',
        'alert_subject_args': ['somefield'],
        'pagerduty_service_key': 'magicalbadgers',
        'pagerduty_event_type': 'trigger',
        'pagerduty_client_name': 'ponies inc.',
        'pagerduty_incident_key': 'custom {0}',
        'pagerduty_incident_key_args': ['someotherfield'],
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = PagerDutyAlerter(rule)
    match = {
        '@timestamp': '2017-01-01T00:00:00',
        'somefield': 'Stinkiest',
        'someotherfield': 'foobarbaz'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])
    expected_data = {
        'client': 'ponies inc.',
        'description': 'Stinkiest kittens',
        'details': {
            'information': 'Test PD Rule\n\n@timestamp: 2017-01-01T00:00:00\nsomefield: Stinkiest\nsomeotherfield: foobarbaz\n'
        },
        'event_type': 'trigger',
        'incident_key': 'custom foobarbaz',
        'service_key': 'magicalbadgers',
    }
    mock_post_request.assert_called_once_with(alert.url, data=mock.ANY, headers={'content-type': 'application/json'}, proxies=None)
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])


def test_pagerduty_alerter_proxy():
    rule = {
        'name': 'Test PD Rule',
        'type': 'any',
        'alert_subject': '{0} kittens',
        'alert_subject_args': ['somefield'],
        'pagerduty_service_key': 'magicalbadgers',
        'pagerduty_event_type': 'trigger',
        'pagerduty_client_name': 'ponies inc.',
        'pagerduty_incident_key': 'custom {0}',
        'pagerduty_incident_key_args': ['someotherfield'],
        'pagerduty_proxy': 'http://proxy.url',
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = PagerDutyAlerter(rule)
    match = {
        '@timestamp': '2017-01-01T00:00:00',
        'somefield': 'Stinkiest',
        'someotherfield': 'foobarbaz'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])
    expected_data = {
        'client': 'ponies inc.',
        'description': 'Stinkiest kittens',
        'details': {
            'information': 'Test PD Rule\n\n@timestamp: 2017-01-01T00:00:00\nsomefield: Stinkiest\nsomeotherfield: foobarbaz\n'
        },
        'event_type': 'trigger',
        'incident_key': 'custom foobarbaz',
        'service_key': 'magicalbadgers',
    }
    mock_post_request.assert_called_once_with(alert.url, data=mock.ANY, headers={'content-type': 'application/json'},
                                              proxies={'https': 'http://proxy.url'})
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])


def test_pagerduty_ea_exception():
    try:
        rule = {
            'name': 'Test PD Rule',
            'type': 'any',
            'alert_subject': '{0} kittens',
            'alert_subject_args': ['somefield'],
            'pagerduty_service_key': 'magicalbadgers',
            'pagerduty_event_type': 'trigger',
            'pagerduty_client_name': 'ponies inc.',
            'pagerduty_incident_key': 'custom {0}',
            'pagerduty_incident_key_args': ['someotherfield'],
            'pagerduty_proxy': 'http://proxy.url',
            'alert': []
        }
        rules_loader = FileRulesLoader({})
        rules_loader.load_modules(rule)
        alert = PagerDutyAlerter(rule)
        match = {
            '@timestamp': '2017-01-01T00:00:00',
            'somefield': 'Stinkiest',
            'someotherfield': 'foobarbaz'
        }
        mock_run = mock.MagicMock(side_effect=RequestException)
        with mock.patch('requests.post', mock_run), pytest.raises(RequestException):
            alert.alert([match])
    except EAException:
        assert True
