from core.component.profile_info_component import get_profile_info
from loguru import logger

from dto.ProfileDto import ProfileInfo

mapper = {
    "Answer topic filters": "topic_detector",
    "Request topic filters": "topic_detector",
    "Answer toxic filters": "general_filter",
    "Request toxic filters": "general_filter",
    "Recomendation mode": "recomendation_mode",
}


def collect_filters(user: str) -> ([], []):
    profile_info: ProfileInfo = get_profile_info(user)
    input = [mapper[i.name] for i in profile_info.features if "Request" in i.name and i.enabled]
    output = [mapper[i.name] for i in profile_info.features if "Answer" in i.name and i.enabled]
    modes = [i.enabled for i in profile_info.features if "filter_mode" in i.type]

    logger.info(f"filters {user} : {(modes[0] if len(modes) == 1 else None, input, output)}")

    return (modes[0], input, output)