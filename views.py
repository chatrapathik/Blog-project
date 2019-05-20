import json
import ast
from urllib.parse import parse_qs, urlparse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse

from app.models import Blog, View, Comment, Like, UnLike

def get_params(req):
    '''
    Getting params from the url, either it
    may be GET/POST request.
    '''
    if req.method == "GET":
        urlp = urlparse(req.get_full_path())
        params = parse_qs(urlp.query)
        params = dict((k, v[0]) for k, v in params.items())
    else:
        params = json.loads(req.body) if req.body else {}

    data = dict()
    for k, v in params.items():
        try:
            v = ast.literal_eval(v)
        except ValueError:
            v = v
        data[k] = v

    return data

@login_required
def upload(req):
    '''
    Upload user's blog.
    Args:
        title = Blog title.
        blog_id = Blog id.
        content = Blog content.
    '''
    user = req.user
    params = get_params(req)
    title = params.get("title", "")
    blog_id = params.get("blog_id", "")
    content = params.get("content", "")

    if not all([title, blog_id, content]):
        return JsonResponse(dict(success=False,
                    message="Missed required info"))

    blog = Blog.objects.filter(user=user,
                               blog_id=blog_id).first()
    if blog:
        return JsonResponse(dict(success=False,
                    message="Blog already exists!!"))

    Blog.objects.create(blog_id=blog_id,
                        title=title, content=content,
                        user=user)

    return JsonResponse(dict(success=True,
                        message="Blog uploaded successfully!!"))

@login_required
def view(req):
    '''
    When user opens the blog.
    Agrs:
        blog_id = id of the blog.
    '''
    user = req.user
    params = get_params(req)
    blog_id = params.get("blog_id", "")

    if not blog_id:
        return JsonResponse(dict(success=False,
                    message="Blog id missing!!"))

    blog = Blog.objects.filter(blog_id=blog_id).first()
    if not blog:
        return JsonResponse(dict(success=False,
                            message="No blog found with this {}".format(blog_id)))

    View.objects.create(blog=blog, user=user)

    blog.views = blog.views + 1
    blog.save()
    data = blog.as_dict()

    return JsonResponse(dict(success=True, data=data))

@login_required
def like(req):
    '''
    When user like the blog.
    Agrs:
        blog_id = id of the blog.
    '''
    user = req.user
    params = get_params(req)
    blog_id = params.get("blog_id", "")

    if not blog_id:
        return JsonResponse(dict(success=False,
                    message="Blog id missing!!"))

    blog = Blog.objects.filter(blog_id=blog_id).first()
    if not blog:
        return JsonResponse(dict(success=False,
                            message="No blog found with this {}".format(blog_id)))

    like = Like.objects.filter(blog=blog, user=user).first()
    if like:
        return JsonResponse(dict(success=False,
                            message="You already liked this {} blog".format(blog_id)))

    un_like = UnLike.objects.filter(blog=blog, user=user).first()

    if un_like:
        un_like.delete()
        blog.un_likes = blog.un_likes - 1

    Like.objects.create(blog=blog, user=user)
    blog.likes = blog.likes + 1
    blog.save()
    data = blog.as_dict()

    return JsonResponse(dict(success=True, data=data))

@login_required
def unlike(req):
    '''
    When user unlikes the blog.
    Agrs:
        blog_id = id of the blog.
    '''
    user = req.user
    params = get_params(req)
    blog_id = params.get("blog_id", "")

    if not blog_id:
        return JsonResponse(dict(success=False,
                    message="Blog id missed!!"))

    blog = Blog.objects.filter(blog_id=blog_id).first()
    if not blog:
        return JsonResponse(dict(success=False,
                            message="No blog found with this {}".format(blog_id)))

    un_like = UnLike.objects.filter(blog=blog, user=user).first()
    if un_like:
        return JsonResponse(dict(success=False,
                            message="You already un liked this {} blog".format(blog_id)))

    like = Like.objects.filter(blog=blog, user=user).first()
    if like:
        like.delete()
        blog.un_likes = blog.likes - 1

    UnLike.objects.create(blog=blog, user=user)
    blog.un_likes = blog.un_likes + 1
    blog.save()
    data = blog.as_dict()

    return JsonResponse(dict(success=True, data=data))

@login_required
def comment(req):
    '''
    When user un like the blog.
    Agrs:
        blog_id = id of the blog.
        comment = comment on the blog.
    '''
    user = req.user
    params = get_params(req)
    blog_id = params.get("blog_id", "")
    c_desc = params.get("comment", "")

    if not all([blog_id, comment]) :
        return JsonResponse(dict(success=False,
                    message="Missed required info!!"))

    blog = Blog.objects.filter(blog_id=blog_id).first()
    if not blog:
        return JsonResponse(dict(success=False,
                            message="No blog found with this {}".format(blog_id)))

    Comment.objects.create(blog=blog, user=user, comment=c_desc)

    blog.comments = blog.comments + 1
    blog.save()
    data = blog.as_dict()

    return JsonResponse(dict(success=True, data=data))

@login_required
def list_blogs(req):
    '''
    Show the list of blog, by applying the filters.
    Ex: Most viewed, Most commented, Most liked,
        Most disliked, Recent created.
        By default it show results based on most
        recently created.
    Args:
        username = user name.
        comments = True/False. If True, filter results
                   with more comments.
        views = True/False. If True, filter results with
                more views.
        likes = True/False. If True, filter results with
                more likes.
        un_likes = True/False. If True, filter results with
                    more un_likes.
        dt_created = True/False. If True filter results with
                    recently created.
    '''
    params = get_params(req)
    username = params.get("username", "")
    comments = params.get("comments", False)
    likes = params.get("likes", False)
    un_likes = params.get("un_likes", False)
    dt_upload = params.get("dt_upload", True)
    views = params.get("views", False)

    if comments:
        sort_by = "-comments"
    elif views:
        sort_by = "-views"
    elif likes:
        sort_by = "-likes"
    elif un_likes:
        sort_by = "-un_likes"
    elif dt_upload:
        sort_by = "-dt_uploaded"
    else:
        sort_by = "dt_uploaded"

    if username:
        user = User.objects.filter(username=username).first()

        if not user:
            return JsonResponse(dict(success=False,
                        message="No user exist with this name"))

        blogs = Blog.objects.filter(user=user)
    else:
        blogs = Blog.objects.all()

    blogs = blogs.order_by(sort_by)
    data = [blog.as_dict() for blog in blogs]

    return JsonResponse(dict(success=True, blogs=data))

@login_required
def blog_info(req):
    '''
    Entire summary of the blog.
    Args:
        blog_id = blog id.
    '''
    params = get_params(req)
    blog_id = params.get("blog_id", "")
    blog = Blog.objects.filter(blog_id=blog_id).first()
    if not blog:
        return JsonResponse(dict(success=True,
                            message="Blod dosen't exists!!"))

    likes = [ like.as_dict() for like in Like.objects.filter(blog=blog) ]
    unlikes = [ unlike.as_dict() for unlike in UnLike.objects.filter(blog=blog) ]
    views = [ view.as_dict() for view in View.objects.filter(blog=blog) ]
    comments = [ comment.as_dict() for comment in Comment.objects.filter(blog=blog) ]

    data = blog.as_dict()
    data["views"] = views
    data["likes"] = likes
    data["un_likes"] = unlikes
    data["comments"] = comments

    return JsonResponse(dict(success=True,
                        blog=data))
