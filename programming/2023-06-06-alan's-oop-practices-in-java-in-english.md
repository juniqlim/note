# Apply Alan Kay's OOP to your Java code
## Alan Kay's OOP Practices in Java
Let's try to apply Alan Kay's object orientation (as I understand it) to Java code.

He says [only in Smalltalk and LISP](https://github.com/juniqlim/note/blob/master/programming/2023-03-17-alan-kay-oop.md), but let's try what we can.

## Practices
1. [No setters](https://www.quora.com/In-object-oriented-programming-why-is-it-bad-practice-to-make-data-members-public-when-the-get-set-public-members-modify-it-anyway/answer/Alan-Kay-11)
2. [Instance fields are final](https://www.quora.com/Why-is-functional-programming-seen-as-the-opposite-of-OOP-rather-than-an-addition-to-it/answer/Alan-Kay-11)
3. [Keep public method requests/responses simple](https://disqus.com/home/discussion/yegor256/alan_kay_was_wrong_about_him_being_wrong/#comment-3851868732)

## Example
First, I prepared a simple code.  
A blog application called RealWorld needs to create a slug with the title [when creating a post](https://realworld-docs.netlify.app/docs/specs/backend-specs/endpoints#create-article).  
'How to train your dragon' -> 'how-to-train-your-dragon'  
I turned this requirement into code.

Translated with www.DeepL.com/Translator (free version)
```java
    DataStructureArticle makeDataStructureArticle(String title, String content) {
        String lowerCase = title.toLowerCase();
        String slug = lowerCase.replace(" ", "-");
    
        DataStructureArticle article = new DataStructureArticle();
        article.setTitle(title);
        article.setContent(content);
        article.setSlug(slug);
    
        return article;
    }
    
    class DataStructureArticle {
        private String title;
        private String content;
        private String slug;
    
        public void setSlug(String slug) {
            this.slug = slug;
        }
    
        public void setTitle(String title) {
        }
    
        public void setContent(String content) {
        }
    
        public String getSlug() {
            return slug;
        }
    }
```
This is a structure+procedure style of code.

This code is used like the test code below.
```java
    @Test
    void makeDataStructureArticle() {
        MakeArticle.DataStructureArticle article = makeArticle.makeDataStructureArticle("How to train your dragon", "Ever wonder how?");
        assertEquals("how-to-train-your-dragon", article.getSlug());
    }
```
### 1. Apply the "no setter" practice.
```java
    MutableObjectArticle makeMutableObjectArticle(String title, String content) {
        MutableObjectArticle article = new MutableObjectArticle(title, content);
        article.setSlug();

        return article;
    }

    class MutableObjectArticle {
        private String title;
        private String content;
        private String slug;

        public MutableObjectArticle(String title, String content) {
            this.title = title;
            this.content = content;
        }

        public void setSlug() {
            String lowerCase = title.toLowerCase();
            String slug = lowerCase.replace(" ", "-");
            this.slug = slug;
        }

        public String getSlug() {
            return slug;
        }
    }
```
This is variable object style code.  
The imperative logic for creating the slug has been moved into the object where the data is located. The code for creating the 'post' object is smaller.    
The 'post' object has mutable state. If a reference to the 'post' object is used elsewhere, or in a multi-threaded environment, it becomes a race condition.    
The code may have unintended consequences when executed.  
  
This code is used like the test code below.  
```java
    @Test
    void makeMutableObjectArticle() {
        MakeArticle.MutableObjectArticle article = makeArticle.makeMutableObjectArticle("How to train your dragon", "Ever wonder how?");
        assertEquals("how-to-train-your-dragon", article.getSlug());
    }
```  
### 2. Apply the "instance fields are final" practice.
```java
    ImmutableObjectArticle immutableObjectArticle(String title, String content) {
        return new ImmutableObjectArticle(title, content, new SluggedString(title));
    }

    class ImmutableObjectArticle {
        private final String title;
        private final String content;
        private final SluggedString sluggedString;

        public ImmutableObjectArticle(String title, String content, SluggedString sluggedString) {
            this.title = title;
            this.content = content;
            this.sluggedString = sluggedString;
        }

        public SluggedString slug() {
            return sluggedString;
        }
    }

    static class SluggedString {
        private final String raw;

        public SluggedString(String raw) {
            this.raw = raw;
        }

        String value() {
            return raw.toLowerCase().replace(" ", "-");
        }

        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (o == null || getClass() != o.getClass()) return false;
            SluggedString slug = (SluggedString) o;
            return Objects.equals(raw, slug.raw);
        }

        @Override
        public int hashCode() {
            return Objects.hash(raw);
        }
    }
```
This is immutable object style code.  
The logic of creating a slug has been separated into objects. A 'post' object has a 'slug' object (Composition).    
Objects are easier to work with because they don't have mutable state.  
  
This code is used like the test code below.  
```java
    @Test
    void immutableObjectArticle() {
        MakeArticle.ImmutableObjectArticle article = makeArticle.immutableObjectArticle("How to train your dragon", "Ever wonder how?");
        assertEquals("how-to-train-your-dragon", article.slug().value());
        assertEquals(new MakeArticle.SluggedString("How to train your dragon"), article.slug());
    }
```
method's return value is a 'slug' object. Other code will know (rely on) the 'slug' object.  

### 3. Apply the "Make public method requests/responses simple" practice.
```java
    ImmutableObjectDependencyFreeArticle immutableObjectDependencyFreeArticle(String title, String content) {
        return new ImmutableObjectDependencyFreeArticle(title, content, new Slugging().text(title));
    }

    class ImmutableObjectDependencyFreeArticle {
        private final String title;
        private final String content;
        private final String slug;

        public ImmutableObjectDependencyFreeArticle(String title, String content, String slug) {
            this.title = title;
            this.content = content;
            this.slug = slug;
        }

        public String slug() {
            return slug;
        }
    }

    static class Slugging {
        String text(String text) {
            return text.toLowerCase().replace(" ", "-");
        }
    }
```
This is immutable object style code.  
I tried to think of the object as a server, like a module.    
It can also look like a [function with data and computation separated](https://www.yes24.com/Product/Goods/110253986).  
> both OOP and functional computation can be completely compatible (and should be!)
  
I think I may have gotten closer to Alan's point that both OOP and functional computation should be completely compatible.  
  
This code is used like the test code below.  
```java
    @Test
    void immutableObjectDependencyFreeArticle() {
        MakeArticle.ImmutableObjectDependencyFreeArticle article = makeArticle.immutableObjectDependencyFreeArticle("How to train your dragon", "Ever wonder how?");
        assertEquals("how-to-train-your-dragon", article.slug());
    }
```
It's simple to use again.

The full code can be found [here](https://github.com/juniqlim/code-for-article/tree/master/aoop).
## Etc
Similar to Kent Beck's XP, I also created values and principles.
### Principles
1. eliminate the 'data structure and procedure' structure
2. reduce imperative syntax

### Values
Scalable, cleaner, simulation, easily define, etc.

## Conclusion
Alan Kay said.
>[Better and perfect are the two enemies of 'what is actually needed'](https://www.quora.com/What-are-examples-of-Perfect-and-Better-in-regards-to-Alan-Kays-Sweet-Spot)

As Alan Kay says, we should focus on what is actually needed.  
The above practices are my current thoughts, so they may be wrong, and I may change my mind in the future.

---
This document is a translation of the [Korean document](https://github.com/juniqlim/note/blob/master/programming/2023-06-06-alan%27s-oop-practices-in-java.md) into DEEPL.