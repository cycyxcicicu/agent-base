# Communication Diagram

> **Nguồn gốc:** [https://sourcemaking.com/uml/modeling-it-systems/interaction-view/communication-diagram](https://sourcemaking.com/uml/modeling-it-systems/interaction-view/communication-diagram)  
> **Phân mục:** SourceMaking UML 2.0 / modeling-it-systems  
> **Số lượng hình ảnh:** 9  

---

/ UML
                                                / Modeling IT Systems

# Communication Diagram

![Figure 4.59 Elements of the communication diagram](images/img_167.jpg)

Figure 4.59 Elements of the communication diagram

In communication diagrams, as illustrated in Figure 4.59, we work with the following elements:

### Actor “Somebody”

Actor “somebody”represents any actor from a use case diagram. Since the query event that is documented in the communication diagram can be contained in several use cases, and since these use cases have different actors, we use the actor “somebody”:

![](images/img_168.jpg)

In this way, we do not have to commit ourselves to a particular actor. (In communication diagrams actors can also be omitted altogether. In our experience, however, this makes the diagrams hard to understand.)

### Query Event

A query event represents a query for information:

![](images/img_169.jpg)

Normally, a query event from a use case is sent to the IT system, for example, a query for detailed information about a ticket.

### Parameter

Parameters allow for attaching information to an event, e.g., the number of a ticket, so that the correct ticket can be read:

![](images/img_170.jpg)

### Iteration

An iteration indicates that all objects to which an association exists receive the event, for instance, all the coupons of a ticket:

![](images/img_171.jpg)

### Object and Entry Object

The object represents an object of a class in the static view, for instance, “Henry Johnson”, who is an object of the classpassenger:

![](images/img_172.jpg)

The entry object is the first object that receives a query event from an actor. At the entry object the interaction path begins.

## Reading Communication Diagrams

Figure 4.60 shows a communication diagram with the actorsomebodyand the objectsticket,customer,coupon,flight, andflight number. The diagram documents the flow of the query«Q» coupon details.

Starting on the left, the communication diagram is read as follows: Actorsomebody(1)sends the query event,«Q» coupon details(2)to an object of the classcoupon(3).

### Actor “Somebody”

In our IT system model, use cases are the source of events. What is documented in this communication diagram occurs in the context of a use case. It has proven to be of value to use the undefined actorsomebody(1)instead of the actor of the use case. The flow of an event that is described in the communication diagram can occur in various use cases with different actors. The actorsomebody(1)substitutes for the actor of the use case from which the query event«Q» coupon details(2)stems:

![Figure 4.60 Communication diagram](images/img_173.jpg)

Figure 4.60 Communication diagram

Thecoupon object(3)provides its attributes—date of redemption,class, andstandby(4)—and forwards the query event«Q» coupon details(5)to two other objects: to theflightobject(6)that belongs to the coupon, and to theticketobject(7)that belongs to thecoupon.

These two objects, in turn, provide certain attributes(8)and then forward the query event«Q» coupon details(9, 10). In this way, the communication diagram can be used to document the “collection” of attributes as a reaction to a query event.

Unlike sequence diagrams, communication diagrams do not have time dimensions. Objects can be spread across the diagrams in any way. An order in which events are processed can only be partially seen from them:

![Figure 4.61 Sequence in communication diagram](images/img_174.jpg)

Figure 4.61 Sequence in communication diagram

The following statements can be made about the sequence in the diagram in Figure 4.61 (the numbers in the descriptions were intentionally assigned to avoid implying any particular order):

- First, the event is sent from the actorsomebodyto thecoupon(5).
- After that a sequence is not defined:On the one hand, the event goes to theflight(1)and subsequently to theflight number(3).On the other hand, the event goes to theticket(7)and subsequently to thecustomer(9).

The event flow branches at the coupon, without noting an order. In most cases, order is unimportant anyway. However, should order be important, UML allows numbering the sequence of events in a communication diagram.

Iteration indicates that all reachable objects and not just one particular object are addressed:

![Figure 4.62 Iteration in communication diagram](images/img_175.jpg)

Figure 4.62 Iteration in communication diagram

We can read in Figure 4.62 that the query event«Q» pieces of luggage(1)is first sent to acouponobject(2)and from there is sent toall(3)(iteration) connectedpieces of luggage(4). The iteration is documented with an asterisk (*) in front of the event name.