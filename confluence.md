h1. 📊 Analytics Support – [Team/Division Name]

{toc:maxLevel=2|type=list|printable=true}

----

h2. 🧭 1. Overview

This page provides visibility into Analytics projects, dashboards, and priorities for the *[Team or Division Name]*. Use this space to:
- ✅ View active and completed work
- 📈 Access live dashboards and data documentation
- 📨 Submit analytics requests
- 👤 Know who to contact

----

h2. 👥 2. Primary Contacts

|| Role || Name || Notes ||
| 👨‍💼 Primary Analyst | [Name] | Main contact for requests |
| 🧑‍💻 Backup Analyst | [Name] | Backup for escalations or coverage |
| 🧑‍🏫 Business Product Owner | [Name] | Main stakeholder for quarterly planning |

----

h2. 🚧 3. Current Work & Priorities (Q[Insert Quarter] [Insert Year])

Below is a filtered list of active analytics work tied to this team.

{jiraissues:url=https://jira.company.com/issues/?jql=project=ANALYTICS%20AND%20labels%20=%20[team-label]%20AND%20status%20in%20("To Do",%20"In Progress")%20ORDER%20BY%20priority%20DESC|columns=key,summary,status,assignee,duedate}

> *Legend:*  
> - ⏳ “To Do” = Queued for work  
> - 🔄 “In Progress” = Currently being worked on  
> - ❗ “Blocked” = Needs business input or dependency

----

h2. ✅ 4. Completed Work (Past 90 Days)

{jiraissues:url=https://jira.company.com/issues/?jql=project=ANALYTICS%20AND%20labels%20=%20[team-label]%20AND%20status=Done%20AND%20resolved%20>=%20-90d%20ORDER%20BY%20resolved%20DESC|columns=key,summary,resolutiondate}

----

h2. 📂 5. Dashboard & Tool Access

*Live Dashboards:*
- 📊 [Client Funnel Dashboard|https://tableau.company.com/dashboard1]
- 📉 [Retention View Dashboard|https://tableau.company.com/dashboard2]

*Data Resources:*
- 📚 [Data Dictionary|https://confluence.company.com/space/datadictionary]
- 🧾 [Table Access Guide|https://confluence.company.com/space/table-access]

----

h2. 📝 6. Submit a Request

Submit a new analytics or reporting request via one of the methods below:

- 🧠 [Analytics Request Form|https://forms.office.com/request]
- 🛠️ [Jira Service Desk: Analytics Intake|https://jira.company.com/servicedesk/analytics]

*⏱️ Note: Requests are triaged weekly. Response time is 2–3 business days.*

----

h2. 📅 7. Key Milestones

|| 🧱 Milestone || 📆 Date || 👤 Owner ||
| Phase 2 Dashboard Launch | June 14 | [Name] |
| KPI Finalization | July 1 | [Name] |
| Quarterly Planning Session | July 10 | [PO Name] |

----

h2. 💬 8. Feedback or Improvements?

We want to keep this page useful. If anything is unclear or you have suggestions:

- 🗣️ [Submit feedback here|https://forms.office.com/feedback]
- ✉️ Or email [Primary Analyst Email]

----