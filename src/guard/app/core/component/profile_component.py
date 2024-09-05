from typing import Union

from sqlalchemy import text
from sqlmodel import Session

from core.component.user_component import get_user_by_login
from core.data.UserFeatureData import UserFeatureData
from core.database.database import get_session
from core.models.model import UserFeaturesConfig


def get_features(login: str, session: Session = get_session()) -> list[UserFeatureData]:
    user = get_user_by_login(login)
    query = f"""
            select 
                COALESCE(feature_type_id, f.id) as feature_type_id,
                "name" as name,
                "type" as type,
                (coalesce(uf.enabled, True) and f.enabled) as enabled,
                config
            from user_features uf 
            right join (select {user.id} as user_id, * from features) f on f.id = uf.feature_type_id and f.user_id = uf.user_id
    """
    results = session.execute(text(query)).fetchall()
    return [UserFeatureData(feature_type_id=value[0], name=value[1], type=value[2], enabled=value[3], config=value[4]) for value in results]


def get_feature_by_id(login: str, feature_type_id: str, session: Session = get_session()) -> Union[UserFeatureData, None]:
    features = get_features(login, session)
    temp = [i for i in features if i.feature_type_id == feature_type_id]
    if len(temp) >= 0:
        return temp[0]
    return None


def set_value_to(login, feature_id, field: str, value: str, session: Session = get_session()):
    user = get_user_by_login(login, session=session)

    current_state = session.query(UserFeaturesConfig) \
        .where((UserFeaturesConfig.feature_type_id == feature_id) & (UserFeaturesConfig.user_id == user.id)) \
        .one_or_none()

    if current_state:
        session.query(UserFeaturesConfig) \
            .where((UserFeaturesConfig.feature_type_id == feature_id) & (UserFeaturesConfig.user_id == user.id)) \
            .update({field: value})
    else:
        data = {
            "user_id": user.id,
            field: value,
            "feature_type_id": feature_id,
            "enabled": False
        }
        session.add(
            UserFeaturesConfig(**data)
        )

    session.commit()


def set_config_to(login, feature_id, value: str, session: Session = get_session()):
    set_value_to(login, feature_id, "config", value, session)


def toggle_feature(login, feature_id, value, session: Session = get_session()):
    set_value_to(login, feature_id, "enabled", value, session)
