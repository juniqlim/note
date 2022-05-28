## 테스트코드로 개발속도 올리기 2 (persistence test-리포지터리 테스트2)
spring boot 프로젝트를 준비한 후
entity, repository 코드를 이전과 똑같이 작성한다.
```
@Entity
@Table(name = "Post")
public class Post {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "ID")
    private Long id;
    @Column(name = "CATEGORY_ID")
    private Long categoryId;
    @Column(name = "TITLE")
    private String title;
    @Column(name = "CONTENT")
    private String content;
    @Column(name = "REG_DT")
    private LocalDateTime createdAt;
    @Column(name = "UPT_DT")
    private LocalDateTime modifiedAt;
}
```



```
@Entity
@Table(name = "Category")
public class Category {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "ID")
    private Long id;
    @Column(name = "NAME")
    private String name;
    @Column(name = "REG_DT")
    private LocalDateTime createdAt;
    @Column(name = "UPT_DT")
    private LocalDateTime modifiedAt;
}
```



```
public interface PostRepository extends JpaRepository<Post, Long> {
}
```



```
public interface CategoryRepository extends JpaRepository<Category, Long> {
}
```



그리고 service를 만들기 전에 테스트 코드를 작성한다. 테스트 코드를 작성하고 싶은 클래스에서 단축키 (맥 :command+shift+T)를 누르면, 자동으로 빈 클래스가 생성된다.

```
@SpringBootTest
class CategoryRepositoryTest {
    @Autowired
    private CategoryRepository categoryRepository;

    @Test
    void save() {
        Category category = new Category("test_name");
        categoryRepository.save(category);
    }
}
```



클래스명(CategoryRepositoryTest)으로 커서를 옴기고 실행 단축키(맥: controll+shift+r)로 테스트를 실행한다.

```
***************************
APPLICATION FAILED TO START
***************************

Description:

Failed to configure a DataSource: 'url' attribute is not specified and no embedded datasource could be configured.

Reason: Failed to determine a suitable driver class
```

아까 봤던 오류다. DB설정을 하자.



build.gradle

```
dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-data-jpa'
    implementation 'org.springframework.boot:spring-boot-starter-web'
    compileOnly 'org.projectlombok:lombok'
    annotationProcessor 'org.projectlombok:lombok'
    testImplementation 'org.springframework.boot:spring-boot-starter-test'
    implementation 'com.h2database:h2:1.4.200'
}
```

application.properties

```
spring.h2.console.enabled=true
spring.h2.console.path=/h2-console

spring.datasource.url=jdbc:h2:~/test;
spring.datasource.driverClassName=org.h2.Driver
spring.datasource.username=sa
spring.datasource.password=
spring.jpa.database-platform=org.hibernate.dialect.H2Dialect
```



설정 후 다시 테스트를 실행하자.  이제는 성공한다.

![](./02b22d01-3bf0-4aa5-a49a-7f3f299645e4.png)



테스트 코드를 좀 고쳐보자.

```
@Test
void 저장후_조회() {
    Category category = new Category("test_name");
    Category savedCategory = categoryRepository.save(category);

    Optional<Category> selectedCategory = categoryRepository.findById(savedCategory.getId());

    assertThat(savedCategory.getId()).isEqualTo(selectedCategory.get().getId());
}

```

카테고리 객체를 만들어 디비에 저장 후에, 저장 한 데이터를 조회하고, 저장한 객체와 조회한 객체를 서로 비교하는 것으로 repository를 검증했다. Category클래스에 생성자를 만들고, lombok 어노테이션으로  getter를 추가했다. assertThat은 assertj모듈의 것을 사용했다.



테스트를 실행해보면 초록색이 뜬다. 허술한 테스트이다. 하지만 카테고리를 저장하는 코드에 대해, 문제가 있는지 없는지 빠르게 알 수 있다.



PostRepository 에서도 마찬가지 방법으로 테스트를 작성한다. 단축키 (맥 :command+shift+T)를 누르고 빈(empty) 클래스를 생성한 후 테스트 메소드를 작성한다.

```
@SpringBootTest
class PostRepositoryTest {
    @Autowired
    private PostRepository postRepository;

    @Test
    void 저장후_조회() {
        Post post = new Post(1L, "test title", "test content");
        Post savedPost = postRepository.save(post);

        Optional<Post> selectedPost = postRepository.findById(savedPost.getId());

        assertThat(savedPost.getId()).isEqualTo(selectedPost.get().getId());
    }
}
```

클래스명(PostRepositoryTest)으로 커서를 옴기고 실행 단축키(맥: controll+shift+r)로 테스트를 실행하면 성공했다는 메세지를 볼 수 있다.



이제는(아까 전에도 만들었지만) service를 만들어보자.

```
@Service
@RequiredArgsConstructor
public class BlogService {
    private final CategoryRepository categoryRepository;
    private final PostRepository postRepository;

    public List<Category> getCategoryAll() {
        return categoryRepository.findAll();
    }

    public List<Post> getPostAll() {
        return postRepository.findAll();
    }

    public List<Post> getPosts(Long categoryId) {
        return postRepository.findByCategoryId(categoryId);
    }
}
```

PostRepository에 findByCategoryId 메소드가 추가적으로 필요하다. 메소드를 추가한 후 테스트 코드도 추가해주자.



PostRepositoryTest.java

```
@Test
void 저장후_categoryId로_조회() {
    Post post1 = new Post(1L, "test title", "test content");
    Post post2 = new Post(1L, "test title2", "test content2");
    postRepository.save(post1);
    postRepository.save(post2);

    List<Post> posts = postRepository.findByCategoryId(1L);

    assertThat(posts.size()).isEqualTo(2);
}
```



실행해보니 테스트가 실패한다. ![](./9d411415-2ec6-4722-88ef-8bf597af26eb.png)

테스트를 실행하면서, 기존에 저장된 데이터 때문에 조회되는 post개수가 2가가 넘었다.



테스트코드에 @Transactional 코드를 추가하면 테스트 실행후 DB상태를 롤백한다고 한다.

```
@Test
@Transactional
void 저장후_categoryId로_조회() {
```



전체 post를 삭제하는 코드로 모두 삭제후

```
@Test
void deleteAll() {
    postRepository.deleteAll();
}
```

repository 테스트 코드에는 모두 @Transactional 어노테이션을 붙여준다. 테스트의 실행으로 DB데이터가 변경되지 않도록 처리 한다.



그래서 다시 실행하면 테스트가 성공한다.

지금까지 테스트코드를 작성한 패키지에서 실행 단축키(맥: controll+shift+r)를 누르면 전체 테스트를 실행해 결과를 볼 수 있다.

![](./8efd661d-f1bd-44d1-a77e-3592f08ecd8e.png)



![](./b33fa8c4-7631-4a57-b592-5cf7566427c8.png)

일단 내가 작성한 테스트는 모두 통과했다!



다음은 controller를 추가하자.

```
@RestController
@RequiredArgsConstructor
public class BlogController {
    private final BlogService blogService;

    @GetMapping("/categorys")
    public List<Category> getCategorys() {
        return blogService.getCategoryAll();
    }

    @GetMapping("/category/{categoryId}/posts")
    public List<Post> getPosts(@PathVariable Long categoryId) {
        return blogService.getPosts(categoryId);
    }
}
```



이제 애플리케이션을 실행하여 동작시킬 수 있다. http 요청을 보내보자.

```
http://localhost:8080/categorys

HTTP/1.1 200
Content-Type: application/json
Transfer-Encoding: chunked
Date: Sun, 23 Jan 2022 06:05:26 GMT
Keep-Alive: timeout=60
Connection: keep-alive

[
{
"id": 1,
"name": "test name",
"createdAt": "2022-01-16T00:00:00",
"modifiedAt": "2022-01-16T00:00:00"
},
{
```

테스트코드를 실행하며 DB에 저장된 데이터가 있어서 http응답에 데이터가 있다. 만약 없다면 테스트 코드를 이용해서 category 데이터를 만들어도 된다.



이 것으로 repository 레이어에 (허술하지만)테스트 코드가 추가 되었다.



그럼 테스트코드를 작성해서 속도가 빨려졌을까? 작성하지 않았을때와 무엇이 달라졌나?

1. service와 controller를 작성하기 전에 코드를 실행하였다.
2. 전체 애플리케이션을 작성하기전에 DB설정 관련 오류를 만났다.

1. 애플리케이션 동작확인을 위해 데이터를 셋팅할때 테스트코드를 이용할 수 있다.



만들어본 간단한 블로그에서는 위의 항목들이 달라진 것 같다. 테스트 코드없이 작성했을때보다 시행착오의 빈도가 줄고, 애플리케이션을 실행해서 테스트하는것도 편해졌다.



무엇보다도 오류발생의 피드백을 받는 것이 빨라졌다. DB연동과 사용에 대해 애플리케이션을 다 만들지 않고도, 빠르게 결과를 확인 할 수 있었다. 애플리케이션의 다른 오류와 헷갈리지 않을 수 있게 되었다.

내가 관리 할 수 있는 시스템이 아니라 관리할 수 없는 시스템(외부 API등)에 접근하는 테스트는 더욱 효용이 클 것이다.