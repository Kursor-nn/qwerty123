#
# Think how to fix this stupid bullshit
#

def build_alarm_rule_request(rule_id: str, title_id: str, folder_id: str, client_id: str, notification_id: str):
    alert_template = """
    {
    "uid": "{USER-ALERT-RULE-ID}",
        "title": "{USER-ALERT-TITLE-}",
        "condition": "B",
        "folderUID": "{FOLDER_UID}",
        "data": [
            {
    "refId": "A",
                "relativeTimeRange": {
    "from": 600,
                    "to": 0
                },
                "datasourceUid": "PBFA97CFB590B2093",
                "model": {
    "disableTextWrap": false,
                    "editorMode": "builder",
                    "expr": "count_over_time(input_toxic_text_total{toxic_client_id=\\"{CLIENT_ID}\\"}[1m])",
                    "fullMetaSearch": false,
                    "includeNullMetadata": true,
                    "instant": true,
                    "intervalMs": 1000,
                    "legendFormat": "__auto",
                    "maxDataPoints": 43200,
                    "range": false,
                    "refId": "A",
                    "useBackend": false
                }
            },
            {
    "refId": "B",
                "relativeTimeRange": {
    "from": 0,
                    "to": 0
                },
                "datasourceUid": "__expr__",
                "model": {
    "conditions": [
                        {
    "evaluator": {
    "params": [
                                    20,
                                    0
                                ],
                                "type": "gt"
                            },
                            "operator": {
    "type": "and"
                            },
                            "query": {
    "params": []
                            },
                            "reducer": {
    "params": [],
                                "type": "avg"
                            },
                            "type": "query"
                        }
                    ],
                    "datasource": {
    "name": "Expression",
                        "type": "__expr__",
                        "uid": "__expr__"
                    },
                    "expression": "A",
                    "intervalMs": 1000,
                    "maxDataPoints": 43200,
                    "refId": "B",
                    "type": "threshold"
                }
            }
        ],
        "noDataState": "NoData",
        "execErrState": "Error",
        "for": "1m",
        "annotations": {
    "description": "",
            "runbook_url": "",
            "summary": ""
        },
        "labels": {
    "": ""
        },
        "isPaused": false,
        "notification_settings": {
    "receiver": "{USER-NOTIFICATION-ID}"
        }
    }
    """

    request = alert_template.replace("{USER-ALERT-RULE-ID}", rule_id).replace("{USER-ALERT-TITLE-ID}", title_id).replace(
        "{USER-NOTIFICATION-ID}", notification_id).replace("{CLIENT_ID}", client_id).replace("{FOLDER_UID}", folder_id)

    return request
