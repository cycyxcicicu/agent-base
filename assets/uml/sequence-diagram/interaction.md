---
source_url: "https://www.uml-diagrams.org/interaction.html"
crawled_at: "2026-11-10 06:47:12"
title: "interaction"
---

Title: UML interaction is an emergent behavior which focuses on the observable exchange of information between connectable elements.

URL Source: https://www.uml-diagrams.org/interaction.html

Markdown Content:
An **interaction** is a specialization of both [behavior](https://www.uml-diagrams.org/common-behaviors.html#behavior) and of [interaction fragment](https://www.uml-diagrams.org/sequence-diagrams.html#interaction-fragment) which represents a unit of behavior that focuses on the observable exchange of information between **connectable elements**.

An interaction is an [emergent behavior](https://www.uml-diagrams.org/common-behaviors.html#emergent-behavior). Interactions focus on the passing of information with messages between the connectable elements of the classifier.

The semantics of an interaction is defined in UML as a pair of sets of **traces** - valid traces and invalid traces. The traces that are not included in these two sets are not described by the interaction, and it is unknown whether they are valid or invalid. A trace is a sequence of event occurrences denoted <e1, e2, ... , en>, each of which is described by an [occurrence specification](https://www.uml-diagrams.org/sequence-diagrams.html#occurrence).

Each occurrence in interactions is normally interpreted to take zero time. Duration is always assumed to be measured between occurrences.

As a behavior an interaction is specializable and redefineable. Specializing an interaction simply allows to add more traces to those of the original. The traces defined by the specialization are combined with those of the inherited interaction with a union. The classifier owning an interaction may be specialized, and in the specialization the interaction may be redefined. Redefining an interaction means to exchange the redefining interaction for the redefined one.

The notation for an interaction is a solid-outline rectangle frame. The pentagon in the upper left corner of the rectangle contains the keyword **sd** followed by the interaction name and parameters. It uses the general notation for the behavior name. The notation within the rectangular frame is one of the form of: [sequence diagram](https://www.uml-diagrams.org/sequence-diagrams.html), [communication diagram](https://www.uml-diagrams.org/communication-diagrams.html), [timing diagram](https://www.uml-diagrams.org/timing-diagrams.html), or [interaction overview diagram](https://www.uml-diagrams.org/interaction-overview-diagrams.html).

![Image 1: An example of an interaction in the form of a sequence diagram.](https://www.uml-diagrams.org/sequence-diagrams/sequence-diagram-overview.png)

An example of an interaction in the form of a sequence diagram.

The [interaction overview diagram](https://www.uml-diagrams.org/interaction-overview-diagrams.html) may include a list of [lifelines](https://www.uml-diagrams.org/sequence-diagrams.html#lifeline) through a lifeline-clause. The list of lifelines is a listing of the lifelines involved in the interaction. An interaction overview diagram does not in itself show the involved lifelines even though the lifelines may occur explicitly within inline interactions in the graph nodes.

An interaction diagram may also include definitions of **local attributes** with the same syntax as [attributes](https://www.uml-diagrams.org/property.html#classifier-attribute) shown within class compartments. These attribute definitions may appear near the top of the diagram frame or within the note symbols at other places in the diagram.
