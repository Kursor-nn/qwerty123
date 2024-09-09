from grafana_api.alerting_provisioning import AlertingProvisioning
from grafana_api.dashboard import Dashboard
from grafana_api.model import APIModel, AlertRule, AlertQuery, AlertRuleQueryModel, AlertRuleQueryModelCondition


def __create_alert_rule(uid: str, title: str) -> AlertRule:
    alert_rule_query_model_condition: AlertRuleQueryModelCondition = (
        AlertRuleQueryModelCondition([20], "gt", "and", ["A"], [], "lost", "query")
    )

    alert_rule_query_model: AlertRuleQueryModel = AlertRuleQueryModel(
        [alert_rule_query_model_condition],
        {"type": "__expr__", "uid": "-100"},
        "",
        False,
        1000,
        43200,
        "A",
        "classic_conditions",
    )

    alert_query: AlertQuery = AlertQuery(
        "PBFA97CFB590B2093", alert_rule_query_model, "", "A", 600, 0
    )
    return AlertRule(
        "B",
        [alert_query],
        "Alerting",
        "cdx02ka6znn5se",
        "NoData",
        4,
        "General",
        title,
        uid,
        "5m",
    )


if __name__ == "__main__":
    model: APIModel = APIModel(host="http://localhost:3000", token="glsa_dSjUgivoAnnefXfX7exrlnBEe86Jde7j_77f253e4")

    dashboard: Dashboard = Dashboard(model)
    alerting = AlertingProvisioning(model)

    # result = alerting.add_alert_rule(
    #    __create_alert_rule("asdqweqwe", "asasdasddasd")
    # )

    # result = alerting.get_alert_rule("bdx06lpdf3ugwd")

    # alerting.create.add_alert_rule(AlertRule(**result))
    # alerting.add_alert_rule()
