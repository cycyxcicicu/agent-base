# Transformation of UML Messages into Various Standard Formats

> **Nguồn gốc:** [https://sourcemaking.com/uml/modeling-for-system-integration/the-static-view/transformation-of-uml-messages-into-various-stan](https://sourcemaking.com/uml/modeling-for-system-integration/the-static-view/transformation-of-uml-messages-into-various-stan)  
> **Phân mục:** SourceMaking UML 2.0 / modeling-for-system-integration  
> **Số lượng hình ảnh:** 0  

---

/ UML
                                                / Modeling for System Integration

# Transformation of UML Messages into Various Standard Formats

All standard formats for data exchange, whetherebXML,SWIFT, orUN/EDIFACT, have their own way ofstructuringandrepresentingmessages.SWIFTmessages are described not only graphically, but also with text. The same is true forUN/EDIFACT, where the graphic illustrations are standardized through the use of branching diagrams.

The trend is clearly going into the direction of modeling messages in a fundamentally protocol and implementation neutral way, with UML.

Then all the standard formats can be derived from the representation in UML, the “mother of all messages”. Depending on availability this can even be done according to firmly defined transformation rules. (The profileUML Profile for Enterprise Distributed Object Computingwas developed as guidelines for the translation of UML descriptions into ‘real’ business systems. This profile, in turn, is based upon standards ofebXML.) Some of the arguments for choosing UML as a neutral form of representation are:

- System-and implementation-independent description of business objects and messages
- Accepted and widely used standard
- Option of depicting messages and business processes
- Unified language for the description of systems

An essential advantage of neutral message specification in UML is the much easier conversion of messages from one format to another. Because of this, we recommend the modeling of messages in UML first, and subsequently transforming messages into the appropriate format. Here, it is not important whether the target format is a standard format or an in-house proprietary format. Especially in the later case, it is much easier to convert a project from a proprietary format to a standard one if neutral UML specifications are available.

A detailed description of transformation rules would go well beyond the scope of this text. Because of this, we would like to refer toOMG'sModel Driven Architecture(MDA) and the two profilesUML Profile for Enterprise Distributed Object ComputingandUML Profile for Enterprise Application Integration, which provide comprehensive insight into this subject matter from a UML perspective.