# Redis

[交互式redis教程](http://try.redis.io/)

## What's redis?
Redis is in the family of databases called key-value stores.

The essence of a key-value store is the ability to store some data, called a value, inside a key. This data can later be retrieved only if we know the exact key used to store it. Often Redis it is called a **data structure server** because it has outer key-value shell, but each value can contain a complex data structure, such as a string, a list, a hashes, or ordered data structures called sorted sets as well as probabilistic data structures like hyperloglog.

All the Redis operations implemented by single commands are **atomic**, including the ones operating on more complex data structures. So when you use a Redis command that modifies some value, you don't have to think about concurrent access.

## Basic Operations

```
SET connections 10
INCR connections => 11
INCRBY connections 4 => 15
DECR connections => 14
DECRBY connections 4 => 10

# Delete a k/v pair
SET resource:lock "Redis Demo"
EXPIRE resource:lock 120

# Check how long it will exist.
TTL resource:lock => 113

// after 113s
TTL resource:lock => -2  # -2 means doesn't exist, -1 means the key will exist forever

# Cancel the time to live of a key
SET resource:lock "Redis Demo 3" EX 5
PERSIST resource:lock
TTL resource:lock => -1

```








