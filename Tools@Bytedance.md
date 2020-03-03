# 一些实习需要学习的工具

## Euler - 基于Thrift的微服务框架
微服务框架风格是一种通过一组小的服务开发新的应用的方式，这些微服务在其自己的进程中运行并通过轻量级方式如HTTP进行通讯。

In short, the microservice architectural style is an approach to developing a single application as a suite of small services, each running in its own process and communicating with lightweight mechanisms, often an HTTP resource API. These services are built around business capabilities and independently deployable by fully automated deployment machinery. There is a bare minimum of centralized management of these services, which may be written in different programming languages and use different data storage technologies.

## Thrift

Thrift是一套包含序列化功能和支持服务通信的RPC框架，主要包含三大部分：代码生成、序列化框架、RPC框架，大致相当于protoc + protobuffer + grpc，并且支持大量语言，保证常用功能在跨语言间功能一致，是一套全栈式的RPC解决方案。整体架构图：

### IDL和代码生成
Interface Definition Languages 接口描述语言

The Apache Thrift framework is entirely focused on enabling programmers to design and construct **cross-language, distributed computing interfaces**. Interfaces consist of two principle parts:

- User-defined types (UDTs)—The things exchanged between systems
- Services—Sets of methods exposing cohesive functionality

Interface Definition Languages are designed to allow programmers to define interface contracts in an abstract fashion, **independent of** any programming language or system platform. IDL contracts ensure that all parties communicating over an interface know exactly what will be exchanged and how to exchange it. This allows tools to do the busy work of generating code to interoperate over the interface. **IDLs allow developers to focus on the problem domain, not the mechanics of remote procedure calls or cross-language serialization.**

