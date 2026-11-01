# Messages in UML

> **Nguồn gốc:** [https://sourcemaking.com/uml/modeling-for-system-integration/messages-in-uml](https://sourcemaking.com/uml/modeling-for-system-integration/messages-in-uml)  
> **Phân mục:** SourceMaking UML 2.0 / modeling-for-system-integration  
> **Số lượng hình ảnh:** 0  

---

/ UML
                                                / Modeling for System Integration

# Messages in UML

In the UML sequence diagram, messages are illustrated with an arrow symbol, together with the name of the message and its parameters (if present). In this way, in UML a message is categorically divided into two parts:

- The name of the message specifies theevent.
- The arguments of the message contain theinformationthat is attached to the message, so that the receiver can perform the necessary activities. Control information belongs in this category as well.

We refer to the information that is exchanged as abusiness object, if the information:

- Is coherent
- Is structured
- Covers the requirements for a certain activity (e.g., invoice, passenger list)
- Is self-contained (no in-house reference keys, etc.)
- Outlives individual interactions

In the UML model of system integration, business objects are structured information sent as arguments in a message from a sender to a receiver.