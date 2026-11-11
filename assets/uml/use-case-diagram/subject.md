---
source_url: "https://www.uml-diagrams.org/use-case-subject.html"
crawled_at: "2026-11-10 06:47:12"
title: "subject"
---

Title: UML subject (of use cases) is a system under analysis or design to which a set of use cases apply. The subject could be a business or company, software system, physical system or device, or a smaller subsystem.

URL Source: https://www.uml-diagrams.org/use-case-subject.html

Markdown Content:
## Use Case Subject

A subject of a use case defines and represents boundaries of a business, software system, physical system or device, [subsystem](https://www.uml-diagrams.org/component.html#subsystem), [component](https://www.uml-diagrams.org/component.html) or even single class in relation to the requirements gathering and analysis.

In UML terms, **subject** is a [classifier](https://www.uml-diagrams.org/classifier.html) playing the "subject" role. They did not create a separate special class for subject, as it was done with actor and use case. UML 2.5 states that a subject of a UseCase could be a system or any other element that may have behavior, such as a Component or Class.". Classifier that may have owned behaviors is called [behaviored classifier](https://www.uml-diagrams.org/common-behaviors.html#behaviored-classifier). Still, UML 2.5 abstract syntax shows subject as plain vanilla classifier.

A **subject** is a [classifier](https://www.uml-diagrams.org/classifier.html) (including [subsystem](https://www.uml-diagrams.org/component.html#subsystem), [component](https://www.uml-diagrams.org/component.html), or even [class](https://www.uml-diagrams.org/class.html)) representing a business, software system, physical system or device under analysis, design, or consideration, having some [behavior](https://www.uml-diagrams.org/common-behaviors.html#behavior), and to which a set of [use cases](https://www.uml-diagrams.org/use-case.html)[applies](https://www.uml-diagrams.org/use-case-subject.html#apply-use-case).

Subject is related to applicable use cases and is different from classifier owning use cases. In UML 2.x until 2.5 use case classifier was a classifier extended with the capability to own use cases. In UML 2.5 any classifier may own use cases.

#### Notation

**Subject** (sometimes called a system boundary) is presented by a rectangle with subject's name, associated keywords and stereotypes in the top left corner. [Use cases](https://www.uml-diagrams.org/use-case.html) applicable to the subject are located inside the rectangle and [actors](https://www.uml-diagrams.org/use-case-actor.html) - outside of the system boundary.

![Image 1: Subject is presented by a rectangle with subject name in upper corner.](https://www.uml-diagrams.org/use-case-diagrams/subject.png)

Books Online (subject) with applicable use cases and Web Customer actor.

#### Revisions

The requirement for the subject's name to be in the **top left corner** of the system boundary was added only in **UML 2.5**. Previous versions of UML allowed to use and had examples with the name in either one of top corners. Personally, I think it is too restrictive to use only the top left corner. When most of the actors are on the left side, subject's name looks better on the right side. In some cases I wouldn't mind having subject's name even in the top middle.

Use cases could be used to model some _business_ to analyse business processes, recognize the problems being experienced, determine the opportunities to better serve customers.

Subject of use cases in this case is business, enterprise, company or its division, department, team.

Examples of business subjects:

*   Department Store
*   Airport
*   Restaurant

UML provides no standard stereotypes to model business processes but we can use custom stereotypes like **«Business»** or **«Department»**, if needed for clarity.

Example below shows «Business» Restaurant with [business actors](https://www.uml-diagrams.org/use-case-actor.html#business-actor) Customer, Advertiser and Supplier and related [business use cases](https://www.uml-diagrams.org/use-case.html#business-use-case).

![Image 2: Restaurant business subject with business actors and applicable use cases.](https://www.uml-diagrams.org/use-case-diagrams/business-subject.png)

Restaurant business **subject** with business actors and applicable use cases

#### Common Mistakes

Example below shows typical misconception for the «Business» Restaurant with [business actors](https://www.uml-diagrams.org/use-case-actor.html#business-actor) mistakenly including Waiter and Cashier. These are both working for the restaurant and are part of the business. They should not be shown as actors because actors are **external** users (customers) of the business (system).

![Image 3: Mistake: Restaurant business should not have Waiter and Cashier as actors.](https://www.uml-diagrams.org/use-case-diagrams/use-case-business-error.png)

Mistake: Restaurant business should not have Waiter and Cashier as actors

## Software System Subject

System use cases describe a system that automates some business use case(s) or process. Subject in this case is software and/or hardware system, subsystem, component or device.

**Examples** of systems:

*   Web Site
*   Payment System
*   Automated Teller Machine (ATM)
*   Point of Sale (POS) Terminal

**UML** provides no standard [stereotypes](https://www.uml-diagrams.org/stereotype.html) for subject (i.e. use case classifier) but UML 2.4 specification examples use the stereotypes from [components](https://www.uml-diagrams.org/component.html):

*   [«Subsystem»](https://www.uml-diagrams.org/component.html#subsystem)
*   [«Process»](https://www.uml-diagrams.org/component.html#process)
*   [«Service»](https://www.uml-diagrams.org/component.html#service)
*   [«Component»](https://www.uml-diagrams.org/component.html)

![Image 4: Weather Service subject stereotyped as «Service».](https://www.uml-diagrams.org/use-case-diagrams/use-case-service-subject.png)

Weather Service **subject** stereotyped as «Service».

## Applicability of Use Cases

Use cases visually located inside the system boundaries are use cases **applicable** to the [subject](https://www.uml-diagrams.org/use-case-subject.html) (but not necessarily **owned** by the subject).

![Image 5: Use cases located inside the system boundaries are applicable to the subject.](https://www.uml-diagrams.org/use-case-diagrams/use-case-applicable.png)

Use cases Browse Items and Buy Items are applicable to Retail Website subject

It is possible for some use cases to be applicable to **multiple subjects**.

## Ownership of Use Cases

In **UML 2.4**[subject](https://www.uml-diagrams.org/use-case-subject.html) could **own** some or all of **applicable** use cases. This **owning (nesting)** of a use case is represented using the standard notation for nested [classifier](https://www.uml-diagrams.org/classifier.html).

![Image 6: Use cases owned (nested) by a classifier (subject).](https://www.uml-diagrams.org/use-case-diagrams/use-case-owned.png)

Retail Website **subject****owns** use cases

![Image 7: Next](https://www.uml-diagrams.org/images/arrow-next.png)[UML Actor](https://www.uml-diagrams.org/use-case-actor.html "UML actor")
