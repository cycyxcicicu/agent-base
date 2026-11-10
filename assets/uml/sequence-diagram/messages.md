---
source_url: "https://www.uml-diagrams.org/interaction-message.html"
crawled_at: "2026-11-10 06:47:12"
title: "messages"
---

Title: UML Message defines specific kind of communication between lifelines of an interaction.

URL Source: https://www.uml-diagrams.org/interaction-message.html

Markdown Content:
**Message** is a [named element](https://www.uml-diagrams.org/uml-core.html#named-element) that defines one specific kind of communication between [lifelines](https://www.uml-diagrams.org/sequence-diagrams.html#lifeline) of an interaction. The message specifies not only the kind of communication, but also the sender and the receiver. Sender and receiver are normally two **occurrence specifications** (points at the ends of messages).

Syntax for the message is:

message ::= [ attribute'='] signal-or-operation-name [ arguments ] [':' return-value ] |'*'   
arguments ::= '('[argument[','argument]*')'   
argument ::= [ parameter-name '='] argument-value |attribute '=' out-parameter-name [':' argument-value ] |' -'

Arguments of a message could only be:

*   attributes of the sending lifeline,
*   constants,
*   symbolic values (which are wildcard values representing any legal value),
*   explicit parameters of the enclosing interaction,
*   attributes of the class owning the interaction.

A message is shown as a line from the sender message end to the receiver message end. The line must be such that every line fragment is either horizontal or downwards when traversed from send event to receive event. The send and receive events may both be on the same lifeline. The form of the line or arrowhead reflects properties of the message.

## Messages by Action Type

A message reflects either an [operation](https://www.uml-diagrams.org/operation.html) call and start of execution or a sending and reception of a [signal](https://www.uml-diagrams.org/common-behaviors.html#signal).

When a message represents an operation call, the arguments of the message are the arguments of the operation. When a message represents a signal, the arguments of the message are the attributes of the signal.

Depending on the type of [action](https://www.uml-diagrams.org/activity-diagrams-actions.html) that was used to generate the message, message could be one of:

*   [synchronous call](https://www.uml-diagrams.org/interaction-message.html#synchronous-call)
*   [asynchronous call](https://www.uml-diagrams.org/interaction-message.html#asynchronous-call)
*   [asynchronous signal](https://www.uml-diagrams.org/interaction-message.html#asynchronous-signal)
*   [create](https://www.uml-diagrams.org/interaction-message.html#create)
*   [delete](https://www.uml-diagrams.org/interaction-message.html#delete)
*   [reply](https://www.uml-diagrams.org/interaction-message.html#reply)

### Synchronous Call

**Synchronous call** typically represents operation call - send message and suspend execution while waiting for response. Synchronous call messages are shown with filled arrow head.

![Image 1: Web Client searches Online Bookshop and waits for results.](https://www.uml-diagrams.org/notation/sequence-message-synchro-call.png)

Web Client searches Online Bookshop and waits for results.

### Asynchronous Call

**Asynchronous call** - send message and proceed immediately without waiting for return value. Asynchronous messages have an open arrow head.

![Image 2: Service starts Task and proceeds in parallel without waiting.](https://www.uml-diagrams.org/notation/sequence-message-asynchro-call.png)

Service starts Task and proceeds in parallel without waiting.

### Asynchronous Signal

**Asynchronous signal** message corresponds to asynchronous [send signal action](https://www.uml-diagrams.org/activity-diagrams-actions.html#send-signal-action).

### Create Message

**Create** message is sent to a [lifeline](https://www.uml-diagrams.org/sequence-diagrams.html#lifeline) to create itself. It is shown as a dashed line with open arrowhead (looks the same as [reply message](https://www.uml-diagrams.org/interaction-message.html#reply)), and pointing to the created lifeline's head.

![Image 3: Online Bookshop creates Account.](https://www.uml-diagrams.org/notation/sequence-message-create.png)

Online Bookshop creates Account.

Note, that this weird convention to send a message to a nonexisting object to create itself is used both in UML 1.x and 2.x. In OOAD practice create message should probably be sent to the **class**, see [Message in OOAD](https://www.uml-diagrams.org/uml-object-oriented-concepts.html#message) discussion for the backgound information. In Smalltalk-80 new objects are created by sending messages **to classes**, with an instance of the class created and returned back. So one way to interpret UML create message notation is probably as a shortcut for these actions.

### Delete Message

**Delete** message (called **stop** in previous versions of UML) is sent to terminate another [lifeline](https://www.uml-diagrams.org/sequence-diagrams.html#lifeline). The lifeline usually ends with a cross in the form of an **X** at the bottom denoting [destruction occurrence](https://www.uml-diagrams.org/sequence-diagrams.html#destruction-occurrence-seq).

UML 2.4 specification provides neither specific notation for delete message nor a stereotype. Until they provide some notation, we can use custom «destroy» stereotype.

![Image 4: Online Bookshop terminates Account.](https://www.uml-diagrams.org/notation/sequence-message-delete.png)

Online Bookshop terminates Account.

### Reply Message

**Reply** message to an operation call is shown as a dashed line with open arrow head (looks similar to **creation message**).

![Image 5: Web Client searches Online Bookshop and waits for results to be returned.](https://www.uml-diagrams.org/notation/sequence-message-return.png)

Web Client searches Online Bookshop and waits for results to be returned.

## Messages by Presence of Events

Depending on whether message send event and receive events are present, message could be one of:

*   **complete message**
*   [lost message](https://www.uml-diagrams.org/interaction-message.html#lost-message)
*   [found message](https://www.uml-diagrams.org/interaction-message.html#found-message)
*   **unknown message** (default)

The semantics of a **complete** message is the trace <sendEvent, receiveEvent>. Both sendEvent and receiveEvent are present.

**Unknown message** - both sendEvent and receiveEvent are absent (should not appear).

### Lost Message

**Lost Message** is a message where the sending event is known, but there is no receiving event. It is interpreted as if the message never reached its destination. The semantics is the trace <sendEvent>, receiveEvent is absent. Lost messages are denoted with as a small black circle at the arrow end of the message.

![Image 6: Web Client sent search message which was lost.](https://www.uml-diagrams.org/notation/sequence-message-lost.png)

Web Client sent search message which was lost.

### Found Message

**Found Message** is a message where the receiving event is known, but there is no (known) sending event. It is interpreted as if the origin of the message is outside the scope of the description. This may for example be noise or other activity that we do not want to describe in detail. The semantics is simply the trace: <receiveEvent>, while send event is absent.

Found Messages are denoted with a small black circle at the starting end of the message.

![Image 7: Online Bookshop gets search message of unknown origin.](https://www.uml-diagrams.org/notation/sequence-message-found.png)

Online Bookshop gets search message of unknown origin.
