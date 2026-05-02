---
title: "Dissecting the OASIS CAMP Specification"
date: 2015-02-18T10:34:00.001Z
lastmod: 2026-01-13T23:34:40.391Z
aliases:
  - /2015/02/dissecting-oasis-camp-specification.html
---
# 1. Background
## 1.1 OASIS - The organization behind CAMP
OASIS is a non-profit consortium that drives the development, convergence and adoption of open standards for the global information society. The consortium has representation from private/public sector technology leaders and influencers and has over 5K participants from over 600 organizations! They are behind various standards such as [MQTT](https://www.oasis-open.org/standards#mqttv3.1.1), Web services security etc., A full list is [here](https://www.oasis-open.org/standards).
## 1.2 CAMP (Cloud application management for platforms)
CAMP is an open specification defining artifacts and APIs that need to be offered by complying PaaS providers. It’s purpose is to enable interoperability among self-service interfaces to PaaS clouds so that applications can be (relatively) easily ported across different complying PaaS clouds. Why would people accept this?
  * PaaS consumers

    * Can achieve portability between clouds
    * Can benefit from quality implementations when accepted by a wide variety of people
  * Cloud Providers

    * The management API offered by a PaaS platform will most likely not be seen as a differentiator amongst competitors. Supporting an open specification will turn out be an advantage because customers would prefer compliant platforms over locked-in ones.
    * This will help providers address “portability between clouds” and thereby increase the market for PaaS consumption.
  * The spec draws from insights and experience of well known players and people in the field. The specification actually makes a good proposal of building robust and flexible PaaS offerings, at the same time giving enough hooks to the provider to customize where needed.


# 2. The CAMP Spec
## 2.1 TL;DR Version
Here is a mindmap capturing essentials of the spec.
![CAMP_mindmap](https://drive.google.com/file/d/0Bxij1Yjk6QNqcmxyWkpWQ0d1Rnc/view?usp=sharing)
[Download](https://drive.google.com/file/d/0Bxij1Yjk6QNqcmxyWkpWQ0d1Rnc/view?usp=sharing)
## 2.2 TL version
The full specification can be found [here](http://docs.oasis-open.org/camp/camp-spec/v1.1/camp-spec-v1.1.html) I will be examining the spec from the following angles:
  * PaaS Provider:
    * How does CAMP propose I design my resources?
    * What does it take to create a simple CAMP compliant paas platform?
    * Will the spec help me take care of specific issues/offerings unique to my PaaS?
  * App Developer:
    * How do I write my applications so that it becomes CAMP compliant?
    * Will the spec help me in articulating very specific requirements that I have for a given PaaS?


This post will touch upon CAMP spec in general. I will also do further posts looking into specific PaaS usecases (heroku, openshift, cloudfoundry etc.,) and how to model my app’s requirements using CAMP specification. Please note that, for the sake of brevity, I will not delve into greater detail into the aspects of platform extensions, metadata, type/parameter definitions etc., of the specification.
## 2.3 Diving in
### 2.3.1 Scope
The interfaces exposed by the components and services in a PaaS system can be broadly split into two categories; functional interfaces and management interfaces. Functional interfaces are those that involve the specific utility provided by that component. For example, the interface used to submit a message to a message queuing service is as a functional interface. Management interfaces are those that deal with the administration of components. For example, the interface used to deploy and start an application on the platform is a management interface. The specification of functional interfaces is out of scope for this document. In its core, CAMP v1.1 defines:
  * **Resources** : A set of resources that can be used to model a PaaS offering. The representation and operations on these resources are made available over secure RESTful APIs.
  * **PDP:** (Platform deployment package) format: Description of how an application needs to be packaged so that it can be hosted on a complying PaaS platform.


## 2.4 Resources
Most of the PaaS offerings provide self service management API for the platform so that developers and administrator can manage applications and its use of the platform. Below is a typical view of manageability provided by most PaaS platforms:
![Typical PaaS manageability architecture](http://docs.oasis-open.org/camp/camp-spec/v1.1/cs01/camp-spec-v1.1-cs01_files/image002.png)
_Courtesy: CAMP specification document_ The CAMP API is made up of resources in a REST protocol. The resources represent elements of the underlying system. The protocol enables interaction with the resources. The following are the main resources in the API: _Refer to the TL;DR version for an overview of resources_
### 2.4.1 Resource Definitions
#### 2.4.1.1. CAMP Resource
This is the base resource from which all other resources are implemented. Has the following attributes:
```http
uri: URI
name: String
description: String
tags: StringArray
type: String
representation_skew: String
```
#### 2.4.1.2. Platform
Identifies the CAMP provider platform and gives a primary view of what is running on the paas platform.
```text
supported_formats_uri: URI
extensions_uri: URI
type_definitions_uri : URI
platform_endpoints_uri: URI
specification_version: String
implementation_version: String
assemblies_uri: URI
services_uri: URI
plans_uri: URI
parameterDefinitions_uri: URI
```
#### 2.4.1.3. Assembly
Identifies an application on the platform. Is made up of components and services. Operations on this resource will effect its constituent components.
```http
components: LinkArray
plan_uri: URI
operations_uri: URI
sensors_uri: URI
```
#### 2.4.1.4. Assemblies
A collection of assembly resources.
```http
assembly_links: LinkArray
parameter_definitions_uri: URI
```
#### 2.4.1.5. Service
Blueprint for creating component resources that utilize or embody a platform provided service.
```http
parameter_definitions_uri: URI
characteristics: CharacteristicsSpecArray[]
```
#### 2.4.1.6. Services
A collection of service resources
```http
service_links: LinkArray
```
#### 2.4.1.7. Component
Rrepresents a discrete/dynamic element of an app. Ex. a deployed ruby gem, a war file, set of entries in LDAP directory etc.,
```text
assemblies: LinkArray
artifact:uri
service:uri
status: String
external_management_resource: URI
related_components: linkArray
operations_uri: URI
sensors_uri: URI
```
#### 2.4.1.8. Plan
Plan is the meta-data that provides a description of the artifacts and services that make up an application.
```javascript
camp_version : String
origin : String
artifacts : StringArray
services : StringArray
```
#### 2.4.1.9. Plans
Collection of plan resources
```http
plan_links: LinkArray
parameter_definitions_uri: URI
```
### 2.4.2 Resource Actions
Other than the standard operations allowed over HTTP (GET, POST, PUT, DELETE, PATCH etc.,), if there are other operations and values that need to be done over the defined resources, CAMP makes way for it by defining sensors and operations on any camp resource.
#### Sensors
A sensor resource exposes dynamic data about resources such as state, metrics, consumption etc., For instance, the start/stop/restart operations on an app can be defined as a Sensor whose type can be “STATE” and possible values can be “STARTED, STOPPED etc.,”. It is also possible to define operations on writeable sensors (ex. state, metrics collection frequency etc.,) _Sensor_
```text
target_resource:uri
sensor_type: String
value: String
timestamp : Timestamp
operations_uri: URI
```
_Sensors_
```http
target_resource: camp_resource
sensor_links: LinkArray
```
#### Operations
An operation resource represents actions that can be taken on a camp resource or it’s sensors. It affects the properties of a resource. _Operation_
```css
target_resource:uri
```
_Operations_
```text
operations
target_resource: uri
operation_links: LinkArray
```
Multiple operation resources and sensor resources can be exposed both on assembly resources and component resources. Operations are also known as effectors. The combination of Operations and Sensors enables ongoing management. This can include automation techniques such as using policies, event-condition-action paradigms, or autonomic control. A Consumer can use the REST API to perform such management. A Provider can also use them. For example, a component resource could be offered that allows for “autoscaling” capacity based on the volume of work an application performs.
### 2.4.3 Attribute types
The spec defines a top level CampCommonType. Further the following types are defined:
```vbnet
boolean
string
timestamp
uri
resource_state
link
linkarray
characterstic_spec
characterstic_spec_array
string_array
```
It is possible to extend the data types by using platform extensions and customizations.
### 2.4.4 Extensions and Customizations
  * The specification allows easy extendability by allowing extensions and capability to support multiple platform endpoints
  * Capability to define additional parameters on any camp_resource. The defined parameters above are normative and must be supported.
  * Capability to support multiple endpoints and versions. The spec also makes it easy for a consumer to discover the offering.


The spec also talks about resource relationships, possible extensions, customizations etc., in detail. I will not get into those details for the purpose of this document.
### 2.4.5 Representation skew
There can be situations in which the information in the resources provided by the CAMP API is not a complete or accurate representation of the state of the underlying implementation. For example, while generating a new instance of an application, a CAMP server might be asked to provide a representation of a Component that corresponds to a dataset that is in the process of being loaded onto a database. While the CAMP server might not be able to provide all of the information about this Component, it would be inaccurate to say that the Component does not exist; it exists but in an intermediate state. I Such exceptions can be represented using the `representation_skew` attribute of most camp resources.
## 2.5 Platform Deployment Package (PDP)
The other important aspect of the camp specification is the laying out of an application. PDP ensures portability across platforms.
### 2.5.1 PDP Package structure
  * Can be a .tar, .tgz or a .zip
  * Should contain camp.yaml (plan file) at the root of the package
  * Support for Integrity checks

    * A manifest file (camp.mf) containing sha256 digests of files in package
    * An X.509 certificate (camp.cert) at the root that contains signed sha256 digest for camp.mf with x.509 certificate.
    * Format of manifest is same as in OVF spec


### 2.5.2 Plan file
The Plan provides a description of the artifacts that make up an application, the services that are required to execute or utilize those artifacts, and the relationship of the artifacts to those services. As discussed previously, Plans can be represented in two ways, either as YAML files or as CAMP resources. The examples in this section show Plans as YAML files. A plan file is named as camp.yaml and should adhere to the YAML specification. If present, it should be in the root of the PDP.
#### 2.5.2.1 Type Nodes
Each node in the camp.yaml file is identified by its type node. ‘Type’ nodes are strings that describe entities that are managed by CAMP, but whose value and semantics are defined outside the specification. For example, a group of PaaS providers could agree to use the artifact type “org.rpm:RPM” to identify RPM packages.
#### 2.5.2.2 Artifacts
  * Units that make up the application
  * Identified by artifact_type which is a type node
  * content attribute refers to the location of the artifact
  * Each artifact can specify requirements indicating what to do with the artifact


#### 2.5.2.3 Requirements
  * identified by requirement_type (type node)
  * can specify specific flags relevant to the type of the requriement


Example:
```text
00 camp_version: CAMP 1.1
01 artifacts:
02   -
03     artifact_type: org.rpm:RPM
04     content: { my-app.rpm }
05     requirements:
06       -
07         requirement_type: org.rpm:Install
08         org.rpm.installopts.excludedocs: true
```
In the above yaml file, it is specified that the artifact’s requirement is that it needs to be installed. Further more, parameters specific to the requirement can also be specified - such as: `org.rpm.installopts.excludedocs: true`
#### 2.5.2.4 Fulfillment criteria
Each requirement can further specify how exactly that requirement has to be fulfilled. Each fulfillment criteria is made of characteristics that is identified by a `characterstic_type` and can contain additional types based on its type. Ex.
```text
00 camp_version: CAMP 1.1
01 artifacts:
02   -
03     artifact_type: org.rpm:RPM
04     content: { my-app.rpm }
05     requirements:
06       -
07         requirement_type: org.rpm:Install
08         org.rpm.installopts.excludedocs: true
09         fulfillment:
10           characteristics:
11             -
12               characteristic_type: com.example:Linux
13               com.example.linux.kernelVersion: [3.9.6]
14               org.iaas.bitsize: 64
```
In the above example, the developer is able to clearly articulate that the rpm he wants to install should be done so on a 64 bit linux machine with a kernel version of 3.9.6! Though this provides lot of flexibility, this comes at a cost of portability. Furthermore, most of the PaaS players will not let app developer / administrator get to such fine grained infrastructure level details for this falls into the IaaS realm!
#### 2.5.2.5 Services
Applications artifacts may need to share services (ex. db). Such requirements can be declared in a separate section called services and will be identified by its `id` attribute. Each artifact’s requirement criteria can now refer to the service spec via its uniqe id. Example:
```text
00 camp_version: CAMP 1.1
01 artifacts:
02   -
03     artifact_type: com.java:WAR
04     content: { href: vitaminder.war }
05     requirements:
06       -
07         requirement_type: com.java:HostOn
08         com.java.servlet.contextName: "/vitaM"
09         fulfillment:
10           …
11       -
12         requirement_type: com.java.jdbc:ConnectTo
13         fulfillment: id:db
14   -
15     artifact_type: org.sql:SqlScript
16     content: { href: vitaminder.sql }
17     requirements:
18       -
19         requirement_type: org.sql:ExecuteAt
20         fulfillment: id:db
21 services:
22   -
23     id: db
24     characteristics:
25       -
26         characteristic_type: org.storage.db:RDBM
27         …
28       -
29         characteristic_type: org.storage.db:Replication
30         …
31       -
32         characteristic_type: org.iso.sql:SQL
```
In the above example, both the warfile artifact and the sql_script artifact refer to the same database requirement using `id:db`.
* * *
