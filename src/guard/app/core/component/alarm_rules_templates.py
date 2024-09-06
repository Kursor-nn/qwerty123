alert_template = """
{
    "uid": "{USER-ALERT-RULE-ID}",
    "title": "{USER-ALERT-TITLE-ID}",
    "condition": "B",
    "folderUID": "cdwyfawljvnk0d",
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
        "receiver": "{USER-NOTIFICAITON-ID}"
    }
}
"""
