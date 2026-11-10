---
source_url: "https://www.uml-diagrams.org/artifact.html"
crawled_at: "2026-11-10 07:12:36"
title: "artifact"
---

Title: UML artifact represents some physical entity or a piece of information that is used or is produced by a software development process.

URL Source: https://www.uml-diagrams.org/artifact.html

Markdown Content:
An **artifact** is a [classifier](https://www.uml-diagrams.org/classifier.html) that represents some **physical entity**, a piece of information that is used or is produced by a software development process, or by deployment and operation of a system. Artifact is a source of a [deployment](https://www.uml-diagrams.org/deployment-diagrams.html#deployment) to a [node](https://www.uml-diagrams.org/deployment-diagrams.html#node). A particular instance (or "copy") of an artifact is deployed to a node instance.

Some real life examples of UML artifacts are:

*   text document
*   source file
*   script
*   binary executable file
*   archive file
*   database table

The **UML****Standard Profile** defines several **standard stereotypes** that apply to artifacts:

«file»A physical file in the context of the system developed.

Standard stereotypes - subclasses of **«file»**:

«document»A generic file that is not a «source» file or «executable».
«source»A source file that can be compiled into an executable file.
«library»A static or dynamic library file.
«executable»A program file that can be executed on a computer system.
«script»A script file that can be interpreted by a computer system.

Standard UML 1.x stereotype that is now obsolete:

«table»Table in database.

Standard stereotypes can be further specialized into implementation and platform specific stereotypes in profiles. For example, Java profile might define **«jar»** as a subclass of «executable» for executable Java archives. Specific profiles are expected to provide some stereotype for artifact representing sets of files.

UML specifications define **artifact** as a subclass of abstract **deployed artifact**. Deployed artifact is described as an **artifact** or artifact instance that has been deployed to a [deployment target](https://www.uml-diagrams.org/deployment-diagrams.html#deployment-target). Common sense says that the relationship has to be reversed - deployed artifact should be a subclass of artifact, while it has to be allowed for some artifacts not to be deployed at all.

![Image 1: UML abstract syntax of Artifact.](https://www.uml-diagrams.org/deployment-diagrams/deployment-artifact-overview.png)

UML abstract syntax of Artifact.

Artifacts may have **properties** that represent [features](https://www.uml-diagrams.org/uml-core.html#feature) of the artifact, and [operations](https://www.uml-diagrams.org/operation.html) that can be performed on its instances. Artifacts have **fileName** attribute - a concrete name that is used to refer to the artifact in a physical context - e.g. **file name** or **URI**. Artifact could have nested artifacts.

Artifacts are deployed to a [deployment target](https://www.uml-diagrams.org/deployment-diagrams.html#deployment-target). **Instance specification** was extended in UML to allow instances of **artifacts** to be **deployed artifacts** in a [deployment](https://www.uml-diagrams.org/deployment-diagrams.html#deployment) relationship.

An artifact is presented using an ordinary class rectangle with the keyword **«artifact»**. Examples in **UML** specification also show **document icon** in upper right corner.

![Image 2: Artifact is presented using an ordinary class rectangle with the keyword artifact.](https://www.uml-diagrams.org/deployment-diagrams/deployment-artifact.png)

Artifact web-app.war

![Image 3: Artifact presented using an ordinary class rectangle with the keyword source.](https://www.uml-diagrams.org/deployment-diagrams/deployment-artifact-source.png)

C# source file artifact UserServices.cs

![Image 4: Artifact presented using an ordinary class rectangle with the keyword library](https://www.uml-diagrams.org/deployment-diagrams/deployment-artifact-library.png)

Library commons.dll

Alternatively, artifact may be depicted by an icon.

![Image 5: Artifact may be depicted by an icon.](https://www.uml-diagrams.org/deployment-diagrams/deployment-artifact-custom.png)

Artifact web-tools-lib.jar

Optionally, the underlining of the name of an artifact instance may be omitted, as the context is assumed to be known to users.

## Associations between Artifacts

Artifacts can be involved in [associations](https://www.uml-diagrams.org/association.html) to other artifacts, e.g. [composition](https://www.uml-diagrams.org/composition.html) associations. For instance, a deployment descriptor artifact for a component may be contained within the artifact that [manifests](https://www.uml-diagrams.org/deployment-diagrams.html#manifestation) that component. In that way, the component and its descriptor are deployed to a node instance as one artifact instance.

![Image 6: Deployment descriptor artifact for a component may be contained within the artifact that manifests that component](https://www.uml-diagrams.org/deployment-diagrams/deployment-artifact-composition.png)

Application book-club.ear artifact contains EJB user-service.jar artifact and deployment descriptor.

## Dependency between Artifacts

[Artifacts](https://www.uml-diagrams.org/artifact.html) can be involved in [dependency](https://www.uml-diagrams.org/dependency.html) relationship with other artifacts.

Dependency between artifacts is notated in the same way as general [dependency](https://www.uml-diagrams.org/dependency.html), i.e. as a general dashed line with an open arrow head directed from client artifact to supplier artifact.

![Image 7: Dependency shown as dashed line with an open arrow-head directed from client artifact to supplier artifact.](https://www.uml-diagrams.org/deployment-diagrams/deployment-artifact-dependency.png)

The book-club.war artifact depends on web-tools-lib.jar artifact.

![Image 8: Next](https://www.uml-diagrams.org/images/arrow-next.png)[Manifestation](https://www.uml-diagrams.org/deployment-diagrams.html#manifestation "UML manifestation")
