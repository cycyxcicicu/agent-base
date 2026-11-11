---
source_url: "https://www.uml-diagrams.org/sequence-diagrams-combined-fragment.html"
crawled_at: "2026-11-10 06:47:12"
title: "fragments"
---

Title: UML sequence diagram combined fragment is an interaction fragment which defines a combination (expression) of interaction fragments.

URL Source: https://www.uml-diagrams.org/sequence-diagrams-combined-fragment.html

Markdown Content:
**Combined fragment** is an [interaction fragment](https://www.uml-diagrams.org/sequence-diagrams.html#interaction-fragment) which defines a combination (expression) of interaction fragments. A combined fragment is defined by an **interaction operator** and corresponding **interaction operands**. Through the use of combined fragments the user will be able to describe a number of **traces** in a compact and concise manner.

Combined fragment may have [interaction constraints](https://www.uml-diagrams.org/sequence-diagrams-combined-fragment.html#interaction-constraint) also called **guards** in UML 2.4.

Interaction **operator** could be one of:

*   **alt** - [alternatives](https://www.uml-diagrams.org/sequence-diagrams-combined-fragment.html#operator-alt)
*   **opt** - [option](https://www.uml-diagrams.org/sequence-diagrams-combined-fragment.html#operator-opt)
*   **loop** - [iteration](https://www.uml-diagrams.org/sequence-diagrams-combined-fragment.html#operator-loop)
*   **break** - [break](https://www.uml-diagrams.org/sequence-diagrams-combined-fragment.html#operator-break)
*   **par** - [parallel](https://www.uml-diagrams.org/sequence-diagrams-combined-fragment.html#operator-par)
*   **strict** - [strict sequencing](https://www.uml-diagrams.org/sequence-diagrams-combined-fragment.html#operator-strict)
*   **seq** - [weak sequencing](https://www.uml-diagrams.org/sequence-diagrams-combined-fragment.html#operator-seq)
*   **critical** - [critical region](https://www.uml-diagrams.org/sequence-diagrams-combined-fragment.html#operator-critical)
*   **ignore** - [ignore](https://www.uml-diagrams.org/sequence-diagrams-combined-fragment.html#operator-ignore)
*   **consider** - [consider](https://www.uml-diagrams.org/sequence-diagrams-combined-fragment.html#operator-consider)
*   **assert** - [assertion](https://www.uml-diagrams.org/sequence-diagrams-combined-fragment.html#operator-assert)
*   **neg** - [negative](https://www.uml-diagrams.org/sequence-diagrams-combined-fragment.html#operator-neg)

## Interaction Constraint

An **interaction constraint** is a [constraint](https://www.uml-diagrams.org/constraint.html) used in interactions - a Boolean expression that **guards** an operand in a combined fragment.

An interaction constraint is shown in square brackets covering the [lifeline](https://www.uml-diagrams.org/sequence-diagrams.html#lifeline) where the first event occurrence will occur, positioned above that event, in the containing interaction or interaction operand.

UML 2.4 often refers to interaction constraint as a **guard**.

## Alternatives

The interaction operator **alt** means that the combined fragment represents a **choice** or alternatives of behavior. At most one of the operands will be chosen. The chosen operand must have an explicit or implicit guard expression that evaluates to true at this point in the interaction.

An implicit true guard is implied if the operand has no guard.

An operand guarded by **else** means a guard that is the negation of the disjunction of all other guards. If none of the operands has a guard that evaluates to true, none of the operands are executed and the remainder of the enclosing interaction fragment is executed.

![Image 1: Interaction operator alt example.](https://www.uml-diagrams.org/notation/sequence-operator-alt.png)

Call accept() if balance > 0, call reject() otherwise.

## Option

The interaction operator **opt** means that the combined fragment represents a **choice** of behavior where either the (sole) operand happens or nothing happens. An option is semantically equivalent to an alternative combined fragment where there is one operand with non-empty content and the second operand is empty.

![Image 2: Interaction operator opt example.](https://www.uml-diagrams.org/notation/sequence-operator-opt.png)

Post comments if there were no errors.

## Loop

The interaction operator **loop** means that the combined fragment represents a loop. The loop operand will be repeated a number of times. The loop construct represents a recursive application of the **seq** operator where the loop operand is sequenced after the result of earlier iterations.

UML 2.4 specification provides weird description of the loop operator with odd examples. I will try to extract here some sense from that.

Loop could be controlled by either or both iteration bounds and a guard.

Loop operand could have iteration bounds which may include a lower and an upper number of iterations of the loop. Textual syntax of the loop is:

loop-operand ::= **loop**[ '(' min-int [ ',' max-int ] ')' ]   
min-int ::= non-negative-integer  
max-int ::= positive-integer | '*'

If loop has no bounds specified, it means potentially infinite loop with zero as lower bound and infinite upper bound.

![Image 3: Potentially infinite loop.](https://www.uml-diagrams.org/notation/sequence-loop-infinite.png)

Potentially infinite loop.

If only min-int is specified, it means that upper bound is equal to the lower bound, and loop will be executed exactly the specified number of times.

![Image 4: Loop to execute exactly 10 times.](https://www.uml-diagrams.org/notation/sequence-loop-fixed.png)

Loop to execute exactly 10 times.

If max-int is specified, it should be greater than or equal to min-int. Loop will iterate minimum the min-int number of times and at most the max-int number of times.

Besides **iteration bounds** loop could also have an [interaction constraint](https://www.uml-diagrams.org/sequence-diagrams-combined-fragment.html#interaction-constraint) - a Boolean expression in square brackets. To add to the other confusions, UML 2.4 also calls both of them **guards**.

UML tries to shuffle the simplest form of **for loop** and **while loop** which causes weird UML 2.3 loop semantics on p.488 [[UML 2.3 - Superstructure]](https://www.uml-diagrams.org/references.html#ref-uml-23-super "UML 2.3 - Superstructure"): "after the minimum number of iterations have executed and the Boolean expression is false the loop will terminate". This is clarified - though with opposite meaning - on the next page as "the loop will only continue if that specification evaluates to true during execution regardless of the minimum number of iterations specified in the loop."

![Image 5: Loop will execute minimum 5 times max 10 times unless guard is false.](https://www.uml-diagrams.org/notation/sequence-loop-bounds-guard.png)

We may guess that as per UML 2.3, the loop is expected to execute  
 minimum 5 times and no more than 10 times.  
 If guard condition [size<0] becomes false loop terminates  
 regardless of the minimum number of iterations specified.  
 (Then why do we need that min number specified?!)

## Break

The interaction operator **break** represents a **breaking** or exceptional scenario that is performed instead of the remainder of the enclosing interaction fragment.

A break operator with a **guard** is chosen when the guard is true. In this case the rest of the directly enclosing interaction fragment is ignored. When the guard of the break operand is false, the break operand is ignored and the rest of the enclosing interaction fragment proceeds.

![Image 6: Break enclosing loop if y>0.](https://www.uml-diagrams.org/notation/sequence-operator-break.png)

Break enclosing loop if y>0.

A combined fragment with the operator **break** should cover all lifelines of the enclosing interaction fragment.

Note, UML allows only one level - directly enclosing interaction fragment - to be abandoned. This could become really annoying if double loop or loop with other combined fragments should be broken.

UML 2.3 states that when break operand has **no guard**, the choice between the break operand and the rest of the enclosing interaction fragment is done "non-deterministically" which most likely means "unpredictable". Don't use break without guard.

## Parallel

The interaction operator **par** defines potentially parallel execution of behaviors of the operands of the combined fragment. Different operands can be interleaved in any way as long as the ordering imposed by each operand is preserved.

Set of traces of the parallel operator describes all the possible ways or combinations that occurrence specifications of the operands may be interleaved without changing the order within each operand.

![Image 7: Search Google, Bing and Ask in any order, possibly parallel.](https://www.uml-diagrams.org/notation/sequence-operator-par.png)

Search Google, Bing and Ask in any order, possibly parallel.

Parallel combined fragment has notational shorthand for the common situations where the order of events on one [lifeline](https://www.uml-diagrams.org/sequence-diagrams.html#lifeline) is insignificant. In a **coregion** area of a lifeline restricted by horizontal square brackets all directly contained fragments are considered as separate operands of a parallel combined fragment.

![Image 8: Coregion - search Google, Bing and Ask in any order, possibly parallel.](https://www.uml-diagrams.org/notation/sequence-operator-par-coregion.png)

Coregion - search Google, Bing and Ask in any order, possibly parallel.

## Strict Sequencing

The interaction operator **strict** requires a strict sequencing (order) of the operands on the first level within the combined fragment.

![Image 9: Search Google, Bing and Yahoo in the strict sequential order.](https://www.uml-diagrams.org/notation/sequence-operator-strict.png)

Search Google, Bing and Yahoo in the strict sequential order.

Operands of lower levels within the contained combined fragment will not directly be compared with other occurrence specifications of the enclosing combined fragment. Notationally, this means that the vertical coordinate of the contained fragments is significant throughout the whole scope of the combined fragment and not only on one lifeline.

## Weak Sequencing

The interaction operator **seq** means that the combined fragment represents a weak sequencing between the behaviors of the operands.

Weak sequencing is defined by the set of traces with these properties:

*    The ordering of occurrence specifications within each of the operands is maintained. 
*    Occurrence specifications on different lifelines from different operands may come in any order. 
*    Occurrence specifications on the same lifeline from different operands are ordered such that an occurrence specification of the first operand comes before that of the second operand. 

**Weak** sequencing reduces to a **parallel** merge when the operands are on different sets of participants. Weak sequencing reduces to **strict** sequencing when the operands work on the same participant.

![Image 10: Search Google, Bing and Yahoo in the strict sequential order.](https://www.uml-diagrams.org/notation/sequence-operator-seq.png)

Search Google possibly parallel with Bing and Yahoo, but search Bing before Yahoo.

## Critical Region

The interaction operator **critical** defines that the combined fragment represents a **critical region**. A critical region is a region with traces that cannot be interleaved by other occurrence specifications (on the lifelines covered by the region). This means that the region is treated **atomically** by the enclosing fragment and can't be interleaved, e.g. by parallel operator.

![Image 11: Add() or remove() could be called in parallel, but each one should run as a critical region.](https://www.uml-diagrams.org/notation/sequence-operator-critical.png)

Add() or remove() could be called in parallel,  
 but each one should run as a critical region.

## Ignore

Semantics and the purpose of the interaction operator **ignore** is obscure. UML 2.3 defines its meaning as "there are some message types that are not shown within this combined fragment. These message types can be considered insignificant and are implicitly ignored if they appear in a corresponding execution. Alternatively, one can understand ignore to mean that the message types that are ignored can appear anywhere in the traces."

On the other hand, explanations to the Figure 14.25 on p. 530 [[UML 2.3 - Superstructure]](https://www.uml-diagrams.org/references.html#ref-uml-23-super "UML 2.3 - Superstructure") are that this kind of interaction could be used to specify a **test** of an existing system. At the runtime the messages ignored in tests "will of course be handled in some manner by the running system".

The list of ignored messages follows the operand enclosed in a pair of curly braces "{" and "}". Ignore operation is typically combined with other operations such as "assert ignore {m, s}."

![Image 12: Ignore get and set messages, if any.](https://www.uml-diagrams.org/notation/sequence-operator-ignore.png)

Ignore get() and set() messages, if any.

## Consider

The interaction operator **consider** defines which messages should be considered within this combined fragment, meaning that any other message will be ignored.

The list of considered messages follows the operand enclosed in a pair of curly braces "{" and "}". Consider operation is typically combined with other operations such as "assert consider {m, s}."

![Image 13: Consider only add() or remove() messages, ignore any other.](https://www.uml-diagrams.org/notation/sequence-operator-consider.png)

Consider only add() or remove() messages,  
 ignore any other.

## Assertion

The interaction operator **assert** means that the combined fragment represents the assertion that the sequences of the assert operand are the only valid continuations (must be satisfied by a correct design of the system). All other continuations result in an invalid trace.

![Image 14: Commit() message should occur, following with state invariant evaluation.](https://www.uml-diagrams.org/notation/sequence-operator-assert.png)

Commit() message should occur at this point,  
 following with evaluation of state invariant.

## Negative

The interaction operator **neg** describes combined fragment of traces that are defined to be **negative** (invalid). Negative traces are the traces which occur when the system has failed. All interaction fragments that are different from the negative are considered **positive**, meaning that they describe traces that are valid and should be possible.

![Image 15: Should we receive back timeout message, it means the system has failed.](https://www.uml-diagrams.org/notation/sequence-operator-neg.png)

Should we receive back timeout message,  
 it means the system has failed.
