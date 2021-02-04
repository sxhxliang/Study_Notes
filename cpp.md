# C++

## 智能指针
### 1. std::shared_ptr
![](https://www.google.com/url?sa=i&url=http%3A%2F%2Fzhaoyan.website%2Fxinzhi%2Fcpp%2Fhtml%2Fcppsu43.html&psig=AOvVaw1VpPukzttPqgph7AeLsAGi&ust=1612509471923000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCOjdtIXYz-4CFQAAAAAdAAAAABAO)

shared_ptr basic 1: create shared_ptr from new. make_shared is better than inside new, inside new is better than outside new.
```cpp
string * cp = new string("hello␣world"); 
 
shared_ptr<string> ps = cp; // NOT allow 
 
//method1: use constructor 
shared_ptr<string> ps (cp); //ok, but not good style 
shared_ptr<string> ps (new string("hello␣world")); //good style 
 
//method2: make_unique 
unique_ptr<string> ps( std::make_shared<string>("hello␣world") );
```

shared_ptr basic 2: Create shared_ptr from another shared_ptr
```cpp
shared_ptr<string> ps1 (new string("hello␣world")); 
 
shared_ptr<string> ps2 ( ps1 ); 
//use_count of ps1 and ps2 are all 2 
 
shared_ptr<string> ps2 ( move(ps1) ); 
// use_count of ps2 is 1, and ps1 is 0. 
________________________________________//Just transfer use_count to ps2, not ownership.
```

shared_ptr basic 3: shared_ptr assignment
```cpp
shared_ptr<string> ps1 (new string("ps1")); 
shared_ptr<string> ps2 (new string("ps2")); 
 
//method1: use assignment 
ps1= ps2; 
___________________________// 1) previous use_count decrements 1(If equal 0, will delete) 
___________________________// 2) ps1 points to current use_count 
___________________________// 3) and current use_count increments 1 
 
//method2: use move 
ps1 = std::move(ps2); 
___________________________// 1) previous use_count decrements 1(If equal 0, will delete) 
___________________________// 2) ps1 points to current use_count 
___________________________// 3) ps2 will not point to use_count, ps1 point it, but NOT increment 1 
 
 
//method3: reset 
ps1.reset(cp); //ok 
//pointer inside previous ps1 will be deleted.
```

shared_ptr basic 4: Just observer, not transfer ownership , you can get pointer, or use shared_ptr reference.
```cpp
shared_ptr<string> ps1 (new string("ps1")); 
 
fun(string* pstr); 
fun(shared_ptr<string> & ref_ptr);
```

#### When are control block created?
- std::make_shared always creates a control block. It manufactures a new object to point to, so there is certainly no control block for that object at the time std::make_shared is called.
- A control block is created when a std::shared_ptr is constructed from a unique-ownership pointer (i.e., a std::unique_ptr ). As part of its construction, the std::shared_ptr assumes ownership of the pointed-to object, so the uniqueownership pointer is set to null.
- When a std::shared_ptr constructor is called with a raw pointer, it creates a control block.
- std::shared_ptr constructors taking std::shared_ptrs or std::weak_ptrs as constructor arguments do NOT create new control blocks, because they can rely on the smart pointers passed to them to point to any necessary control blocks

#### Like std::unique_ptr, std::shared_ptr uses delete as its default resource-destruction mechanism, but it also supports custom deleters.
```cpp
std::unique_ptr< Widget, decltype(loggingDel) > 
                               upw(new Widget, loggingDel); 
// deleter type is ptr type 
 
std::shared_ptr<Widget> spw(new Widget, loggingDel); 
 // deleter type is not part of ptr type
```

In order to correctly use shared_ptr with an array, you must supply a custom deleter.
```cpp
template< typename T > 
struct array_deleter { 
  void operator ()( T const * p){ 
    delete[] p; 
  } 
}; 
 
std::shared_ptr<int> sp( new int[10], array_deleter<int>() );
```

- If the program uses more than one pointer to an object, shared_ptr is your choice. Such as you have two objects that contain pointers to the same third object. Or you may have an STL container of pointers.

#### There are at least two lessons regarding std::shared_ptr use here. 
1) try to avoid passing raw pointers to a std::shared_ptr constructor. 
2) use `make_share()`. 
3) if you have customed delete and can’t use `make_share()`, pass the result of `new` directly instead of going through a raw pointer variable.
```cpp
auto pw = new Widget; // pw is raw ptr 
 
std::shared_ptr<Widget> spw1(pw, loggingDel); 
// create control block for *pw 
std::shared_ptr<Widget> spw2(pw, loggingDel); 
// create 2nd control block for *pw! 
 
 
std::shared_ptr<Widget> spw1(new Widget, loggingDel); 
// direct use of new 
std::shared_ptr<Widget> spw2(spw1);
```

Sometimes, I want to keep file alive, because foo and bar will use them.

You can’t use RAII auto object, since it will be deleted outsied function scope. And If you use raw pointer, It’s difficult to trace and delete it. shared_ptr is the best options right now. you don’t needs to worry about deleting file - once both foo and bar have finished and no longer have any references to file (probably due to foo and bar being destroyed), file will automatically be deleted.
```cpp
void setLog(const Foo & foo, const Bar & bar) { 
//File file("/path/to/file", File::append);              //1) RAII auto obj 
//File* file = new File("/path/to/file", File::append);  //2) raw new 
   shared_ptr<File> file = 
              new File("/path/to/file", File::append);   //3) best 
   foo.setLogFile(file); 
   bar.setLogFile(file); 
}
```
