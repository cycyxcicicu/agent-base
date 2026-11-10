---
source_url: "https://www.uml-diagrams.org/deployment-diagrams-overview.html"
crawled_at: "2026-11-10 07:12:36"
title: "overview"
---

Title: UML deployment diagrams overview, common types of deployment diagrams

URL Source: https://www.uml-diagrams.org/deployment-diagrams-overview.html

Markdown Content:
**Deployment diagram** is a [structure diagram](https://www.uml-diagrams.org/uml-25-diagrams.html#structure-diagram) which shows architecture of the system as deployment (distribution) of software artifacts to deployment targets.

[Artifacts](https://www.uml-diagrams.org/artifact.html) represent concrete elements in the physical world that are the result of a development process. Examples of artifacts are executable files, libraries, archives, database schemas, configuration files, etc.

[Deployment target](https://www.uml-diagrams.org/deployment-diagrams.html#deployment-target) is usually represented by a [node](https://www.uml-diagrams.org/deployment-diagrams.html#node) which is either hardware device or some software execution environment. Nodes could be connected through [communication paths](https://www.uml-diagrams.org/deployment-diagrams.html#communication-path) to create networked systems of arbitrary complexity.

Note, that [components](https://www.uml-diagrams.org/component.html) were directly deployed to nodes in UML 1.x deployment diagrams. In UML 2.x [artifacts](https://www.uml-diagrams.org/artifact.html) are deployed to nodes, and artifacts could [manifest](https://www.uml-diagrams.org/deployment-diagrams.html#manifestation) (implement) components. Components are deployed to nodes indirectly through artifacts.

Deployment diagrams could describe architecture at **specification level** (also called type level) or at **instance level** (similar to class diagrams and object diagrams).

**Specification level** deployment diagram shows some overview of [deployment](https://www.uml-diagrams.org/deployment-diagrams.html#deployment) of [artifacts](https://www.uml-diagrams.org/artifact.html) to [deployment targets](https://www.uml-diagrams.org/deployment-diagrams.html#deployment-target), without referencing specific instances of artifacts or nodes.

**Instance level** deployment diagram shows [deployment](https://www.uml-diagrams.org/deployment-diagrams.html#deployment) of instances of [artifacts](https://www.uml-diagrams.org/artifact.html) to specific instances of [deployment targets](https://www.uml-diagrams.org/deployment-diagrams.html#deployment-target). It could be used for example to show differences in deployments to development, staging or production environments with the names/ids of specific build or deployment servers or devices.

Some common types of deployment diagrams are:

*   [Implementation (manifestation) of components by artifacts](https://www.uml-diagrams.org/deployment-diagrams-overview.html#deployment-manifestation-artifacts),
*   [Specification level deployment diagram](https://www.uml-diagrams.org/deployment-diagrams-overview.html#specification-level-deployment),
*   [Instance level deployment diagram](https://www.uml-diagrams.org/deployment-diagrams-overview.html#instance-level-deployment),
*   [Network architecture of the system](https://www.uml-diagrams.org/network-architecture-diagrams.html).

## Manifestation of Components by Artifacts

While [component diagrams](https://www.uml-diagrams.org/component-diagrams.html) show components and relationships between components and classifiers, and [deployment diagrams](https://www.uml-diagrams.org/deployment-diagrams-overview.html) - [deployments](https://www.uml-diagrams.org/deployment-diagrams.html#deployment) of artifacts to deployment targets, some missing intermediate diagram is **manifestation diagram** to be used to show [manifestation](https://www.uml-diagrams.org/deployment-diagrams.html#manifestation) (implementation) of [components](https://www.uml-diagrams.org/component.html) by [artifacts](https://www.uml-diagrams.org/artifact.html) and internal structure of artifacts.

Because **manifestation diagrams** are not defined by UML 2.4 specification, manifestation of components by artifacts could be shown using either component diagrams or deployment diagrams.

![Image 1: Deployment overview - manifestation of components by artifacts.](https://www.uml-diagrams.org/deployment-diagrams/deployment-diagram-overview-manifestation.png)

Manifestation of components by artifacts.

## Specification Level Deployment Diagram

Specification level (also called type level) deployment diagram shows some overview of [deployment](https://www.uml-diagrams.org/deployment-diagrams.html#deployment) of [artifacts](https://www.uml-diagrams.org/artifact.html) to [deployment targets](https://www.uml-diagrams.org/deployment-diagrams.html#deployment-target), without referencing specific instances of artifacts or nodes.

![Image 2: Specification level deployment diagram - web application deployed to Tomcat JSP server and database schemas - to database system.](https://www.uml-diagrams.org/deployment-diagrams/deployment-diagram-overview-specification.png)

Specification level deployment diagram - web application deployed to Tomcat JSP server and database schemas - to database system.

## Instance Level Deployment Diagram

Instance level deployment diagram shows [deployment](https://www.uml-diagrams.org/deployment-diagrams.html#deployment) of instances of [artifacts](https://www.uml-diagrams.org/artifact.html) to specific instances of [deployment targets](https://www.uml-diagrams.org/deployment-diagrams.html#deployment-target). It could be used for example to show differences in deployments to development, staging or production environments with the names/ids of specific deployment servers or devices.

In the example below, web application is deployed to the application server **wsrv-01** and several database schemas - to the database server **dbsrv-14**.

![Image 3: Instance level deployment diagram - web application deployed to Tomcat JSP server and database schemas - to database system.](https://www.uml-diagrams.org/deployment-diagrams/deployment-diagram-overview-instance.png)

Instance level deployment diagram - web application deployed to Tomcat JSP server and database schemas - to database system.

## Specification Level Network Architecture

Deployment diagrams could be used to show logical or physical [network architecture](https://www.uml-diagrams.org/network-architecture-diagrams.html) of the system. Network architecture diagram could show no artifacts or deployments at all or only the major ones.

![Image 4: Next](https://www.uml-diagrams.org/images/next-deploy.png)[Network architecture diagrams](https://www.uml-diagrams.org/network-architecture-diagrams.html "Network architecture diagrams")
