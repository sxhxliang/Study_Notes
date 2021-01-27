如果时间充裕，强烈建议学习 google C++ coding style 

## 目录
- Formatting
  - 用clang format来修正代码格式
    - Indentation 
    - Length of Functions
    - Class member declaration order
    - No commented code
    - TODO format
    - Proto format
    - 变量名定义
    - primitive 类型变量声明时候要赋初值
- Header Files
    - pragma once
    - Include what you use
    - Inline function
    - header 包括顺序
    - Header 中不要直接暴露using
- Scoping
    - Unnamed workspace and static variables
- Naming
    - Variable Names
    - Function Names
    - Enum Names
    - const 命名规范
    - 阈值变量命名
    - 用const variable代替magic number
- Functions
    - Function Inputs
    - Function Outputs 
- Classes
    - Structs Vs Classes
    - Structs Vs Pairs
- Other C++ Features
    - Auto
    - LOGGING
    - C++ 的类型转换
    - 使用base::Optional<>作为函数返回值
    - 智能指针使用
    - Exception (try catch)

## Formatting
用clang format来修正代码格式
```
XXX@meituan:~/autocar$ ./scripts/clang-format-diff
```

注意：需要安装clang-format
```
sudo apt install clang-format-8
```

注意：老的代码没有copyright等信息，所以检查时屏蔽了一些copyright等信息，但是新的代码仍然需要写上


## C++
```
python cpplint.py --linelength=80 --filter=-build/include_order,-build/namespaces,-legal/copyright,-runtime/references,-readability/multiline_string --recursive --extensions=h,cc modules/traffic_light/
Indentation 
```
只使用空格, 每次缩进 2 个空格.

### Length of Functions
为增强代码可读性，建议的函数长度为60-80行

### Class member declaration order
推荐按照下面的顺序声明类成员函数，常量和变量：

```cpp
class GeometryCameraConverter {
 public:
  GeometryCameraConverter();
  virtual ~GeometryCameraConverter();
  
  // Public function declaration.
  bool Init();
 
 private:
  // Using directives goes first.
  using Vector3f = Eigen::Matrix<float, 3, 1>;
  
  // Private function declaration.
  bool LoadCameraIntrinsics(const std::string &file_path);
  
  // Const variable definition.
  static constexpr int kMaxDistanceSearchDepth = 10;
  
  // Private variable definition.
  std::vector<Vector3f> corners_;
}  
```

### No commented code
不应该存在被注释掉的代码；不需要的代码请直接删除；调试用的代码尝试使用FLAG区分线上和线下环境。

### TODO format
TODO 的格式为

```cpp
// TODO(engineer name, date): XXX
```

### Proto format
注意Proto enum的写法和记得写Next id

```proto
// Next id: 7
enum SpecAreaType {
  DEFAULT = 1;
  UNKNOWN = 2;
  BUS_STATION = 3;
  NO_PERCEPTION = 4;
  ROUGH_ROAD = 5;
  ISOLATION_ZONE = 6;
}
​
// Next id: 6
message BitmapConfig {
  optional double range = 1 [default = 70.0];
  optional double cell_size = 2 [default = 0.2]; 
  optional bool is_extend = 3 [default = false];
  optional double extend_dist = 4 [default = 0.0];
  optional bool is_extend_hole = 5 [default = true];
}
```

### 变量名定义
```cpp
// 变量定义不要放在一行。
int32_t width_, height_;
std::unique_ptr<image::Image> lidar, lidar_ts, lidar_dr;
​
// 应该改成下面格式。
int32_t width_ = 0;
int32_t height_ = 0;
std::unique_ptr<image::Image> lidar;
std::unique_ptr<image::Image> lidar_ts;
std::unique_ptr<image::Image> lidar_dr;
```

### primitive 类型变量声明时候要赋初值

```cpp
struct LocalPointCloud{
  double timestamp = 0.0; // 注意浮点型赋值要写0.0不是0
  uint8 intensity = 0;
  float distance = 0.0f; // 注意float和double的区别
  float local_x = 0.0f;
  float local_y = 0.0f;
  float local_z = 0.0f;
};
```

## Header Files
### pragma once
使用#pragma once用来避免header被多次include

```cpp
// Copyright @2020 COMPANY Technology Inc. All rights reserved.
// Authors: XXX XX (XXXX@COMPANY.com)
​
#pragma once
```

### Include what you use
代码中直接引用自己使用到的内容，尤其是c++标准库中的头文件

```cpp
// a.h
#include <vector>
​
// b.h
#include <vector>  // 哪怕a.h中有了，也要再写一遍
#include "a.h"
```

### Inline function
建议只对小于10行的函数使用inline

### header 包括顺序
在 dir/foo.cc or dir/foo_test.cc中，因为其主要目的是实现和测试header： dir2/foo2.h, 所以你的header包括顺序因该按照如下顺序：
```
dir2/foo2.h.

A blank line

C system headers (more precisely: headers in angle brackets with the .h extension), e.g., <unistd.h>, <stdlib.h>.

A blank line

C++ standard library headers (without file extension), e.g., <algorithm>, <cstddef>.

A blank line

Other libraries' .h files.

Your project's .h files.
```

例如, 在 google-awesome-project/src/foo/internal/fooserver.cc header包括顺序为：

```cpp
#include "foo/server/fooserver.h"
​
#include <sys/types.h>
#include <unistd.h>
​
#include <string>
#include <vector>
​
#include "base/basictypes.h"
#include "base/commandlineflags.h"
#include "foo/server/bar.h"
```

### Header 中不要直接暴露using
在hdmap_lanes.h中，using 直接写在了header里class定义的外面，这样只要包括了这个header，就会造成在walle::perception这个命名空间下都会共享这些alias，可能造成不必要的bug。

```cpp
namespace walle {
namespace perception {
 
using apollo::hdmap::LaneInfoConstPtr;
using math::Vector2d;
using math::Vector3d;
 
class HDMapLanes {
  ...
}
​
}  // namespace perception
}  // namespace walle
```

可以改成：

```cpp
namespace walle {
namespace perception {
 
class HDMapLanes {
 public：
  using LaneInfoConstPtr = apollo::hdmap::LaneInfoConstPtr;
  using Vector2d = math::Vector2d;
  using Vector3d = math::Vector3d;
  ...
}
​
}  // namespace perception
}  // namespace walle
```

## Scoping
### Unnamed workspace and static variables
应将所有文件内可见的属性如using和参数包裹在一个unnamed workspace中。如此可以提升代码的可读性和安全性。

例如：

```cpp
void PerceptionProcessor::GenerateExtraInfo() {
  base::JsonUtil::AddJsonObjectIntoJson(&evaluation_result_, "extra_info");
  base::JsonUtil::AddJsonObjectIntoJson(&(evaluation_result_["extra_info"]), "type_label_num");
  for (const auto& type_str : kTypeStringMap) {
    base::JsonUtil::AddJsonObjectIntoJson(&(evaluation_result_["extra_info"]["type_label_num"]), type_str.second);
    evaluation_result_["extra_info"]["type_label_num"][type_str.second] =
        statistical_extra_info_.type_label_num[type_str.second];
  }
  evaluation_result_["extra_info"]["frame_num"] = statistical_extra_info_.frame_num;
  evaluation_result_["extra_info"]["label_num"] = statistical_extra_info_.all_label_num;
}
```
应替换为：

```cpp
namespace apollo {
namespace perception {
​
namespace {
constexpr char kExtraInfo[] = "extra_info";
constexpr char kTypeLabelNum[] = "type_label_num";
constexpr char kLabelNum[] = "label_num";
constexpr char kFrameNum[] = "frame_num";
constexpr char kAllType[] = "all";
}  // namespace
​
void PerceptionProcessor::GenerateExtraInfo() {
  base::JsonUtil::AddJsonObjectIntoJson(&evaluation_result_, kExtraInfo);
  base::JsonUtil::AddJsonObjectIntoJson(&(evaluation_result_[kExtraInfo]), kTypeLabelNum);
  for (int i = 0; i < config_.valid_type_size(); ++i) {
      const std::string type_str = GetObjectName(static_cast<apollo::perception::ObjectType>(config_.valid_type(i)));
    base::JsonUtil::AddJsonObjectIntoJson(&(evaluation_result_[kExtraInfo][kTypeLabelNum]), type_str);
    evaluation_result_[kExtraInfo][kTypeLabelNum][type_str] = 0;
  }
  for (const auto& type_label_num : statistical_extra_info_.type_label_num) {
    evaluation_result_[kExtraInfo][kTypeLabelNum][type_label_num.first] = type_label_num.second;
  }
  evaluation_result_[kExtraInfo][kFrameNum] = statistical_extra_info_.frame_num;
  evaluation_result_[kExtraInfo][kLabelNum] = statistical_extra_info_.all_label_num;
}
```

## Naming
### Variable Names
通常变量使用小写字母、下划线区分单词

```cpp
std::string traffic_light_name;
```
class的data member规则同1，但是以下划线结尾

```cpp
class CameraCalibration {
  std::string device_name_;
  PinholeData pinhole_data_;
  base::Optional<Rigid3d> lidar_to_camera_;
  base::Optional<Rigid3d> imu_to_camera_;
}
```
struct的data member规则同1，注意无下划线结尾

```cpp
struct PinholeData {
  int height = 0;
  int width = 0;
  double focal_x = 0.;
  double focal_y = 0.;
  double center_x = 0.;
  double center_y = 0.;
};
```

### 通用命名规则

为了代码的可读性变量名要有描述性

```cpp
// Good case
int price_count_reader;    // 无缩写
int num_errors;            // "num" 是一个常见的写法
int num_dns_connections;   // 人人都知道 "DNS" 是什么
​
// Bad case
int a;                     // 毫无意义.
int nerr;                  // 含糊不清的缩写.
int n_comp_conns;          // 含糊不清的缩写.
int wgc_connections;       // 只有贵团队知道是什么意思.
int pc_reader;             // "pc" 有太多可能的解释了.
int cstmr_id;              // 删减了若干字母.
​
// Bad case, str毫无意义，hasdualreturn最好单词间用_隔开
RangeImage(const std::string& str, int yaw, int pitch, int data_channel, int bytes, bool hasdualreturn);
```

### Function Names
通常每个单词的首字母大写

```cpp
void RecordLidarExtrinsic(const LidarExtrinsic& extrinsic);
```
变量的get和set函数可以使用类似变量名的命名方式(无下划线结尾)

```cpp
class CameraCalibration {
 public:
  const std::string& device_name() const;
  int width() const;
  const Rigid3d& lidar_to_camera() const;
  const Rigid3d& imu_to_camera() const;
}
```

### Enum Names
建议优先使用Enum Class，所有Enum名字都和const变量命名一样（以小写k开头，后面每个单词首字母大写）

```cpp
enum class UrlTableError {
  kOk = 0,
  kOutOfMemory,
  kMalformedInput,
};
```

注意: 推荐使用 enum class

### const 命名规范
推荐使用constexpr, 变量名以小写“k”开头

```cpp
class Bar { 
 ...
 private:
  static constexpr int kJpegMaxSize = 1024 * 1024 * 16;
  static constexpr char kClockName[] = "SimulationClock";
}
​
void Foo() {
  constexpr int kColumnWidth = 50;
}
```

### 阈值变量命名
```cpp
// 不好的命名。使用的时候不知道是用">"还是"<" 
double distance_threshold_ = 5.0;
int num_point_threshold_ = 10;
​
// 好的命名。
double min_distance_ = 5.0;
int max_num_point_ = 10;
```

### 用 const variable 代替 magic number
推荐的用法：

```cpp
const int kFenceParamSize = 4;
// ...
if (values.size() != kFenceParamSize) {
  LOG(ERROR) << "Invalid hacking fence: " << iter.first;
  return false;
}
hacking_fence_.emplace_back(math::Vector2d(values[0], values[1]),
                            math::Vector2d(values[2], values[3]));
```
不推荐的用法：

```cpp
if (values.size() != 4) {
  LOG(ERROR) << "Invalid hacking fence: " << iter.first;
  return false;
}
hacking_fence_.emplace_back(math::Vector2d(values[0], values[1]),
                            math::Vector2d(values[2], values[3]));
```

## Functions
### Function Inputs
函数的输入变量类型按照const， primitive， non-const排序， 例如:

```cpp
void FunctionInputExample(const T& A, const T& B, int a, boolean b, T* output);
```

自定义函数按照引用传递的参数除非特殊情况都应该是 const

```cpp
// 错误使用
void Foo(string& in, string* out); 
​
// 正确使用
void Foo(const string& in, string* out); 
```

### Function Outputs 
函数可以通过return值和输出参数来输出。

优先使用return值作为输出：这样能够提高代码的可读性，有时候甚至能够带来更好的性能。C++ Copy Elision

推荐的用法：

```cpp
std::vector<PolygonDType> road_polygons = MergeRoadBoundariesToPolygons(hdmap_struct_ptr->road_boundary);
...
std::vector<PolygonDType> HdmapUtil::MergeRoadBoundariesToPolygons(const std::vector<RoadBoundary>& road_boundaries) {
...
}
```
不推荐的用法：

```cpp
std::vector<PolygonDType> road_polygons;
MergeRoadBoundariesToPolygons(hdmap_struct_ptr->road_boundary, &road_polygons);
...
void HdmapUtil::MergeRoadBoundariesToPolygons(const std::vector<RoadBoundary>& road_boundaries,
                                              std::vector<PolygonDType>* polygons) {
...
}
```

## Classes
### Structs Vs Classes
语法上，struct和class的唯一区别是struct中成员默认访问权限是public，而class的默认访问权限是private

struct用来定义包含数据的被动式对象, 也可以包含相关的常量，所有字段保持public，用户可直接访问struct中的字段，无需get或set函数

注意：struct和class中成员变量的命名方式不同

```cpp
struct LaserConfig {
  explicit LaserConfig(int num_lasers);
  virtual ~LaserConfig() = default;
  int num_lasers = 0;
  std::vector<double> horizontal_angle_offset;
  std::vector<double> horizontal_angle[kLidarMaxAzimuth];
  std::vector<double> sin_horizontal_angle[kLidarMaxAzimuth];
  std::vector<double> cos_horizontal_angle[kLidarMaxAzimuth];
  std::vector<double> vertical_angle;
  std::vector<double> sin_vertical_angle;
  std::vector<double> cos_vertical_angle;
  std::vector<int> laser_order;
  std::vector<int> inverse_laser_order;
};
```

### Structs Vs Pairs
当成员可以用有意义的变量名来表示时，推荐使用struct 而不是pair或者a tuple，例如

```cpp
// 可读性不好的代码
std::vector<std::vector<std::pair<int, double>>> label_to_obstacle_map(obstacles.size());
for (int i = 0; i < obstacles.size(); ++i) {
  label_to_obstacle_map.push_back(std::make_pair(i, 0.5));
}
...
std::sort(label_to_obstacle_map[i].begin(), label_to_obstacle_map[i].end(),
          [](const std::pair<int, double>& a, const std::pair<int, double>& b) {
              return a.second > b.second;});
```
```cpp
// 可读性好的代码
struct MatchedObstacle {
  int obstacle_idx = -1;
  double iou = 0.0;
};
std::vector<std::vector<MatchedObstacle>> label_to_obstacle_map(obstacles.size());
for (int i = 0; i < obstacles.size(); ++i) {
  MatchedObstacle matched_obstacle;
  matched_obstacle.obstacle_idx = i;
  matched_obstacle.iou = 0.5;
  label_to_obstacle_map.push_back(matched_obstacle);
}
...
std::sort(label_to_obstacle_map[i].begin(), label_to_obstacle_map[i].end(),
          [](const MatchedObstacle& a, const MatchedObstacle& b) {
              return a.iou > b.iou;});
```
```cpp
// 可读性不好的代码: 用户拿到结果后需要到函数实现中找first/second分别代表什么
template <typename DataType>
std::pair<double, double> GetPacketAzimuthRange(const LidarRawPacket& raw_packet, int block_cnt) {
  constexpr double kLidarAzimuthMultiple = 100.0;
  CHECK_EQ(raw_packet.raw_data().size(), sizeof(DataType));
  const DataType* data = reinterpret_cast<const DataType*>(raw_packet.raw_data().data());
  double start_azimuth = static_cast<double>(data->block[0].azimuth) / kLidarAzimuthMultiple;
  double end_azimuth =
      static_cast<double>(data->block[block_cnt - 1].azimuth) / kLidarAzimuthMultiple;
  return std::make_pair(start_azimuth, end_azimuth);
}
```
​
```cpp
// 可读性好的代码
struct AzimuthRange {
  double start = 0.0;
  double end = 0.0;
}
​
template <typename DataType>
AzimuthRange GetPacketAzimuthRange(const LidarRawPacket& raw_packet, int block_cnt) {
  constexpr double kLidarAzimuthMultiple = 100.0;
  CHECK_EQ(raw_packet.raw_data().size(), sizeof(DataType));
  const DataType* data = reinterpret_cast<const DataType*>(raw_packet.raw_data().data());
  AzimuthRange range;
  range.start = static_cast<double>(data->block[0].azimuth) / kLidarAzimuthMultiple;
  range.end = static_cast<double>(data->block[block_cnt - 1].azimuth) / kLidarAzimuthMultiple;
  return range;
}
```

## Other C++ Features
### Auto
为了保证可读性，在代码中我们不用过度使用auto。auto只应该被用在类型较为明确，或者无关的地方。

推荐的用法：

```cpp
auto bitmap = std::make_shared<Bitmap2D>(min_p, max_p, grid_size, major_dir);

std::unordered_map<string, int> name_to_id;
for (const auto& entry : name_to_id) {
  const std::string& name = entry.first;
  int id = entry.second;
}
```

不推荐的用法：

```cpp
auto& mapped_boundary = (*mapptr)->road_boundary[i];
```

### LOGGING
统一使用GLOG，例如对于ERROR，统一使用LOG(ERROR)，而不再使用apollo 的 AERROR等宏。

```cpp
if (some_ptr == nullptr) {
  LOG(ERROR) << "some_ptr is empty!!!";
  // Instead of:
  // AERROR << "some_ptr is empty!!!"; 
}
​
CHECK(another_ptr != nullptr);
// Instead of:
// ACHECK(another_ptr != nullptr);
```

### C++ 的类型转换
使用 C++ 的类型转换, 如 static_cast<>(). 不要使用 int y = (int)x 或 int y = int(x) 等转换方式;

- 用 static_cast 替代 C 风格的值转换, 或某个类指针需要明确的向上转换为父类指针时.

- 用 const_cast 去掉 const 限定符.

- 用 reinterpret_cast 指针类型和整型或其它指针之间进行不安全的相互转换. 仅在你对所做一切了然于心时使用.
- 用 dynamic_cast 有条件转换，动态类型转换，运行时检查类型安全（转换失败返回NULL）
- 使用base::Optional<>作为函数返回值

有时函数中要同时返回一个值和一个状态，会写成下面的方式：


```cpp
bool LoadExtrinsic(const walle::OnboardContextBase* onboard_context, const std::string& file_path, Rigid3d* rigid3d) {
  std::string absolute_path;
  base::Status status = onboard_context->GetCalibrationConfigRealPath(file_path, &absolute_path);
  if (!status.ok()) {
    LOG(ERROR) << "Failed to get config real path for " << file_path;
    return false;
  }
  return LoadExtrinsic(absolute_path, rigid3d);
}
```

推荐使用base::Optional<> 写成下面的方式：

```cpp
base::Optional<Rigid3d> LoadExtrinsic(const walle::OnboardContextBase* onboard_context, const std::string& file_path) {
  std::string absolute_path;
  base::Status status = onboard_context->GetCalibrationConfigRealPath(file_path, &absolute_path);
  if (!status.ok()) {
    LOG(ERROR) << "Failed to get config real path for " << file_path;
    return base::none;
  }
  Rigid3d rigid3d;
  LoadExtrinsic(absolute_path, &rigid3d);
  return rigid3d;
}
```

### 智能指针使用
推荐对每个生成的类实例有唯一并且固定的所有者，推荐使用智能指针来管理实例的所有权，除个别case代码里不应该出现new和delete关键字。对所有权和智能指针的好处请见 link

```cpp
// 代码中不应该出现如下使用方法，需要明确SensorObjects的所有权，不应该滥用shared_ptr.
class CameraObstacleSubnode {
 public:
  std::shared_ptr<SensorObjects> GetObstacle() {
     ...
     std::shared_ptr<SensorObjects> sensor_objects(new SensorObjects);
     ...
     return sensor_objects;
  }
}
​
// 可以改成
class CameraObstacleSubnode {
 public:
  const SensorObjects& GetObstacle() {
     return sensor_objects;
  }
  
  void ProcessFrames() {
    // Update sensor_objects inside this function.
  }
 
 private:
  SensorObjects sensor_objects;
}
```

### Exception (try catch)
线上代码不要使用用try catch，使用LOG(FATAL) 或者 CHECK 终止运行