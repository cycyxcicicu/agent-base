---
source_url: "https://www.uml-diagrams.org/element-import.html"
crawled_at: "2026-11-10 07:12:36"
title: "element-import"
---

Title: UML element import is a relationship between an importing namespace and imported packageable element to allow the element to be referenced using its name.

URL Source: https://www.uml-diagrams.org/element-import.html

Markdown Content:
**Element import** is a [directed relationship](https://www.uml-diagrams.org/uml-core.html#directed-relationship) between an importing [namespace](https://www.uml-diagrams.org/namespace.html) and imported [packageable element](https://www.uml-diagrams.org/package-diagrams.html#packageable-element). It allows the element to be referenced using its name without a qualifier. An element import is used to selectively import individual elements without relying on a [package import](https://www.uml-diagrams.org/package-import.html).

The name of the packageable element or its alias is to be added to the namespace of the importing namespace. It works by reference, which means that it is not possible to add features to the element import itself, but it is possible to modify the referenced element in the namespace from which it was imported.

It is possible to control whether the imported element can be further imported by other namespaces using either element or package imports. The visibility of the element import may be either the same or more restricted than that of the imported element. The visibility of an element import is either public or private.

The default visibility is the same as that of the imported element. If the imported element does not have a visibility, it is possible to add visibility to the element import. Default value is public.

In case of a name clash with an outer name (an element that is defined in an enclosing namespace is available using its unqualified name in enclosed namespaces) in the importing namespace, the outer name is hidden by an element import, and the unqualified name refers to the imported element. The outer name can be accessed using its qualified name.

If more than one element with the same name would be imported to a namespace as a consequence of element imports or package imports, the elements are not added to the importing namespace and the names of those elements must be qualified in order to be used in that namespace. If the name of an imported element is the same as the name of an element owned by the importing namespace, that element is not added to the importing namespace and the name of that element must be qualified in order to be used.

**Alias** specifies the name that should be added to the namespace of the importing [package](https://www.uml-diagrams.org/package-diagrams.html#package) in lieu of the name of the imported packagable element. The aliased name must not clash with any other member name in the importing package. By default, no alias is used.

An element import is shown using a dashed arrow with an open arrowhead from the importing namespace to the imported element. **Note**, that though it looks exactly like [dependency](https://www.uml-diagrams.org/dependency.html) and [usage](https://www.uml-diagrams.org/dependency.html#usage) relationships, it is a completely separate [directed relationship](https://www.uml-diagrams.org/uml-core.html#directed-relationship).

The keyword **«import»** is shown near the dashed arrow if the visibility of import is **public** while the keyword **«access»** is used to indicate **private** visibility. If the imported element is not a package, the keyword may optionally be preceded by element, i.e., «element import».

![Image 1: Public element import shown using a import keyword, private - using access keyword.](https://www.uml-diagrams.org/package-diagrams/package-element-import-access.png)

Public import of PageInfo element and private import of SortInfo element from Domain package.

Elements that become available for use in an importing package through an element import may have a distinct color or be dimmed to indicate that they cannot be modified.

The aliased name may be shown after or below the keyword «import».

As an alternative to the dashed arrow, it is allowed to show an element import by having a text that uniquely identifies the imported element within curly brackets either below or after the name of the namespace. The syntax in this case could be described as (note, this is my modified version of the syntax):

element-import ::= '{'('element import'|'element access')qualified-name['as'alias]'}'

![Image 2: Next](https://www.uml-diagrams.org/images/arrow-next.png)[Package import](https://www.uml-diagrams.org/package-import.html "Package import")
