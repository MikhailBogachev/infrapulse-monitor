# Accessibility specification and checks

IP-006 · MVP v0.1.0 · Stage 03 COMPLETED AND APPROVED

Target [WCAG 2.2 AA](https://www.w3.org/TR/WCAG22/) across normal, degraded and recovered journeys. Apply [NFR-028](../product/srs.md#nfr-028) and [AC-092](../product/acceptance-criteria.md#ac-092).

## Contrast

Ratios use the WCAG linear-sRGB relative-luminance formula. Normal text requires 4.5:1, large text requires 3:1, and required non-text indicators use 3:1 against adjacent colors. The base brand indigo yields 4.47:1 with white, so primary controls use a deeper fill and a separate outline. The low-contrast panel border serves as decorative separation.

| Pair | Ratio | Role |
|---|---:|---|
| Text / Background | 17.52:1 | Main text |
| Text / Surface | 16.54:1 | Panel text |
| Muted / Elevated | 6.36:1 | Secondary UI |
| Muted / Selected | 5.74:1 | Selected or hover surface text |
| Link / Selected | 7.39:1 | Links and focus on selected surface |
| Accent / Surface | 6.07:1 | Data series and accent outlines |
| White / Primary fill | 6.29:1 | Primary action label |
| White / Primary hover | 5.88:1 | Primary action hover label |
| Control / Background | 4.03:1 | Input boundary against fill |
| Control / Surface | 3.81:1 | Input and button boundary |
| Control / Elevated | 3.43:1 | Outlined button and elevated surface |
| Control / Selected | 3.09:1 | Outlined hover state |
| Success / Success tint | 7.98:1 | UP and successful outcomes |
| Danger / Danger tint | 5.59:1 | DOWN and destructive actions |
| Danger / Danger hover | 4.79:1 | Destructive hover label |
| Warning / Warning tint | 8.87:1 | PENDING and warning states |
| Neutral / Elevated | 6.36:1 | PAUSED and inactive states |

## Verification checklist

- **Structure and alternatives, 1.1.1, 1.3.1 and 1.3.2.** Traverse headings, landmarks, form relationships and table headers. Read chart summary and chart data for each range, including a missing bucket. Verify icon-only controls have accessible names and decorative icons are ignored.
- **Perception and reflow, 1.4.1, 1.4.3, 1.4.4, 1.4.10–1.4.12.** Verify status without color, interactive edge and text contrast across states, text-spacing overrides, resize and 320 CSS px reflow. Confirm stable horizontal scrolling only for content requiring two-dimensional presentation.
- **Keyboard and focus, 2.1.1, 2.1.2, 2.4.1–2.4.3, 2.4.7 and 2.4.11.** Test skip link, sequential navigation, selection, drawer, chart disclosure, confirm/cancel, validation focus, Escape, and focus restoration. New route focus lands on its H1. Confirm the topbar and transient feedback leave focused controls visible.
- **Motion and auto-updates, 2.2.2.** Offer Pause live updates and Resume live updates in polling views. Keep manual refresh. Check that a refresh preserves the form draft and keyboard location. Use no automatic animation or flashing.
- **Pointer and labeling, 2.5.3 and 2.5.8.** Keep meaningful visible labels in accessible names and verify minimum 24 × 24 CSS px targets or equivalent spacing.
- **Validation and authentication, 3.3.1–3.3.4, 3.3.7 and 3.3.8.** Verify required fields, accessible descriptions, a safe cancellation path, generic identity errors, copy/paste, password managers and status messages. Test account loss and session recovery with authorized and unauthorized return paths.
- **Name, role, value and announcements, 4.1.2 and 4.1.3.** Verify current link, pressed period control, expanded disclosure and dialog accessible names. Confirm success and failed freshness transitions are announced without forcing focus. Read confirmation copy and test status badges with a screen reader across principal journeys.

The checklist is a verification plan. Browser reflow, keyboard interaction and assistive technology evidence are required before making a conformance claim.
