class AdCondition:
    """Возможные состояния товара."""

    NEW = 'new'
    USED = 'used'


AD_CONDITION_CHOICES = (
    (AdCondition.NEW, 'новый'),
    (AdCondition.USED, 'б/у'),
)


class Status:
    """Возможные статусы для предложения обмена."""

    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'


PROPOSAL_STATUS_CHOICES = (
    (Status.PENDING, 'ожидает'),
    (Status.APPROVED, 'принята'),
    (Status.REJECTED, 'отклонена'),
)
