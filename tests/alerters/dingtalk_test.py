import json

import mock
import pytest
from requests import RequestException
from requests.auth import HTTPProxyAuth

from elastalert.alerters.dingtalk import DingTalkAlerter
from elastalert.loaders import FileRulesLoader
from elastalert.util import EAException


def test_dingtalk_text():
    rule = {
        'name': 'Test DingTalk Rule',
        'type': 'any',
        'dingtalk_access_token': 'xxxxxxx',
        'dingtalk_msgtype': 'text',
        'alert': [],
        'alert_subject': 'Test DingTalk'
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = DingTalkAlerter(rule)
    match = {
        '@timestamp': '2021-01-01T00:00:00',
        'somefield': 'foobarbaz'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        'msgtype': 'text',
        'text': {'content': 'Test DingTalk Rule\n\n@timestamp: 2021-01-01T00:00:00\nsomefield: foobarbaz\n'}
    }

    mock_post_request.assert_called_once_with(
        'https://oapi.dingtalk.com/robot/send?access_token=xxxxxxx',
        data=mock.ANY,
        headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json;charset=utf-8'
        },
        proxies=None,
        auth=None
    )

    actual_data = json.loads(mock_post_request.call_args_list[0][1]['data'])
    assert expected_data == actual_data


def test_dingtalk_markdown():
    rule = {
        'name': 'Test DingTalk Rule',
        'type': 'any',
        'dingtalk_access_token': 'xxxxxxx',
        'dingtalk_msgtype': 'markdown',
        'alert': [],
        'alert_subject': 'Test DingTalk'
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = DingTalkAlerter(rule)
    match = {
        '@timestamp': '2021-01-01T00:00:00',
        'somefield': 'foobarbaz'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        'msgtype': 'markdown',
        'markdown': {
            'title': 'Test DingTalk',
            'text': 'Test DingTalk Rule\n\n@timestamp: 2021-01-01T00:00:00\nsomefield: foobarbaz\n'
        }
    }

    mock_post_request.assert_called_once_with(
        'https://oapi.dingtalk.com/robot/send?access_token=xxxxxxx',
        data=mock.ANY,
        headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json;charset=utf-8'
        },
        proxies=None,
        auth=None
    )

    actual_data = json.loads(mock_post_request.call_args_list[0][1]['data'])
    assert expected_data == actual_data


def test_dingtalk_single_action_card():
    rule = {
        'name': 'Test DingTalk Rule',
        'type': 'any',
        'dingtalk_access_token': 'xxxxxxx',
        'dingtalk_msgtype': 'single_action_card',
        'dingtalk_single_title': 'elastalert',
        'dingtalk_single_url': 'http://xxxxx2',
        'alert': [],
        'alert_subject': 'Test DingTalk'
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = DingTalkAlerter(rule)
    match = {
        '@timestamp': '2021-01-01T00:00:00',
        'somefield': 'foobarbaz'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        'msgtype': 'actionCard',
        'actionCard': {
            'title': 'Test DingTalk',
            'text': 'Test DingTalk Rule\n\n@timestamp: 2021-01-01T00:00:00\nsomefield: foobarbaz\n',
            'singleTitle': rule['dingtalk_single_title'],
            'singleURL': rule['dingtalk_single_url']
        }
    }

    mock_post_request.assert_called_once_with(
        'https://oapi.dingtalk.com/robot/send?access_token=xxxxxxx',
        data=mock.ANY,
        headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json;charset=utf-8'
        },
        proxies=None,
        auth=None
    )

    actual_data = json.loads(mock_post_request.call_args_list[0][1]['data'])
    assert expected_data == actual_data


def test_dingtalk_action_card():
    rule = {
        'name': 'Test DingTalk Rule',
        'type': 'any',
        'dingtalk_access_token': 'xxxxxxx',
        'dingtalk_msgtype': 'action_card',
        'dingtalk_single_title': 'elastalert',
        'dingtalk_single_url': 'http://xxxxx2',
        'dingtalk_btn_orientation': '1',
        'dingtalk_btns': [
            {
                'title': 'test1',
                'actionURL': 'https://xxxxx0/'
            },
            {
                'title': 'test2',
                'actionURL': 'https://xxxxx1/'
            }
        ],
        'alert': [],
        'alert_subject': 'Test DingTalk'
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = DingTalkAlerter(rule)
    match = {
        '@timestamp': '2021-01-01T00:00:00',
        'somefield': 'foobarbaz'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        'msgtype': 'actionCard',
        'actionCard': {
            'title': 'Test DingTalk',
            'text': 'Test DingTalk Rule\n\n@timestamp: 2021-01-01T00:00:00\nsomefield: foobarbaz\n',
            'btnOrientation': rule['dingtalk_btn_orientation'],
            'btns': rule['dingtalk_btns']
        }
    }

    mock_post_request.assert_called_once_with(
        'https://oapi.dingtalk.com/robot/send?access_token=xxxxxxx',
        data=mock.ANY,
        headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json;charset=utf-8'
        },
        proxies=None,
        auth=None
    )

    actual_data = json.loads(mock_post_request.call_args_list[0][1]['data'])
    assert expected_data == actual_data


def test_dingtalk_proxy():
    rule = {
        'name': 'Test DingTalk Rule',
        'type': 'any',
        'dingtalk_access_token': 'xxxxxxx',
        'dingtalk_msgtype': 'action_card',
        'dingtalk_single_title': 'elastalert',
        'dingtalk_single_url': 'http://xxxxx2',
        'dingtalk_btn_orientation': '1',
        'dingtalk_btns': [
            {
                'title': 'test1',
                'actionURL': 'https://xxxxx0/'
            },
            {
                'title': 'test2',
                'actionURL': 'https://xxxxx1/'
            }
        ],
        'dingtalk_proxy': 'http://proxy.url',
        'dingtalk_proxy_login': 'admin',
        'dingtalk_proxy_pass': 'password',
        'alert': [],
        'alert_subject': 'Test DingTalk'
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = DingTalkAlerter(rule)
    match = {
        '@timestamp': '2021-01-01T00:00:00',
        'somefield': 'foobarbaz'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        'msgtype': 'actionCard',
        'actionCard': {
            'title': 'Test DingTalk',
            'text': 'Test DingTalk Rule\n\n@timestamp: 2021-01-01T00:00:00\nsomefield: foobarbaz\n',
            'btnOrientation': rule['dingtalk_btn_orientation'],
            'btns': rule['dingtalk_btns']
        }
    }

    mock_post_request.assert_called_once_with(
        'https://oapi.dingtalk.com/robot/send?access_token=xxxxxxx',
        data=mock.ANY,
        headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json;charset=utf-8'
        },
        proxies={'https': 'http://proxy.url'},
        auth=HTTPProxyAuth('admin', 'password')
    )

    actual_data = json.loads(mock_post_request.call_args_list[0][1]['data'])
    assert expected_data == actual_data


def test_dingtalk_ea_exception():
    try:
        rule = {
            'name': 'Test DingTalk Rule',
            'type': 'any',
            'dingtalk_access_token': 'xxxxxxx',
            'dingtalk_msgtype': 'action_card',
            'dingtalk_single_title': 'elastalert',
            'dingtalk_single_url': 'http://xxxxx2',
            'dingtalk_btn_orientation': '1',
            'dingtalk_btns': [
                {
                    'title': 'test1',
                    'actionURL': 'https://xxxxx0/'
                },
                {
                    'title': 'test2',
                    'actionURL': 'https://xxxxx1/'
                }
            ],
            'dingtalk_proxy': 'http://proxy.url',
            'dingtalk_proxy_login': 'admin',
            'dingtalk_proxy_pass': 'password',
            'alert': [],
            'alert_subject': 'Test DingTalk'
        }
        rules_loader = FileRulesLoader({})
        rules_loader.load_modules(rule)
        alert = DingTalkAlerter(rule)
        match = {
            '@timestamp': '2021-01-01T00:00:00',
            'somefield': 'foobarbaz'
        }
        mock_run = mock.MagicMock(side_effect=RequestException)
        with mock.patch('requests.post', mock_run), pytest.raises(RequestException):
            alert.alert([match])
    except EAException:
        assert True
