---
source_url: "https://www.uml-diagrams.org/package-import.html"
crawled_at: "2026-11-10 07:12:36"
title: "package-import"
---

Title: UML Package import is a relationship between an importing namespace and a package to allow the use of unqualified names to refer to the package members.

URL Source: https://www.uml-diagrams.org/package-import.html

Warning: Target URL returned error 400: Bad Request

Markdown Content:
**Package import** is a [directed relationship](https://www.uml-diagrams.org/uml-core.html#directed-relationship) between an importing [namespace](https://www.uml-diagrams.org/namespace.html) and imported [package](https://www.uml-diagrams.org/package-diagrams.html#package), that allows the use of unqualified names to refer to the package members from the other namespace(s).

Importing namespace adds the names of the members of the imported package to its own namespace. Conceptually, a package import is equivalent to having an [element import](https://www.uml-diagrams.org/element-import.html) to each individual member of the imported namespace, unless there is already a separately-defined element import.

A package import is shown using a dashed arrow with an open arrowhead from the importing namespace to the imported package.

![Image 1: Package import shown using a dashed arrow with an open arrowhead from the importing namespace to the imported package](https://www.uml-diagrams.org/package-diagrams/package-package-import-default.png)

WebApplication imports Presentation package.

Note, that though it looks exactly like [dependency](https://www.uml-diagrams.org/dependency.html) and [usage](https://www.uml-diagrams.org/dependency.html#usage) relationships, it is a completely separate **directed relationship**.

The **visibility** of a package import could be either public or private. If the package import is **public**, the imported elements will be added to the namespace and made visible outside the namespace, while if it is **private** they will still be added to the namespace but without being visible outside.

A keyword is shown near the dashed arrow to identify which kind of package import is intended. The predefined keywords are **«import»** for a **public** package import, and **«access»** for a **private** package import. By default, the value of visibility is public.

![Image 2: Public package import shown using a import keyword, private - using access keyword](https://www.uml-diagrams.org/package-diagrams/package-package-import-access.png)

**Private import** of Presentation package and **public import** of Domain package

As an alternative to the dashed arrow, it is possible to show an package import by having a text that uniquely identifies the imported package within curly brackets either below or after the name of the namespace. The syntax in this case could be described as (note, this is my modified version of the syntax):

package-import ::= '{'('import'|'access')qualified-name'}'

Elements that become available for use in an importing package through a package import may have a distinct color or be dimmed to indicate that they cannot be modified.

![Image 3: Next](https://www.uml-diagrams.org/images/arrow-next.png)[Package merge](https://www.uml-diagrams.org/package-merge.html "Package merge")
