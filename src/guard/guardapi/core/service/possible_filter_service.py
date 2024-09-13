from core.component.profile_info_component import get_profile_info
from loguru import logger

from dto.ProfileDto import ProfileInfo

mapper = {
    "binary_filter": "general_filter",
    "multi_filter": "topic_detector",
    "filter_mode": "recomendation_mode",
}


def collect_filters(user: str) -> ([], []):
    profile_info: ProfileInfo = get_profile_info(user)
    input = [mapper[i.type] for i in profile_info.features if "request" in i.name and i.enabled]
    output = [mapper[i.type] for i in profile_info.features if "answer" in i.name and i.enabled]
    modes = [i.enabled for i in profile_info.features if "filter_mode" in i.type]

    logger.info(f"filters {user} : {(modes[0] if len(modes) == 1 else None, input, output)}")
    logger.info(f"filters {user} : {profile_info}")

    return (modes[0], input, output)
