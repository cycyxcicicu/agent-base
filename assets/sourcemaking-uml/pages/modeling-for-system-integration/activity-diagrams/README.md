# Activity Diagrams

> **Nguồn gốc:** [https://sourcemaking.com/uml/modeling-for-system-integration/process-view/activity-diagrams](https://sourcemaking.com/uml/modeling-for-system-integration/process-view/activity-diagrams)  
> **Phân mục:** SourceMaking UML 2.0 / modeling-for-system-integration  
> **Số lượng hình ảnh:** 7  

---

/ UML
                                                / Modeling for System Integration

# Activity Diagrams

We explained the basic elements of activity diagrams inActivity Diagrams. Therefore, here we will only go into the special interpretations and supplemental uses of activity diagrams for system integration.

From the activity diagram in Figure 5.5, we can already extract some initial information for the integration of IT systems for the processno boarding. For example, we can learn which business objects are exchanged, etc.

![Figure 5.5 Activity diagram “No Boarding”](images/img_200.jpg)

Figure 5.5 Activity diagram “No Boarding”

![Figure 5.6 Elements of the activity diagram](images/img_201.jpg)

Figure 5.6 Elements of the activity diagram

### Activity

In activity diagrams one single activity is depicted as shown in Figure 5.6. In our context, an activity represents a business process. Actions, control elements (decision, branching, merge, start, end, etc.), and objects are essential parts of an activity.

These elements are connected to each other with so-called edges. The connected actions and control elements make up the control flow, which can also be called theflow:

![](images/img_202.jpg)

The object flow represents the path of objects that move through the activity. The object flow can also be omitted when constructing activity diagrams. Carrying out an activity can include several parallel flows.

### Object Flow (Edge)

Edges, which are depicted as arrows, connect the individual components of the activity diagram and represent the control flow and object flow (edge) of the activity. The control flow determines the flow within an activity. The incoming arrow starts an individual step of an activity. After this step is completed the flow continues along the outgoing arrow. The object flow describes the flow of objects and data within activities. Edges can be labeled with a name (close to the arrow):

![](images/img_203.jpg)

The object flow in an activity diagram shows the path of one or more business objects between the various activities.

### Acceptinga Signal (Action)

The sending of signals means that a signal is sent to a receiving activity:

![](images/img_204.jpg)

The receiving activity accepts the signal with the actionaccepting a signaland can respond accordingly, meaning, according to the flow that comes from this node in the activity diagram.

### Business Object

A business object consists of structured data that is exchanged between actions (seeMessages in UML). Generally, the business object that is the output of one action is simultaneously the input of another action:

![](images/img_205.jpg)

A business object that leaves its original activity partition is sent from one IT system to another IT system.

## Reading Activity Diagrams

![Figure 5.7 Activity diagram](images/img_206.jpg)

Figure 5.7 Activity diagram

Activity diagrams show the interaction between the various IT systems that are involved in the message exchange. Figure 5.7 shows that the IT system ofpassenger services(1)initiates the action sendingpassenger list(3)through the eventpassenger list requested(2), and that the business objectpassenger list(4)is sent to the IT system ofcustoms at destination airport(5). The IT system of customs at the destination airport accepts thepassenger list(4)with the actionreceiving passenger list(6).

In this diagram, we cannot see that the business object passenger list is sent as the argument of a message. In order to see this, we need to use a sequence diagram.