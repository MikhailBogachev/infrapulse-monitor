# InfraPulse design system

IP-006 · MVP v0.1.0 · Stage 03 COMPLETED AND APPROVED · [Approved UX decisions](../project/decision-register.md#approved-stage-03-ux-decisions)

## Visual direction

The workspace opens with an operational summary, then supports investigation through scoped monitors, incidents and delivery history. Graphite surfaces separate navigation, working panels and overlays. Indigo identifies the primary action, current location, focus and time series. The interface stays dark in both OS color schemes and uses English labels. Status colors carry operational meaning alongside explicit labels and Lucide-style outline symbols.

## Tokens

Use semantic Tailwind color aliases backed by CSS variables. The [prototype stylesheet](prototype/styles.css) contains the literal values.

| Role | Token and value | Use |
|---|---|---|
| Canvas | Background `#0C0F14` | Main canvas, input fill |
| Panel | Surface `#12161E` | Sidebar, cards, dialogs |
| Overlay and secondary actions | Elevated `#1A202C` | Toast, hover, secondary buttons |
| Divider | Border `#252B36` | Decorative panel borders and dividers |
| Interactive boundary | Control `#64748B` | Inputs, outlined actions and scroll-region empty states |
| Brand | Primary `#6366F1` | Base indigo; use accessible derivatives for control fills |
| Primary action | Fill `#4F46E5`, hover `#554BE9`, foreground `#FFFFFF` | Primary button |
| Accent | Accent `#818CF8` | Selected mark, chart stroke, primary outline |
| Focus and links | Link `#A5B4FC`, selected fill `#242640` | 2 px focus outline with 3 px offset, links, selected navigation |
| Text | Text `#F1F5F9`, Muted `#94A3B8` | Primary content, secondary information and axes |
| Success | Success `#34D399`, tint `#132923` | Healthy, saved or delivered |
| Danger | Danger `#F87171`, tint `#2F2028`, hover tint `#432830` | Confirmed downtime, field error, destructive action |
| Warning | Warning `#FBBF24`, tint `#2D271C` | Pending, stale, unknown or internal fault |
| Neutral | Neutral `#94A3B8` on Elevated | Paused or inactive |

| Status | Label | Icon | Tone |
|---|---|---|---|
| UP | UP | Check | Success |
| DOWN | DOWN | Alert triangle | Danger |
| PENDING | PENDING | Clock | Warning |
| PAUSED | PAUSED | Pause | Neutral |

Use Inter at 14/21 px for body and controls, 12/18 px for table labels and badge copy, 13/19.5 px for help, 16/22 px for section headings, and 24–28/29–34 px for page headings. Use JetBrains Mono for UTC timestamps, endpoints and tabular metric values at 28–36 px. Preserve system sans and monospace fallbacks. Use 4 px spacing increments as the implementation grid, 8 px for control and panel corners, 6 px for status chips and 10 px for modal corners. See [responsive design](responsive-design.md) for layout grids and control sizing.

## Components and frontend mapping

| Pattern | Tailwind and shadcn/ui mapping | States |
|---|---|---|
| Workspace shell | Sidebar, Sheet, Button, Avatar | Current route indicated by label and selection mark, hover, focus, mobile open/closed |
| Controls | Button, Input, Select, Checkbox, Label | Default, hover, focus-visible, pending, unavailable with reason, invalid with adjacent text |
| Status | Badge with Lucide React icon | Four monitor states, open/closed incident, delivery status |
| Data | Card, Table, ScrollArea, Skeleton | Loading, empty, no match, normal, retained stale snapshot, first-load error |
| Chart | Recharts with accessible figure and native table disclosure | Period selected, null gaps, No data, updated and stale |
| Feedback | Alert, AlertDialog, Sonner | Inline validation, persistent retry or conflict alert, success toast, safe default focus in confirmation |

Use one prominent action per screen section. Underline inline links and keep visible labels on primary actions. Pair icon-only actions with accessible names. Use bordered panels with modest depth and reserve elevation for overlays. See [accessibility and contrast](accessibility.md) and [interaction patterns](interaction-patterns.md).
