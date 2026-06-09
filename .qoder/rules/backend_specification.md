---
trigger: glob
glob: *.java, *.kt, pom.xml, *.gradle, application.yml
---

# Java 后端工程规范

适用版本：Java 17+, Spring Boot 3.x  
参考来源：Google Java Style Guide, 阿里巴巴 Java 开发手册, Spring Framework Documentation

## 一、项目结构

```
src/main/java/{groupId}/{artifactId}/
├── config/              # 配置类
├── controller/          # REST 控制器
├── service/             # 业务接口
│   └── impl/           # 业务实现
├── repository/          # 数据访问层
├── entity/             # 实体类
├── dto/                 # 数据传输对象
├── exception/           # 异常定义
├── util/                # 工具类
└── Application.java     # 启动类
```

## 二、命名规范

| 类型 | 风格 | 正例 | 反例 |
|------|------|------|------|
| 类名 | PascalCase | `UserService` | `userService` |
| 方法名 | camelCase | `getUserById` | `GetUserById` |
| 变量名 | camelCase | `userName` | `_userName` |
| 常量 | SCREAMING_SNAKE | `MAX_RETRY` | `maxRetryCount` |
| 包名 | 全小写 | `com.example` | `com.Example` |

## 三、格式化规范

- 缩进：4 个空格（不使用 Tab）
- 行长度：100 字符
- 大括号：K&R 风格（左大括号不换行）
- 方法之间空 1 行，逻辑块之间空 1 行

```java
// ✅ 正确：K&R 风格
if (condition) {
    doSomething();
} else {
    doOther();
}
```

## 四、注释规范

```java
/**
 * 类功能描述。
 *
 * @param paramName 参数说明
 * @return 返回值说明
 * @throws ExceptionType 异常说明
 */
```

- ✅ 注释解释业务规则（Why），不解释代码本身（What）
- ❌ 避免无意义注释如 `i++; // i 自增`

## 五、依赖注入

```java
// ✅ 推荐：构造器注入（保证不可变性，便于测试）
@Service
@RequiredArgsConstructor
public class UserService {
    private final UserRepository userRepository;
    private final EmailService emailService;
}

// ❌ 避免：字段注入
@Service
public class UserService {
    @Autowired
    private UserRepository userRepository;
}
```

## 六、REST API 设计

- ✅ 资源名词复数：`/users`, `/users/{id}`
- ❌ 避免动词：`/getUsers`, `/createUser`

| 状态码 | 含义 | 使用场景 |
|--------|------|----------|
| 200 | OK | 成功获取/更新资源 |
| 201 | Created | 成功创建资源 |
| 204 | No Content | 成功删除 |
| 400 | Bad Request | 请求参数错误 |
| 401 | Unauthorized | 未认证 |
| 403 | Forbidden | 无权限 |
| 404 | Not Found | 资源不存在 |
| 500 | Internal Server Error | 服务器内部错误 |

## 七、异常处理

```java
// ✅ 定义业务异常
public class BusinessException extends RuntimeException {
    private final String code;

    public BusinessException(String code, String message) {
        super(message);
        this.code = code;
    }
}

// ✅ 全局异常处理
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(BusinessException.class)
    public ResponseEntity<ErrorResponse> handle(BusinessException e) {
        return ResponseEntity.badRequest()
            .body(new ErrorResponse(e.getCode(), e.getMessage()));
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleOther(Exception e) {
        log.error("Unexpected error", e);
        return ResponseEntity.internalServerError()
            .body(new ErrorResponse("INTERNAL_ERROR", "系统错误"));
    }
}
```

- ✅ 捕获异常后记录日志并转换为业务异常
- ❌ 禁止吞掉异常（catch 后什么都不做）

## 八、日志规范

| 级别 | 使用场景 |
|------|----------|
| ERROR | 系统错误、异常 |
| WARN | 降级处理、可恢复的错误 |
| INFO | 关键业务流程 |
| DEBUG | 调试信息 |

```java
// ✅ 使用占位符
log.error("Payment failed for order: {}", orderId, exception);
log.info("User {} logged in", userId);

// ❌ 禁止
System.out.println("Result: " + result);
log.info("User " + userId + " logged in");  // 字符串拼接
```

## 九、数据库规范

```java
// ✅ 参数化查询
@Query("SELECT u FROM User u WHERE u.status = :status")
List<User> findByStatus(@Param("status") UserStatus status);

// ❌ 禁止字符串拼接
String sql = "SELECT * FROM users WHERE id = " + id;
```

- ❌ 禁止 `SELECT *`，必须明确字段
- ❌ 禁止循环内查询数据库（N+1 问题）
- ✅ 分页查询必须限制最大页数

## 十、阿里巴巴规范要点

| 规范项 | 要求 |
|--------|------|
| 异常处理 | catch 后必须记录日志或向上抛出 |
| 日志 | 禁止 System.out，必须使用 SLF4J |
| 并发 | 线程池必须手动创建，禁止 Executors 快捷方法 |
| 集合 | 必须使用泛型 |
| 缓存 | key 必须加前缀，避免冲突 |

```java
// ✅ 线程池手动创建
ThreadPoolExecutor executor = new ThreadPoolExecutor(
    5, 10, 60L, TimeUnit.SECONDS,
    new LinkedBlockingQueue<>(100),
    new ThreadFactoryBuilder().setNameFormat("task-%d").build(),
    new ThreadPoolExecutor.CallerRunsPolicy()
);

// ❌ 使用 Executors（可能导致 OOM）
ExecutorService executor = Executors.newFixedThreadPool(10);
```

## 十一、单元测试

```java
// ✅ Given-When-Then 模式
@Test
void shouldReturnUser_whenUserIdIsValid() {
    // Given
    String userId = "123";
    User expectedUser = new User(userId, "John");
    when(repository.findById(userId)).thenReturn(expectedUser);

    // When
    User result = userService.getUserById(userId);

    // Then
    assertThat(result).isEqualTo(expectedUser);
}
```

## 十二、项目编码配置

```xml
<!-- Maven pom.xml -->
<properties>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
</properties>
```

```groovy
// Gradle build.gradle
tasks.withType(JavaCompile) {
    options.encoding = 'UTF-8'
}
```
