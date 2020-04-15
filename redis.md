# Redis

[交互式redis教程](http://try.redis.io/)

## What's redis?
Redis is in the family of databases called key-value stores.

The essence of a key-value store is the ability to store some data, called a value, inside a key. This data can later be retrieved only if we know the exact key used to store it. Often Redis it is called a **data structure server** because it has outer key-value shell, but each value can contain a complex data structure, such as a string, a list, a hashes, or ordered data structures called sorted sets as well as probabilistic data structures like hyperloglog.

All the Redis operations implemented by single commands are **atomic**, including the ones operating on more complex data structures. So when you use a Redis command that modifies some value, you don't have to think about concurrent access.

## Basic Operations

```sql
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

# after 113s...
TTL resource:lock => -2  # -2 means doesn't exist, -1 means the key will exist forever

# Cancel the time to live of a key
SET resource:lock "Redis Demo 3" EX 5
PERSIST resource:lock
TTL resource:lock => -1

```

## Data Structure

This concept is generally true for every Redis data structure: you don't create a key first, and add things to it later, but you can **just directly use the command in order to add new elements**. As side effect the key will be create if it did not exist. Similarly keys that will result empty after executing some command will automatically be removed from the key space.

### List
```sql
# Commands: RPUSH, LPUSH, LLEN, LRANGE, LPOP, and RPOP...
RPUSH friends "Sam"
RPUSH friends "Alice"
RPUSH friends "Bob"
LRANGE friends 0 -1 => Sam Alice Bob
LPOP friends => "Sam"

# Push arbitrary num of elements
RPUSH friends 1 2 3 => 5
LLEN friends => 5
```
### Set
The next data structure that we'll look at is a set. A set is similar to a list, except it does not have a specific order and each element may only appear once. Both the data structures are very useful because while in a list is fast to access the elements near the top or the bottom, and the order of the elements is preserved, in a set is very fast to test for membership, that is, to immediately know if a given element was added or not. Moreover in a set a given element can exist only in a single copy.

```sql
# Commands: SADD, SREM, SISMEMBER, SMEMBERS and SUNION...
SADD superpowers "flight"
SADD superpowers "x-ray vision" "reflexes"

# Remove elements, 1 for exists
SREM superpowers "reflexes" => 1
SREM superpowers "making pizza" => 0

SISMEMBER superpowers "flight" => 1
SISMEMBER superpowers "reflexes" => 0
    
SMEMBERS superpowers => 1) "flight", 2) "x-ray vision"

# Union two sets
SADD birdpowers "pecking"
SADD birdpowers "flight"
SUNION superpowers birdpowers => 1) "pecking", 2) "x-ray vision", 3) "flight"
```

`SPOP` aims to extract elements from the set and return them to the client in a single operation. However since sets are not ordered data structures the returned (and removed) elements are totally casual in this case.

```sql
SADD letters a b c d e f => 6
SPOP letters 2 => 1) "c" 2) "a"
```

## Sorted Sets (zset)
A sorted set is similar to a regular set, but now each value has an associated score. This score is used to sort the elements in the set.

```sql
# 19xx are years of birth, used as ranking score
ZADD hackers 1940 "Alan Kay"
ZADD hackers 1906 "Grace Hopper"
ZADD hackers 1953 "Richard Stallman"
ZADD hackers 1965 "Yukihiro Matsumoto"
ZADD hackers 1916 "Claude Shannon"
ZADD hackers 1969 "Linus Torvalds"
ZADD hackers 1957 "Sophie Wilson"
ZADD hackers 1912 "Alan Turing"

ZRANGE hackers 2 4 => 1) "Claude Shannon", 2) "Alan Kay", 3) "Richard Stallman"
```

## Hash Table
```sql
HSET user:1000 name "John Smith"
HSET user:1000 email "john.smith@example.com"
HSET user:1000 password "s3cret"

# Set multiple fields
HMSET user:1001 name "Mary Jones" password "hidden" email "mjones@example.com"

# Get values
HGETALL user:1001
HGET user:1001 name => "Mary Jones"
```

Numerical values in hash fields are handled exactly the same as in simple strings and there are operations to increment this value in an atomic way.

```sql
HSET user:1000 visits 10
HINCRBY user:1000 visits 1 => 11
HINCRBY user:1000 visits 10 => 21
HDEL user:1000 visits
HINCRBY user:1000 visits 1 => 1
```


