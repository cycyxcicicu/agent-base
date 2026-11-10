---
source_url: "https://www.uml-diagrams.org/use-case-diagrams-how-to.html"
crawled_at: "2026-11-10 06:47:12"
title: "how-to"
---

Title: How to Draw UML Use Case Diagram

URL Source: https://www.uml-diagrams.org/use-case-diagrams-how-to.html

Markdown Content:
There are several approaches on how to draw UML use case diagrams. If you don't know from where to start, try to follow the steps described here.

## Define Subject

[Subject](https://www.uml-diagrams.org/use-case-subject.html) is a business, software system, subsystem, component, device, etc. that we are designing or just trying to understand how it is working. It is very important to define what kind of system it is, and what is its scope or boundary. Give it a proper name, and use appropriate [stereotype](https://www.uml-diagrams.org/stereotype.html), e.g. «Business» or «Subsystem».

For example, we want to describe a **Pharmacy**, and it is not software pharmacy prescription system but actual pharmacy business. So, we will draw it as shown below, using «Business» stereotype.

![Image 1: Use case business Pharmacy as UML subject.](https://www.uml-diagrams.org/use-case-diagrams/subject-business-pharmacy.png)

«Business» Pharmacy as UML subject.

Another example of a subject shown below is **Ticket vending machine**, i.e. vending machine that sells and produces tickets to commuters. This kind of machine is a combination of both hardware and software, and it is only a part of the whole system selling tickets to the customers. So we will use «Subsystem» stereotype.

![Image 2: Ticket vending machine as UML subject.](https://www.uml-diagrams.org/use-case-diagrams/subject-ticket-vending-machine.png)

Ticket vending machine as UML subject.

Here are some other examples of UML subject name:

*   Department Store
*   Airport
*   Automated Teller Machine (ATM)
*   Point of Sale (POS) Terminal
*   Online Travel Reservation System
*   Electronic Prescription Service

By declaring a subject we are defining boundaries of the system, to be able to determine what or who is inside the system, and what or who is outside of it.

## Define Actors

UML [actor](https://www.uml-diagrams.org/use-case-actor.html) is some type, group or particular facet of users that require some services from the subject. Actor is an **external entity**, which could be a human user of the designed system, or some other system or device using our system.

For the Pharmacy business we defined above, Customer is an example of an actor. Customer uses services provided by pharmacy. Pharmacist working in the pharmacy is not an actor, he or she is part of the business and is usually called business worker.

![Image 3: Customer is a business actor for the Pharmacy business.](https://www.uml-diagrams.org/use-case-diagrams/business-pharmacy-customer.png)

Customer is a business actor for the Pharmacy business.

Ticket vending machine allows commuters to buy tickets. So Commuter is our actor in this case.

![Image 4: Commuter is an actor for the ticket vending machine.](https://www.uml-diagrams.org/use-case-diagrams/actor-commuter.png)

Commuter is an actor for the ticket vending machine.

Actors should have names according to the role they play in relation to our system. Examples of actor names (user roles):

*   Supplier
*   Passenger
*   Receptionist
*   Web Client
*   Bank
*   Payment Authorization System

## Define Use Cases

Now as we defined the boundaries of the system that we are designing or analysing, and external users of the system, we need to define what do those users need from the system. Each [use case](https://www.uml-diagrams.org/use-case.html) specifies a unit of **complete** and **useful functionality** that the subject provides to the actor(s). Use case should reflect user needs and goals, and should be initiated by an actor.

For the pharmacy customer a business use case would be to get some medicine. So we are adding **Procure Medicines** business use case. Business actor Customer participating in the business use case should be connected to the use case by association.

![Image 5: Business use case Procure Medicines for the Customer of the Pharmacy business.](https://www.uml-diagrams.org/use-case-diagrams/business-use-case-procure-medicine.png)

Business use case Procure Medicines for the Customer  
 of the Pharmacy business.

The ultimate goal of the Commuter in relation to our ticket vending machine is to buy a ticket. So we are adding **Purchase Ticket** use case. Purchasing ticket might involve a bank, if payment is to be made using a debit or credit card. So we are also adding another actor - **Bank**. Both actors participating in the use case should be connected to the use case by association.

![Image 6: Ticket vending machine supports Purchase Ticket use case for the Commuter and Bank actors.](https://www.uml-diagrams.org/use-case-diagrams/use-case-purchase-ticket.png)

Ticket vending machine provides Purchase Ticket use case  
 for the Commuter and Bank actors.

Top-level use cases should describe complete unit of functionality provided to the actor. Examples of use case names:

*   Hire Employee
*   Transfer Funds
*   Find Book
*   Make Travel Reservations
*   Schedule Patient Appointment

## Describe Use Case Behaviors

Use case [behaviors](https://www.uml-diagrams.org/common-behaviors.html#behavior) may be described in a natural language text (opaque behavior), which is current common practice, or by using UML [behavior diagrams](https://www.uml-diagrams.org/uml-25-diagrams.html#behavior-diagram) for specific behaviors such as

*   [activity](https://www.uml-diagrams.org/activity-diagrams.html#activity),
*   [state machine](https://www.uml-diagrams.org/state-machine-diagrams.html#behavioral-state-machine),
*   [interaction](https://www.uml-diagrams.org/interaction.html).

UML tools should allow linking behaviors to the described use case. Example of such binding of a use case to the behavior represented by activity is shown below using UML 2.5 notation.

![Image 7: Purchase Ticket use case owns behavior represented by Purchase Ticket activity.](https://www.uml-diagrams.org/use-case-diagrams/use-case-purchase-ticket-owned-behaviors.png)

Purchase Ticket use case owns behavior  
 represented by Purchase Ticket activity.

Purchase Ticket activity diagram example below describes behavior of the Purchase Ticket use case.

![Image 8: Example of Purchase Ticket use case behavior described using activity diagram.](https://www.uml-diagrams.org/examples/activity-example-ticket-vending-machine.png)

Example of Purchase Ticket use case behavior described using activity diagram.

![Image 9: Next](https://www.uml-diagrams.org/images/arrow-next.png)[Use case diagrams examples](https://www.uml-diagrams.org/use-case-diagrams-examples.html "Use case diagrams examples")
