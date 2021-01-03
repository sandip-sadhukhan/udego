from django.shortcuts import render, redirect
from .models import BlogPost, SubCourse, Course, Topic


def findPopularBlogs():
    popularCourse =  Course.objects.filter(tranding=True)[:8]
    popularBlogs = {}
    for i in popularCourse:
        firstSub = SubCourse.objects.filter(course = i).order_by('date')[0]
        firstBlog = BlogPost.objects.filter(sub_course=firstSub).order_by('date')[0]
        popularBlogs[i.name] = {'image': i.coverPic.url, 'slug': firstBlog.slug}
    return popularBlogs

def index(request):
    context = {'popularBlogs': findPopularBlogs()}
    return render(request, 'website/index.html', context)


def post(request, slug):
    try:
        blog = BlogPost.objects.get(slug=slug)
        subCourse = blog.sub_course
        course = subCourse.course
    except BlogPost.DoesNotExist:
        return redirect('notFound')
    allSubCourse = SubCourse.objects.filter(course=course)
    allBlogs = []
    blogsDict = {}
    for sub in allSubCourse:
        blogs = BlogPost.objects.filter(sub_course=sub)
        blognames = {}
        for j in blogs:
            allBlogs.append(j)
            blognames[j.slug] = j.title
        blogsDict[sub.name] = blognames
    index = allBlogs.index(blog)
    prev = None
    next = None
    if(index > 0):
        prev = allBlogs[index-1]
    if(index < len(allBlogs)-1):
        next = allBlogs[index+1]
    # print(blogsDict)
    context = {'blog': blog, 'allBlogs': blogsDict, 'prev': prev,
               'next': next, 'course': course.name, 'coverPic': course.coverPic.url,'popularBlogs': findPopularBlogs()}
    return render(request, 'website/post.html', context)


def allCourses(request):
    context = {'popularBlogs': findPopularBlogs()}

    alltopics = Topic.objects.all()
    #{topicname1: [course1]}
    topicDict = {}
    for topic in alltopics:
        courses =  Course.objects.filter(topic=topic)
        popularBlogs = {}
        for i in courses:
            firstSub = SubCourse.objects.filter(course = i).order_by('date')[0]
            firstBlog = BlogPost.objects.filter(sub_course=firstSub).order_by('date')[0]
            popularBlogs[i.name] = {'image': i.coverPic.url, 'slug': firstBlog.slug}
        topicDict[topic.name] = popularBlogs
    # print(topicDict)
    context['topicDict'] = topicDict

    return render(request, 'website/all-courses.html', context)


def about(request):
    context = {'popularBlogs': findPopularBlogs()}
    return render(request, 'website/about.html', context)


def search(request):
    query = request.GET.get('q').strip()
    # print(query)
    if(not query):
        return redirect('index')
    searchCourses = Course.objects.filter(name__contains=query)
    searchBlogs = BlogPost.objects.filter(title__contains=query)

    context = {'popularBlogs': findPopularBlogs(), 'searchBlogs':searchBlogs, 'q':query, 'searchCourses':searchCourses}
    return render(request, 'website/search.html', context)

def notFound(request):
    context = {'popularBlogs': findPopularBlogs()}
    return render(request, 'website/404.html', context)
