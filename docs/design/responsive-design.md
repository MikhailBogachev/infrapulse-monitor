# Responsive design

IP-006 · MVP v0.1.0 · Stage 03 COMPLETED AND APPROVED

| Width | Navigation | Content |
|---|---|---|
| 1440 px and ≥1200 px | Persistent 232 px sidebar, sticky topbar | 28 px page padding, four metric columns, main chart and status rail, wide tables |
| 1024 px / 1000–1199 px | Persistent 196 px sidebar, sticky topbar | 20 px page padding, four metric columns, wrapping actions and two-column chart region |
| 768 px / 700–999 px | Sticky topbar with modal drawer trigger | Full-width page with 20 px padding, four metric columns where they fit, chart and rail, paired form fields |
| 360 px / <700 px | Sticky compact topbar with modal drawer trigger | 16 px page padding, 24 px H1, two-column KPIs, stacked panels and form fields, local table scrolling |

The breakpoint boundaries are design choices for this prototype. Use a fluid content column capped at 1512 px and a 760 px form column. Use CSS Grid for major columns and Flexbox for actions, status labels and filters. Keep the DOM reading order as navigation, context, actions and content. Avoid whole-document sideways scrolling. Tables keep header semantics with a focusable named horizontal region when needed. Critical actions live in headings or wrap in the current row. Long names, target URLs, dates and errors wrap in available space. Authentication and dialog widths are clamped to the available viewport.

The drawer uses modal focus containment, scrollable content, Escape, a labeled close control and focus return. Opening a destination focuses its heading. Dismiss the drawer when entering persistent-sidebar width. Keep buttons and primary inputs at least 40 px high and compact controls at least 32 px. Make sticky headers compatible with focus scrolling and avoid fixed footers covering controls.

Verify 360, 768, 1024 and 1440 px, and reflow at 320 CSS px and 200% text resize. Use a long workspace name, a long URL, a validation error, an open modal and a scrollable table. Resize with the drawer open. Test table scrolling with an external keyboard. [AC-093](../product/acceptance-criteria.md#ac-093)
