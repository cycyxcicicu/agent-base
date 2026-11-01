---
source_url: "https://www.uml-diagrams.org/activity-diagrams.html"
crawled_at: "2026-11-01 02:34:39"
title: "spec"
---

Title: UML activity diagrams are UML behavior diagrams which show flow of control or object flow with emphasis on the sequence and conditions of the flow.

URL Source: https://www.uml-diagrams.org/activity-diagrams.html

Markdown Content:
Menu►
*   [UML diagrams](https://www.uml-diagrams.org/ "UML graphical notation overview, examples, and reference.")
*   [Activity diagrams](https://www.uml-diagrams.org/activity-diagrams.html "UML activity diagrams show flow of control or object flow with emphasis on the sequence and conditions of the flow.")
*   [Actions](https://www.uml-diagrams.org/activity-diagrams-actions.html "UML activity diagram actions - object, variable, invocation, structural, link, event actions.")
*   [Controls](https://www.uml-diagrams.org/activity-diagrams-controls.html "UML activity diagram controls - initial, flow final, activity final, decision, merge, fork, join.")
*   [Objects](https://www.uml-diagrams.org/activity-diagrams-objects.html "UML activity diagram object nodes - object, pin, parameter, central buffer, data store.")
*   [Activity reference](https://www.uml-diagrams.org/activity-diagrams-reference.html "UML activity diagrams reference.")
*   [Activity examples](https://www.uml-diagrams.org/activity-diagrams-examples.html "UML activity diagrams examples.")
*   [UML index](https://www.uml-diagrams.org/index-references.html "Index of UML elements")

# Activity Diagrams

**Activity diagram** is UML [behavior diagram](https://www.uml-diagrams.org/uml-25-diagrams.html#behavior-diagram) which shows **flow of control** or **object flow** with emphasis on the sequence and conditions of the flow. The actions coordinated by activity models can be initiated because other actions finish executing, because objects and data become available, or because some events external to the flow occur.

The following nodes and edges are typically drawn on **UML****activity diagrams**: [activity](https://www.uml-diagrams.org/activity-diagrams.html#activity), [partition](https://www.uml-diagrams.org/activity-diagrams.html#partition), [action](https://www.uml-diagrams.org/activity-diagrams-actions.html), [object](https://www.uml-diagrams.org/activity-diagrams-objects.html), [control](https://www.uml-diagrams.org/activity-diagrams-controls.html), [activity edge](https://www.uml-diagrams.org/activity-diagrams.html#activity-edge).

You can find some [activity diagram examples](https://www.uml-diagrams.org/activity-diagrams-examples.html) here:

*   [Online Shopping](https://www.uml-diagrams.org/online-shopping-uml-activity-diagram-example.html?context=activity-examples)
*   Business Flow - [Process Order](https://www.uml-diagrams.org/shopping-process-order-uml-activity-diagram-example.html?context=activity-examples)
*   Business Flow - [Document Management Process](https://www.uml-diagrams.org/document-management-uml-activity-diagram-example.html)
*   Software Design - [Resolve Issue](https://www.uml-diagrams.org/software-resolve-issue-uml-activity-diagram-example.html)
*   [Sentinel HASP SL - Manual Activation of Trial Product](https://www.uml-diagrams.org/software-licensing-activity-diagram-example.html?context=activity-examples)
*   [Single Sign-On for Google Apps](https://www.uml-diagrams.org/google-sign-on-uml-activity-diagram-example.html)

## Activity

**Activity** is a parameterized [behavior](https://www.uml-diagrams.org/common-behaviors.html#behavior) represented as coordinated flow of [actions](https://www.uml-diagrams.org/activity-diagrams-actions.html).

The **flow of execution** is modeled as activity nodes connected by activity edges. A node can be the execution of a subordinate behavior, such as an arithmetic computation, a call to an operation, or manipulation of object contents. Activity nodes also include flow of control constructs, such as synchronization, decision, and concurrency control. Activities may form invocation hierarchies invoking other activities, ultimately resolving to individual actions. In an object-oriented model, activities are usually invoked indirectly as methods bound to operations that are directly invoked.

Activity contains **activity nodes** which could be:

*   [action](https://www.uml-diagrams.org/activity-diagrams-actions.html)
*   [object](https://www.uml-diagrams.org/activity-diagrams-objects.html)
*   [control](https://www.uml-diagrams.org/activity-diagrams-controls.html)

Activities may contain **actions** of various kinds:

*   Occurrences of primitive functions, such as arithmetic functions.
*   Invocations of behavior, such as activities.
*   Communication actions, such as sending of signals.
*   Manipulations of objects, such as reading or writing attributes or associations.

There are actions that invoke activities - either directly using [call behavior action](https://www.uml-diagrams.org/activity-diagrams-actions.html#call-behavior-action) or indirectly with **call operation action**.

Activity could be rendered as round-cornered rectangle with activity name in the upper left corner and nodes and edges of the activity inside the border. UML 2.4 specification examples show activity name in bold.

![Image 1: Online Shopping activity.](images/activity.png)
Online Shopping activity.

Activity parameters are displayed on the border and listed below the activity name as:  
parameter-name: parameter-type.

![Image 2: Authenticate User activity with two parameters - Login Id and Password.](images/activity-parameters.png)
Authenticate User activity with two parameters - Login Id and Password.

As a [behavior](https://www.uml-diagrams.org/common-behaviors.html#behavior) activity could have pre- and post-condition constraints. If present, these are shown with the keywords «precondition» and «postcondition», respectively.

The keyword «singleExecution» is used for activities that execute as a single shared execution (singleton), otherwise, each invocation executes in its own space.

The round-cornered activity border may be replaced with the frame notation for diagrams. The kind of the frame in this case is **activity** or **act** in short form. Activity parameters if any are displayed on the frame.

![Image 3: Authenticate User activity frame with two parameters - Login Id and Password.](images/activity-frame.png)
Authenticate User activity frame with two parameters - Login Id and Password.

The notation for classes with the keyword «activity» can be used to show the features of a reflective activity, to indicate it is an activity class. Association and state machine notation can also be used as necessary.

UML allows behaviors to produce tokens that are **activities** and which can in turn be executed at the runtime.

## Activity Partition

An activity **partition** is **activity group** for actions that have some common characteristic.

Partitions often correspond to **organizational units** or **business actors** in a **business model**.

Partitions provide a constrained view on the behaviors invoked in activities. Constraints could be selected according to the type of the element that the partition represents. The following constraints are normative (standard) in UML 2.4:

*   [classifier](https://www.uml-diagrams.org/classifier.html)
*   [instance](https://www.uml-diagrams.org/uml-core.html#instance-core)
*   [part](https://www.uml-diagrams.org/composite-structure-diagrams/part.html)
*   [attribute](https://www.uml-diagrams.org/property.html#classifier-attribute) and value

For example, partitions could represent specific [classifiers](https://www.uml-diagrams.org/classifier.html). In this case actions in each partition should be operations or signals targeting objects that are instances of the corresponding classifier.

A partition may represent some [attribute](https://www.uml-diagrams.org/property.html#classifier-attribute) and its subpartitions - specific values of that attribute. For example, a partition may represent the location at which a behavior is carried out, and the subpartitions would represent specific values for that attribute, such as New York.

Activity **partition** may be shown using a **swimlane** notation - with two, usually parallel lines, either horizontal or vertical, and a name labeling the partition in a box at one end. Any activity nodes, e.g. actions and edges placed between these lines are considered to be contained within the partition.

![Image 4: Activity partition shown using horizontal swimlane notation.](images/activity-partition-horizontal.png)
Activity partitions Customer and Order Dept as horizontal swimlanes

![Image 5: Activity partition shown using vertical swimlane notation.](images/activity-partition-vertical.png)
Activity partitions Customer and Order Dept as vertical swimlanes

**Hierarchical partitioning** is represented using swimlanes for subpartitions as illustrated below.

![Image 6: Hierarchical partitioning with subpartitions.](images/activity-partition-hierachy.png)
Hierarchical partitioning with subpartitions

A partition may be marked as a **dimension** for its subpartitions to contain (group) those subpartitions along dimension. For example, an activity may have one dimension of partitions for location at which the contained behaviors are carried out, and another for the cost of performing them. **Dimension partitions** cannot be contained by any other partition.

Diagrams can also be partitioned multidimensionally, where each swim cell is an intersection of multiple partitions. The partitions within each dimension may be grouped into an enclosing activity partition with isDimension=true, whose name is the dimension name. Rather than being shown as a partition itself, however, the dimension is indicated by placing its name along side the set of partitions in the dimension.

Partition could represent an **external entity** to which the partitioning structure does not apply. **External partitions** are intentional exceptions to the rules for partition structure. For example, a dimension may have partitions showing parts of a [structured classifier](https://www.uml-diagrams.org/structured-classifier.html). It can have an **external partition** that does not represent one of the parts, but a completely separate classifier. In **business modeling**, external partitions can be used to model entities outside a business.

When activities are considered to occur outside the domain of a particular model, the partition can be labeled with the keyword **«external»**. Whenever an activity in a swimlane is marked «external», this overrides the swimlane and dimension designation.

![Image 7: External partition labeled with the keyword external.](images/activity-partition-external.png)
Buy **action** occurs in external **partition** Customer

In the situations when swimlanes can't be used to show partitions, alternate text notation with qualified action name could be used instead. In this case **partition** name is placed in parenthesis above the **action** name. A comma-delimited list of partition names means that the node is contained in more than one partition. A double colon within a partition name indicates that the partition is nested, with the larger partitions coming earlier in the name.

![Image 8: Partitioning using qualified action names.](images/activity-partition-qualified.png)
Buy **action** occurs in the external **partition** Customer

## Activity Edge

**Activity Edge** is an abstract class for the directed connections along which **tokens** or **data objects** flow between **activity nodes**. It includes **control edges** and [object flow edges](https://www.uml-diagrams.org/activity-diagrams.html#object-flow-edge). The source and target of an edge must be in the same activity as the edge.

Activity edge is notated by an open arrowhead line connecting two activity nodes.

![Image 9: An activity edge is notated by an open arrowhead line connecting two activity nodes.](images/activity-edge-no-name.png)
**Activity edge** connects Fill Order and Review Order.

Edges can be named, however, edges are not required to have unique names within an activity. If the edge has a name, it is notated near the arrow.

![Image 10: Activity edge can be named. Name is shown near the arrow.](images/activity-edge-named.png)
**Activity edge** "updated" connects two nodes.

Activity edge can have a **guard** - specification evaluated at runtime to determine if the edge can be traversed. The guard must evaluate to true for every token that is offered to pass along the edge.

The **guard** of the activity edge is shown in square brackets that contain the guard.

![Image 11: Guard of the activity edge is shown in square brackets that contain the guard.](images/activity-edge-guard.png)
Fill Order when priority is 1

An activity edge can be notated using a **connector**, which is a small circle with a **name** inside. Though UML 2.4 specification calls it **name of the edge**, provided connector notation and examples suggest that connector has its own name (also called **label**).

Connectors are generally used to avoid drawing a long edge. This is purely notational. It does not affect the underlying model. The circles and lines involved map to a **single activity edge** in the model. Every connector with a given label must be paired with exactly one other with the same label on the same activity diagram. One connector must have exactly one incoming edge and the other exactly one outgoing edge, each with the same type of flow, object or control.

![Image 12: Connector is shown as small circle with label in it and is used to avoid drawing a long edge.](images/activity-edge-connector.png)
Connector A connects two edges between Fill Order and Review Order.

### Object Flow Edge

**Object flow** edges are [activity edges](https://www.uml-diagrams.org/activity-diagrams.html#activity-edge) used to show **data flow** of [object](https://www.uml-diagrams.org/activity-diagrams-objects.html#object-node) and data tokens between action nodes.

An object flow is notated by an arrowed line.

![Image 13: Object flow edges are activity edges used to show data flow between action nodes.](images/activity-edge-object-flow.png)
**Object flow** of **Orders** between Fill Order and Review Order actions

Any number of tokens can pass along the edge, in groups at one time, or individually at different times. The **weight** attribute dictates the **minimum number** of tokens that must traverse the edge at the same time. When the minimum number of tokens are offered, all the tokens at the source are offered to the target all at once.

The **weight** of the edge may be shown in curly braces that contain the weight. The weight is a value specification, which may be a constant, that evaluates to a non-zero unlimited natural value. An **unlimited weight** is notated as "*".

![Image 14: Weight of the edge may be shown in curly braces that contain the weight.](images/activity-edge-weight.png)
Send Notification when number of Warnings reaches 6.

### Interrupting Edge

**Interrupting edge** is activity edge expressing interruption for regions having interruptions. It is rendered as a lightning-bolt.

![Image 15: Interrupting edge is rendered as a lightning-bolt.](images/activity-edge-interrupting.png)
Cancel Request signal causes interruption resulting in Cancel Order.

An option for notating an interrupting edge is a zig zag adornment on a straight line.

![Image 16: Interrupting edge rendered as zig zag adornment on a straight line.](images/activity-edge-interrupting-zig-zag.png)
Cancel Request signal causes interruption resulting in Cancel Order.

  

This document describes UML versions up to **[UML 2.5](https://www.uml-diagrams.org/references.html#ref-uml-25 "UML 2.5 Specification")** and is based on the corresponding **OMG™ Unified Modeling Language™ (OMG UML®)** specifications. UML diagrams were created in **Microsoft® Visio®** 2007-2016 using **[UML 2.x Visio Stencils](http://softwarestencils.com/uml/index.html "Visio Stencil and Template for UML 2.5")**. You can send your comments and suggestions to [webmaster](mailto:webmaster@uml-diagrams.org). [Privacy policy](https://www.uml-diagrams.org/privacy-policy.html).

_Copyright © 2009-2026 uml-diagrams.org. All rights reserved. Authored by Kirill Fakhroutdinov._

![Image 17](images/www.uml-diagrams.org)

[](https://www.goodrx.com/conditions/weight-loss/bone-mass-decrease-with-weight-loss)[How to Protect Your Bone Health During Weight Loss GoodRx | [Sponsored](https://popup.taboola.com/en/?template=colorbox&utm_source=uml-diagrams&utm_medium=referral&utm_content=next-up-a-delta:Next%20Up:)[Sponsored](https://popup.taboola.com/en/?template=colorbox&utm_source=uml-diagrams&utm_medium=referral&utm_content=next-up-a-delta:Next%20Up:) Read Next Story](https://www.goodrx.com/conditions/weight-loss/bone-mass-decrease-with-weight-loss "How to Protect Your Bone Health During Weight Loss")
