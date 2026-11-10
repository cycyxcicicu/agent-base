---
source_url: "https://www.uml-diagrams.org/use-case-actor-association.html"
crawled_at: "2026-11-10 06:47:12"
title: "actor-association"
---

Title: An association between UML actor and a use case indicates that the actor and the use case communicate with each other.

URL Source: https://www.uml-diagrams.org/use-case-actor-association.html

Markdown Content:
Each [use case](https://www.uml-diagrams.org/use-case.html) represents a unit of useful functionality that [subjects](https://www.uml-diagrams.org/use-case-subject.html) provide to [actors](https://www.uml-diagrams.org/use-case-actor.html). An [association](https://www.uml-diagrams.org/association.html) between an actor and a use case indicates that the actor and the use case somehow interact or communicate with each other.

Only [binary associations](https://www.uml-diagrams.org/association.html#binary-association) are allowed between actors and use cases.

An actor could be associated to one or several use cases.

![Image 1: An actor could be associated to one or several UML use cases.](https://www.uml-diagrams.org/use-case-diagrams/use-case-association-actor.png)

Customer actor is associated with two use cases -  
 Browse Items and Place Order.

A use case may have one or several associated actors.

![Image 2: UML use case may have one or several associated actors.](https://www.uml-diagrams.org/use-case-diagrams/use-case-association-actors.png)

Manage Account use case is associated with  
 Customer and Bank actors.

If there are several actors associated to the same use case, it may not be obvious from use case diagram which actor **initiates** the use case, i.e. is a "**primary actor**". (In non-standard UML, **primary actors** are those using system services, and **supporting actors** are actors providing services to the system.)

### Multiplicity of Association Ends

UML allows the use of [multiplicity](https://www.uml-diagrams.org/multiplicity.html) at one or both ends of an association between the actor and the use case.

#### Multiplicity of a Use Case

When an actor has an association to a [use case](https://www.uml-diagrams.org/use-case.html) with a [multiplicity](https://www.uml-diagrams.org/multiplicity.html) that is greater than one at the use case end, it means that a given actor can be involved in **multiple use cases** of that type.

![Image 3: Use case multiplicity - given actor can be involved in multiple use cases.](https://www.uml-diagrams.org/use-case-diagrams/use-case-association-many-cases.png)

Bank actor is involved in multiple Transfer Funds use cases.

UML 2.x specifications including UML 2.5 allow any reasonable interpretation of this kind of interaction of a given actor with **multiple use cases**, and intentionally keep it **undefined**.

For example, **use case multiplicity** could mean that an actor interacts with multiple use cases:

*   in parallel (concurrently), or
*   at different points in time (overlapping), or
*   mutually exclusive (sequentially, random, etc).

#### Multiplicity of an Actor

Required actor may be explicitly denoted using multiplicity 1 or greater. UML 2.5 also allows actor to be optional. Multiplicity **0..1** of actor means that the actor may or may not participate in any of their associated use cases.

![Image 4: Actor multiplicity - more than one actor instance initiating the use case.](https://www.uml-diagrams.org/use-case-diagrams/use-case-association-optional-actors.png)

Checkout use case requires Customer actor, hence  
 the 1 multiplicity of Customer. The use case may not need  
 Credit Payment Service (for example, if payment is in cash),  
 thus the 0..1 multiplicity.

When a use case has an association to an [actor](https://www.uml-diagrams.org/use-case-actor.html) with a [multiplicity](https://www.uml-diagrams.org/multiplicity.html) that is greater than one at the actor end, it means that more than one actor instance is involved in the use case.

![Image 5: Actor multiplicity - more than one actor instances are involved in the use case.](https://www.uml-diagrams.org/use-case-diagrams/use-case-association-many-actors.png)

Two or more Player actors are involved  
 in the Play Game use case.  
 Each Player participates in one Play Game.

UML 2.x specifications including UML 2.5 allow any reasonable interpretation of this kind of interaction of **multiple actors** with a use case, and intentionally keep it **undefined**.

For instance, **multiplicity of actor** could mean that interaction of a particular use case with several separate actor instances might be:

*   simultaneous (concurrent) interaction, or
*   overlapping interaction, at different points in time, or
*   mutually exclusive (sequential, random, etc.) interaction.

![Image 6: Next](https://www.uml-diagrams.org/images/arrow-next.png)[Use Case](https://www.uml-diagrams.org/use-case.html "UML use case")
