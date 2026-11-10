---
source_url: "https://www.uml-diagrams.org/use-case-extend.html"
crawled_at: "2026-11-10 06:47:12"
title: "extend"
---

Title: UML use case extend relationship is used to show how and when some optional extending use case can be inserted into extended (base) use case.

URL Source: https://www.uml-diagrams.org/use-case-extend.html

Markdown Content:
**Extend** is a [directed relationship](https://www.uml-diagrams.org/uml-core.html#directed-relationship) that specifies how and when the behavior defined in usually supplementary (optional) **extending use case** can be inserted into the [behavior](https://www.uml-diagrams.org/common-behaviors.html#behavior) defined in the **extended use case**.

**Extended** use case is meaningful on its own, it is **independent** of the extending use case. **Extending** use case typically defines **optional**[behavior](https://www.uml-diagrams.org/common-behaviors.html#behavior) that is not necessarily meaningful by itself. The extend relationship is **owned** by the extending use case. The same extending use case can extend more than one use case, and extending use case may itself be extended.

The extension takes place at one or more [extension points](https://www.uml-diagrams.org/use-case-extend.html#extension-point) defined in the **extended use case**.

**Extend** relationship is shown as a dashed line with an open arrowhead directed from the **extending use case** to the **extended (base) use case**. The arrow is labeled with the keyword **«extend»**.

![Image 1: UML extend relationship example - Registration use case is extended with optional Get Help use case.](https://www.uml-diagrams.org/use-case-diagrams/use-case-extend.png)

**Registration** use case is complete and meaningful on its own.  
 It could be extended with optional **Get Help On Registration** use case.

The **condition** of the extend relationship as well as the references to the [extension points](https://www.uml-diagrams.org/use-case-extend.html#extension-point) are optionally shown in a [comment](https://www.uml-diagrams.org/uml-core.html#comment) note attached to the corresponding extend relationship.

![Image 2: UML extend relationship example - Registration use case is conditionally extended by Get Help On Registration.](https://www.uml-diagrams.org/use-case-diagrams/use-case-extend-condition.png)

Registration use case is conditionally extended by Get Help On Registration  
 use case in extension point Registration Help.

## Extension Point

An **extension point** is a **feature** of a [use case](https://www.uml-diagrams.org/use-case.html) which identifies (references) a point in the behavior of the use case where that behavior can be extended by some other (extending) use case, as specified by [extend](https://www.uml-diagrams.org/use-case-extend.html) relationship.

Extension points may be shown in a compartment of the use case oval symbol under the heading **extension points**. Each extension point must have a **name**, unique within a use case. Extension points are shown as a text string according to the syntax:

extension point ::= name [: explanation ]

The optional explanation is some description usually given as informal text. It could be in other forms, such as the name of a [state](https://www.uml-diagrams.org/state-machine-diagrams.html#state) in a state machine, an activity in an activity diagram, some precondition or postcondition.

![Image 3: Use case with extension points in a compartment.](https://www.uml-diagrams.org/use-case-diagrams/use-case-extension-points.png)

Registration **use case** with **extension points**  
 Registration Help and User Agreement

Extension points may be shown in a compartment of the use case rectangle with **ellipse icon** under the heading **extension points**.

![Image 4: Use case shown with standard rectangle notation for classifiers.](https://www.uml-diagrams.org/use-case-diagrams/use-case-rectangle.png)

Extension points of the Registration **use case**,  
 shown using the rectangle notation

![Image 5: Next](https://www.uml-diagrams.org/images/arrow-next.png)[Use Case Include](https://www.uml-diagrams.org/use-case-include.html "UML use case include")
