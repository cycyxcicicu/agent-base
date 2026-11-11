---
source_url: "https://www.uml-diagrams.org/package-diagrams-overview.html"
crawled_at: "2026-11-10 07:12:36"
title: "overview"
---

Title: UML package diagrams overview - common types of package diagrams

URL Source: https://www.uml-diagrams.org/package-diagrams-overview.html

Warning: Target URL returned error 400: Bad Request

Markdown Content:
**Package diagram** is **UML**[structure diagram](https://www.uml-diagrams.org/uml-25-diagrams.html#structure-diagram) which shows structure of the designed system at the level of [packages](https://www.uml-diagrams.org/package-diagrams.html#package). The following elements are typically drawn in a package diagram: [package](https://www.uml-diagrams.org/package-diagrams.html#package), [packageable element](https://www.uml-diagrams.org/package-diagrams.html#packageable-element), [dependency](https://www.uml-diagrams.org/dependency.html), [element import](https://www.uml-diagrams.org/element-import.html), [package import](https://www.uml-diagrams.org/package-import.html), [package merge](https://www.uml-diagrams.org/package-merge.html).

[Model diagram](https://www.uml-diagrams.org/package-diagrams-overview.html#model-diagram) is UML auxiliary [structure diagram](https://www.uml-diagrams.org/uml-25-diagrams.html#structure-diagram) which shows some abstraction or specific view of a system, to describe architectural, logical or behavioral aspects of the system. It could show, for example, architecture of a multi-layered (aka multi-tiered) application - [multi-layered application model](https://www.uml-diagrams.org/multi-layered-application-uml-model-diagram-example.html).

## Package Diagram

Some major elements of the package diagram are shown on the drawing below. Web Shopping, Mobile Shopping, Phone Shopping, and Mail Shopping [packages](https://www.uml-diagrams.org/package-diagrams.html#package)[merge](https://www.uml-diagrams.org/package-merge.html) Shopping Cart package. The same 4 packages [use](https://www.uml-diagrams.org/dependency.html) Payment package. Both Payment and Shopping Cart packages [import](https://www.uml-diagrams.org/package-import.html) other packages.

![Image 1: UML package diagram elements - package, import, access, use, merge.](https://www.uml-diagrams.org/package-diagrams/package-diagram-elements.png)

UML package diagram elements - package, import, access, use, merge.

## Model Diagram

**Model diagram** is UML auxiliary [structure diagram](https://www.uml-diagrams.org/uml-25-diagrams.html#structure-diagram) which shows some abstraction or specific view of a system, to describe some architectural, logical or behavioral aspects of the system.

The drawing below shows some major elements of the model diagram. Layered Application is a ["container" model](https://www.uml-diagrams.org/package-diagrams/model.html) which contains three other [models](https://www.uml-diagrams.org/package-diagrams/model.html) - Presentation Layer, Business Layer, and Data Layer. There are [dependencies](https://www.uml-diagrams.org/dependency.html) defined between these contained models.

![Image 2: UML model diagram elements - model, package, dependency, import.](https://www.uml-diagrams.org/package-diagrams/model-diagram-elements.png)

UML model diagram elements - model, package, dependency.

Models usually contain [packages](https://www.uml-diagrams.org/package-diagrams.html#package). Packages could have [dependencies](https://www.uml-diagrams.org/dependency.html) or other relationships, e.g. [import](https://www.uml-diagrams.org/package-import.html), defined between them.

You can find some [examples of package diagrams](https://www.uml-diagrams.org/package-diagrams-examples.html) here:

*   [Multi-Layered Application Model](https://www.uml-diagrams.org/multi-layered-application-uml-model-diagram-example.html)
*   [Multi-Layered Web Architecture](https://www.uml-diagrams.org/multi-layered-web-architecture-uml-package-diagram-example.html)
*   [Java Servlet 2.5 API](https://www.uml-diagrams.org/examples/java-servlet-25-api-package-diagram-example.html?context=pkg-examples)
*   [Java Servlet 3.0 API](https://www.uml-diagrams.org/examples/java-servlet-30-api-package-diagram-example.html?context=pkg-examples)
*   [Spring and Hibernate DAO Classes](https://www.uml-diagrams.org/spring-hibernate-uml-package-diagram-example.html)

![Image 3: Next](https://www.uml-diagrams.org/images/arrow-next.png)[Package](https://www.uml-diagrams.org/package-diagrams.html#package "Package")
