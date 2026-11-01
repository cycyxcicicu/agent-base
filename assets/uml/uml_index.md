---
source_url: "https://www.uml-diagrams.org/"
crawled_at: "2026-11-01 02:33:27"
title: "uml_index"
---

Title: Unified Modeling Language (UML) description, UML diagram examples, tutorials and reference for all types of UML diagrams

URL Source: https://www.uml-diagrams.org/

Markdown Content:
Menu►
*   [Home](https://www.uml-diagrams.org/ "UML Diagrams - overview, reference, and examples.")
*   [UML Diagrams](https://www.uml-diagrams.org/uml-25-diagrams.html "UML 2.5 diagrams overview")
*   [Class Diagrams](https://www.uml-diagrams.org/class-diagrams-overview.html "UML Class Diagrams Overview")
*   [Composite Structures](https://www.uml-diagrams.org/composite-structure-diagrams.html "UML Composite Structure Diagrams Overview")
*   [Packages](https://www.uml-diagrams.org/package-diagrams-overview.html "UML Package Diagrams Overview")
*   [Components](https://www.uml-diagrams.org/component-diagrams.html "UML Component Diagrams")
*   [Deployments](https://www.uml-diagrams.org/deployment-diagrams-overview.html "UML Deployment Diagrams Overview")
*   [Use Case Diagrams](https://www.uml-diagrams.org/use-case-diagrams.html "UML Use Case Diagrams Overview")
*   [Information Flows](https://www.uml-diagrams.org/information-flow-diagrams.html "UML information flow diagrams overview")
*   [Activities](https://www.uml-diagrams.org/activity-diagrams.html "UML Activity Diagrams")
*   [State Machines](https://www.uml-diagrams.org/state-machine-diagrams.html "UML State Machine Diagrams Overview")
*   [Sequence Diagrams](https://www.uml-diagrams.org/sequence-diagrams.html "UML Sequence Diagrams Overview")
*   [Communications](https://www.uml-diagrams.org/communication-diagrams.html "UML Communication Diagrams")
*   [Timing Diagrams](https://www.uml-diagrams.org/timing-diagrams.html "UML Timing Diagrams")
*   [Interaction Overviews](https://www.uml-diagrams.org/interaction-overview-diagrams.html "UML Interaction Overview Diagrams")
*   [Profiles](https://www.uml-diagrams.org/profile-diagrams.html "UML Profile Diagrams")
*   [UML Index](https://www.uml-diagrams.org/index-references.html "Index of UML Elements")
*   [Examples](https://www.uml-diagrams.org/index-examples.html "Index of examples of UML diagrams")
*   [About](https://www.uml-diagrams.org/about.html "About this web site")

# The Unified Modeling Language

The **Unified Modeling Language™** (**UML®**) is a standard visual modeling language intended to be used for

*   modeling business and similar processes,
*   analysis, design, and implementation of software-based systems

UML is a common language for business analysts, software architects and developers used to describe, specify, design, and document existing or new business processes, structure and behavior of artifacts of software systems.

UML can be applied to diverse **application domains** (e.g., banking, finance, internet, aerospace, healthcare, etc.) It can be used with all major object and component **software development methods** and for various **implementation platforms** (e.g., J2EE, .NET).

UML is a standard modeling **language**, not a **software development process**. [UML 1.4.2 Specification](https://www.uml-diagrams.org/references.html#ref-uml-142 "UML 1.4.2 Specification") explained that process:

*   provides guidance as to the order of a team’s activities,
*   specifies what artifacts should be developed,
*   directs the tasks of individual developers and the team as a whole, and
*   offers criteria for monitoring and measuring a project’s products and activities.

UML is intentionally **process independent** and could be applied in the context of different processes. Still, it is most suitable for use case driven, iterative and incremental development processes. An example of such process is **Rational Unified Process** (RUP).

UML is not complete and it is not completely visual. Given some UML diagram, we can't be sure to understand depicted part or behavior of the system from the diagram alone. Some information could be intentionally omitted from the diagram, some information represented on the diagram could have different interpretations, and some concepts of UML have no graphical notation at all, so there is no way to depict those on diagrams.

For example, semantics of **multiplicity of actors** and **multiplicity of use cases** on [use case diagrams](https://www.uml-diagrams.org/use-case-diagrams.html) is not defined precisely in the UML specification and could mean either concurrent or successive usage of use cases.

Name of an [abstract classifier](https://www.uml-diagrams.org/classifier.html#abstract-classifier) is shown in italics while [final classifier](https://www.uml-diagrams.org/classifier.html#final-classifier) has no specific graphical notation, so there is no way to determine whether classifier is final or not from the diagram.

## Versions of UML

The current version of the **Unified Modeling Language™** is **UML 2.5**, released in June 2015 [[UML 2.5 Specification]](https://www.uml-diagrams.org/references.html#ref-uml-25 "UML 2.5 Specification"). **UML® specification** (standard) is updated and managed by the **Object Management Group** (OMG™) [OMG UML](http://www.omg.org/UML/ "OMG UML"). The first versions of UML were created by "**Three Amigos**" - **Grady Booch** (creator of Booch method), **Ivar Jacobson** (Object-Oriented Software Engineering, OOSE), and **Jim Rumbaugh** (Object-Modeling Technique, OMT).

| Version | Date | Description |
| --- | --- | --- |
| 1.1 | 11-1997 | UML 1.1 proposal is adopted by the OMG. |
| 1.3 | 03-2000 | Contains a number of changes to the UML metamodel, semantics, and notation, but should be considered a minor upgrade to the original proposal. |
| 1.4 | 09-2001 | Mostly "tuning" release but not completely upward compatible with the UML 1.3. Addition of [profiles](https://www.uml-diagrams.org/profile.html) as UML extensions grouped together. Updated **visibility** of features. Stick arrowhead in **interaction diagrams** now denotes **asynchronous call**. Model element may now have multiple **stereotypes**. Clarified collaborations. Refined definitions of components and related concepts. [Artifact](https://www.uml-diagrams.org/artifact.html) was added to represent physical representations of components. |
| 1.5 | 03-2003 | Added [actions](https://www.uml-diagrams.org/activity-diagrams-actions.html) (see Part 5 of spec) - executable actions and procedures, including their run-time semantics, defined the concept of a data flow to carry data between actions, etc. |
| 1.4.2 | 01-2005 | This version was accepted as ISO specification (standard) ISO/IEC 19501. UML 1.5 was released 2 years before. |
| 2.0 | 08-2005 | New diagrams: object diagrams, [package diagrams](https://www.uml-diagrams.org/package-diagrams-overview.html), [composite structure diagrams](https://www.uml-diagrams.org/composite-structure-diagrams.html), interaction overview diagrams, timing diagrams, [profile diagrams](https://www.uml-diagrams.org/profile-diagrams.html). **Collaboration diagrams** were renamed to [communication diagrams](https://www.uml-diagrams.org/communication-diagrams.html). [Activity diagrams](https://www.uml-diagrams.org/activity-diagrams.html) and [sequence diagrams](https://www.uml-diagrams.org/sequence-diagrams.html) were enhanced. Activities were redesigned to use a Petri-like semantics. Edges can now be contained in partitions. Partitions can be hierarchical and multidimensional. Explicitly modeled [object flows](https://www.uml-diagrams.org/activity-diagrams.html#object-flow-edge) are new. Classes have been extended with internal structures and [ports](https://www.uml-diagrams.org/port.html) (composite structures). Information flows were added. A collaboration now is a kind of classifier, and can have any kind of behavioral descriptions associated. Interactions are now contained within classifiers and not only within collaborations. It is now possible for [use cases](https://www.uml-diagrams.org/use-case.html) to be owned by [classifiers](https://www.uml-diagrams.org/classifier.html) in general and not just packages. New notation for concurrency and branching using combined fragments. Notation and/or semantics were updated for components, realization, deployments of artifacts. Components can no longer be directly deployed to [nodes](https://www.uml-diagrams.org/deployment-diagrams.html#node). [Artifacts](https://www.uml-diagrams.org/artifact.html) should be deployed instead. Implementation has been replaced by «[manifest](https://www.uml-diagrams.org/deployment-diagrams.html#manifestation)». Artifacts can now manifest any packageable element (not just components, as before). It is now possible to deploy to nodes with an internal structure. New metaclasses were added: connector, collaboration use, connector end, [device](https://www.uml-diagrams.org/deployment-diagrams.html#device), deployment specification, [execution environment](https://www.uml-diagrams.org/deployment-diagrams.html#execution-environment), accept event action, send object action, structural feature action, value pin, activity final, central buffer node, data stores, flow final, interruptible regions, loop nodes, parameter, [port](https://www.uml-diagrams.org/port.html), behavior, behaviored classifier, duration, interval, time constraint, combined fragment, creation event, destruction event, execution event, interaction fragment, interaction use, receive signal event, send signal event, extension, etc. Many stereotypes were eliminated from the Standard UML Profile, e.g. «destroy», «facade», «friend», «profile», «requirement», «table», «thread». Integration between structural and behavioral models was improved with better support for executable models. |
| 2.1 | 04-2006 | Minor revision to UML 2.0 - corrections and consistency improvements. |
| 2.1.1 | 02-2007 | Minor revision to the UML 2.1 |
| 2.1.2 | 11-2007 | Minor revision to the UML 2.1.1 |
| 2.2 | 02-2009 | Fixed numerous minor consistency problems and added clarifications to UML 2.1.2 |
| 2.3 | 05-2010 | Minor revision to the UML 2.2, clarified [associations](https://www.uml-diagrams.org/association.html) and association classes, added [final classifier](https://www.uml-diagrams.org/classifier.html#final-classifier), updated [component diagrams](https://www.uml-diagrams.org/component-diagrams.html), composite structures, actions, etc. |
| 2.4.1 | 08-2011 | UML revision with few fixes and updates to classes, packages - added [URI package attribute](https://www.uml-diagrams.org/package-diagrams.html#uri-package); updated actions; removed creation event, execution event, send and receive operation events, send and receive signal events, renamed destruction event to [destruction occurrence specification](https://www.uml-diagrams.org/sequence-diagrams.html#destruction-occurrence-seq); [profiles](https://www.uml-diagrams.org/profile-diagrams.html) - changed stereotypes and applied stereotypes to have upper-case first letter - [«Metaclass»](https://www.uml-diagrams.org/profile-metaclass.html) and [stereotype application](https://www.uml-diagrams.org/stereotype.html#stereotype-applied-profile). |
| [2.5](https://www.uml-diagrams.org/references.html#ref-uml-25 "UML 2.5 Specification") | 06-2015 | UML 2.5 is called a "minor revision" to the UML 2.4.1, while they spent a lot of efforts to simplify and reorganize UML specification document. The UML specification was re-written "to make it easier to read". For example, they tried to "reduce forward references as much as possible". There are no longer two separate infrastructure and superstructure documents, the UML 2.5 specification is a single document. [Package merge](https://www.uml-diagrams.org/package-merge.html) is no longer used within the specification. Four UML compliance levels (L0, L1, L2, and L3) are eliminated, as they were not useful in practice. UML 2.5 tools will have to support complete UML specification. [Information flows](https://www.uml-diagrams.org/information-flow-diagrams.html), [models](https://www.uml-diagrams.org/package-diagrams/model.html), and [templates](https://www.uml-diagrams.org/template.html) are no longer auxiliary UML constructs. At the same time, [use cases](https://www.uml-diagrams.org/use-case-diagrams.html), [deployments](https://www.uml-diagrams.org/deployment-diagrams-overview.html), and the [information flows](https://www.uml-diagrams.org/information-flow-diagrams.html) became "**supplementary concepts**" in UML 2.5. UML 2.5 has a number of fixes, clarifications, and explanations added. They updated description for multiplicity and multiplicity element, clarified definitions of aggregation and composition, and finally fixed wrong «instantiate» dependency example for Car Factory. New notation for [inherited members](https://www.uml-diagrams.org/inherited-property.html) with a caret '^' symbol was introduced. UML 2.5 clarified [feature redefinition](https://www.uml-diagrams.org/redefining-property.html) and overloading. They also moved and rephrased definition of qualifiers. Default for [generalization sets](https://www.uml-diagrams.org/generalization.html#generalization-set) was changed from **{incomplete, disjoint}** to **{incomplete, overlapping}**. There are few clarifications and fixes for stereotypes, state machines, and activities. Protocol state machines are now denoted using «protocol» instead of {protocol}. [Use cases](https://www.uml-diagrams.org/use-case.html) are no longer required to express some needs of [actors](https://www.uml-diagrams.org/use-case-actor.html) and to be initiated by an actor. |

## UML 2.5 Diagrams

You can proceed to [UML 2.5 diagrams overview](https://www.uml-diagrams.org/uml-25-diagrams.html), specific UML diagrams in the site navigation, or to the [examples of UML diagrams](https://www.uml-diagrams.org/index-examples.html).

  

This document describes UML versions up to **[UML 2.5](https://www.uml-diagrams.org/references.html#ref-uml-25 "UML 2.5 Specification")** and is based on the corresponding **OMG™ Unified Modeling Language™ (OMG UML®)** specifications. UML diagrams were created in **Microsoft® Visio®** 2007-2016 using **[UML 2.x Visio Stencils](http://softwarestencils.com/uml/index.html "Visio Stencil and Template for UML 2.5")**. You can send your comments and suggestions to [webmaster](mailto:webmaster@uml-diagrams.org). [Privacy policy](https://www.uml-diagrams.org/privacy-policy.html).

_Copyright © 2009-2026 uml-diagrams.org. All rights reserved. Authored by Kirill Fakhroutdinov._

![Image 1](images/www.uml-diagrams.org)

[](https://topgadgetlife.com/products/retro-style-digital-camera-with-64mp-photos-4k-video-and-18x-zoom)[Remember When You Packed a Camera for Every Trip TopGadgetlife | [Sponsored](https://popup.taboola.com/en/?template=colorbox&utm_source=uml-diagrams&utm_medium=referral&utm_content=next-up-a-delta:Next%20Up:)[Sponsored](https://popup.taboola.com/en/?template=colorbox&utm_source=uml-diagrams&utm_medium=referral&utm_content=next-up-a-delta:Next%20Up:) Read Next Story](https://topgadgetlife.com/products/retro-style-digital-camera-with-64mp-photos-4k-video-and-18x-zoom "Remember When You Packed a Camera for Every Trip")
