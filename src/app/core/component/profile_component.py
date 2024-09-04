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
                (coalesce(uf.enabled, True) and f.enabled) as enabled
            from user_features uf 
            right join (select {user.id} as user_id, * from features) f on f.id = uf.feature_type_id and f.user_id = uf.user_id
    """
    results = session.execute(text(query)).fetchall()
    return [UserFeatureData(feature_type_id=value[0], name=value[1], type=value[2], enabled=value[3]) for value in results]


def toggle_feature(login, feature_id, value, session: Session = get_session()):
    user = get_user_by_login(login, session=session)

    current_state = session.query(UserFeaturesConfig) \
        .where((UserFeaturesConfig.feature_type_id == feature_id) & (UserFeaturesConfig.user_id == user.id)) \
        .one_or_none()

    if current_state:
        session.query(UserFeaturesConfig) \
            .where((UserFeaturesConfig.feature_type_id == feature_id) & (UserFeaturesConfig.user_id == user.id)) \
            .update({"enabled": value})
    else:
        session.add(
            UserFeaturesConfig(user_id=user.id, enabled=value, feature_type_id=feature_id)
        )

    session.commit()
