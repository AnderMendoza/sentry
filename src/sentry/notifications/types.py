from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from sentry.services.hybrid_cloud import ValueEqualityEnum

"""
TODO(postgres): We've encoded these enums as integers to facilitate
communication with the DB. We'd prefer to encode them as strings to facilitate
communication with the API and plan to do so as soon as we use native enums in
Postgres. In the meantime each enum has an adjacent object that maps the
integers to their string values.
"""


def get_notification_setting_type_name(value: int | NotificationSettingTypes) -> Optional[str]:
    return NOTIFICATION_SETTING_TYPES.get(NotificationSettingTypes(value))


def get_notification_setting_value_name(value: int) -> Optional[str]:
    return NOTIFICATION_SETTING_OPTION_VALUES.get(NotificationSettingOptionValues(value))


def get_notification_scope_name(value: int) -> Optional[str]:
    return NOTIFICATION_SCOPE_TYPE.get(NotificationScopeType(value))


class NotificationSettingTypes(ValueEqualityEnum):
    """
    Each of these categories of Notification settings has at least an option for
    "on" or "off". Workflow also includes SUBSCRIBE_ONLY and Deploy also
    includes COMMITTED_ONLY and both of these values are described below.
    """

    # Control all notification types. Currently unused.
    DEFAULT = 0

    # When Sentry sees there is a new code deploy.
    DEPLOY = 10

    # When Sentry sees and issue that triggers an Alert Rule.
    ISSUE_ALERTS = 20

    # Notifications for changes in assignment, resolution, comments, etc.
    WORKFLOW = 30

    # Notification when an issue happens shortly after your release. This notification type is no longer supported.
    ACTIVE_RELEASE = 31

    # Notifications that require approval like a request to invite a member
    APPROVAL = 40

    # Notifications about quotas
    QUOTA = 50

    # Sub category of quotas for each event category
    QUOTA_ERRORS = 51
    QUOTA_TRANSACTIONS = 52
    QUOTA_ATTACHMENTS = 53
    QUOTA_REPLAYS = 56

    # Sub category of quotas for warnings before hitting the actual limit
    QUOTA_WARNINGS = 54

    # Sub category of quotas for spend allocation notifications
    QUOTA_SPEND_ALLOCATIONS = 55

    # Notifications about spikes
    SPIKE_PROTECTION = 60

    # Nudge notifications
    MISSING_MEMBERS = 70

    # new for settings v2 but only with helper functions
    # This value shouldn't be stored in the DB
    REPORTS = -1


class NotificationSettingEnum(ValueEqualityEnum):
    DEFAULT = "default"
    DEPLOY = "deploy"
    ISSUE_ALERTS = "alerts"
    WORKFLOW = "workflow"
    ACTIVE_RELEASE = "activeRelease"
    APPROVAL = "approval"
    QUOTA = "quota"
    QUOTA_ERRORS = "quotaErrors"
    QUOTA_TRANSACTIONS = "quotaTransactions"
    QUOTA_ATTACHMENTS = "quotaAttachments"
    QUOTA_REPLAYS = "quotaReplays"
    QUOTA_WARNINGS = "quotaWarnings"
    QUOTA_SPEND_ALLOCATIONS = "quotaSpendAllocations"
    SPIKE_PROTECTION = "spikeProtection"
    MISSING_MEMBERS = "missingMembers"
    REPORTS = "reports"


# TODO(Steve): clean up after we finish migrating to settings 2.0
NOTIFICATION_SETTING_TYPES = {
    NotificationSettingTypes.DEFAULT: NotificationSettingEnum.DEFAULT.value,
    NotificationSettingTypes.DEPLOY: NotificationSettingEnum.DEPLOY.value,
    NotificationSettingTypes.ISSUE_ALERTS: NotificationSettingEnum.ISSUE_ALERTS.value,
    NotificationSettingTypes.WORKFLOW: NotificationSettingEnum.WORKFLOW.value,
    NotificationSettingTypes.ACTIVE_RELEASE: NotificationSettingEnum.ACTIVE_RELEASE.value,
    NotificationSettingTypes.APPROVAL: NotificationSettingEnum.APPROVAL.value,
    NotificationSettingTypes.QUOTA: NotificationSettingEnum.QUOTA.value,
    NotificationSettingTypes.QUOTA_ERRORS: NotificationSettingEnum.QUOTA_ERRORS.value,
    NotificationSettingTypes.QUOTA_TRANSACTIONS: NotificationSettingEnum.QUOTA_TRANSACTIONS.value,
    NotificationSettingTypes.QUOTA_ATTACHMENTS: NotificationSettingEnum.QUOTA_ATTACHMENTS.value,
    NotificationSettingTypes.QUOTA_REPLAYS: NotificationSettingEnum.QUOTA_REPLAYS.value,
    NotificationSettingTypes.QUOTA_WARNINGS: NotificationSettingEnum.QUOTA_WARNINGS.value,
    NotificationSettingTypes.QUOTA_SPEND_ALLOCATIONS: NotificationSettingEnum.QUOTA_SPEND_ALLOCATIONS.value,
    NotificationSettingTypes.SPIKE_PROTECTION: NotificationSettingEnum.SPIKE_PROTECTION.value,
    NotificationSettingTypes.REPORTS: NotificationSettingEnum.REPORTS.value,
}


class NotificationSettingOptionValues(ValueEqualityEnum):
    """
    An empty row in the DB should be represented as
    NotificationSettingOptionValues.DEFAULT.
    """

    # Defer to a setting one level up.
    DEFAULT = 0

    # Mute this kind of notification.
    NEVER = 10

    # Un-mute this kind of notification.
    ALWAYS = 20

    # Workflow only. Only send notifications about Issues that the target has
    # explicitly or implicitly opted-into.
    SUBSCRIBE_ONLY = 30

    # Deploy only. Only send notifications when the set of changes in the deploy
    # included a commit authored by the target.
    COMMITTED_ONLY = 40


class NotificationSettingsOptionEnum(ValueEqualityEnum):
    DEFAULT = "default"
    NEVER = "never"
    ALWAYS = "always"
    SUBSCRIBE_ONLY = "subscribe_only"
    COMMITTED_ONLY = "committed_only"


# TODO(Steve): clean up after we finish migrating to settings 2.0
NOTIFICATION_SETTING_OPTION_VALUES = {
    NotificationSettingOptionValues.DEFAULT: NotificationSettingsOptionEnum.DEFAULT.value,
    NotificationSettingOptionValues.NEVER: NotificationSettingsOptionEnum.NEVER.value,
    NotificationSettingOptionValues.ALWAYS: NotificationSettingsOptionEnum.ALWAYS.value,
    NotificationSettingOptionValues.SUBSCRIBE_ONLY: NotificationSettingsOptionEnum.SUBSCRIBE_ONLY.value,
    NotificationSettingOptionValues.COMMITTED_ONLY: NotificationSettingsOptionEnum.COMMITTED_ONLY.value,
}

# default is not a choice anymore, we just delete the row if we want to the default
NOTIFICATION_SETTING_V2_CHOICES = [
    NotificationSettingsOptionEnum.ALWAYS.value,
    NotificationSettingsOptionEnum.NEVER.value,
    NotificationSettingsOptionEnum.SUBSCRIBE_ONLY.value,
    NotificationSettingsOptionEnum.COMMITTED_ONLY.value,
]


class NotificationScopeEnum(ValueEqualityEnum):
    USER = "user"
    ORGANIZATION = "organization"
    PROJECT = "project"
    TEAM = "team"


class NotificationScopeType(ValueEqualityEnum):
    USER = 0
    ORGANIZATION = 10
    PROJECT = 20
    TEAM = 30


# TODO(Steve): clean up after we finish migrating to settings 2.0
NOTIFICATION_SCOPE_TYPE = {
    NotificationScopeType.USER: NotificationScopeEnum.USER.value,
    NotificationScopeType.ORGANIZATION: NotificationScopeEnum.ORGANIZATION.value,
    NotificationScopeType.PROJECT: NotificationScopeEnum.PROJECT.value,
    NotificationScopeType.TEAM: NotificationScopeEnum.TEAM.value,
}


class FineTuningAPIKey(Enum):
    ALERTS = "alerts"
    APPROVAL = "approval"
    DEPLOY = "deploy"
    EMAIL = "email"
    QUOTA = "quota"
    REPORTS = "reports"
    WORKFLOW = "workflow"
    SPIKE_PROTECTION = "spikeProtection"


class UserOptionsSettingsKey(Enum):
    DEPLOY = "deployNotifications"
    SELF_ACTIVITY = "personalActivityNotifications"
    SELF_ASSIGN = "selfAssignOnResolve"
    SUBSCRIBE_BY_DEFAULT = "subscribeByDefault"
    WORKFLOW = "workflowNotifications"
    ACTIVE_RELEASE = "activeReleaseNotifications"
    APPROVAL = "approvalNotifications"
    QUOTA = "quotaNotifications"
    SPIKE_PROTECTION = "spikeProtectionNotifications"


VALID_VALUES_FOR_KEY = {
    NotificationSettingTypes.APPROVAL: {
        NotificationSettingOptionValues.ALWAYS,
        NotificationSettingOptionValues.NEVER,
    },
    NotificationSettingTypes.DEPLOY: {
        NotificationSettingOptionValues.ALWAYS,
        NotificationSettingOptionValues.COMMITTED_ONLY,
        NotificationSettingOptionValues.NEVER,
    },
    NotificationSettingTypes.ISSUE_ALERTS: {
        NotificationSettingOptionValues.ALWAYS,
        NotificationSettingOptionValues.NEVER,
    },
    NotificationSettingTypes.QUOTA: {
        NotificationSettingOptionValues.ALWAYS,
        NotificationSettingOptionValues.NEVER,
    },
    NotificationSettingTypes.QUOTA_ERRORS: {
        NotificationSettingOptionValues.ALWAYS,
        NotificationSettingOptionValues.NEVER,
    },
    NotificationSettingTypes.QUOTA_TRANSACTIONS: {
        NotificationSettingOptionValues.ALWAYS,
        NotificationSettingOptionValues.NEVER,
    },
    NotificationSettingTypes.QUOTA_ATTACHMENTS: {
        NotificationSettingOptionValues.ALWAYS,
        NotificationSettingOptionValues.NEVER,
    },
    NotificationSettingTypes.QUOTA_REPLAYS: {
        NotificationSettingOptionValues.ALWAYS,
        NotificationSettingOptionValues.NEVER,
    },
    NotificationSettingTypes.QUOTA_WARNINGS: {
        NotificationSettingOptionValues.ALWAYS,
        NotificationSettingOptionValues.NEVER,
    },
    NotificationSettingTypes.QUOTA_SPEND_ALLOCATIONS: {
        NotificationSettingOptionValues.ALWAYS,
        NotificationSettingOptionValues.NEVER,
    },
    NotificationSettingTypes.WORKFLOW: {
        NotificationSettingOptionValues.ALWAYS,
        NotificationSettingOptionValues.SUBSCRIBE_ONLY,
        NotificationSettingOptionValues.NEVER,
    },
    NotificationSettingTypes.SPIKE_PROTECTION: {
        NotificationSettingOptionValues.ALWAYS,
        NotificationSettingOptionValues.NEVER,
    },
}

VALID_VALUES_FOR_KEY_V2 = {
    **VALID_VALUES_FOR_KEY,
    NotificationSettingTypes.REPORTS: {
        NotificationSettingOptionValues.ALWAYS,
        NotificationSettingOptionValues.NEVER,
    },
}


class GroupSubscriptionReason:
    implicit = -1  # not for use as a persisted field value
    committed = -2  # not for use as a persisted field value
    processing_issue = -3  # not for use as a persisted field value

    unknown = 0
    comment = 1
    assigned = 2
    bookmark = 3
    status_change = 4
    deploy_setting = 5
    mentioned = 6
    team_mentioned = 7

    descriptions = {
        implicit: "have opted to receive updates for all issues within "
        "projects that you are a member of",
        committed: "were involved in a commit that is part of this release",
        processing_issue: "are subscribed to alerts for this project",
        comment: "have commented on this issue",
        assigned: "have been assigned to this issue",
        bookmark: "have bookmarked this issue",
        status_change: "have changed the resolution status of this issue",
        deploy_setting: "opted to receive all deploy notifications for this organization",
        mentioned: "have been mentioned in this issue",
        team_mentioned: "are a member of a team mentioned in this issue",
    }


SUBSCRIPTION_REASON_MAP = {
    GroupSubscriptionReason.comment: "commented",
    GroupSubscriptionReason.assigned: "assigned",
    GroupSubscriptionReason.bookmark: "bookmarked",
    GroupSubscriptionReason.status_change: "changed_status",
    GroupSubscriptionReason.mentioned: "mentioned",
}


class ActionTargetType(Enum):
    ISSUE_OWNERS = "IssueOwners"
    TEAM = "Team"
    MEMBER = "Member"


ACTION_CHOICES = [
    (ActionTargetType.ISSUE_OWNERS.value, "Issue Owners"),
    (ActionTargetType.TEAM.value, "Team"),
    (ActionTargetType.MEMBER.value, "Member"),
]


class FallthroughChoiceType(Enum):
    ALL_MEMBERS = "AllMembers"
    ACTIVE_MEMBERS = "ActiveMembers"
    NO_ONE = "NoOne"


FALLTHROUGH_CHOICES = [
    (FallthroughChoiceType.ACTIVE_MEMBERS.value, "Recently Active Members"),
    (FallthroughChoiceType.ALL_MEMBERS.value, "All Project Members"),
    (FallthroughChoiceType.NO_ONE.value, "No One"),
]


class AssigneeTargetType(Enum):
    UNASSIGNED = "Unassigned"
    TEAM = "Team"
    MEMBER = "Member"


ASSIGNEE_CHOICES = [
    (AssigneeTargetType.UNASSIGNED.value, "Unassigned"),
    (AssigneeTargetType.TEAM.value, "Team"),
    (AssigneeTargetType.MEMBER.value, "Member"),
]


@dataclass
class GroupSubscriptionStatus:
    is_disabled: bool
    is_active: bool
    has_only_inactive_subscriptions: bool


@dataclass
class UnsubscribeContext:
    resource_id: int
    key: str
    referrer: str | None = None
