from app.domains.user_profile.application.port.user_profile_repository_port import UserProfileRepositoryPort
from app.domains.user_profile.application.response.user_profile_response import (
    UserProfileResponse,
    InteractionHistoryResponse,
    LikeHistoryItem,
)
from app.domains.user_profile.domain.entity.user_interaction import InteractionType
from app.domains.user_profile.domain.entity.user_profile import UserProfile


class GetUserProfileUseCase:
    def __init__(self, repository: UserProfileRepositoryPort):
        self._repository = repository

    def execute(self, account_id: int) -> UserProfileResponse:
        profile = self._repository.find_by_account_id(account_id)
        if profile is None:
            profile = UserProfile(account_id=account_id)

        interactions = self._repository.find_interactions_by_account_id(account_id)

        like_map: dict[str, int] = {}
        comments: list[str] = []

        for interaction in interactions:
            if interaction.interaction_type == InteractionType.LIKE:
                like_map[interaction.symbol] = like_map.get(interaction.symbol, 0) + interaction.count
            elif interaction.interaction_type == InteractionType.COMMENT and interaction.content:
                comments.append(interaction.content)

        likes = [LikeHistoryItem(symbol=symbol, count=count) for symbol, count in like_map.items()]

        return UserProfileResponse(
            account_id=profile.account_id,
            preferred_stocks=profile.preferred_stocks,
            interaction_history=InteractionHistoryResponse(likes=likes, comments=comments),
            interests_text=profile.interests_text,
        )
