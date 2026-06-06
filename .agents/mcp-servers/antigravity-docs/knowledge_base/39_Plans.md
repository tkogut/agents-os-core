# Plans
Source URL: https://antigravity.google/docs/plans

Plans
Plans

At this moment, Google Antigravity is available with terms to individual accounts derived from Google's terms of service, and in preview (pre-general availability) to teams derived from Section 5 of the General Service Terms in Google Cloud's enterprise terms of service.

Rate limits and model availability differs based on usage of Google AI or Google Workspace AI Ultra for Business plans.

Baseline Quota

All plans receive a baseline of:

Use of Gemini 3 Pro, Gemini 3 Flash, and other offered Vertex Model Garden models as the core agent model
Unlimited Tab completions
Unlimited Command requests
Access to all product features, such as the Agent Manager and Browser integration

Users on Google AI Ultra or Google Workspace AI Ultra for Business receive:

The highest, most generous quota, refreshed every five hours
No weekly rate limit

Users on Google AI Pro receive:

High, generous quota, refreshed every five hours until weekly limit reached
Higher weekly rate limit

Users not on AI Pro and Ultra plans receive:

Meaningful quota, refreshed weekly
Weekly rate limit

The baseline rate limits are primarily determined to the degree we have capacity, and exist to prevent abuse. Under the hood, the rate limits are correlated with the amount of work done by the agent, which can differ from prompt to prompt. Thus, you may get many more prompts if your tasks are more straightforward and the agent can complete the work quickly, and the opposite is also true.

Overages

Users on Google AI Pro or Ultra plans also have the ability to utilize their plan-included AI credits for additional overage usage above the baseline provided quota, and can purchase additional AI credits if desired. AI credits are consumed at Vertex API pricing.

Usage of credits once the baseline quota is exhausted for any particular model is controlled by the "AI Credit Overages" user setting, which can be set to the following:

Never: Never use AI credits automatically, wait until the baseline quota refreshes before using this model further
Always: Always use AI credits when the baseline quota is exhausted (will switch back automatically to using the baseline quota once the refresh hits)

Baseline quota usage across models can be viewed in the settings page.

Other

There is currently no support for:

Bring-your-own-key or bring-your-own-endpoint for additional rate limits
Organizational tiers in general availability, or via contract
Separate Chrome Profile
Settings